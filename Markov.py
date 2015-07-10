# -*- coding: utf-8 -*-

import random
from bs4 import BeautifulSoup
from urllib import urlopen

# \s == start of chain
# \e == end of chain

main_chain = {} # {string word, {int amounts, string following_word}}


def get_data_from_page(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	entries = soup.findAll('div', {'class': 'md'})
	results = []
	for entry in entries:
		results.append(str(entry.get_text().encode('ascii', 'ignore')))
	return results


def calculate_probability(dictionary):
	amount = 0
	for i in dictionary:
		amount += dictionary[i]

	for i in dictionary:
		dictionary[i] = float(dictionary[i]) / amount

	return dictionary


def add_words(chain, string):
	d = ' '
	word_list = [e+d for e in string.split(d)]
	word_list = ['\s'] + word_list

	for index, word in enumerate(word_list):
		if '\e' in word:
			word = '\s'

		try:
			next_word = word_list[index + 1]
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
	#print chain

	current_word = '\s'
	sentence = ''

	while current_word != '\e':
		sentence += current_word
		if current_word in chain:
			current_word = get_random_element(chain[current_word])
		else:
			current_word = '\e'


	return sentence[2:] # remove the '\s'


def main():

	urls = ["https://www.reddit.com/r/self/comments/3cudi0/resignation_thank_you/", "https://www.reddit.com/r/announcements/comments/3cucye/an_old_team_at_reddit/", "https://www.reddit.com/r/IAmA/comments/3cthh6/i_am_attorney_jeremy_glapion_and_i_sue_companies/", "https://www.reddit.com/r/explainlikeimfive/comments/3csd4b/eli5_why_are_satellites_and_the_likes_covered/", "https://www.reddit.com/r/changemyview/comments/3csnry/cmv_video_games_offer_the_greatest_potential_for/", "https://www.reddit.com/r/behindthegifs/comments/3ctpmu/two_dogs_one_mission/"]

	for url in urls:
		for entry in get_data_from_page(url):
			add_words(main_chain, entry)

	print print_chain(main_chain)


#for i in range(1, 100):
main()






