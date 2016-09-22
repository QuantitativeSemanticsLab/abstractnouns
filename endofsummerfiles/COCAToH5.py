import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import nltk
from nltk.tokenize import *

from pandas import HDFStore
from nltk.tokenize import sent_tokenize

import re

import subprocess

filepath = sys.argv[1]
filetup = re.findall(r'COCA_corpus\/(\w*)\/\/(\w*).txt', filepath)
 
filename = filetup[0][1]
foldername = filetup[0][0]
h5name = 'COCA_corpus/COCAStore_' + foldername[5:] + '.h5'
#h5name = 'testh5'

f = open(filepath)
text = f.read()

sent_tokenize_list = sent_tokenize(text)
listlen = len(sent_tokenize_list)
df = pd.DataFrame(' ', index = np.arange(listlen), columns = ['sent', 'tags', 'parse'])

#go through list of sentences 
for i in range(listlen):
#for sent in sent_tokenize_list[0:10]:
	sent = sent_tokenize_list[i]
	if "@ @ @" not in sent:
#store sentence in txt
		textfile = open('test.txt', 'w')
		textfile.write(sent)
		textfile.close()
#run tag on txt, strip newlines, store as var
		#tags = subprocess.check_output(['java', '-mx5000m', '-cp', 'stanford-parser.jar:slf4j-simple.jar:slf4j-api.jar', 'edu.stanford.nlp.parser.lexparser.LexicalizedParser', '-retainTMPSubcategories', '-outputFormat', 'wordsAndTags', 'englishPCFG.ser.gz', 'test.txt'])
		#tags = tags.replace('\n', '')
#run parse on txt, strip newlines, store as var
		parse = subprocess.check_output(['java', '-mx5000m', '-cp', 'stanford-parser.jar:slf4j-simple.jar:slf4j-api.jar', 'edu.stanford.nlp.parser.lexparser.LexicalizedParser', '-retainTMPSubcategories', '-outputFormat', 'wordsAndTags,typedDependencies', 'englishPCFG.ser.gz', 'test.txt'])
		parray = parse.split('\n')
		tags = parray[0]
		parse = ' '.join(parray[1:])
#create list of sentence, tags, parse
#append list to dataframe
		df.set_value(i, 'sent', sent)
		df.set_value(i, 'tags', tags)
		df.set_value(i, 'parse', parse)
#store dataframe in h5 under filename

store = HDFStore(h5name)
store[filename] = df

print store

store.close()

