# -*- coding: utf-8 -*-

import random
from bs4 import BeautifulSoup
from urllib import urlopen
import re, urlparse

# \s == start of chain
# \e == end of chain
# chain = {string word, {int amounts, string following_word}}

blocked_chars = ["(", ")"]

main_chain = {}


def calculate_probability(dictionary):
	amount = 0
	for i in dictionary:
		amount += dictionary[i]

	copy_dictionary = dictionary.copy()
	for i in copy_dictionary:
		copy_dictionary[i] = float(dictionary[i]) / amount

	return copy_dictionary


def add_words(chain, string):
	d = ' '
	word_list = [e+d for e in string.split(d)]
	word_list = ['\s'] + word_list

	for index, word in enumerate(word_list):
		if '\e' in word:
			word = '\s'

		for blocked_char in blocked_chars:
			word = word.replace(blocked_char, '')

		try:
			next_word = word_list[index + 1]
			for blocked_char in blocked_chars:
				next_word = next_word.replace(blocked_char, '')
		except IndexError:
			next_word = '\e'

		if word in chain:
			if next_word in chain[word]:
				chain[word][next_word] += 1
			else:
				chain[word][next_word] = 1
		else:
			chain[word] = {next_word: 1}


def get_random_element(dictionary):
	x = 0
	rand = random.random()
	dictionary = calculate_probability(dictionary)
	for i in dictionary:
		x += dictionary[i]
		if(x > rand):
			return i


def print_chain(chain):

	current_word = '\s'
	sentence = ''

	while current_word != '\e':
		sentence += current_word
		if current_word in chain:
			current_word = get_random_element(chain[current_word])
		else:
			current_word = '\e'


	return sentence[2:] # remove the '\s'


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts))


def get_data_from_page(url, html_class):
	print url
	results = []
	try:
		html = urlopen(url).read()
		soup = BeautifulSoup(html, 'html.parser')
		entries = soup.findAll('div', {'class': html_class})
		for entry in entries:
			paragraphs = entry.findAll('p')
			for paragraph in paragraphs:
				results.append(str(paragraph.get_text().encode('utf-8')))
	except IOError:
			print "Bad link: " + url
	return results


# temporary
def load_subreddit(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	commentUrls = soup.findAll('a', {'class': 'comments'})
	urls = []
	for commentUrl in commentUrls:
		urls.append(iriToUri(commentUrl['href']))
	return urls


def main():	

	urls = []

	subreddits = [	"https://www.reddit.com/",
					"https://www.reddit.com/r/askreddit",
					"https://www.reddit.com/r/videos",
					"https://www.reddit.com/r/pics",
					"https://www.reddit.com/r/funny",
					"https://www.reddit.com/r/pcmasterrace",
					"https://www.reddit.com/r/self", 
					"https://www.reddit.com/r/WTF",
					"https://www.reddit.com/r/announcements",
					"https://www.reddit.com/r/learnprogramming",
					"https://www.reddit.com/r/confession",
					"https://www.reddit.com/r/programmerhumor",
					"https://www.reddit.com/r/polandball",
					"https://www.reddit.com/r/globaloffensive",
					"https://www.reddit.com/r/gameofthrones"]

	for subreddit in subreddits:
		for url in load_subreddit(subreddit):
			urls.append(url)

	for url in urls:
		for entry in get_data_from_page(url, 'md'):
			add_words(main_chain, entry)

	for i in range(0, 20):
		print print_chain(main_chain) + "\n"


main()






