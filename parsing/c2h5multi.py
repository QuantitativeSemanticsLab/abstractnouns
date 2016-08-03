import sys

import numpy as np

import pandas as pd
from pandas import Series, DataFrame
from pandas import HDFStore

import nltk
from nltk.tokenize import *
from nltk.tokenize import sent_tokenize

import re
import subprocess

#import joblib
from joblib import Parallel, delayed
import multiprocessing

def storesent(sent):
	textfile = open('test2.txt', 'w')
	textfile.write(sent)
	textfile.close()

def parsesent(i, sent):
	process = multiprocessing.current_process().name
	testfilename = 'test' + process + '.txt'
	textfile = open(testfilename, 'w')
	textfile.write(sent)
	textfile.close()
	parse = subprocess.check_output(['java', '-mx5000m', '-cp', 'stanford-parser.jar:slf4j-simple.jar:slf4j-api.jar', 'edu.stanford.nlp.parser.lexparser.LexicalizedParser', '-retainTMPSubcategories', '-outputFormat', 'wordsAndTags,typedDependencies', 'englishPCFG.ser.gz', testfilename])
	parray = parse.split('\n')
	tags = parray[0]
	parse = ' '.join(parray[1:])
	#df.set_value(i, 'sent', sent)
	#df.set_value(i, 'tags', tags)
	#df.set_value(i, 'parse', parse)
	return [sent, tags, parse]

def parseframe(i):
	sent = sent_tokenize_list[i]
	if "@ @ @" not in sent:
		parse = parsesent(i, sent)
		return parse
	else:
		return ['','','']

filepath = sys.argv[1]
filetup = re.findall(r'COCA_corpus\/(\w*)\/(\w*).txt', filepath)

filename = filetup[0][1]
foldername = filetup[0][0]
h5name = 'COCA_corpus/COCAStore_' + foldername[5:] + '.h5'

f = open(filepath)
text = f.read()

sent_tokenize_list = sent_tokenize(text)
listlen = len(sent_tokenize_list)
dftok = pd.DataFrame(sent_tokenize_list)
dftok.to_csv('dftok.csv')

#df = pd.DataFrame(' ', index = np.arange(listlen), columns = ['sent', 'tags', 'parse'])


inputs = range(listlen)
#inputs = range(listlen/100)
num_cores = multiprocessing.cpu_count()
parselist = Parallel(n_jobs=num_cores)(delayed(parseframe)(i) for i in inputs)
df = pd.DataFrame(parselist, columns = ['sent', 'tags', 'parse'])

print df.head(15)
print 'storing dataframe'
store = HDFStore(h5name)
store[filename] = df

print store
store.close()

