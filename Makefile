.SUFFIXES:
DEST=/home/djwong/rscds_website/
MOINMOIN_DIR=../moin-1.9.7/
FRUMP_SCRIPT=$(MOINMOIN_DIR)/MoinMoin/script/export/frump.py
FONTFORGE=fontforge
TOOLS=$(FONTFORGE) mkdir cp sed python python3

PHP=membership_form.php workshop_form.php
FANCY_HTML=index.html
REGULAR_HTML=classes.html party.html workshop.html demo.html events.html about.html members.html dances.html past_programs.html workshop_reg.html members_reg.html workshop_dirs.html workshop_crib.html past_events.html
GAZETTE_HTML=gazette/index.html gazette/.htaccess
HTML=$(REGULAR_HTML) $(FANCY_HTML) $(GAZETTE_HTML)
TOP_HTML=$(REGULAR_HTML) $(FANCY_HTML)
DEPS=cribs.d events.d sed.d people.d gazette.d
CLEAN=fancy_nav.txt regular_nav.txt slide_data.js scripts/cribs.sed data/eventdb.js $(MOINMOIN_DIR)/MoinMoin/script/export/frump.py data/next_event.js gazette/index.html.in gazette_index.html templates/head_gg.txt membership_form.html workshop_form.html templates/head.txt
JS_BUILD=site2.js
JS=$(JS_BUILD) jquery.slides.js
CSS=style2.css fonts_gg.css
BLOBS=images fonts slides files

all: build_all

# Don't let anything depend on a $(...) list until after the includes.  If you
# compose rules that use vars before the 'include's finish *creating* the vars,
# the build will probably not work.
include fonts.mk
include cribs.d
include events.d
include sed.d
include people.d
include gazette.d

build_all: build_check calendar_check $(HTML) $(JS) $(CSS) $(GAZETTES) $(PHP)

dep: $(DEPS)

build_check:;
	@bash -c "type $(TOOLS) > /dev/null"

events.d: data/eventdb.js Makefile
	scripts/events.py data/eventdb.js makedep > events.d

sed.d: scripts/css.sed scripts/html.sed scripts/js.sed Makefile
	scripts/sed_deps.py scripts/*.sed : $(shell find . -name "*.in" | sed -e 's/^..//g') > sed.d

people.d: data/people.csv Makefile
	scripts/contacts -d > people.d

gazette.d: scripts/cribs.sed Makefile
	scripts/create_gazette_index dep gazette_index.html > gazette.d

cribs.d: Makefile
	scripts/configure_cribs

scripts/cribs.sed:
	scripts/configure_cribs

data/eventdb.js: data/dance_events.js data/big_events.js data/class_events.js data/travel_events.js data/hidden_events.js data/next_event.js data/news_events.js
	scripts/create_eventdb

data/next_event.js:
	scripts/create_eventdb
	scripts/events.py data/eventdb.js next_event > $@

.PHONY: calendar_check
calendar_check: data/eventdb.js
	@scripts/touch_next_event
	@# create events.d
	@scripts/events.py data/eventdb.js makedep > events.d
	@# create gazette.d
	@scripts/create_gazette_index dep gazette_index.html > gazette.d
	@# create cribs.d
	@scripts/configure_cribs

# Only hardlink the blobs, not the generated content.
install: all
	mkdir -p $(DEST)
	chmod -R +r $(BLOBS)
	cp -Rlf $(BLOBS) $(DEST)
	cp -Rf .htaccess $(PHP) $(TOP_HTML) $(JS) $(CSS) $(DEST)
	mkdir -p $(DEST)/gazette/
	cp -Rf $(GAZETTE_HTML) $(GAZETTES) $(DEST)/gazette/

$(REGULAR_HTML) $(GAZETTE_HTML): regular_nav.txt
$(FANCY_HTML): fancy_nav.txt

fancy_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%/ class="embedded"/g' < $< > $@

regular_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%//g' < $< > $@

%.html: %.html.in scripts/html.sed scripts/cribs.sed
	sed -f scripts/html.sed -f scripts/cribs.sed < $< > $@
	scripts/fix_rel_paths $@

%.php: %.php.in scripts/html.sed scripts/cribs.sed
	sed -f scripts/html.sed -f scripts/cribs.sed < $< > $@
	scripts/fix_rel_paths $@

gazette/index.html.in: members.html.in
	cp -pRdu $< $@

gazette/.htaccess: gazette/htaccess.in
	sed -e 's|%DEST%|$(DEST)/gazette/|g' < $< > $@

templates/head.txt: templates/head.txt.in
	cp -pRdu $< $@

templates/head_gg.txt: templates/head.txt.in templates/head_gg.txt.in
	cp -pRdu $< $@
	cat templates/head_gg.txt.in >> $@

site2.js: site2.js.in scripts/js.sed slide_data.js
	sed -f scripts/js.sed < $< > $@

slide_data.js: data/slides.csv scripts/slides.awk
	awk -f scripts/slides.awk < $< > $@

style2.css: style2.css.in scripts/css.sed fonts.css
	sed -f scripts/css.sed < $< > $@

%.crib: %.txt
	./scripts/crib.py -g $<

gazette/%.html.in: gazette/%.txt $(FRUMP_SCRIPT)
	$(MOINMOIN_DIR)/MoinMoin/script/moin.py export frump $< $@

$(FRUMP_SCRIPT): scripts/frump.py
	cp -pRdu $< $@

clean:;
	rm -rf $(HTML) $(CRAP) $(JS_BUILD) $(CRIB_SHEETS) $(CLEAN) $(CSS) $(GAZETTES)

distclean: clean
	rm -rf $(DEPS)
