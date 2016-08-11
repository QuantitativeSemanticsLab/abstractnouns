import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
import ast
from itertools import chain 
from collections import Counter	
import csv

word = sys.argv[1]
infile = 'outfiles/' + word + 'Out.csv'
df = pd.read_csv(infile)

delete = ['sent','tags','parse', 'Index', 'Relevant Dependencies', 'Sentence Fragment',  'Negation', 'Verb Reference', 'Prepositional Phrases', 'Conjunction Phrases', 'Case Modifiers', 'Appositionals']
lists = ['Verb Negation', 'Prepositions', 'Prepositional Subjects', 'Prepositional Objects', 'Determiners', 'Conjunctions', 'Conjoined', 'Compounds', 'Adjectival Modifiers', 'Possesed owned by noun', 'Possesive owner of noun', 'Numeric Modifiers', 'Adverbial Modifiers', 'Appositional Modifiers', 'Modified Appositives', 'Modality', 'Conditional', 'Allan Tests Passed']
freq = ['Verb Subject Lemma', 'Verb Object Lemma', 'Prepositional Subjects', 'Prepositional Objects', 'Conjoined', 'Compounds', 'Adjectival Modifiers', 'Possesed owned by noun', 'Adverbial Modifiers', 'Appositional Modifiers', 'Modified Appositives', 'Allan Tests Passed']
nonlists = ['Verb Subject', 'Verb Subject Lemma', 'Verb Object',  'Verb Object Lemma']
lowercase = ['Verb Subject', 'Verb Subject Lemma', 'Verb Object', 'Verb Object Lemma', 'Verb Negation', 'Prepositions', 'Prepositional Subjects', 'Prepositional Objects', 'Determiners', 'Conjunctions', 'Conjoined', 'Compounds', 'Adjectival Modifiers', 'Possesed owned by noun', 'Possesive owner of noun', 'Numeric Modifiers', 'Adverbial Modifiers', 'Appositional Modifiers', 'Modified Appositives', 'Modality', 'Conditional', 'Denumerator']
def fixEmpty(row):
	if pd.isnull(row[columnname]):
		return ''
	else:
		return row[columnname]

def listCol(row):
	if pd.isnull(row[columnname]):
		return []
	else: 
		lst = ast.literal_eval(row[columnname])
		if len(lst)>= 1:
			cell = lst
			return cell
		else: 
			return []

def freqCol(col):	
	mergedlist = df[col].tolist()
	if col in nonlists:
		freq = Counter(mergedlist)
	else:
		freq = Counter(chain.from_iterable(mergedlist))
	print freq
	return freq

def stripCol(row):
	lst = row[columnname]
	if len(lst) >= 0:
		cell = ', '.join(lst)
		return cell
	else:
		return None

def lowerCol(row):
	return row[columnname].lower()


for d in delete:
	df = df.drop(d, 1)

for l in lists:
	columnname = l 
	df[columnname] = df.apply(listCol, axis=1)

for n in nonlists:
	columnname = n
	df[columnname] = df.apply(fixEmpty, axis=1)

freqdict={}
for f in freq:
	columnname = f
	freqdict[columnname] = freqCol(columnname)

print freqdict

for l in lists:
	columnname = l
	df[columnname] = df.apply(stripCol, axis=1)

for l in lowercase and lists:
	columnname = l
	df[columnname] = df.apply(lowerCol, axis = 1)


outfile = 'postfiles/' + word + 'Post.csv'
df.to_csv(outfile, index = False)


