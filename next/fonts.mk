OTF_FONTS=\
fonts/LinBiolinum_RB.otf \
fonts/LinBiolinum_RI.otf \
fonts/LinBiolinum_R.otf
WOFF_FROM_OTF_FONTS=$(subst otf,woff,$(OTF_FONTS))

CLEAN += $(WOFF_FROM_OTF_FONTS) fonts.css

fonts.css: $(WOFF_FROM_OTF_FONTS)
	echo '/*' > $@
	echo ' * Font loading clauses auto-generated.' >> $@
	echo ' * Get the Linux Biolinum font at http://linuxlibertine.sourceforge.net/' >> $@
	echo ' */' >> $@
	for fon in $(WOFF_FROM_OTF_FONTS); do scripts/woff2css $$fon; done >> $@

%.woff: %.otf
	$(FONTFORGE) -script scripts/otf2woff.pe $< 2> /dev/null
