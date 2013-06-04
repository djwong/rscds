DEST=/home/djwong/rscds_website/next/
FONTFORGE=fontforge
TOOLS=$(FONTFORGE) mkdir cp sed python python3

FANCY_HTML=index.html
REGULAR_HTML=classes.html party.html
HTML=$(REGULAR_HTML) $(FANCY_HTML)
CRAP=fancy_nav.txt regular_nav.txt slide_data.js cribs.d events.d scripts/cribs.sed
JS=slideshow.js
CSS=style2.css
BLOBS=images fonts

all: build_check $(HTML) $(JS) $(CSS)

build_check:;
	@bash -c "type $(TOOLS) > /dev/null"

include fonts.mk
include cribs.d
scripts/cribs.sed: cribs.d
cribs.d:
	scripts/configure_cribs

include events.d
events.d:
	scripts/events.py data/eventdb.js makedep > $@

include sed.d
sed.d:
	scripts/sed_deps.py scripts/*.sed : $(shell find . -name "*.in" | sed -e 's/^..//g') > $@

install: all
	mkdir -p $(DEST)
	cp -Rlf $(HTML) $(JS) $(CSS) $(BLOBS) $(DEST)

$(REGULAR_HTML): regular_nav.txt
$(FANCY_HTML): fancy_nav.txt

fancy_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%/ type="embedded"/g' < $< > $@

regular_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%//g' < $< > $@

%.html: %.html.in scripts/html.sed
	sed -f scripts/html.sed < $< > $@

slideshow.js: slideshow.js.in scripts/js.sed slide_data.js
	sed -f scripts/js.sed < $< > $@

slide_data.js: data/slides.csv scripts/slides.awk
	awk -f scripts/slides.awk < $< > $@

style2.css: style2.css.in scripts/css.sed fonts.css
	sed -f scripts/css.sed < $< > $@

%.crib: %.txt
	./scripts/crib.py $<

clean:;
	rm -rf $(HTML) $(CRAP) $(JS) $(CRIB_SHEETS) $(CLEAN) $(CSS)
