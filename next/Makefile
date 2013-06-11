DEST=/home/djwong/rscds_website/next/
MOINMOIN_DIR=../../moin-1.9.7/
FRUMP_SCRIPT=$(MOINMOIN_DIR)/MoinMoin/script/export/frump.py
FONTFORGE=fontforge
TOOLS=$(FONTFORGE) mkdir cp sed python python3

FANCY_HTML=index.html
REGULAR_HTML=classes.html party.html workshop.html demo.html events.html history.html gazette/index.html dances.html old_programs.html
HTML=$(REGULAR_HTML) $(FANCY_HTML)
DEPS=cribs.d events.d sed.d people.d
CLEAN=fancy_nav.txt regular_nav.txt slide_data.js scripts/cribs.sed data/eventdb.js $(MOINMOIN_DIR)/MoinMoin/script/export/frump.py data/next_event.js
JS=site2.js
CSS=style2.css
BLOBS=images fonts slides

all: build_check calendar_check $(HTML) $(JS) $(CSS)

dep: $(DEPS)

build_check:;
	@bash -c "type $(TOOLS) > /dev/null"

include fonts.mk
include cribs.d
include events.d
include sed.d
include people.d

.PHONY: dep
$(DEPS) dep:
	./configure

data/eventdb.js: data/dance_events.js data/big_events.js data/class_events.js data/travel_events.js data/hidden_events.js data/next_event.js
	scripts/create_eventdb

data/next_event.js:
	scripts/create_eventdb
	scripts/events.py data/eventdb.js next_event > $@

.PHONY: calendar_check
calendar_check: data/eventdb.js
	@scripts/touch_next_event

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
	scripts/fix_rel_paths $@

site2.js: site2.js.in scripts/js.sed slide_data.js
	sed -f scripts/js.sed < $< > $@

slide_data.js: data/slides.csv scripts/slides.awk
	awk -f scripts/slides.awk < $< > $@

style2.css: style2.css.in scripts/css.sed fonts.css
	sed -f scripts/css.sed < $< > $@

%.crib: %.txt
	./scripts/crib.py -g $<

all: gazette/may2013.html
gazette/%.html.in: gazette/%.txt $(FRUMP_SCRIPT)
	$(MOINMOIN_DIR)/MoinMoin/script/moin.py export frump $< $@

$(FRUMP_SCRIPT): scripts/frump.py
	cp -pRdu $< $@

clean:;
	rm -rf $(HTML) $(CRAP) $(JS) $(CRIB_SHEETS) $(CLEAN) $(CSS) $(DEPS)
