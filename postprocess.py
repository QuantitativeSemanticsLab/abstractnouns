import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
import ast

word = sys.argv[1]
infile = 'outfiles/' + word + 'Out.csv'
df = pd.read_csv(infile)


delete = ['sent','tags','parse', 'Index', 'Relevant Dependencies', 'Sentence Fragment',  'Negation', 'Verb Reference', 'Prepositional Phrases', 'Conjunction Phrases', 'Case Modifiers', 'Appositionals']
for i in delete:
	df = df.drop(i, 1)



def mergeCol(row):
	if pd.isnull(row[columnname]):
		return None
	else:
		lst = ast.literal_eval(row[columnname])
		if len(lst) >= 0:
			cell = ', '.join(lst)
			return cell
		else:
			return None

strip = ['Verb Negation', 'Prepositions', 'Prepositional Subjects', 'Prepositional Objects', 'Determiners', 'Conjunctions', 'Conjoined', 'Compounds', 'Adjectival Modifiers', 'Possesed (owned by noun)', 'Possesive (owner of noun)', 'Numeric Modifiers', 'Adverbial Modifiers', 'Appositional Modifiers', 'Modified Appositives', 'Modality', 'Conditional']


for i in strip:
	columnname = i
	df[columnname] = df.apply(mergeCol, axis=1)

outfile = 'postfiles/' + word + 'Post.csv'
df.to_csv(outfile, index = False)
