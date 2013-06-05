DEST=/home/djwong/rscds_website/next/
FONTFORGE=fontforge
TOOLS=$(FONTFORGE) mkdir cp sed python python3

FANCY_HTML=index.html
REGULAR_HTML=classes.html party.html workshop.html demo.html events.html history.html gazette.html dances.html old_programs.html
HTML=$(REGULAR_HTML) $(FANCY_HTML)
DEPS=cribs.d events.d sed.d
CLEAN=fancy_nav.txt regular_nav.txt slide_data.js scripts/cribs.sed data/eventdb.js
JS=site2.js
CSS=style2.css
BLOBS=images fonts

all: build_check $(HTML) $(JS) $(CSS)

dep: $(DEPS)

build_check:;
	@bash -c "type $(TOOLS) > /dev/null"

include fonts.mk
include cribs.d
scripts/cribs.sed: cribs.d
cribs.d:
	scripts/configure_cribs

include events.d
events.d: data/eventdb.js
	scripts/events.py data/eventdb.js makedep > $@

include sed.d
sed.d: scripts/cribs.sed scripts/css.sed scripts/html.sed scripts/js.sed
	scripts/sed_deps.py scripts/*.sed : $(shell find . -name "*.in" | sed -e 's/^..//g') > $@

include people.d
people.d: data/people.csv
	scripts/contacts -d > $@

data/eventdb.js: data/dance_events.js data/big_events.js data/class_events.js data/travel_events.js data/hidden_events.js
	scripts/create_eventdb

install: all
	mkdir -p $(DEST)
	cp -Rlf $(HTML) $(JS) $(CSS) $(BLOBS) $(DEST)

$(REGULAR_HTML): regular_nav.txt
$(FANCY_HTML): fancy_nav.txt

fancy_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%/ type="embedded"/g' < $< > $@

regular_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%//g' < $< > $@

%.html: %.html.in scripts/html.sed scripts/cribs.sed
	sed -f scripts/html.sed -f scripts/cribs.sed < $< > $@

site2.js: site2.js.in scripts/js.sed slide_data.js
	sed -f scripts/js.sed < $< > $@

slide_data.js: data/slides.csv scripts/slides.awk
	awk -f scripts/slides.awk < $< > $@

style2.css: style2.css.in scripts/css.sed fonts.css
	sed -f scripts/css.sed < $< > $@

%.crib: %.txt
	./scripts/crib.py -g $<

clean:;
	rm -rf $(HTML) $(CRAP) $(JS) $(CRIB_SHEETS) $(CLEAN) $(CSS) $(DEPS)
