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
