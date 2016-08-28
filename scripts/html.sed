# All substitution keys (%HEAD%) must be on a separate line!
/%HEAD%/r templates/head.txt
/%HEAD%/d
/%HEAD_GG%/r templates/head_gg.txt
/%HEAD_GG%/d
/%FANCY_NAVIGATION%/r fancy_nav.txt
s/%FANCY_NAVIGATION%//g
/%NAVIGATION%/r regular_nav.txt
s/%NAVIGATION%//g
/%FOOT%/r templates/foot.txt
/%FOOT%/d
/%BODY%/r templates/body.txt
s/%BODY%//g
s/%OPEN_CONTENT%/	<div id="regular_body"><div class="skinny_box">/g
s/%CLOSE_CONTENT%/	<\/div><\/div>/g
/%NEXT_CLASS_SUMMARY%/r next_class_summary.html
s/%NEXT_CLASS_SUMMARY%//g
/%NEXT_DANCE_SUMMARY%/r next_dance_summary.html
s/%NEXT_DANCE_SUMMARY%//g
/%NEXT_DANCE_SUMMARY_ONELINE%/r next_dance_summary_oneline.html
s/%NEXT_DANCE_SUMMARY_ONELINE%//g
/%NEXT_BALL_SUMMARY%/r next_ball_summary.html
s/%NEXT_BALL_SUMMARY%//g
/%NEXT_TRAVEL_SUMMARY%/r next_travel_summary.html
s/%NEXT_TRAVEL_SUMMARY%//g
/%NEXT_DANCE_CRIB%/r next_dance_crib.html
s/%NEXT_DANCE_CRIB%//g
/%SW_WA_BALL_CRIB%/r sw_wa_ball_crib.html
s/%SW_WA_BALL_CRIB%//g
/%PORTLAND_BALL_CRIB%/r portland_ball_crib.html
s/%PORTLAND_BALL_CRIB%//g
/%PAST_EVENTS%/r past_events_list.html
s/%PAST_EVENTS%//g
/%UPCOMING_EVENTS%/r upcoming_events.html
s/%UPCOMING_EVENTS%//g
/%UPCOMING_EVENTS_SHORT%/r upcoming_events_short.html
s/%UPCOMING_EVENTS_SHORT%//g
/%UPCOMING_CLASSES%/r upcoming_classes.html
s/%UPCOMING_CLASSES%//g
/%CHAIR_CONTACT%/r holly.html
s/%CHAIR_CONTACT%//g
/%VICE_CHAIR_CONTACT%/r martin.html
s/%VICE_CHAIR_CONTACT%//g
/%SECRETARY_CONTACT%/r janice.html
s/%SECRETARY_CONTACT%//g
/%TREASURER_CONTACT%/r debbie.html
s/%TREASURER_CONTACT%//g
/%AT_LARGE_CONTACT%/r sally.html
s/%AT_LARGE_CONTACT%//g
/%TEACHER_COORDINATOR_CONTACT%/r lmae.html
s/%TEACHER_COORDINATOR_CONTACT%//g
/%NEWSLETTER_CONTACT%/r djwong.html
s/%NEWSLETTER_CONTACT%//g
/%WEBMASTER_CONTACT%/r djwong.html
s/%WEBMASTER_CONTACT%//g
/%DON_CONTACT%/r don.html
s/%DON_CONTACT%//g
/%DEBBIE_CONTACT%/r debbie.html
s/%DEBBIE_CONTACT%//g
/%GERI_CONTACT%/r geri.html
s/%GERI_CONTACT%//g
/%LMAE_CONTACT%/r lmae.html
s/%LMAE_CONTACT%//g
/%RICHARD_CONTACT%/r richard.html
s/%RICHARD_CONTACT%//g
/%VMAC_CONTACT%/r vmac.html
s/%VMAC_CONTACT%//g
/%MARGE_CONTACT%/r marge.html
s/%MARGE_CONTACT%//g
/%LIZA_CONTACT%/r liza.html
s/%LIZA_CONTACT%//g
/%LINDA_CONTACT%/r linda.html
s/%LINDA_CONTACT%//g
/%ALL_CRIBS%/r has_crib.html
s/%ALL_CRIBS%//g
/%GAZETTE_INDEX%/r gazette_index.html
s/%GAZETTE_INDEX%//g
/%LAST_FIVE_NEWS%/r last_five_news.html
s/%LAST_FIVE_NEWS%//g
/%MEMBERSHIP_FORM%/r membership_form.html
s/%MEMBERSHIP_FORM%//g
/%WORKSHOP_FORM%/r workshop_form.html
s/%WORKSHOP_FORM%//g
/%MEMBERSHIP_CHAIR_MAIL%/r maureen_mail.html
s/%MEMBERSHIP_CHAIR_MAIL%//g
/%WORKSHOP_CHAIR_MAIL%/r lmae_mail.html
s/%WORKSHOP_CHAIR_MAIL%//g
/%WORKSHOP_DIRECTIONS%/r workshop_directions.txt
s/%WORKSHOP_DIRECTIONS%//g
/%SUSIE_CONTACT%/r susie.html
s/%SUSIE_CONTACT%//g
/%LEONE_CONTACT%/r leone.html
s/%LEONE_CONTACT%//g
/%BLEDSOE_CONTACT%/r bledsoe.html
s/%BLEDSOE_CONTACT%//g
/%LINDA_KELSO_CONTACT%/r linda_kelso.html
s/%LINDA_KELSO_CONTACT%//g
/%DWAYNE_CONTACT%/r dwayne.html
s/%DWAYNE_CONTACT%//g
