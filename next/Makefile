DEST=/home/djwong/rscds_website/next/

FANCY_HTML=index.html
REGULAR_HTML=classes.html
HTML=$(REGULAR_HTML) $(FANCY_HTML)
CRAP=fancy_nav.txt regular_nav.txt slide_data.js
JS=slideshow.js
CSS=style2.css
BLOBS=images

all: $(HTML) $(JS)

install: all
	mkdir -p $(DEST)
	cp -pRl $(HTML) $(JS) $(CSS) $(BLOBS) $(DEST)

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

clean:;
	rm -rf $(HTML) $(CRAP) $(JS)
