import re
from nltk.stem import WordNetLemmatizer
import csv

#returns a string of the relevant dependencies (those that contain the target noun)
def getRelDeps(dep, noun, index):
	reldep = ''
	reldepleft = re.findall(r'(\S*\(%s-%d, \w*-[0-9]*\))' % (noun, index), dep)
	reldepright = re.findall(r'(\S*\(\w*-[0-9]*, %s-%d\))' % (noun, index), dep)
	for r in reldepleft:
		reldep += r + ' '
	for r in reldepright:
		reldep += r + ' '
	return reldep

#returns a list of tuples of nouns, indeces, and tags from a tagged sentence for a given lemma
def getNouns(tagged, lemma):
	tokenized = tagged.split()
	nouns = []
	for i in range(len(tokenized)):
		noun = re.findall(r'(\S*)/N', tokenized[i])
		if len(noun) == 1 and WordNetLemmatizer().lemmatize(noun[0], 'n') == lemma:
			tag = re.findall(r'%s\/(\w*)' % noun[0], tokenized[i])
			nouns.append((noun[0], i+1, tag[0]))
	return nouns

#looks at tagged sentence to get the tag of a given word
def getTag(tagged, word):
	tag = re.findall(r'%s\/(\w*)' % word, tagged)
	return tag[0]

#classifying verbs
verbtag = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

#looks at tagged sentence to get the verb the noun refers to
def getVerb(tagged, dep, noun, index):
	nsubj = re.findall(r'nsubj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	dobj = re.findall(r'dobj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	if len(nsubj) >= 1:
		stype = getTag(tagged, nsubj[0])
		#handles the copula case, in which the parser uses a non-verb(esp. adjectives) in the nsubj instead of the base verb
		if stype not in verbtag:
			verb = re.findall(r'cop\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
			vtag = getTag(tagged, verb[0])
		#handles the gerund case, in which the parser returns the gerund of the vp rather than the base verb
		elif stype == 'VBG':
			verb = re.findall(r'aux\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
			vtag = getTag(tagged, verb[0])
		#all other cases
		else:
			verb = nsubj
			vtag = stype
		return verb[0], vtag
	elif len(dobj) >= 1:
		vtag = getTag(tagged, dobj[0])
		return dobj[0], vtag
	else:
		return '', ''

#determines whether the noun is included in a prep phrase, then returns a tuple of the position in the phrase(modifier vs. modified) with the rest of the phrase		
def getPrepOfN(dep, noun, index):
	nmod = re.findall(r'nmod\:(\w*)\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	modn = re.findall(r'nmod\:(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	if len(nmod) >=1:
		return 'modified', nmod
	elif len(modn) >=1:
		return 'modifier', modn
	else:
		return '', []

#determines whether there is a determiner for the given noun in a dependency parse, and returns the determiner(s)
def getDetOfN(dep, noun, index):
	det = re.findall(r'det\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return det

#determines whether there is an adjectival modifier for the given noun in a dependency parse, and returns the adjective(s)
def getAmodOfN(dep, noun, index):
	amod = re.findall(r'amod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return amod

#determines whether there is a possesive pronoun or proper noun for the given noun in a dependency parse, and returns the pronoun(s) or noun(s)
def getPossOfN(dep, noun, index):
	poss = re.findall(r'nmod\:poss\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return poss

#determines whether there is a numeric modifier for the given noun in a dependency parse, and returns the number(s)
def getNumOfN(dep, noun, index):
	num = re.findall(r'nummod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	compnum = re.findall(r'compound\(%s*-[0-9]*, (\w*)-[0-9]*\)' % num, dep)
	num = compnum + num
	return num

#determines whether there is a case modifier for the given noun in a dependency parse, and returns the case(s)
def getCaseOfN(dep, noun, index):
	case = re.findall(r'case\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return case

#determines whether there is a adverbial modifier for the given noun in a dependency parse, and returns the adverb(s)
def getAdvOfN(dep, noun, index):
	adv = re.findall(r'advmod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return adv

#classifying denumerators
unit = ['a', 'an', 'one', '1'] #fall under determiners or numbers
fuzzy = ['several', 'many', 'few'] #fall under adjectives, excludes fuzzy numbers
typeO = ['each', 'every','either', 'both'] #fall under determiners, excludes concrete numbers

#determines whether the noun is modified by a denumerator, and returns a tuple of the denumerator and what type of denumerator it is, or nothing if there is no denumerator
def getDenOfN(dt, jj, nm, adv):
	for n in nm: #listed first to avoid discrepancies like "a thousand" or "several hundred"
		if n in unit:
			return n, "unit"
		else:
			if n not in adv:
				return n, "other"
			else:
				return n, "fuzzy"
	for d in dt:
		if d in unit:
			return d, "unit"
		if d in typeO:
			return d, "other"
	for j in jj:
		if j in fuzzy:
			return j, "fuzzy"
	return "", ""

#classifying noun types
singulartag = ['NN', 'NNP']
pluraltag = ['NNS', 'NNPS']

#determines whether a noun is concretely plural, concretely singular, or ambiguous(mixed results) and returns the plurality of the noun
def isPluralN(noun, lemma, ntag):
	if ntag in singulartag:
		if noun != lemma:
			return "ambiguous"
		else:
			return "singular"
	if ntag in pluraltag:
		if noun != lemma:
			return "plural"
		else:
			return "ambiguous"

#determines whether a verb is concretely plural, concretely singular, or ambiguous(in the past tense) and returns the plurality of the verb
def isPluralV(vtag):
	if vtag == 'VBP':
		return "plural"
	elif vtag == 'VBZ':
		return "singular"
	elif vtag == '':
		return ''
	else:
		return "ambiguous"

#looks at sentence to determine what allan test(s?) the sentence is modeled after for the given noun, and returns the name of the test(s?) the sentence fits 
def allanTests(dent, det, pluN, pluV):
	test = ""
	#A+N test
	if dent == "unit" and pluN != "plural":
		test += "A+N"
	#F+Ns test
	if dent == "fuzzy" and pluN != "singular": 
		test += "F+NS"
	#EX-PL test
	if pluN != "plural" and pluV == "plural":
		test += "EX-PL"
	#O-DEN test
	if dent == "other":  
		test += "O-DEN"
	#All+N test
	for d in det:
		if d == "all" and len(det) == 1:
			test+= "All+N"
	return test

#looks at sentence to determine whether the noun is countable in the given context based on the allan tests
def isCountable(tests):
	if tests != "":
		if tests == "All+N":
			return "uncountable"
		else:
			return "countable"
	else: 
		return "unknown"

#takes in a sentence, tags, dependencies, and lemma and returns a list of the outputs to all noun tests
def returnNounTests(sentence, lemma, nountup):
	sent = sentence[0]
	tagged = sentence[1]
	extdep = sentence[2]
	noun = nountup[0]
	index = nountup[1]
	dep = getRelDeps(extdep, noun, index)
	nountag = nountup[2]
	verbtup = getVerb(tagged, extdep, noun, index)
	verbref = verbtup[0]
	verbtag = verbtup[1]
	preptup = getPrepOfN(dep, noun, index)
	prep = preptup[0]
	prepp = preptup[1]
	dets = getDetOfN(dep, noun, index)
	adjs = getAmodOfN(dep, noun, index)
	poss = getPossOfN(dep, noun, index)
	num = getNumOfN(extdep, noun, index)
	case = getCaseOfN(dep, noun, index)
	adv = getAdvOfN(dep, noun, index)
	dens = getDenOfN(dets, adjs, num, adv) 
	den = dens[0]
	dentype = dens[1]
	pluN = isPluralN(noun, lemma, nountag)
	pluV = isPluralV(verbtag)
	passedT = allanTests(dentype, dets, pluN, pluV)
	countable = isCountable(passedT)
	return [noun, index, dep, nountag, verbref, verbtag, prep, prepp, dets, adjs, poss, num, case, adv, den, dentype, pluN, pluV, passedT, countable]


# #test sentence 1: A darkness fell over the room
# sentence1 = [
#     "a/DT darkness/NNS fell/VBD over/IN the/DT room/NN", 
#     "det(darkness-2, a-1) nsubj(fell-3, darkness-2) root(ROOT-0, fell-3) case(room-6, over-4) det(room-6, the-5) nmod(fell-3, room-6)", 
#     "darkness"]
# #test sentence 2: Several lambs ran from their pasture
# sentence2 = [
#     "several/JJ lambs/NNS ran/VBD from/IN their/PRP$ pasture/NN",
#     "amod(lambs-2, several-1) nsubj(ran-3, lambs-2) root(ROOT-0, ran-3) case(pasture-6, from-4) nmod:poss(pasture-6, their-5) nmod(ran-3, pasture-6)", 
#     "lamb"]
# #test sentence 3: The cattle are grazing in the field
# sentence3 = [
#     "the/DT cattle/NNS are/VBP grazing/VBG in/IN the/DT field/NN",
#     "det(cattle-2, the-1) nsubj(grazing-4, cattle-2) aux(grazing-4, are-3) root(ROOT-0, grazing-4) case(field-7, in-5) det(field-7, the-6) nmod(grazing-4, field-7)", 
#     "cattle"]
# #test sentence 4: Each kitten was fluffy 
# sentence4 = [
#     "each/DT kitten/NN was/VBD fluffy/JJ",
#     "det(kitten-2, each-1) nsubj(fluffy-4, kitten-2) cop(fluffy-4, was-3) root(ROOT-0, fluffy-4)", 
#     "kitten"]
# #test sentence 5: All lightning is frightening to the child
# sentence5 = [
#     "all/DT lightning/NN is/VBZ frightening/JJ to/TO the/DT child/NN",
#     "det(lightning-2, all-1) nsubj(frightening-4, lightning-2) cop(frightening-4, is-3) root(ROOT-0, frightening-4) case(child-7, to-5) det(child-7, the-6) nmod(frightening-4, child-7)", 
#     "lightning"]

#print returnNounTests(sentence1)
#print returnNounTests(sentence2)
#print returnNounTests(sentence3)
#print returnNounTests(sentence4)
#print returnNounTests(sentence5)


#takes in a CSV with the sentences, tagged sentences, dependency parses, and lemmas, and writes a new file with extended categorizations for each sentence
#for files with mixed lemmas, reads the lemmas stored in the csv
def appendToMixedCSV(infile, outfile):
	csvifile = open(infile, 'rU')
	csvofile = open(outfile, 'w')
	reader = csv.reader(csvifile)
	writer = csv.writer(csvofile)
	header = True
	for row in reader:
		if header:
			row.extend(['Noun', 'Noun Tag', 'Verb', 'Verb Tag', 'Determiners', 'Adjectival Modifiers', 'Possesives', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Plurality of Verb', 'Allan Tests Passed', 'Countability'])
			header = False
			writer.writerow(row)
		else:
			nounoccs = getNouns(row[1], row[3])
			for i in range(len(nounoccs)):
				newrow = []
				newrow.extend([row[0], row[1], row[2], row[3]])
				newrow.extend(returnNounTests([row[0], row[1], row[2]], row[3], nounoccs[i]))
				writer.writerow(newrow)

#for files with the same lemma, takes in the lemma and does not store sentence lemmas in the csv
def appendToCSV(infile, outfile, lemma):
	csvifile = open(infile, 'rU')
	csvofile = open(outfile, 'w')
	reader = csv.reader(csvifile)
	writer = csv.writer(csvofile)
	header = True
	for row in reader:
		if header:
			row.extend(['Noun', 'Index', 'Relevant Dependencies', 'Noun Tag', 'Verb', 'Verb Tag', 'Prepositional Position', 'Prepositional Phrase', 'Determiners', 'Adjectival Modifiers', 'Possesives', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Plurality of Verb', 'Allan Tests Passed', 'Countability'])
			header = False
			writer.writerow(row)
		else:
			nounoccs = getNouns(row[1], lemma)
			for i in range(len(nounoccs)):
				newrow = []
				newrow.extend([row[0], row[1], row[2]])
				newrow.extend(returnNounTests([row[0], row[1], row[2]], lemma, nounoccs[i]))
				writer.writerow(newrow)
	#csvifile.close()
	#csvofile.close()

appendToCSV('crimeI.csv', 'crimeO.csv', 'crime')



