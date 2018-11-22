NAME:=main

# To update, run: latex-process-inputs -makefilelist main.tex
TEX_FILES = \
$(NAME).tex

.DEFAULT_GOAL := pdf

acmart:
	latex acmart.ins

pdf:
	latexmk -bibtex -pdf $(NAME)

final: pdf
	@echo '******** Did you spell-check the paper? ********'
	pdffonts $(NAME).pdf; fi

clean:
	-rm -f *aux *bbl *blg *log *.dvi $(NAME).pdf *.fdb_latexmk *.fls *.out *.spl

read:
	evince main.pdf

tags: TAGS
TAGS: ${TEX_FILES}
	etags ${TEX_FILES}
