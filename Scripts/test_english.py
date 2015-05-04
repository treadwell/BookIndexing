import nltk
from nltk.corpus import words
import json

# - text for English words


title_dict = json.load(open('../data/file_data.json'))

text_words = title_dict["words"]


print len(words.words())  # not big enough - I need a much better dictionary

English_words = [w.lower() for w in words.words()]

English_words = set(English_words)

text_valid =  [w for w in text_words if w in English_words]

text_invalid =  [w for w in text_words if w not in English_words]  # missing some obvious ones

#print text_invalid
invalid_text_freq = nltk.FreqDist(text_invalid)
tenMostCommon_invalid = invalid_text_freq.most_common(10)

print tenMostCommon_invalid