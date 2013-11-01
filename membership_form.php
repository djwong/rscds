<?php

print_r($_POST);

function submit_form() {
	global $_POST;

	if ($_POST['gribble'] != 'ihatecaptchas') {
		echo '<form>';
		echo '<p>Sorry, but the form was not filled out correctly.  ';
		echo 'Please go back and try again.</p>';
		echo '</form>';

		return;
	}

	$email = "Someone (".$_SERVER["REMOTE_ADDR"].") has made a comment about the page \""
		.$_POST['pagekey']."\"!\n"
		."Below is an XML extract to be put under comment group \"".$_POST['commentid']."\".\n"
		."They were using ".$_SERVER["HTTP_USER_AGENT"].".\n"
		."\n"
		."<comment poster=\"".$_POST['name']."\" date=\"".strftime("%Y%m%d")."\">\n"
		.$_POST['comment']."\n"
		."</comment>\n";

	mail("djwong+comment@djwong.org",
		"Comment Posted to Web Site",
		$email
	);

	echo "<form>";
	echo "<p>Thank you for your submission.  It will be reviewed shortly.</p>";
	echo "<p>You may close this window now.</p>\n";
	echo "</form>";
}
?>
