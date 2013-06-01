DEST=/home/djwong/rscds_website/next/

FANCY_HTML=index.html
REGULAR_HTML=classes.html party.html
HTML=$(REGULAR_HTML) $(FANCY_HTML)
CRAP=fancy_nav.txt regular_nav.txt slide_data.js cribs.d scripts/cribs.sed
JS=slideshow.js
CSS=style2.css
BLOBS=images

all: $(HTML) $(JS)

include cribs.d
cribs.d:
	scripts/configure_cribs

scripts/cribs.sed: cribs.d

install: all
	mkdir -p $(DEST)
	cp -Rlf $(HTML) $(JS) $(CSS) $(BLOBS) $(DEST)

$(REGULAR_HTML): regular_nav.txt
$(FANCY_HTML): fancy_nav.txt

fancy_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%/ type="embedded"/g' < $< > $@

regular_nav.txt: templates/navigation.txt.in
	sed -e 's/%FANCY%//g' < $< > $@

%.html: %.html.in scripts/html.sed templates/head.txt templates/foot.txt templates/body.txt templates/navigation.txt.in
	sed -f scripts/html.sed < $< > $@

slideshow.js: slideshow.js.in scripts/js.sed slide_data.js
	sed -f scripts/js.sed < $< > $@

slide_data.js: data/slides.csv scripts/slides.awk
	awk -f scripts/slides.awk < $< > $@

%.crib: %.txt
	./scripts/crib.py $<

clean:;
	rm -rf $(HTML) $(CRAP) $(JS) $(CRIB_SHEETS)
