#!/usr/bin/env python3

# Events calendar module
import json
import datetime
import sys
import inspect
import crib
import hashlib

EVENT_TYPES = {'class', 'dance', 'workshop', 'ball', 'demo', 'hidden', 'news'}
CALENDAR_TYPES = {'class', 'dance', 'workshop', 'ball', 'demo', 'hidden'}

# Event db schema: The file format is JSON.
# The whole file is an array full of event objects.
# Each event object is an associative array of key=value pairs; the key MUST
# be expressed as a string.
#
# Keys are as follows:
# start:	The start date/time of the event, in YYYY/MM/DD HH:MM format. (required)
# type:		One of EVENT_TYPES above. (required)
# name:		The name of the event. (required)
#
# end:		The end date/time of the event, in YYYY/MM/DD HH:MM format.
# date_format:	A Python strptime format string, if "start" and "end" are in a
#		different format.
# location:	Where the event is happening.
# local:	Is this a local event? (True/False, default is True)
# cribfile:	Name of a crib file describing the dances for this event.
# url:		URL describing this event.
# ready:	Is this event ready for display? (True/False, default is True)
class event_database:
	'''Load and query events.'''
	def __init__(self):
		self.dbfile = ''
		self.events = []

	def load_from_json(self, fd):
		'''Load events from a JSON source.'''
		global EVENT_TYPES

		raw_data = json.load(fd)
		self.dbfile = fd.name
		for entry in raw_data:
			if len(entry) == 0:
				continue
			assert "start" in entry, "All entries must have a start date/time."
			assert "type" in entry, "All entries must have a type."
			assert "name" in entry, "All entries must have a name."
			assert entry['type'] in EVENT_TYPES, "All events must be either a class, dance, workshop, or ball."
			if 'date_format' in entry:
				date_format = entry['date_format']
			else:
				date_format = '%Y/%m/%d %H:%M'
			if entry['start'] is None:
				entry['start'] = datetime.datetime.min
			else:
				entry['start'] = datetime.datetime.strptime(entry['start'], date_format)
			if 'end' in entry:
				entry['end'] = datetime.datetime.strptime(entry['end'], date_format)
			if 'ready' in entry:
				entry['ready'] = bool(entry['ready'])
			else:
				entry['ready'] = True
			if 'local' in entry:
				entry['local'] = bool(entry['local'])
			else:
				entry['local'] = True
			self.events.append(entry)
		self.events.sort(key = lambda x: x['start'])

	def __repr__(self):
		return repr(self.events)

	def today():
		'''Returns today as a datetime.'''
		return datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

	def week_from_now():
		'''Returns today + 7 days as a datetime.'''
		d = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		td = datetime.timedelta(7)
		return d + td

	def event_start_satisfies(evt, before, after):
		'''Does the start of this event fit between these dates?'''
		if (before is None or (evt['start'] != datetime.datetime.min and evt['start'] <= before)) and \
		   (after is None or (evt['start'] != datetime.datetime.min and evt['start'] >= after)):
			return True
		return False

	def iterate_events(self, evt_type, starts_before, starts_after, is_local):
		'''Iterate over events, given criteria.'''
		global CALENDAR_TYPES

		for evt in self.events:
			if evt['type'] in CALENDAR_TYPES and \
			   (evt_type is None or evt['type'] in evt_type) and \
			   (is_local is None or evt['local'] == is_local) and \
			   event_database.event_start_satisfies(evt, starts_before, starts_after):
				yield evt

	def iterate_news(self, starts_before, starts_after):
		'''Iterate over news items, given criteria.'''
		global CALENDAR_EVENTS

		for evt in self.events:
			if evt['type'] == 'news' and \
			   event_database.event_start_satisfies(evt, starts_before, starts_after):
				yield evt

	def next_3mo_events(self):
		'''Iterate over all upcoming events.'''
		y = datetime.timedelta(days = 90)
		d = event_database.today()
		return self.iterate_events(EVENT_TYPES - {'class'}, d + y, d, None)

	def all_upcoming(self):
		'''Iterate over all upcoming events.'''
		return self.iterate_events(None, None, event_database.today(), None)

	def all_non_class_past(self):
		'''Iterate over all past events except classes.'''
		all_but_classes = CALENDAR_TYPES - set(['class'])
		return self.iterate_events(all_but_classes, event_database.today(), None, None)

	def classes(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over class events.'''
		return self.iterate_events(['class'], starts_before, starts_after, is_local)

	def dances(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over dance events.'''
		return self.iterate_events(['dance', 'ball'], starts_before, starts_after, is_local)

	def balls(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over ball events.'''
		return self.iterate_events(['ball'], starts_before, starts_after, is_local)

	def nonlocal_events(self, starts_before = None, starts_after = None):
		'''Iterate over non local events.'''
		return self.iterate_events(None, starts_before, starts_after, False)

class event_queries:
	'''Queries of the event database.'''

	def __format_date(d, show_year = True, show_time = True):
		'''Format the dates all nice.'''
		now = event_database.today()
		if d.hour > 12:
			meridian = 'pm'
			hour = d.hour - 12;
		elif d.hour == 12:
			meridian = 'pm'
			hour = d.hour
		elif d.hour == 0 and d.minute == 0:
			show_time = False
		else:
			meridian = 'am'
			hour = d.hour
		if now.year != d.year and show_year:
			ret = '%d/%d/%d' % (d.month, d.day, d.year)
		else:
			ret = '%d/%d' % (d.month, d.day)
		if show_time:
			ret = ret + ' at %d:%02d%s' % (hour, d.minute, meridian)
		return ret

	def next_class_summary(events):
		'''When and where are the next classes?'''
		for evt in events.classes(starts_after = event_database.today(), is_local = True):
			print('%s<br />%s<br />%s' % (evt['name'], event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_dance_summary(events):
		'''When and where are the next dances?'''
		for evt in events.dances(starts_after = event_database.today(), is_local = True):
			url = evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], url)
			print('%s<br />%s<br />%s' % (url, event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_dance_summary_oneline(events):
		'''When and where are the next dances?  (Single line version)'''
		for evt in events.dances(starts_after = event_database.today(), is_local = True):
			url = evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], url)
			print('%s (%s, %s)' % (url, event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_dance_crib(events):
		'''Generate a crib of the next dance.'''
		for evt in events.dances(starts_after = event_database.today(), is_local = True):
			if 'crib' in evt:
				crib_name = 'cribs/' + evt['crib']
				crib.generate_crib(crib_name, open(crib_name), sys.stdout)
				sys.stdout.write('<p class="noprint">[<a href="javascript:crib_toggle_all(true);">Expand All</a> | <a href="javascript:crib_toggle_all(false);">Collapse All</a>]</p>\n')
			elif 'url' in evt:
				sys.stdout.write('<p>Download a <a href="%s">crib sheet</a> of the dances on the program.</p>\n' % evt['url'])
			else:
				print('We are sorry, but there is no posted program yet.  Please check back later.')
			return

	def next_ball_summary(events):
		'''When and where is the next ball?'''
		for evt in events.balls(starts_after = event_database.today(), is_local = True):
			url = evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], url)
			print('%s<br />%s<br />%s' % (url, event_queries.__format_date(evt['start']), evt['location']))
			return

	def portland_ball_crib(events):
		'''Generate a crib of the most recent complete Portland ball.'''
		ready_balls = [x for x in events.balls() if (x['local'] and x['ready'] and x['location'] == "Portland")]
		crib_fname = None
		for evt in ready_balls:
			if 'crib' in evt:
				crib_fname = evt['crib']

		if crib_fname == None:
			print('We are sorry, but there is no posted program yet.  Please check back later.')
		else:
			crib_name = 'cribs/' + crib_fname
			crib.generate_crib(crib_name, open(crib_name), sys.stdout)

	def sw_wa_ball_crib(events):
		'''Generate a crib of the most recent complete SW Washington ball.'''
		ready_balls = [x for x in events.balls() if (x['local'] and x['ready'] and x['location'] == "Vancouver, Wash.")]
		crib_fname = None
		for evt in ready_balls:
			if 'crib' in evt:
				crib_fname = evt['crib']

		if crib_fname == None:
			print('We are sorry, but there is no posted program yet.  Please check back later.')
		else:
			crib_name = 'cribs/' + crib_fname
			crib.generate_crib(crib_name, open(crib_name), sys.stdout)

	def next_travel_summary(events):
		'''When and where are the next three non-local events?'''
		print('<ul id="ps_travel">')
		for evt in list(events.nonlocal_events(starts_after = event_database.today()))[:3]:
			url = '%s' % evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], evt['name'])
			print('<li>%s (%s)</li>' % (url, event_queries.__format_date(evt['start'])))
		print('</ul>')

	def upcoming_classes(events):
		'''All upcoming classes in the next seven days.'''
		print('<ul id="ps_travel">')
		for evt in list(events.classes(starts_after = event_database.today(), starts_before = event_database.week_from_now())):
			url = '%s' % evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], evt['name'])
			print('<li>%s (%s, %s)</li>' % (url, event_queries.__format_date(evt['start']), evt['location']))
		print('</ul>')

	def next_event(events):
		'''The next event.'''
		for evt in events.all_upcoming():
			print(evt)
			return

	def upcoming_events_short(events):
		'''All upcoming events in the next 90 days.'''
		return event_queries.upcoming_events_generator(events.next_3mo_events(), 3)

	def upcoming_events(events):
		'''All upcoming events that we know about.'''
		return event_queries.upcoming_events_generator(events.all_upcoming(), 2, True)

	def past_events_list(events):
		'''All past events that we know about.'''
		return event_queries.upcoming_events_generator(events.all_non_class_past(), 2)

	def upcoming_events_generator(event_iterator, heading_level, bold_for_nonregular = False):
		last_date = None
		list_open = False
		for evt in event_iterator:
			if last_date is None or \
			   last_date.year != evt['start'].year or \
			   last_date.month != evt['start'].month:
				if list_open:
					print("\t</table>")
				print("<h%d>%s</h%d>" % (heading_level, evt['start'].strftime('%B %Y'), heading_level))
				print("\t<table class=\"event_list\">")
				list_open = True
			url = evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], evt['name'])
			loc = ''
			if 'location' in evt:
				loc = '%s' % evt['location']
			style = ''
			if evt['type'] == 'class':
				style = ' class="regular_event"'
				bullet = '○'
			else:
				style = ' class="nonregular_event"'
				bullet = '●'
			if not bold_for_nonregular:
				style = ''
			criburl = ''
			if 'crib' in evt:
				alg = hashlib.sha1()
				alg.update(evt['crib'].encode('utf-8'))
				dance_id = alg.hexdigest()
				criburl = ' [<a href="/past_programs.html#program_%s">crib</a>]' % dance_id
			print("\t<tr><td>%s</td><td><div><span%s>%s</span>%s</div><div class=\"event_location\">%s</div></td><td>%s</td></tr>" % (bullet, style, url, criburl, loc, event_queries.__format_date(evt['start'], False)))
			last_date = evt['start']

		if list_open:
			print("\t</table>")

	def has_crib(events):
		'''Anything with a crib.'''
		for evt in sorted(events.events, key = lambda x: x['start'], reverse = True):
			if 'crib' not in evt:
				continue
			alg = hashlib.sha1()
			alg.update(evt['crib'].encode('utf-8'))
			dance_id = alg.hexdigest()
			print("<table class=\"program_box\">\n")
			print("<tr><td>\n")
			print("<span id=\"progbody_%s_ctl\" onclick=\"crib_toggle('progbody_%s');\" class=\"crib_ctl\">&#9654;</span>\n" % (dance_id, dance_id))
			print("</td><td class=\"program_title_cell\">\n")
			print("<h2>")
			print("<a id=\"program_%s\"></a>" % dance_id)
			print("<a href=\"#program_%s\" onclick=\"crib_toggle('progbody_%s'); return false;\" class=\"program_title\">%s</a>\n" % (dance_id, dance_id, evt['name']))
			print("</h2>\n")
			print("</td></tr>\n")
			loc = ''
			if 'location' in evt:
				loc = '%s on ' % evt['location']
			date = ''
			if evt['start'] > datetime.datetime.min:
				date = evt['start'].strftime('%e %B %Y')
			if loc != '' or date != '':
				print("<tr><td></td><td>\n")
				print("<p>%s%s</p>" % (loc, date))
				print("</td></tr>\n")

			print("<tr id=\"progbody_%s\" class=\"program_body\"><td></td><td>\n" % dance_id);
			crib_name = 'cribs/' + evt['crib']
			crib.generate_crib(crib_name, open(crib_name), sys.stdout)
			print("</td></tr>\n")
			print("</table>\n")

	def last_five_news(events):
		'''Last five events.'''
		n = 0
		print("<ul>\n")
		before_date = event_database.today().replace(hour = 23, minute = 59, second = 59)
		for evt in sorted(events.iterate_news(starts_before = before_date, starts_after = None), key = lambda x: x['start'], reverse = True):
			if 'details' in evt:
				print("<li><b>(%s) %s</b>: %s</li>\n" % (event_queries.__format_date(evt['start'], show_time = False), evt['name'], evt['details']))
			else:
				print("<li><b>(%s) %s</b></li>\n" % (event_queries.__format_date(evt['start'], show_time = False), evt['name']))
			n += 1
			if n > 5:
				break
		print("</ul>\n")

	def dump(events):
		print(repr(events))

	def help(events):
		print('Possible queries:')
		pred = lambda x: inspect.isfunction(x) and \
				 not x.__name__.startswith('__')
		for m in inspect.getmembers(event_queries, pred):
			print(m[0])

	def makedep(events):
		'''Generate Makefile dependencies.'''
		pred = lambda x: inspect.isfunction(x) and \
				 not x.__name__.startswith('__') and \
				 not x.__name__ in ['dump', 'help', 'makedep']
		for m in inspect.getmembers(event_queries, pred):
			func = m[0]
			print('CLEAN+=%s.html' % func)
			print('%s.html: %s' % (func, events.dbfile))
			print('\t%s %s %s > $@' % (sys.argv[0], events.dbfile, func))
			print('')

		crib_dep = '%s: ' % events.dbfile
		for e in events.events:
			if 'crib' in e:
				crib_dep = crib_dep + ' cribs/%s.crib' % e['crib'][:-4]
		print(crib_dep)

def main():
	if len(sys.argv) != 3 or '--help' in sys.argv:
		print("Usage: %s dbfile query" % sys.argv[0])
		event_queries.help(None)
		return 0

	events = event_database()
	events.load_from_json(open(sys.argv[1], 'r'))
	member = inspect.getmembers(event_queries, lambda x: inspect.isfunction(x) and x.__name__ == sys.argv[2])
	assert len(member) == 1, "Unknown query name."
	member[0][1](events)
	return 0

if __name__ == "__main__":
	sys.exit(main())
