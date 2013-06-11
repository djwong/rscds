# -*- coding: iso-8859-1 -*-
"""
MoinMoin - Dump an arbitrary text file in wikilanguage to html.

@copyright: 2013 Darrick J. Wong <djwong.rscds@djwong.org>,
	    2002-2004 Juergen Hermann <jh@web.de>,
	    2005-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

import sys, os, time, codecs, shutil, re, errno

from MoinMoin import config, wikiutil, Page, user
from MoinMoin import script
from MoinMoin.action import AttachFile

url_prefix_static = "."
logo_html = '<img src="logo.png">'
HTML_SUFFIX = ".html"

# Be careful about the %...% escaping here
page_template = u'''%%HEAD%%
	<title>%(date_str)s Ghillie Gazette</title>
%%BODY%%
%%NAVIGATION%%
%%OPEN_CONTENT%%
<div id="gazette">
<h1>The Ghillie Gazette, %(date_str)s</h1>
<p>The newsletter of the Portland Oregon Branch of the R.S.C.D.S. $1.00 -- Free to Members.</p>
%(pagehtml)s
</div>
%%CLOSE_CONTENT%%
%%FOOT%%
'''

class FSPage(Page.Page):
	'''Load pages from the filesystem.'''
	def __init__(self, request, fname):
		'''Store the filename of the input, pass the rest through to Page.'''
		super(FSPage, self).__init__(request, fname)
		self._real_fname = fname

	def get_rev(self, use_underlay=-1, rev=0):
		'''Just pump the passed-in filename straight to the wiki engine.'''
		return (self._real_fname, 1, False)

def _attachment(request, pagename, filename, outputdir, **kw):
	filename = filename.encode(config.charset)
	source_dir = AttachFile.getAttachDir(request, pagename)
	source_file = os.path.join(source_dir, filename)
	dest_dir = os.path.join(outputdir, "attachments", wikiutil.quoteWikinameFS(pagename))
	dest_file = os.path.join(dest_dir, filename)
	dest_url = "attachments/%s/%s" % (wikiutil.quoteWikinameFS(pagename), wikiutil.url_quote(filename))
	if os.access(source_file, os.R_OK):
		if not os.access(dest_dir, os.F_OK):
			try:
				os.makedirs(dest_dir)
			except:
				script.fatal("Cannot create attachment directory '%s'" % dest_dir)
		elif not os.path.isdir(dest_dir):
			script.fatal("'%s' is not a directory" % dest_dir)

		shutil.copyfile(source_file, dest_file)
		script.log('Writing "%s"...' % dest_url)
		return dest_url
	else:
		return ""


class PluginScript(script.MoinScript):
	"""\
Purpose:
========
This tool converts a file containing wiki language into a static HTML file.

Detailed Instructions:
======================
General syntax: moin [options] export frump input_file output_file
"""

	def __init__(self, argv=None, def_values=None):
		if len(argv) != 2:
			raise ValueError("Must pass exactly two filenames.")
		self._input_file = argv[0]
		self._output_file = argv[1]
		script.MoinScript.__init__(self, [], def_values)
		self.parser.add_option(
			"-t", "--target-dir", dest = "target_dir",
			help = "Write html dump to DIRECTORY"
		)
		self.parser.add_option(
			"-u", "--username", dest = "dump_user",
			help = "User the dump will be performed as (for ACL checks, etc)"
		)

	def mainloop(self):
		""" moin-dump's main code. """

		outputdir = '/'
		with open(self._input_file, 'r') as fd:
			for line in fd:
				if line.startswith("pubdate ="):
					date_str = line[10:]
					break

		# Insert config dir or the current directory to the start of the path.
		config_dir = self.options.config_dir
		if config_dir and os.path.isfile(config_dir):
			config_dir = os.path.dirname(config_dir)
		if config_dir and not os.path.isdir(config_dir):
			script.fatal("bad path given to --config-dir option")
		sys.path.insert(0, os.path.abspath(config_dir or os.curdir))

		self.init_request()
		request = self.request

		# fix script_root so we get relative paths in output html
		request.script_root = url_prefix_static

		# use this user for permissions checks
		request.user = user.User(request, name=self.options.dump_user)

		pages = request.rootpage.getPageList(user='') # get list of all pages in wiki
		pages.sort()
		if self._input_file: # did user request a particular page or group of pages?
			try:
				namematch = re.compile(self._input_file)
				pages = [page for page in pages if namematch.match(page)]
				if not pages:
					pages = [self._input_file]
			except:
				pages = [self._input_file]

		wikiutil.quoteWikinameURL = lambda pagename, qfn=wikiutil.quoteWikinameFS: (qfn(pagename) + HTML_SUFFIX)

		AttachFile.getAttachUrl = lambda pagename, filename, request, **kw: _attachment(request, pagename, filename, outputdir, **kw)

		errlog = sys.stderr
		errcnt = 0

		page_front_page = wikiutil.getLocalizedPage(request, request.cfg.page_front_page).page_name
		page_title_index = wikiutil.getLocalizedPage(request, 'TitleIndex').page_name
		page_word_index = wikiutil.getLocalizedPage(request, 'WordIndex').page_name

		navibar_html = ''

		urlbase = request.url # save wiki base url
		for pagename in pages:
			# we have the same name in URL and FS
			script.log('Writing "%s"...' % self._output_file)
			try:
				pagehtml = ''
				request.url = urlbase + pagename # add current pagename to url base
				page = FSPage(request, pagename)
				request.page = page
				try:
					request.reset()
					pagehtml = request.redirectedOutput(page.send_page, count_hit=0, content_only=1, do_cache=0)
				except:
					errcnt = errcnt + 1
					print >> sys.stderr, "*** Caught exception while writing page!"
					print >> errlog, "~" * 78
					print >> errlog, file # page filename
					import traceback
					traceback.print_exc(None, errlog)
			finally:
				timestamp = time.strftime("%Y-%m-%d %H:%M")
				filepath = self._output_file
				fileout = codecs.open(filepath, 'w', config.charset)
				fileout.write(page_template % {
					'charset': config.charset,
					'pagename': pagename,
					'pagehtml': pagehtml,
					'logo_html': logo_html,
					'navibar_html': navibar_html,
					'timestamp': timestamp,
					'theme': request.cfg.theme_default,
					'date_str': date_str,
				})
				fileout.close()
