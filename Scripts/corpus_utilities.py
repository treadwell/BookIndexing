import os
import json
import extract_words


def create_English_wordlist(textfile):
	'''Creates an English word list from a text file.  Allows removal of words that shouldn't
	bet in the file (removals) and addition of words that should be there (additions).'''

	# f =  open('../data/' + textfile, 'w')

	with open('../data/' + textfile, 'r') as f:
		lines = f.readlines()

	lines = [line.strip() for line in lines]

	removals  = ["b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", 
			"o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
			"ah", "ad", "aa", "fe", "ae", "ed", "ab", "ni", "fa", "cid", 
			u'ca', u'aga', u'z', u'z', u'z', u'z', u'z', u'z', u'z', u'ah']



	words = [line for line in lines if line.lower() not in removals]

	additions = [u'operations', u'wiki', u'cons', u'methods', u'exists', 
	u'called', u'int', u'wikipedia', u'variables', u'africa', 
	u'heard', u'numbers',  u'org', u'contains', 
 u'asked', u'functions', u'errors', u'dna', u'dimensions', u'usa',  u'began', 
u'forests',   u'systems', u'algorithms', u'seemed', 
u'bits',   u'http', u'wanted', u'models', u'turing', u'processing', 
u'problems', u'trees', u'plyr', u'edges',  u'scores', u'using', u'evaluator', u'packages', 
u'procedures', u'obtained', u'processes',   u'things', u'follows', u'notes',  
u'accepts', u'cells',  u'looked', u'graphs', u'boolean', u'extensions', u'adaboost', 
u'sets', u'shared', u'okay', u'com', u'strings', u'gates', u'cdf', 
u'results', u'stored', u'expressions',  u'2011', u'heidelberg', 
u'pruned',  u'feet',  u'bytes', u'courses', 
 u'ddply', u'www',   u'measurements', 
u'steps', u'shows',  u'terms',  u'boosting', u'100',  
u'programming', u'threads', u'followed', u'others', u'dataset',  u'agents', u'frames', 
u'loc', u'answered', u'pred',  u'returns', u'passed', u'toc', u'eyes', u'semaphores', 
u'labelled',  u'nodded',  u'circuits',  u'bounds', u'values', 
u'def',   u'computing', u'moves',  u'html', u'arguments', 
  u'blocks',  u'accepting',  u'pages', 
 u'programs', u'patterns', u'2006', u'exp', u'cpu', u'randomforest',  u'registers', u'satisfies', u'summaries', 
 u'means', u'rules', u'words', 
 	u'shadows', u'rpart', u'runs', 
 	u'markov', u'configurations',  u'examples', u'download',  u'sounds', 
 	u'machines', u'nondeterministic', u'pyplot',   u'proc', u'lapply', 
u'objects', u'groups', u'byte', u'pairs',  u'players', u'ants',  u'unix', 
u'wasn', u'reached', u'allocated', u"''.", u'takes', u'predictions',  u'500', 
 u'splits', u'arrays', 
u'moved',  u'gcd', u'frakir',  u'env', 
u'elements', u'uses',  u'eval',   u'fsm', 
u'proceedings', u'components', u'caching']

	words += additions

	with open('../data/' + "English_wordlist" + '.json', 'w') as outfile:
		json.dump(words, outfile, 
			sort_keys = True, 
			indent = 4,
			# ensure_ascii=False,
			)

def update_English_wordlist(json_wordlist, addition_list):
	'''Updates an existing wordlist file with new words gathered from looking at a corpus.'''

	English_wordlist = json.load(open('../data/' + "English_wordlist.json"))

	English_wordlist += addition_list

	English_wordlist = list(set(English_wordlist))

	with open('../data/' + "English_wordlist" + '.json', 'w') as outfile:
		json.dump(English_wordlist, outfile, 
			sort_keys = True, 
			indent = 4,
			# ensure_ascii=False,
			)


if __name__ == '__main__':


	print("--------------------------------")

	English_wordlist = json.load(open('../data/' + "English_wordlist.json"))

	path_to_data = "../data"

	search_list = []

	for root, dirs, files in os.walk(path_to_data):
		for file in files:
			if file.endswith(".json"):
				#print root
				#print file

				search_list.append(os.path.join(path_to_data, file))

	search_list.remove('../data/corpus_data.json')
	search_list.remove('../data/English_wordlist.json')
	print(search_list)

	to_be_added = []

	for item in search_list:
		test_book_dict = json.load(open(item))

		test_book_words = test_book_dict["words"]

		print("\nTest book words:", test_book_words[0:10])

		good_words, invalid_words = extract_words.filter_English_words(test_book_words, English_wordlist, 10)

		print("good words:", good_words[0:10])
		print("invalid words:", invalid_words[0:10])
		to_be_added += invalid_words[0:20]

	to_be_added = list(set(to_be_added))
	print("\n", to_be_added)

	json_wordlist = json.load(open('../data/' + "English_wordlist.json"))

	print(len(json_wordlist))

	addition_list = [ u'add', u'new', u'words', u'here', u'test123',
						u'mit', u'etc', u'lookup', u'structures', u'korea', u'sapply', u'lines' ]

	update_English_wordlist(json_wordlist, addition_list)

	new_json_wordlist = json.load(open('../data/' + "English_wordlist.json"))

	print(len(new_json_wordlist))




