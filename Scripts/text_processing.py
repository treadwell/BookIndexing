import json
import math


def find_ll_keywords(text_freq_dict, corpus_freq_dict):
	'''Use log-likelihood statistic to return the list of text words in "surprisingness"
	order. Function returns a tuple of (word, text occurrences, corpus occurrences, 
		log-likelihood metric'''

	text_size = sum(text_freq_dict.values())
	corpus_size = sum(corpus_freq_dict.values())
	keyword_list = []
	
	for w in text_freq_dict.keys()[0:100]:
	 	a = text_freq_dict[w]
	 	try:
	 		b = corpus_freq_dict[w]
	 	except KeyError:
	 		b = 1
	 	c = text_size - a
	 	d = corpus_size - b
	 	Gsquare = 2*(a*math.log(a) + b*math.log(b) + c*math.log(c) + d*math.log(d) -
	 		(a + b)*math.log(a+b) - (a+c)* math.log(a+c) -
	 		(b + d)*math.log(b+d) - (c+d)*math.log(c+d) +
	 		(a + b + c +d)*math.log(a+b+c+d))  # is natural log correct?
	 	keyword_list.append((w, a, b, Gsquare))
	 	
	keyword_list = sorted(keyword_list, key=lambda word: word[3], reverse=True)
	return keyword_list


if __name__ == "__main__":

	# for each of the title files in the data directory:  (I think...)

	try:
		text_file = json.load(open('../data/file_data.json'))
		text_freq = text_file["freq"]
		print type(text_freq)
		print "title_dict imported"
	except IOError:  # 
		print "No existing title dictionary, execution halted"

	try:
		corpus_file = json.load(open('../data/corpus_data.json'))
		corpus_freq = corpus_file['freq']
		print type(corpus_freq)
		print "corpus_data imported"
	except IOError:  # 
		print "No existing corpus dictionary, execution halted"

	print find_ll_keywords(text_freq, corpus_freq)
