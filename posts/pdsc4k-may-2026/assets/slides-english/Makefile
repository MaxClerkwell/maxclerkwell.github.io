MAIN = main
LATEXMK = latexmk
LATEXMKFLAGS = -pdf -interaction=nonstopmode

.PHONY: all clean distclean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex architecture.png ceph.png horus.png
	$(LATEXMK) $(LATEXMKFLAGS) $(MAIN).tex

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
