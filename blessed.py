import random, pronouncing, tweepy, nltk
from adjs import adjectives

from twitter_secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

word2 = None

def is_adj(word):
	for i in adjectives:
		if str(i[0]) == str(word):
			return True
	return False

def is_negated(word1, word2):
	prefixes = [ 'un', 'in', 'im', 'non', 'dis', 'de' ]
	for prefix in prefixes:
		if str(word1) == prefix + str(word2) or str(word2) == prefix + str(word1):
			return True
	return False

while not word2:
	rhymes = []

	while len(rhymes) < 1:
		word1 = random.choice(adjectives)[0]
		print word1
		rhymes = pronouncing.rhymes(str(word1))
		print rhymes
		print len(rhymes)

	word2 = random.choice(rhymes)
	random.shuffle(rhymes)

	for attempt in rhymes:
		print "Trying %s." % attempt
		if is_adj(attempt) and not is_negated(word1, attempt):
			word2 = attempt
			break

phrase = "too %s to be %s" % (word1, word2)
print phrase
api.update_status(phrase)
