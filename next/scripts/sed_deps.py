#!/usr/bin/env python3

# Generate Makefile dependencies for our sed templating nonsense.
# Assume that we're only doing this for *.in files.
import sys

def extract_subst_from_sed(rules, fd):
	'''Extract key->file mappings from a sed script.'''
	for line in fd:
		line = line.strip()
		if not line.startswith('/'):
			continue
		end_slash = line[1:].find('/')
		assert end_slash >= 1, "Unknown key '%s'!" % (line[1:])
		cmd = line[end_slash + 2 : end_slash + 3]
		if cmd != 'r':
			continue
		key = line[1 : end_slash + 1]
		value = line[end_slash + 4:]
		assert key not in rules, "Rule '%s' already exists!" % key
		rules[key] = value

def iterate_deps(rules, fd):
	'''Iterate the file dependencies of a particular file.'''
	for line in fd:
		for key in rules:
			if key in line:
				yield rules[key]

def main():
	if len(sys.argv) < 2 or '--help' in sys.argv:
		print('Usage: %s sed_files : template_files' % sys.argv[0])
		return 0

	rules = {}
	collecting_rules = True
	for arg in sys.argv[1:]:
		if arg == ':':
			collecting_rules = False
			continue
		if collecting_rules:
			extract_subst_from_sed(rules, open(arg))
		else:
			sys.stdout.write('%s:' % arg)
			for dep in iterate_deps(rules, open(arg)):
				sys.stdout.write(' %s' % dep)
			sys.stdout.write('\n')

if __name__ == '__main__':
	main()
