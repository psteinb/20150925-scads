
all : sqy.html

%.html : %.md
	pandoc $< --template=pandoc-revealjs.template -t revealjs -o $@ -V revealjs-width:1600 --section-divs --filter tools/filters/columnfilter.py
