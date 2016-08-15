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
		if columnname == 'Prepositional Phrases':
			lst2 = []
			for i in lst:
				string = ' '.join(i)
				string.lower()
				lst2.append(string) 
			cell = lst2
			return lst2
		elif len(lst)>= 1:
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
	return freq

def stripCol(row):
	lst = row[columnname]
	if len(lst) >= 1:
		cell = ', '.join(lst)
		return cell
	else:
		return None

def lowerCol(row):
	if columnname in lowerlist: 
		if len(row[columnname]) >= 1:
			newlist = []
			for i in row[columnname]:
				newlist.append(i.lower())
			return newlist
		else:
			return []
	else:
		return row[columnname].lower()

nonlists = []
lowerlist = []

#do nothing to sent
#delete tags, parse
df = df.drop('tags', 1)
df = df.drop('parse', 1)

#Noun: use to count number of occurances
Noun = word
# print 'Noun:' + Noun
Noun_Count = len(df['Noun'])
# print 'Noun Count:',  Noun_Count

#delete index 
df = df.drop('Index', 1)

#do nothing to Relevant Dependencies

#delete Sentence Fragment
df = df.drop('Sentence Fragment', 1)

#Noun Tag: use to get counts for noun types
columnname = 'Noun Tag'
nonlists.append(columnname)
nountag = freqCol(columnname)
# print nountag
NN_Count = nountag.get('NN')
# print 'NN Count:', NN_Count
NNS_Count = nountag.get('NNS')
# print 'NNS Count:', NNS_Count
NNP_Count = nountag.get('NNP')
# print 'NNP Count:', NNP_Count
NNPS_Count = nountag.get('NNPS')
# print 'NNPS Count:', NNPS_Count

#Plurality of Noun: use to get plural and singular counts
columnname = 'Plurality of Noun'
nonlists.append(columnname)
pluN = freqCol(columnname)
Plural_Noun_Count = pluN.get('plural')
# print 'Plural Noun Count:', Plural_Noun_Count
Singular_Noun_Count = pluN.get('singular')
# print 'Singular Noun Count:', Singular_Noun_Count

#Negation: convert from string to list, use to get negation count, strip of list formatting
columnname = 'Negation'
df[columnname] = df.apply(listCol, axis = 1)
nounNeg = freqCol(columnname)
Noun_Negation_Count = sum(nounNeg.values())
# print 'Noun Negation Count:', Noun_Negation_Count
df[columnname] = df.apply(stripCol, axis = 1)

#delete Verb Reference
df = df.drop('Verb Reference', 1)

#Verb Tag: fix column to include empty strings, adjust for nonlist frequency, use to get verb type counts
columnname = 'Verb Tag'
df[columnname] = df.apply(fixEmpty, axis = 1)
nonlists.append(columnname)
verbtag = freqCol(columnname)
del verbtag['']
Verb_Construction_Count = sum(verbtag.values()) 
# print 'Verb Construction Count:', Verb_Construction_Count
VB_Count = verbtag.get('VB')
# print 'VB Count:', VB_Count
VBD_Count = verbtag.get('VBD')
# print 'VBD Count:', VBD_Count
VBG_Count = verbtag.get('VBG')
# print 'VBG Count:', VBG_Count
VBN_Count = verbtag.get('VBN')
# print 'VBN Count:', VBN_Count
VBP_Count = verbtag.get('VBP')
# print 'VBP Count:', VBP_Count
VBZ_Count = verbtag.get('VBZ')
# print 'VBZ Count:', VBZ_Count

#Plurality of Verb: fix column to include empty strings, use to get singular and plural counts
columnname = 'Plurality of Verb'
df[columnname] = df.apply(fixEmpty, axis = 1)
nonlists.append(columnname)
pluV = freqCol(columnname)
Plural_Verb_Count = pluV.get('plural')
# print 'Plural Verb Count:', Plural_Verb_Count
Singular_Verb_Count = pluV.get('singular')
# print 'Singular Verb Count:', Singular_Verb_Count

#delete Relation to Verb
df = df.drop('Relation to Verb', 1)

#do nothing to Verb Subject

#Verb Subject Lemma: fix column to include empty strings, strip to lowercase, adjust for nonlist frequency, use to get verb subject count, unique count, frequency list
columnname = 'Verb Subject Lemma'
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
nonlists.append(columnname)
verbsubj = freqCol(columnname)
del verbsubj['']
Verb_Subject_Count = sum(verbsubj.values()) 
# print 'Verb Subject Count:', Verb_Subject_Count
Unique_Verb_Subject_Count = len(verbsubj) 
# print 'Unique Verb Subject Count:', Unique_Verb_Subject_Count
for l in list(verbsubj):
	if verbsubj[l] <= (Unique_Verb_Subject_Count * .10):
		del verbsubj[l]
Significant_Verb_Subjects = verbsubj 
# print 'Significant Verb Subjects:', Significant_Verb_Subjects

#Verb Object Lemma: fix column to include empty strings, strip to lowercase, adjust for nonlist frequency,use to get verb object count, unique count, frequency list
columnname = 'Verb Object Lemma'
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
nonlists.append(columnname)
verbobj = freqCol(columnname)
del verbobj['']
Verb_Object_Count = sum(verbobj.values()) 
# print 'Verb Object Count:', Verb_Object_Count
Unique_Verb_Object_Count = len(verbobj) 
# print 'Unique Verb Object Count:', Unique_Verb_Object_Count
for l in list(verbobj):
	if verbobj[l] <= (Unique_Verb_Object_Count * .10):
		del verbobj[l]
Significant_Verb_Objects = verbobj 
# print 'Significant Verb Objects:', Significant_Verb_Objects

#Verb Negation: convert from string to list, use to get negation count, strip of list formatting
columnname = 'Verb Negation'
df[columnname] = df.apply(listCol, 1)
verbNeg = freqCol(columnname)
Verb_Negation_Count = sum(verbNeg.values())
# print 'Verb Negation Count:', Verb_Negation_Count
df[columnname] = df.apply(stripCol, 1)

#Prepositional Phrases: simplify tuples to strings, strip to lowercase, get prep phrase count, strip of list formatting
columnname = 'Prepositional Phrases'
df[columnname] = df.apply(listCol, axis = 1)
preps = freqCol(columnname)
del preps['']
Prepositional_Phrase_Count = sum(preps.values())
# print 'Prepositional Phrase Count:', Prepositional_Phrase_Count
df[columnname] = df.apply(stripCol, axis = 1)


#Prepositions: strip to lowercase, strip of list format
columnname = 'Prepositions'
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(stripCol, axis = 1)
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)

#Prepositional Subjects: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Prepositional Subjects'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
prepsubj = freqCol(columnname)
del prepsubj['']
Prepositional_Subject_Count = sum(prepsubj.values())
# print 'Prepositional Subject Count:', Prepositional_Subject_Count
Unique_Prepositional_Subject_Count = len(prepsubj)
# print 'Unique Prepositional Subject Count:', Unique_Prepositional_Subject_Count
for l in list(prepsubj):
	if prepsubj[l] <= (Unique_Prepositional_Subject_Count * .10):
		del prepsubj[l]
Significant_Prepositional_Subjects = prepsubj
# print 'Significant Prepositional Subjects:', Significant_Prepositional_Subjects
df[columnname] = df.apply(stripCol, axis = 1)


#Prepositional Objects: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Prepositional Objects'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
prepobj = freqCol(columnname)
del prepobj['']
Prepositional_Object_Count = sum(prepobj.values())
# print 'Prepositional Object Count:', Prepositional_Object_Count
Unique_Prepositional_Object_Count = len(prepobj)
# print 'Unique Prepositional Object Count:', Unique_Prepositional_Object_Count
for l in list(prepobj):
	if prepobj[l] <= (Unique_Prepositional_Object_Count * .10):
		del prepobj[l]
Significant_Prepositional_Objects = prepobj
# print 'Significant Prepositional Objects:', Significant_Prepositional_Objects
df[columnname] = df.apply(stripCol, axis = 1)


#Determiners: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Determiners'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
det = freqCol(columnname)
del det['']
Determiner_Count = sum(det.values())
# print 'Determiner Count:', Determiner_Count
Unique_Determiner_Count = len(det)
# print 'Unique Determiner Count:', Unique_Determiner_Count
for l in list(det):
	if det[l] <= (Unique_Determiner_Count * .10):
		del det[l]
Significant_Determiners = det
# print 'Significant Determiners:', Significant_Determiners
df[columnname] = df.apply(stripCol, axis = 1)


#delete Conjunction Phrases
df = df.drop('Conjunction Phrases', 1)

#Conjunctions: convert from string to list, strip to lowercase, strip of list formatting
columnname = 'Conjunctions'
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(stripCol, axis = 1)
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)

#Conjoined: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Conjoined'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
conj = freqCol(columnname)
del conj['']
Conjoined_Count = sum(conj.values())
# print 'Conjunction Count:', Conjoined_Count
Unique_Conjoined_Count = len(conj)
# print 'Unique Conjoined Count:', Unique_Conjoined_Count
for l in list(conj):
	if conj[l] <= (Unique_Conjoined_Count * .10):
		del conj[l]
Significant_Conjoined = conj
# print 'Significant Conjoined:', Significant_Conjoined
df[columnname] = df.apply(stripCol, axis = 1)

#Compounds: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Compounds'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
comp = freqCol(columnname)
del comp['']
Compound_Count = sum(comp.values())
# print 'Compound Count:', Compound_Count
Unique_Compound_Count = len(comp)
# print 'Unique Compound Count:', Unique_Compound_Count
for l in list(comp):
	if comp[l] <= (Unique_Compound_Count * .10):
		del comp[l]
Significant_Compounds = comp
# print 'Significant Compounds:', Significant_Compounds
df[columnname] = df.apply(stripCol, axis = 1)

#Adjectival Modifiers: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Adjectival Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
adj = freqCol(columnname)
del adj['']
Adjective_Count = sum(adj.values())
# print 'Adjective Count:', Adjective_Count
Unique_Adjective_Count = len(adj)
# print 'Unique Adjective Count:', Unique_Adjective_Count
for l in list(adj):
	if adj[l] <= (Unique_Adjective_Count * .10):
		del adj[l]
Significant_Adjectives = adj
# print 'Significant Adjectives:', Significant_Adjectives
df[columnname] = df.apply(stripCol, axis = 1)

#Possesed owned by noun: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Possesed owned by noun'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
possd = freqCol(columnname)
del possd['']
Possesed_Count = sum(possd.values())
# print 'Possesed Count:', Possesed_Count
Unique_Possesed_Count = len(possd)
# print 'Unique Possesed Count:', Unique_Possesed_Count
for l in list(possd):
	if possd[l] <= (Unique_Possesed_Count * .10):
		del possd[l]
Significant_Possesed = possd
# print 'Significant Possesed:', Significant_Possesed
df[columnname] = df.apply(stripCol, axis = 1)

#Possesive owner of noun: convert from string to list, strip to lowercase, get count,  strip of list formatting 
columnname = 'Possesive owner of noun'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
possv = freqCol(columnname)
del possv['']
Possesive_Count = sum(possv.values())
# print 'Possesive Count:', Possesive_Count
df[columnname] = df.apply(stripCol, axis = 1)

#Numeric Modifiers: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Numeric Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
num = freqCol(columnname)
del num['']
Numeric_Count = sum(num.values())
# print 'Numeric Count:', Numeric_Count
df[columnname] = df.apply(stripCol, axis = 1)

#delete Case Modifiers
df = df.drop('Case Modifiers', 1)

#Adverbial Modifiers: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Adverbial Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
adv = freqCol(columnname)
del adv['']
Adverb_Count = sum(adv.values())
# print 'Adverb Count:', Adverb_Count
df[columnname] = df.apply(stripCol, axis = 1)

#Appositionals: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Appositionals'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
appos = freqCol(columnname)
del appos['']
Appositive_Count = sum(appos.values())
# print 'Appositive Count:', Appositive_Count
df[columnname] = df.apply(stripCol, axis = 1)

#Appositional Modifiers: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Appositional Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
apposmod = freqCol(columnname)
del apposmod['']
Appositional_Modifier_Count = sum(apposmod.values())
# print 'Appositional Modifier Count:', Appositional_Modifier_Count
Unique_Appositional_Modifier_Count = len(apposmod)
# print 'Unique Appositional Modifier Count:', Unique_Appositional_Modifier_Count
for l in list(apposmod):
	if apposmod[l] <= (Unique_Appositional_Modifier_Count * .10):
		del apposmod[l]
Significant_Appositional_Modifiers = apposmod
# print 'Significant Appositional Modifiers:', Significant_Appositional_Modifiers
df[columnname] = df.apply(stripCol, axis = 1)


#Modified Appositives: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Modified Appositives'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
modappos = freqCol(columnname)
del modappos['']
Modified_Appositive_Count = sum(modappos.values())
# print 'Modified Appositive Count:', Modified_Appositive_Count
Unique_Modified_Appositive_Count = len(modappos)
# print 'Unique Modified Appositive Count:', Unique_Modified_Appositive_Count
for l in list(modappos):
	if modappos[l] <= (Unique_Modified_Appositive_Count * .10):
		del modappos[l]
Significant_Modified_Appositives = modappos
# print 'Significant Modified Appositives:', Significant_Modified_Appositives
df[columnname] = df.apply(stripCol, axis = 1)

#Modality: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Modality'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
modl = freqCol(columnname)
del modl['']
Modal_Count = sum(modl.values())
# print 'Modal Count:', Modal_Count
df[columnname] = df.apply(stripCol, axis = 1)

#Conditional: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Conditional'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
condl = freqCol(columnname)
del condl['']
Conditional_Count = sum(condl.values())
# print 'Conditional Count:', Conditional_Count
df[columnname] = df.apply(stripCol, axis = 1)

#Denumerator: strip to lowercase
columnname = 'Denumerator'
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)

#Type of Denumerator: fix column to include empty strings, strip to lowercase, adjust for nonlist frequency, use to get denumerator, unit, fuzzy, other counts
columnname = 'Type of Denumerator'
df[columnname] = df.apply(fixEmpty, axis = 1)
nonlists.append(columnname)
dentype = freqCol(columnname)
del dentype['']
Denumerator_Count = sum(dentype.values()) 
# print 'Denumerator Count:', Denumerator_Count
Unit_Count = dentype.get('unit')
# print 'Unit Denumerator Count:', Unit_Count
Fuzzy_Count = dentype.get('fuzzy')
# print 'Fuzzy Denumerator Count:', Fuzzy_Count
Other_Count = dentype.get('other')
# print 'Other Denumerator Count:', Other_Count

#Allan Tests Passed: convert from string to list, get frequency list
columnname = 'Allan Tests Passed'
df[columnname] = df.apply(listCol, axis = 1)
allan = freqCol(columnname)
del allan['']
Allan_Count = sum(allan.values())
# print 'Allan Count:', Allan_Count
A_N_Count = allan.get('A+N')
# print 'A+N Count:', A_N_Count
F_NS_Count = allan.get('F+Ns')
# print 'F+NS Count:', F_NS_Count
Ex_Pl_Count = allan.get('EX-PL')
# print 'Ex-Pl Count:', Ex_Pl_Count
O_Den_Count = allan.get('O-DEN')
# print 'O-Den Count:', O_Den_Count
All_N_Count = allan.get('All+N')
# print 'All+N Count:', All_N_Count

#Countability: adjust for nonlist frequency, get countable, uncountable counts
columnname = 'Countability'
nonlists.append(columnname)
county = freqCol(columnname)
Countable_Count = county.get('countable')
# print 'Countable Count:', Countable_Count
Uncountable_Count = county.get('uncountable')
# print 'Uncountable Count:', Uncountable_Count

#Verdicality: adjust for nonlist frequency, get countable, uncountable counts
columnname = 'Verdicality'
nonlists.append(columnname)
verd = freqCol(columnname)
Verdical_Count = verd.get('verdical')
# print 'Verdical Count:', Verdical_Count
NonVerdical_Count = verd.get('nonverdical')
# print 'NonVerdical Count:', NonVerdical_Count


outfile = 'postfiles/' + word + 'Post.csv'
print 'wrote to ' + word+ 'Post.csv'
df.to_csv(outfile, index = False)

master = 'master.csv'
f = open(master, 'a')
row = [Noun, Noun_Count, NN_Count, NNS_Count, NNP_Count, NNPS_Count, Plural_Noun_Count, Singular_Noun_Count, Noun_Negation_Count, Verb_Construction_Count, VB_Count, VBD_Count, VBG_Count, VBN_Count, VBP_Count, VBZ_Count, Plural_Verb_Count, Singular_Verb_Count, Verb_Subject_Count, Unique_Verb_Subject_Count, Significant_Verb_Subjects, Verb_Object_Count, Unique_Verb_Object_Count, Significant_Verb_Objects, Verb_Negation_Count, Prepositional_Phrase_Count, Prepositional_Subject_Count, Unique_Prepositional_Subject_Count, Significant_Prepositional_Subjects, Prepositional_Object_Count, Unique_Prepositional_Object_Count, Significant_Prepositional_Objects, Determiner_Count, Unique_Determiner_Count, Significant_Determiners, Conjoined_Count, Unique_Conjoined_Count, Significant_Conjoined, Compound_Count, Unique_Compound_Count, Significant_Compounds, Adjective_Count, Unique_Adjective_Count, Significant_Adjectives, Possesed_Count, Unique_Possesed_Count, Significant_Possesed, Possesive_Count, Numeric_Count, Adverb_Count, Appositive_Count, Appositional_Modifier_Count, Unique_Appositional_Modifier_Count, Significant_Appositional_Modifiers, Modified_Appositive_Count, Unique_Modified_Appositive_Count, Significant_Modified_Appositives, Modal_Count, Conditional_Count, Denumerator_Count, Unit_Count, Fuzzy_Count, Other_Count, Allan_Count, A_N_Count, F_NS_Count, Ex_Pl_Count, O_Den_Count, All_N_Count, Countable_Count, Uncountable_Count, Verdical_Count, NonVerdical_Count]
for r in range(len(row)):
	if row[r] == None:
		row[r] = 0
	if isinstance(row[r], dict):
		freqdict = {}
		for d in row[r]:
			freqdict[d] = row[r].get(d)
		row[r] = freqdict
writer = csv.writer(f)
writer.writerow(row)
print 'wrote to master.csv'