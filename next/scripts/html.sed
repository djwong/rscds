# All substitution keys (%HEAD%) must be on a separate line!
/%HEAD%/r templates/head.txt
/%HEAD%/d
/%FANCY_NAVIGATION%/r fancy_nav.txt
/%FANCY_NAVIGATION%/d
/%NAVIGATION%/r regular_nav.txt
/%NAVIGATION%/d
/%FOOT%/r templates/foot.txt
/%FOOT%/d
/%BODY%/r templates/body.txt
/%BODY%/d
s/%OPEN_CONTENT%/	<div id="regular_body">/g
s/%CLOSE_CONTENT%/	<\/div>/g
/%NEXT_CLASS_SUMMARY%/r next_class_summary.html
/%NEXT_CLASS_SUMMARY%/d
/%NEXT_DANCE_SUMMARY%/r next_dance_summary.html
/%NEXT_DANCE_SUMMARY%/d
/%NEXT_BALL_SUMMARY%/r next_ball_summary.html
/%NEXT_BALL_SUMMARY%/d
/%NEXT_TRAVEL_SUMMARY%/r next_travel_summary.html
/%NEXT_TRAVEL_SUMMARY%/d
/%NEXT_DANCE_CRIB%/r next_dance_crib.html
/%NEXT_DANCE_CRIB%/d
/%PORTLAND_BALL_CRIB%/r portland_ball_crib.html
/%PORTLAND_BALL_CRIB%/d
/%UPCOMING_EVENTS%/r upcoming_events.html
/%UPCOMING_EVENTS%/d
/%CHAIR_CONTACT%/r linda.html
/%CHAIR_CONTACT%/d
/%VICE_CHAIR_CONTACT%/r holly.html
/%VICE_CHAIR_CONTACT%/d
/%SECRETARY_CONTACT%/r chris.html
/%SECRETARY_CONTACT%/d
/%TREASURER_CONTACT%/r pat.html
/%TREASURER_CONTACT%/d
/%AT_LARGE_CONTACT%/r sally.html
/%AT_LARGE_CONTACT%/d
/%TEACHER_COORDINATOR_CONTACT%/r don.html
/%TEACHER_COORDINATOR_CONTACT%/d
/%NEWSLETTER_CONTACT%/r lmae.html
/%NEWSLETTER_CONTACT%/d
/%WEBMASTER_CONTACT%/r djwong.html
/%WEBMASTER_CONTACT%/d
/%DON_CONTACT%/r don.html
/%DON_CONTACT%/d
/%DEBBIE_CONTACT%/r debbie.html
/%DEBBIE_CONTACT%/d
/%LMAE_CONTACT%/r lmae.html
/%LMAE_CONTACT%/d
/%RICHARD_CONTACT%/r richard.html
/%RICHARD_CONTACT%/d
/%VMAC_CONTACT%/r vmac.html
/%VMAC_CONTACT%/d
/%ALL_CRIBS%/r has_crib.html
/%ALL_CRIBS%/d
