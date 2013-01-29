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

FONTS=\
LinLibertine_Bd.otf \
LinLibertine_Bd.ttf \
LinLibertine_BI.otf \
LinLibertine_BI.ttf \
LinLibertine_It.otf \
LinLibertine_It.ttf \
LinLibertine_Re.otf \
LinLibertine_Re.ttf

FILES=ball_minicrib_2010.pdf \
ball_minicrib_2011.pdf \
nov_2012_crib.pdf \
ball_minicrib_2012.pdf \
ball_minicrib_2013.pdf \
content_bottom.jpg \
content_top.jpg \
dancing_feet.jpg \
debbie.jpg \
dinner_dance_2012.pdf \
dinner_dance_2013.pdf \
don.jpg \
fifth_tuesday_mixer.pdf \
footer.jpg \
header.jpg \
hogcribs10.pdf \
hogflyer10.pdf \
lmae.jpg \
logo_inv.gif \
michael.jpg \
picnicflyer12.pdf \
workshop_flyer_2008.pdf \
workshop_flyer_2009.pdf \
workshop_flyer_2011.pdf \
workshop_registration_2009.pdf \
workshop_registration_2010.pdf \
workshop_registration_2011.pdf \
workshop_registration_2012.pdf \
workshop_registration_2013.pdf \
vancouver_dance_2009.pdf \
middle.jpg \
ruth_jappy.jpg \
sidebar_top.jpg \
sidebar_bottom.jpg \
sidebar.jpg \
style.css \
fonts.css \
turkey_2012.pdf \
betwixt_2012.pdf \
ball_program_2013.pdf \
DD11flyer.pdf

all: $(HTML)

install: all
	mkdir -p $(DEST)
	cp -pR $(HTML) $(FILES) $(FONTS) $(DEST)

%.html: %.xhtml links.txt files.txt part0 part1 part2 part3
	./build.sh $< $@

clean:;
	rm -rf $(HTML)
