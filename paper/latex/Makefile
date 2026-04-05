.PHONY: all clean

PAPER = paper

all: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex references.bib
	pdflatex $(PAPER).tex
	bibtex $(PAPER)
	pdflatex $(PAPER).tex
	pdflatex $(PAPER).tex

clean:
	rm -f $(PAPER).{aux,bbl,blg,log,out,pdf,toc,lof,lot,fdb_latexmk,fls,synctex.gz}
