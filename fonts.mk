OTF_FONTS=\
fonts/LinBiolinum_RB.otf \
fonts/LinBiolinum_RI.otf \
fonts/LinBiolinum_R.otf

GG_OTF_FONTS=\
fonts/LinLibertine_RBI.otf \
fonts/LinLibertine_RB.otf \
fonts/LinLibertine_RI.otf \
fonts/LinLibertine_R.otf \
fonts/SourceCodePro-Bold.otf \
fonts/SourceCodePro-Regular.otf

WOFF_FONTS=$(subst otf,woff,$(OTF_FONTS))
GG_WOFF_FONTS=$(subst otf,woff,$(GG_OTF_FONTS))

CLEAN += $(WOFF_FONTS) $(GG_WOFF_FONTS) fonts.css fonts_gg.css

fonts.css: $(WOFF_FONTS)
	echo '/*' > $@
	echo ' * Font loading clauses auto-generated.' >> $@
	echo ' * Get the Linux Biolinum font at http://linuxlibertine.sourceforge.net/' >> $@
	echo ' */' >> $@
	for fon in $(WOFF_FONTS); do scripts/woff2css $$fon; done >> $@

fonts_gg.css: $(GG_WOFF_FONTS)
	echo '/*' > $@
	echo ' * Font loading clauses auto-generated.' >> $@
	echo ' * Get the Linux Libertine font at http://linuxlibertine.sourceforge.net/' >> $@
	echo ' * Get the Source Code Pro font at http://sourceforge.net/projects/sourcecodepro.adobe/' >> $@
	echo ' */' >> $@
	for fon in $(GG_WOFF_FONTS); do scripts/woff2css $$fon; done >> $@

%.woff: %.otf
	$(FONTFORGE) -script scripts/otf2woff.pe $< 2> /dev/null
