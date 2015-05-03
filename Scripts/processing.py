import json


def find_kws(text_pcnt_dict, corpus_pcnt_dict):
	
	for w in text_pcnt_dict.keys():
		a = 



if __name__ == "__main__":

	try:
		text_file = json.load(open('../data/file_data.json'))
		text_pcnt = text_file["percent"]
		print "title_dict imported"
	except IOError:  # 
		print "No existing title dictionary, execution halted"

	try:
		corpus_pcnt = json.load(open('../data/corpus_pcnt.json'))
		print "corpus_pcnt imported"
	except IOError:  # 
		print "No existing corpus dictionary, execution halted"

	find_keywords(text_pcnt, corpus_pcnt)
