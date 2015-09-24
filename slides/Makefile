MARKDOWNFILES=$(wildcard *.md)
HTMLFILES=$(patsubst %.md,%.html,$(MARKDOWNFILES))

all : ${HTMLFILES}

%.html : %.md
	pandoc $< --template=pandoc-revealjs.template -t revealjs -o $@ -V revealjs-width:1600 --section-divs --filter tools/filters/columnfilter.py
