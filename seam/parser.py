"""Recursive descent parser for The Calculus notation.

Handles both Unicode (∅ ⊗ μ ◊) and ASCII (silence seam mu witness) forms.
Comments: -- to end of line.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union

from seam.ast import (
    Expr, Silence, Var, Seam, Edge, Return, Witness, Room, Word,
)
from seam.membrane import (
    Membrane, BreathMembrane, OnceMembrane, CrossingMembrane,
)


class ParseError(Exception):
    """A parse error with location information."""
    def __init__(self, msg: str, line: int, col: int):
        self.line, self.col = line, col
        super().__init__(f"{msg} (line {line}, col {col})")


@dataclass
class Token:
    kind: str; value: str; line: int; col: int

_KEYWORDS = {
    "silence": "SILENCE", "\u2205": "SILENCE",
    "seam": "SEAM",       "\u2297": "SEAM",
    "mu": "MU",           "\u03bc": "MU",
    "witness": "WITNESS",  "\u25ca": "WITNESS",
    "breath": "IDENT", "crossing": "IDENT", "once": "IDENT",
}

_TOKEN_RE = re.compile(r"""
    (?P<COMMENT>--[^\n]*)          |
    (?P<WS>\s+)                    |
    (?P<NUMBER>[0-9]+(?:\.[0-9]+)?)|
    (?P<VISIBLE>visible:)          |
    (?P<VEILED>veiled:)            |
    (?P<IDENT>[a-zA-Z_][a-zA-Z0-9_-]*) |
    (?P<SYM>[\u2205\u2297\u03bc\u25ca.()\[\]|,])
""", re.VERBOSE)

_SYM_MAP = {
    "(": "LPAREN", ")": "RPAREN",
    "[": "LBRACKET", "]": "RBRACKET",
    "|": "PIPE", ".": "DOT", ",": "COMMA",
    "\u2205": "SILENCE", "\u2297": "SEAM",
    "\u03bc": "MU", "\u25ca": "WITNESS",
}


def _tokenise(src: str) -> list[Token]:
    tokens: list[Token] = []
    line = 1
    col = 1
    pos = 0
    while pos < len(src):
        m = _TOKEN_RE.match(src, pos)
        if m is None:
            raise ParseError(f"unexpected character {src[pos]!r}", line, col)
        kind = m.lastgroup
        value = m.group()
        start_line, start_col = line, col

        # advance line/col tracking
        for ch in value:
            if ch == "\n":
                line += 1
                col = 1
            else:
                col += 1
        pos = m.end()

        if kind in ("WS", "COMMENT"):
            continue

        if kind == "SYM":
            kind = _SYM_MAP[value]
        elif kind == "IDENT" and value in _KEYWORDS:
            kind = _KEYWORDS[value]

        tokens.append(Token(kind, value, start_line, start_col))

    tokens.append(Token("EOF", "", line, col))
    return tokens


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class _Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _at(self, *kinds: str) -> bool:
        return self._peek().kind in kinds

    def _eat(self, kind: str) -> Token:
        tok = self._peek()
        if tok.kind != kind:
            raise ParseError(
                f"expected {kind}, got {tok.kind} ({tok.value!r})",
                tok.line, tok.col)
        self._pos += 1
        return tok

    def _error(self, msg: str) -> ParseError:
        tok = self._peek()
        return ParseError(msg, tok.line, tok.col)

    def parse_expr(self) -> Expr:
        """expr := atom (('⊗' | 'seam') atom)*"""
        left = self.parse_atom()
        while self._at("SEAM"):
            self._eat("SEAM")
            right = self.parse_atom()
            left = Seam(left, right)
        return left

    def parse_atom(self) -> Expr:
        """atom := silence | return_expr | witness | room | '(' expr ')' | var_or_edge_or_word"""
        tok = self._peek()

        if tok.kind == "SILENCE":
            self._eat("SILENCE")
            return Silence()

        if tok.kind == "MU":
            return self._parse_return()

        if tok.kind == "WITNESS":
            self._eat("WITNESS")
            inner = self.parse_atom()
            return Witness(inner)

        if tok.kind == "LBRACKET":
            return self._parse_room()

        if tok.kind == "LPAREN":
            self._eat("LPAREN")
            inner = self.parse_expr()
            self._eat("RPAREN")
            return inner

        if tok.kind in ("IDENT", "NUMBER"):
            return self._parse_primary_and_maybe_edge()

        raise self._error(f"unexpected token {tok.kind} ({tok.value!r})")

    def _parse_return(self) -> Return:
        """return_expr := ('μ' | 'mu') IDENT '.' expr"""
        self._eat("MU")
        name_tok = self._eat("IDENT")
        self._eat("DOT")
        body = self.parse_expr()
        return Return(name_tok.value, body)

    def _parse_room(self) -> Room:
        """room := '[' expr ']'"""
        self._eat("LBRACKET")
        inner = self.parse_expr()
        self._eat("RBRACKET")
        return Room(inner)

    def _parse_primary_and_maybe_edge(self) -> Expr:
        """Parse IDENT/NUMBER, then check for trailing |...| (Edge or Word)."""
        left = self._parse_primary()
        if not self._at("PIPE"):
            return left
        return self._parse_edge_or_word(left)

    def _parse_primary(self) -> Expr:
        tok = self._peek()
        if tok.kind in ("IDENT", "NUMBER"):
            self._eat(tok.kind)
            return Var(tok.value)
        raise self._error(f"expected identifier or number, got {tok.kind}")

    def _parse_edge_or_word(self, left: Expr) -> Expr:
        """Parse  |...| right  after left has been consumed."""
        self._eat("PIPE")

        # Check for Word syntax: visible: ... , veiled: ...
        if self._at("VISIBLE"):
            return self._parse_word_body(left)

        # Otherwise: membrane_spec
        membrane = self._parse_membrane_spec()
        self._eat("PIPE")
        right = self.parse_atom()
        return Edge(left, right, membrane)

    def _parse_membrane_spec(self) -> Union[Membrane, BreathMembrane, OnceMembrane, CrossingMembrane]:
        tok = self._peek()

        if tok.kind == "NUMBER":
            self._eat("NUMBER")
            return Membrane(threshold=float(tok.value))

        if tok.kind == "IDENT":
            name = tok.value
            self._eat("IDENT")

            if name == "breath":
                if self._at("LPAREN"):
                    self._eat("LPAREN")
                    params = self._parse_breath_params()
                    self._eat("RPAREN")
                    return BreathMembrane(**params)
                return BreathMembrane()

            if name == "crossing":
                return CrossingMembrane()

            if name == "once":
                return OnceMembrane()

            # Fallback: treat identifier as a named membrane with default
            return Membrane(threshold=0.5)

        raise self._error(f"expected membrane spec, got {tok.kind}")

    def _parse_breath_params(self) -> dict:
        """Parse positional params inside breath(). Placeholder for future use."""
        params: dict = {}
        while not self._at("RPAREN"):
            raise self._error("breath() params not yet supported; use bare 'breath'")
        return params

    def _parse_word_body(self, left: Expr) -> Word:
        self._eat("VISIBLE")
        visible = self._parse_ident_list()
        self._eat("COMMA")
        self._eat("VEILED")
        veiled = self._parse_ident_list()
        self._eat("PIPE")
        right = self.parse_atom()
        return Word(left, right,
                    visible_share=tuple(visible),
                    veiled_duty=tuple(veiled))

    def _parse_ident_list(self) -> list[str]:
        """Parse comma-separated identifiers; stops before veiled:/pipe."""
        names: list[str] = [self._eat("IDENT").value]
        while self._at("COMMA"):
            # Peek ahead: if after comma we see VEILED or PIPE, stop
            next_tok = self._tokens[self._pos + 1] if self._pos + 1 < len(self._tokens) else None
            if next_tok and next_tok.kind in ("VEILED", "PIPE"):
                break
            self._eat("COMMA")
            names.append(self._eat("IDENT").value)
        return names

    def parse_top(self) -> Expr:
        expr = self.parse_expr()
        if not self._at("EOF"):
            tok = self._peek()
            raise ParseError(
                f"unexpected trailing token {tok.kind} ({tok.value!r})",
                tok.line, tok.col)
        return expr


def parse(text: str) -> Expr:
    """Parse a Calculus expression from a string."""
    tokens = _tokenise(text)
    return _Parser(tokens).parse_top()


def parse_file(path: str) -> Expr:
    """Parse a Calculus expression from a file."""
    with open(path, encoding="utf-8") as f:
        return parse(f.read())
