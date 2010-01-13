DEST=/home/djwong/rscds_website/

HTML=index.html \
classes.html \
people.html \
demo.html \
links.html \
events.html \
party.html \
workshop.html \
maps.html \
pictures.html \
movies.html

FILES=content_bottom.jpg \
content_top.jpg \
dancing_feet.jpg \
debbie.jpg \
don.jpg \
footer.jpg \
header.jpg \
lmae.jpg \
logo_inv.gif \
michael.jpg \
workshop_flyer_2008.pdf \
workshop_flyer_2009.pdf \
workshop_registration_2009.pdf \
workshop_registration_2010.pdf \
vancouver_dance_2009.pdf \
middle.jpg \
ruth_jappy.jpg \
sidebar_top.jpg \
sidebar_bottom.jpg \
sidebar.jpg \
style.css

all: $(HTML)

install: all
	mkdir -p $(DEST)
	cp -pR $(HTML) $(FILES) $(DEST)

%.html: %.xhtml links.txt files.txt part0 part1 part2 part3
	./build.sh $< $@

clean:;
	rm -rf $(HTML)
