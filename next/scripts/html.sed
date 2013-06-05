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
