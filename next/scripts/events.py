#!/usr/bin/env python3

# Events calendar module
import json
import datetime
import sys
import inspect
import crib

EVENT_TYPES = {'class', 'dance', 'workshop', 'ball', 'demo'}

# Event db schema: The file format is JSON.
# The whole file is an array full of event objects.
# Each event object is an associative array of key=value pairs; the key MUST
# be expressed as a string.
#
# Keys are as follows:
# start:	The start date/time of the event, in YYYY/MM/DD HH:MM format. (required)
# type:		One of EVENT_TYPES above. (required)
# end:		The end date/time of the event, in YYYY/MM/DD HH:MM format.
# date_format:	A Python strptime format string, if "start" and "end" are in a
#		different format.
# name:		The name of the event.
# location:	Where the event is happening.
# local:	Is this a local event? (True/False, default is True)
# cribfile:	Name of a crib file describing the dances for this event.
# url:		URL describing this event.
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
			assert entry['type'] in EVENT_TYPES, "All events must be either a class, dance, workshop, or ball."
			if 'date_format' in entry:
				date_format = entry['date_format']
			else:
				date_format = '%Y/%m/%d %H:%M'
			entry['start'] = datetime.datetime.strptime(entry['start'], date_format)
			if 'end' in entry:
				entry['end'] = datetime.datetime.strptime(entry['end'], date_format)
			if 'local' in entry:
				entry['local'] = bool(entry['local'])
			else:
				entry['local'] = True
			self.events.append(entry)

	def __repr__(self):
		return repr(self.events)

	def event_start_satisfies(evt, before, after):
		'''Does the start of this event fit between these dates?'''
		if (before is None or evt['start'] < before) and \
		   (after is None or evt['start'] > after):
			return True
		return False

	def iterate_events(self, evt_type, starts_before, starts_after, is_local):
		'''Iterate over events, given criteria.'''
		for evt in self.events:
			if (evt_type is None or evt['type'] == evt_type) and \
			   (is_local is None or evt['local'] == is_local) and \
			   event_database.event_start_satisfies(evt, starts_before, starts_after):
				yield evt

	def classes(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over class events.'''
		return self.iterate_events('class', starts_before, starts_after, is_local)

	def dances(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over dance events.'''
		return self.iterate_events('dance', starts_before, starts_after, is_local)

	def balls(self, starts_before = None, starts_after = None, is_local = None):
		'''Iterate over ball events.'''
		return self.iterate_events('ball', starts_before, starts_after, is_local)

	def nonlocal_events(self, starts_before = None, starts_after = None):
		'''Iterate over non local events.'''
		return self.iterate_events(None, starts_before, starts_after, False)

class event_queries:
	'''Queries of the event database.'''

	def __format_date(d):
		'''Format the dates all nice.'''
		now = datetime.datetime.now()
		if now.year != d.year:
			return d.strftime('%m/%d/%Y')
		return d.strftime('%m/%d')

	def next_class_summary(events):
		'''When and where are the next classes?'''
		for evt in events.classes(starts_after = datetime.datetime.now(), is_local = True):
			print('%s at %s' % (event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_dance_summary(events):
		'''When and where are the next dances?'''
		for evt in events.dances(starts_after = datetime.datetime.now(), is_local = True):
			print('%s at %s' % (event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_dance_crib(events):
		'''Generate a crib of the next dance.'''
		for evt in events.dances(starts_after = datetime.datetime.now(), is_local = True):
			if 'crib' in evt:
				crib.generate_crib(open('cribs/' + evt['crib']), sys.stdout)
			else:
				print('We are sorry, but there is no posted program yet.  Please check back later.')
			return

	def next_ball_summary(events):
		'''When and where is the next ball?'''
		for evt in events.balls(starts_after = datetime.datetime.now(), is_local = True):
			print('%s at %s' % (event_queries.__format_date(evt['start']), evt['location']))
			return

	def next_travel_summary(events):
		'''When and where are the next three non-local events?'''
		for evt in list(events.nonlocal_events(starts_after = datetime.datetime.now()))[:3]:
			url = '%s' % evt['name']
			if 'url' in evt:
				url = '<a href="%s">%s</a>' % (evt['url'], evt['name'])
			print('%s (%s), %s<br />' % (url, evt['location'], event_queries.__format_date(evt['start'])))

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
