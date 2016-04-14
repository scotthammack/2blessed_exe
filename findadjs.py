#!/usr/local/bin/python
# coding: utf-8
#
# findadjs.py
# reads a tagged part-of-speech list for adjectives and tries to filter out
# comparative and superlative forms. (It actually just filters out anything
# that ends with "er" or "est", which is not ideal, but close enough for
# my purposes.)
# Output is a python-formatted array of strings called 'adjectives'.
#
# uses the Moby part-of-speech II list
# (http://icon.shef.ac.uk/Moby/mpos.html)

import re, sys, csv

wordlist_file = "mobyposi.i"

with open(wordlist_file, 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	pattern1 = re.compile('A')
	pattern2 = re.compile('(er|est)$')
	print "#!/usr/local/bin/python\n# coding: utf-8\n\n"
	print "adjectives = ["
	for row in csvreader:
		if pattern1.search(row[1]):
			if not pattern2.search(row[0]):
				print "\t\"" + row[0] + "\", "
	print "]"
