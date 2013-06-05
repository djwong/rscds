#!/usr/bin/env python3

# Take a crib description file and generate an interactive HTML crib sheet.
# CSS/JS are still required.  This is NOT QUITE the same script as was on the
# Youth Weekend West 2013 site.
# Copyright 2013 Darrick J. Wong.  All rights reserved.

# Dance program file format:
# I: <description of interlude>
# D: <name of dance>

# Dance crib file format:
# Name: <name of dance>
# Format: <what kind of dance -- 8x32R, 4x32S, etc>
# Source: <where you got it from>
# <bars>	<steps>
#
# Note: Any line not starting with Name:/Format:/Source: is assumed to be
# the start of dance figure instructions.
#
# Dance crib files should be dances/<filename_of_dance>.txt
# wherein the "name of dance" above has been converted to lowercase, the
# spaces replaced with underscores, and all non alphanumeric letters removed.
# Hence, "Postie's Jig" becomes "dances/posties_jig.txt".
#
# Look for anything with "crib_" in the name in style2.css and site2.js,
# if you're trying to extract the crib generator code.

import sys
import cgi
import hashlib

def write_dance(dance_name, output):
	dance_fname = 'dances/'
	for letter in dance_name.lower():
		if letter.isalnum():
			dance_fname = dance_fname + letter
		elif letter == ' ':
			dance_fname = dance_fname + '_'
	dance_fname = dance_fname + '.txt'
	in_instructions = False
	source = ''
	notes = None
	youtube = None
	endnote = None
	alg = hashlib.sha1()
	dance_id = '%s:%s' % (dance_fname, output.name)
	alg.update(dance_id.encode('utf-8'))
	dance_id = alg.hexdigest()
	with open(dance_fname) as dancefile:
		for danceline in dancefile:
			if danceline[0] == '#':
				continue
			danceline = danceline.strip()
			if in_instructions:
				x = danceline.partition('	')
				output.write('	<tr><td class="crib_step_bars">%s</td><td>%s</td></tr>\n' % (cgi.escape(x[0]), cgi.escape(x[2])))
			elif danceline.startswith("Name: "):
				name = danceline[6:]
			elif danceline.startswith("Format: "):
				fmt = danceline[8:]
			elif danceline.startswith("Source: "):
				source = danceline[8:]
			elif danceline.startswith("Notes: "):
				notes = danceline[7:]
			elif danceline.startswith("Youtube: "):
				youtube = danceline[9:]
			elif danceline.startswith("Endnote: "):
				endnote = danceline[9:]
			else:
				in_instructions = True
				if youtube != None:
					youtube_str = '<span class="crib_youtube">&nbsp;[<a href="http://www.youtube.com/watch?v=%s">video</a>]</span>' % youtube
				else:
					youtube_str = ''
				output.write('<tr class="crib_header" onclick="crib_toggle(\'crib_%s\');"><td><span id="crib_%s_ctl" class="crib_ctl">&#9654;</span><span class="crib_name">%s</span> (%s)%s</td><td>%s</td></tr>\n' % (dance_id, dance_id, cgi.escape(name), cgi.escape(fmt), youtube_str, cgi.escape(source)))
				output.write('<tr id="crib_%s" class="crib_steps"><td colspan="2">\n' % dance_id)
				if notes != None:
					output.write('	<p>%s</p>\n' % cgi.escape(notes))
				output.write('	<table class="crib_step_table">\n')
				x = danceline.partition('	')
				output.write('	<tr><td class="crib_step_bars">%s</td><td>%s</td></tr>\n' % (cgi.escape(x[0]), cgi.escape(x[2])))
		if in_instructions:
			output.write('	</table>\n')
			if endnote != None:
				output.write('<p>%s</p>\n' % cgi.escape(endnote))
			output.write('</td></tr>\n')

def generate_crib(cribfile, output):
	'''Given an input cribfile, generate an output.'''

	output.write('<p class="crib_dropdown">Click on the name of a dance ')
	output.write('to see its crib sheet.  The complete crib will print ')
	output.write('on your printer.</p>\n')
	output.write('<table class="crib_table">\n')
	for cribline in cribfile:
		if cribline[0] == '#':
			continue
		elif cribline[:3] == "I: ":
			output.write('<tr class="crib_interlude"><td colspan="2">' + cgi.escape(cribline[3:].strip()) + '</td></tr>\n')
		elif cribline[:3] == "D: ":
			write_dance(cribline[3:].strip(), output)
	output.write('</table>\n');

if __name__ == '__main__':
	if len(sys.argv) == 1 or len(sys.argv) > 1 and sys.argv[1] == "--help":
		print("Usage: %s template [templates...]" % sys.argv[0])
		sys.exit(0)

	for fname in sys.argv[1:]:
		with open(fname, "r") as cribfile:
			dot_location = fname.rfind('.')
			if dot_location >= 0:
				outfname = fname[:dot_location] + ".crib"
			else:
				outfname = fname + ".crib"
			with open(outfname, "w") as output:
				generate_crib(cribfile, output)
