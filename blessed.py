#!/usr/local/bin/python
# coding: utf-8
#
# blessed.py by Scott Hammack
# https://twitter.com/2blessed_exe
# generates rhyming variations on the phrase "too blessed to be stressed"
#
# This is kind of shitty because the word list I'm using to decide whether
# a word is an adjective is completely separate from the word list used by
# the pronouncing library, so there are plenty of possible rhymes that it
# won't find. But, whatever.

import random, pronouncing, tweepy
from adjs import adjectives

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

word2 = None
prefixes = [ 'un', 'in', 'im', 'non', 'dis', 'de', 'ir', 'a', 'an' ]

def is_adj(word):
	# to determine whether the result is a viable adjective, check it
	# against the list generated by adjs.py
	for i in adjectives:
		if i == word:
			return True
	return False

def is_negated(word1, word2):
	# check to see if the rhyme is just the other word with a negative
	# prefix stuck on. stuff like "too unhappy to be happy" is crappy
	for prefix in prefixes:
		if word1 == prefix + word2 or word2 == prefix + word1:
			return True
	return False

while not word2:
	rhymes = []

	# pick random words until we find one with at least one rhyme
	while len(rhymes) < 1:
		word1 = str(random.choice(adjectives))
		print word1
		rhymes = pronouncing.rhymes(word1)
		print rhymes
		print len(rhymes)

	# we're about to iterate through the rhyme list and post the
	# first suitable rhyme we find. thus, we need to randomize the
	# order of the list; otherwise the same word will always end up
	# with the same rhyme.
	random.shuffle(rhymes)

	# try each rhyme in the list until we find one that is an
	# adjective but is not just our first word with a prefix that
	# negates it
	for attempt in rhymes:
		attempt = str(attempt)
		print "Trying %s." % attempt
		if is_adj(attempt) and not is_negated(word1, attempt):
			word2 = attempt
			break
	
	# if we didn't find anything suitable, we just go back to the
	# beginning of the loop and pick a new word.

# compose and post the tweet
phrase = "too %s to be %s" % (word1, word2)
print phrase
api.update_status(phrase)
