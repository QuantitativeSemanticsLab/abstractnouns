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

def getPercent(num, den):
	if num is None or den is None:
		return '0%'
	num = float(num)
	den = float(den)
	if den != 0:
		pct = (num/den) * 100
		trim = "%.2f" % pct
		return str(trim) + '%'
	else:
		return '0%'
nonlists = []
lowerlist = []
results = []

#do nothing to sent
#delete tags, parse
df = df.drop('tags', 1)
df = df.drop('parse', 1)

#Noun: use to count number of occurances
Noun = word
results.append(Noun)
Noun_Count = len(df['Noun'])
results.append(Noun_Count)

#delete index 
df = df.drop('Index', 1)

#do nothing to Relevant Dependencies

#delete Sentence Fragment
df = df.drop('Sentence Fragment', 1)

#Noun Tag: use to get counts for noun types
columnname = 'Noun Tag'
nonlists.append(columnname)
nountag = freqCol(columnname)
NN_Count = nountag.get('NN')
NN_Percentage = getPercent(NN_Count, Noun_Count)
NNS_Count = nountag.get('NNS')
NNS_Percentage = getPercent(NNS_Count, Noun_Count)
NNP_Count = nountag.get('NNP')
NNP_Percentage = getPercent(NNP_Count, Noun_Count)
NNPS_Count = nountag.get('NNPS')
NNPS_Percentage = getPercent(NNPS_Count, Noun_Count)
results.extend([NN_Count, NN_Percentage, NNS_Count, NNS_Percentage, NNP_Count, NNP_Percentage, NNPS_Count, NNPS_Percentage])

#Plurality of Noun: use to get plural and singular counts
columnname = 'Plurality of Noun'
nonlists.append(columnname)
pluN = freqCol(columnname)
Plural_Noun_Count = pluN.get('plural')
Plural_Noun_Percentage = getPercent(Plural_Noun_Count, Noun_Count)
Singular_Noun_Count = pluN.get('singular')
Singular_Noun_Percentage = getPercent(Singular_Noun_Count, Noun_Count)
results.extend([Plural_Noun_Count, Plural_Noun_Percentage, Singular_Noun_Count, Singular_Noun_Percentage])

#Bareness of Noun: use to get bare singular, bare plural, or linked counts
columnname = 'Bareness of Noun'
nonlists.append(columnname)
bareN = freqCol(columnname)
Bare_Plural_Noun_Count = bareN.get('bare plural')
Bare_Plural_Noun_Percentage = getPercent(Bare_Plural_Noun_Count, Noun_Count)
Bare_Singular_Noun_Count = bareN.get('bare singular')
Bare_Singular_Noun_Percentage = getPercent(Bare_Singular_Noun_Count, Noun_Count)
Linked_Noun_Count = bareN.get('linked')
Linked_Noun_Percentage = getPercent(Linked_Noun_Count, Noun_Count)
results.extend([Bare_Plural_Noun_Count, Bare_Plural_Noun_Percentage, Bare_Singular_Noun_Count, Bare_Singular_Noun_Percentage, Linked_Noun_Count, Linked_Noun_Percentage])

#Negation: convert from string to list, use to get negation count, strip of list formatting
columnname = 'Negation'
df[columnname] = df.apply(listCol, axis = 1)
nounNeg = freqCol(columnname)
Noun_Negation_Count = sum(nounNeg.values())
Noun_Negation_Percentage = getPercent(Noun_Negation_Count, Noun_Count)
results.extend([Noun_Negation_Count, Noun_Negation_Percentage])
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
Verb_Construction_Percentage = getPercent(Verb_Construction_Count, Noun_Count)
VB_Count = verbtag.get('VB')
VB_Percentage = getPercent(VB_Count, Verb_Construction_Count)
VBD_Count = verbtag.get('VBD')
VBD_Percentage = getPercent(VBD_Count, Verb_Construction_Count)
VBG_Count = verbtag.get('VBG')
VBG_Percentage = getPercent(VBG_Count, Verb_Construction_Count)
VBN_Count = verbtag.get('VBN')
VBN_Percentage = getPercent(VBN_Count, Verb_Construction_Count)
VBP_Count = verbtag.get('VBP')
VBP_Percentage = getPercent(VBP_Count, Verb_Construction_Count)
VBZ_Count = verbtag.get('VBZ')
VBZ_Percentage = getPercent(VBZ_Count, Verb_Construction_Count)
results.extend([Verb_Construction_Count, Verb_Construction_Percentage, VB_Count, VB_Percentage, VBD_Count, VBD_Percentage, VBG_Count, VBG_Percentage, VBN_Count, VBN_Percentage, VBP_Count, VBP_Percentage, VBZ_Count, VBZ_Percentage])


#Plurality of Verb: fix column to include empty strings, use to get singular and plural counts
columnname = 'Plurality of Verb'
df[columnname] = df.apply(fixEmpty, axis = 1)
nonlists.append(columnname)
pluV = freqCol(columnname)
Plural_Verb_Count = pluV.get('plural')
Plural_Verb_Percentage = getPercent(Plural_Verb_Count, Verb_Construction_Count)
Singular_Verb_Count = pluV.get('singular')
Singular_Verb_Percentage = getPercent(Singular_Verb_Count, Verb_Construction_Count)
results.extend([Plural_Verb_Count, Plural_Verb_Percentage, Singular_Verb_Count, Singular_Verb_Percentage])

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
Verb_Subject_Percentage = getPercent(Verb_Subject_Count, Verb_Construction_Count)
Unique_Verb_Subject_Count = len(verbsubj) 
for l in list(verbsubj):
	if verbsubj[l] <= (Unique_Verb_Subject_Count * .10):
		del verbsubj[l]
Significant_Verb_Subjects = verbsubj 
Significant_Verb_Subject_Count = len(verbsubj)
results.extend([Verb_Subject_Count, Verb_Subject_Percentage, Unique_Verb_Subject_Count, Significant_Verb_Subjects, Significant_Verb_Subject_Count])

#Verb Object Lemma: fix column to include empty strings, strip to lowercase, adjust for nonlist frequency,use to get verb object count, unique count, frequency list
columnname = 'Verb Object Lemma'
df[columnname] = df.apply(fixEmpty, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
nonlists.append(columnname)
verbobj = freqCol(columnname)
del verbobj['']
Verb_Object_Count = sum(verbobj.values()) 
Verb_Object_Percentage = getPercent(Verb_Object_Count, Verb_Construction_Count)
Unique_Verb_Object_Count = len(verbobj) 
for l in list(verbobj):
	if verbobj[l] <= (Unique_Verb_Object_Count * .10):
		del verbobj[l]
Significant_Verb_Objects = verbobj 
Significant_Verb_Object_Count = len(verbobj)
results.extend([Verb_Object_Count, Verb_Object_Percentage, Unique_Verb_Object_Count, Significant_Verb_Objects, Significant_Verb_Object_Count])

#Verb Negation: convert from string to list, use to get negation count, strip of list formatting
columnname = 'Verb Negation'
df[columnname] = df.apply(listCol, 1)
verbNeg = freqCol(columnname)
Verb_Negation_Count = sum(verbNeg.values())
Verb_Negation_Percentage = getPercent(Verb_Negation_Count, Verb_Construction_Count)
df[columnname] = df.apply(stripCol, 1)
results.extend([Verb_Negation_Count, Verb_Negation_Percentage])

#Prepositional Phrases: simplify tuples to strings, strip to lowercase, get prep phrase count, strip of list formatting
columnname = 'Prepositional Phrases'
df[columnname] = df.apply(listCol, axis = 1)
preps = freqCol(columnname)
del preps['']
Prepositional_Phrase_Count = sum(preps.values())
Prepositional_Phrase_Percentage = getPercent(Prepositional_Phrase_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Prepositional_Phrase_Count, Prepositional_Phrase_Percentage])

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
Prepositional_Subject_Percentage = getPercent(Prepositional_Subject_Count, Prepositional_Phrase_Count)
Unique_Prepositional_Subject_Count = len(prepsubj)
for l in list(prepsubj):
	if prepsubj[l] <= (Unique_Prepositional_Subject_Count * .10):
		del prepsubj[l]
Significant_Prepositional_Subjects = prepsubj
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Prepositional_Subject_Count, Prepositional_Subject_Percentage, Unique_Prepositional_Subject_Count, Significant_Prepositional_Subjects])


#Prepositional Objects: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Prepositional Objects'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
prepobj = freqCol(columnname)
del prepobj['']
Prepositional_Object_Count = sum(prepobj.values())
Prepositional_Object_Percentage = getPercent(Prepositional_Object_Count, Prepositional_Phrase_Count)
Unique_Prepositional_Object_Count = len(prepobj)
for l in list(prepobj):
	if prepobj[l] <= (Unique_Prepositional_Object_Count * .10):
		del prepobj[l]
Significant_Prepositional_Objects = prepobj
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Prepositional_Object_Count, Prepositional_Object_Percentage, Unique_Prepositional_Object_Count, Significant_Prepositional_Objects])


#Determiners: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Determiners'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
det = freqCol(columnname)
del det['']
Determiner_Count = sum(det.values())
Determiner_Percentage = getPercent(Determiner_Count, Noun_Count)
Unique_Determiner_Count = len(det)
for l in list(det):
	if det[l] <= (Unique_Determiner_Count * .10):
		del det[l]
Significant_Determiners = det
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Determiner_Count, Determiner_Percentage, Unique_Determiner_Count, Significant_Determiners])

#Determiner Type: fix column to include empty strings, adjust for nonlist frequency, use to get verb type counts
columnname = 'Determiner Type'
nonlists.append(columnname)
dettype = freqCol(columnname)
Indefinite_Article_Count = dettype.get('indefinite article')
Indefinite_Article_Percentage = getPercent(Indefinite_Article_Count, Determiner_Count)
Definite_Article_Count = dettype.get('definite article')
Definite_Article_Percentage = getPercent(Definite_Article_Count, Determiner_Count)
Demonstrative_Pronoun_Count = dettype.get('demonstrative')
Demonstrative_Pronoun_Percentage = getPercent(Demonstrative_Pronoun_Count, Determiner_Count)
Quantifier_Count = dettype.get('quantifier')
Quantifier_Percentage = getPercent(Quantifier_Count, Determiner_Count)
Other_Determiner_Count = dettype.get('other')
Other_Determiner_Percentage = getPercent(Other_Determiner_Count, Determiner_Count)
results.extend([Indefinite_Article_Count, Indefinite_Article_Percentage, Definite_Article_Count, Definite_Article_Percentage, Demonstrative_Pronoun_Count, Demonstrative_Pronoun_Percentage, Quantifier_Count, Quantifier_Percentage, Other_Determiner_Count, Other_Determiner_Percentage])

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
Conjoined_Percentage = getPercent(Conjoined_Count, Noun_Count)
Unique_Conjoined_Count = len(conj)
for l in list(conj):
	if conj[l] <= (Unique_Conjoined_Count * .10):
		del conj[l]
Significant_Conjoined = conj
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Conjoined_Count, Conjoined_Percentage, Unique_Conjoined_Count, Significant_Conjoined])

#Compounds: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Compounds'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
comp = freqCol(columnname)
del comp['']
Compound_Count = sum(comp.values())
Compound_Percentage = getPercent(Compound_Count, Noun_Count)
Unique_Compound_Count = len(comp)
for l in list(comp):
	if comp[l] <= (Unique_Compound_Count * .10):
		del comp[l]
Significant_Compounds = comp
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Compound_Count, Compound_Percentage, Unique_Compound_Count, Significant_Compounds])

#Adjectival Modifiers: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Adjectival Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
adj = freqCol(columnname)
del adj['']
Adjective_Count = sum(adj.values())
Adjective_Percentage = getPercent(Adjective_Count, Noun_Count)
Unique_Adjective_Count = len(adj)
for l in list(adj):
	if adj[l] <= (Unique_Adjective_Count * .10):
		del adj[l]
Significant_Adjectives = adj
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Adjective_Count, Adjective_Percentage, Unique_Adjective_Count, Significant_Adjectives])

#Possesed owned by noun: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Possesed owned by noun'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
possd = freqCol(columnname)
del possd['']
Possesed_Count = sum(possd.values())
Possesed_Percentage = getPercent(Possesed_Count, Noun_Count)
Unique_Possesed_Count = len(possd)
for l in list(possd):
	if possd[l] <= (Unique_Possesed_Count * .10):
		del possd[l]
Significant_Possesed = possd
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Possesed_Count, Possesed_Percentage, Unique_Possesed_Count, Significant_Possesed])

#Possesive owner of noun: convert from string to list, strip to lowercase, get count,  strip of list formatting 
columnname = 'Possesive owner of noun'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
possv = freqCol(columnname)
del possv['']
Possesive_Count = sum(possv.values())
Possesive_Percentage = getPercent(Possesive_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Possesive_Count, Possesive_Percentage])

#Numeric Modifiers: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Numeric Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
num = freqCol(columnname)
del num['']
Numeric_Count = sum(num.values())
Numeric_Percentage = getPercent(Numeric_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Numeric_Count, Numeric_Percentage])

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
Adverb_Percentage = getPercent(Adverb_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Adverb_Count, Adverb_Percentage])

#Appositionals: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Appositionals'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
appos = freqCol(columnname)
del appos['']
Appositive_Count = sum(appos.values())
Appositive_Percentage = getPercent(Appositive_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Appositive_Count, Appositive_Percentage])

#Appositional Modifiers: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Appositional Modifiers'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
apposmod = freqCol(columnname)
del apposmod['']
Appositional_Modifier_Count = sum(apposmod.values())
Appositional_Modifier_Percentage = getPercent(Appositional_Modifier_Count, Appositive_Count)
Unique_Appositional_Modifier_Count = len(apposmod)
for l in list(apposmod):
	if apposmod[l] <= (Unique_Appositional_Modifier_Count * .10):
		del apposmod[l]
Significant_Appositional_Modifiers = apposmod
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Appositional_Modifier_Count, Appositional_Modifier_Percentage, Unique_Appositional_Modifier_Count, Significant_Appositional_Modifiers])


#Modified Appositives: convert from string to list, strip to lowercase, get count, unique count, freq list, strip of list formatting 
columnname = 'Modified Appositives'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
modappos = freqCol(columnname)
del modappos['']
Modified_Appositive_Count = sum(modappos.values())
Modified_Appositive_Percentage = getPercent(Modified_Appositive_Count, Appositive_Count)
Unique_Modified_Appositive_Count = len(modappos)
for l in list(modappos):
	if modappos[l] <= (Unique_Modified_Appositive_Count * .10):
		del modappos[l]
Significant_Modified_Appositives = modappos
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Modified_Appositive_Count, Modified_Appositive_Percentage, Unique_Modified_Appositive_Count, Significant_Modified_Appositives])

#Modality: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Modality'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
modl = freqCol(columnname)
del modl['']
Modal_Count = sum(modl.values())
Modal_Percentage = getPercent(Modal_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Modal_Count, Modal_Percentage])

#Conditional: convert from string to list, strip to lowercase, get count, strip of list formatting 
columnname = 'Conditional'
lowerlist.append(columnname)
df[columnname] = df.apply(listCol, axis = 1)
df[columnname] = df.apply(lowerCol, axis = 1)
condl = freqCol(columnname)
del condl['']
Conditional_Count = sum(condl.values())
Conditional_Percentage = getPercent(Conditional_Count, Noun_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Conditional_Count, Conditional_Percentage])

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
Denumerator_Percentage = getPercent(Denumerator_Count, Noun_Count)
Unit_Denumerator_Count = dentype.get('unit')
Unit_Denumerator_Percentage = getPercent(Unit_Denumerator_Count, Denumerator_Count)
Fuzzy_Denumerator_Count = dentype.get('fuzzy')
Fuzzy_Denumerator_Percentage = getPercent(Fuzzy_Denumerator_Count, Denumerator_Count)
Other_Denumerator_Count = dentype.get('other')
Other_Denumerator_Percentage = getPercent(Other_Denumerator_Count, Denumerator_Count)
results.extend([Denumerator_Count, Denumerator_Percentage, Unit_Denumerator_Count, Unit_Denumerator_Percentage, Fuzzy_Denumerator_Count, Fuzzy_Denumerator_Percentage, Other_Denumerator_Count, Other_Denumerator_Percentage])


#Allan Tests Passed: convert from string to list, get frequency list
columnname = 'Allan Tests Passed'
df[columnname] = df.apply(listCol, axis = 1)
allan = freqCol(columnname)
del allan['']
Allan_Count = sum(allan.values())
Allan_Percentage = getPercent(Allan_Count, Noun_Count)
A_N_Count = allan.get('A+N')
A_N_Percentage = getPercent(A_N_Count, Allan_Count)
F_Ns_Count = allan.get('F+Ns')
F_Ns_Percentage = getPercent(F_Ns_Count, Allan_Count)
Ex_Pl_Count = allan.get('EX-PL')
Ex_Pl_Percentage = getPercent(Ex_Pl_Count, Allan_Count)
O_Den_Count = allan.get('O-DEN')
O_Den_Percentage = getPercent(O_Den_Count, Allan_Count)
All_N_Count = allan.get('All+N')
All_N_Percentage = getPercent(All_N_Count, Allan_Count)
df[columnname] = df.apply(stripCol, axis = 1)
results.extend([Allan_Count, Allan_Percentage, A_N_Count, A_N_Percentage, F_Ns_Count, F_Ns_Percentage, Ex_Pl_Count, Ex_Pl_Percentage, O_Den_Count, O_Den_Percentage, All_N_Count, All_N_Percentage])

#Countability: adjust for nonlist frequency, get countable, uncountable counts
columnname = 'Countability'
nonlists.append(columnname)
county = freqCol(columnname)
Countable_Count = county.get('countable')
Countable_Percentage = getPercent(Countable_Count, Noun_Count)
Uncountable_Count = county.get('uncountable')
Uncountable_Percentage = getPercent(Uncountable_Count, Noun_Count)
results.extend([Countable_Count, Countable_Percentage, Uncountable_Count, Uncountable_Percentage])

#Verdicality: adjust for nonlist frequency, get countable, uncountable counts
columnname = 'Verdicality'
nonlists.append(columnname)
verd = freqCol(columnname)
Verdical_Count = verd.get('verdical')
Verdical_Percentage = getPercent(Verdical_Count, Noun_Count)
NonVerdical_Count = verd.get('nonverdical')
NonVerdical_Percentage = getPercent(NonVerdical_Count, Noun_Count)
results.extend([Verdical_Count, Verdical_Percentage, NonVerdical_Count, NonVerdical_Percentage])


outfile = 'postfiles/' + word + 'Post.csv'
print 'wrote to ' + word+ 'Post.csv'
df.to_csv(outfile, index = False)

master = 'master.csv'
f = open(master, 'a')
for r in range(len(results)):
	if results[r] == None:
		results[r] = 0
	if isinstance(results[r], dict):
		freqdict = {}
		for d in results[r]:
			freqdict[d] = results[r].get(d)
		results[r] = freqdict
writer = csv.writer(f)
writer.writerow(results)
print 'wrote to master.csv'