import re
from nltk.stem import WordNetLemmatizer


#returns a list of nouns from a tagged sentence
def getNoun(tagged, lemma):
	nouns = re.findall(r'\s(\S*)/N', tagged)
	noun = ''
	for n in nouns:
		if WordNetLemmatizer().lemmatize(n, 'n') == lemma:
			noun = n
	return noun

#looks at tagged sentence to get the tag of a given word
def getTag(tagged, word):
	tag = re.findall(r'%s\/(\w*)' % word, tagged)
	return tag[0]

#classifying verbs
verbtag = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

#looks at tagged sentence to get the verb the noun refers to
def getVerb(tagged, dep, noun):
	nsubj = re.findall(r'nsubj\((\w*)-[0-9]*, %s-[0-9]*\)' % noun, dep)
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
	return verb[0]

#determines whether there is a determiner for the given noun in a dependency parse, and returns the determiner(s)
def getDetOfN(dep, noun):
	det = re.findall(r'det\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return det

#determines whether there is an adjectival modifier for the given noun in a dependency parse, and returns the adjective(s)
def getAmodOfN(dep, noun):
	amod = re.findall(r'amod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return amod

#determines whether there is a possesive pronoun or proper noun for the given noun in a dependency parse, and returns the pronoun(s) or noun(s)
def getPossOfN(dep, noun):
	poss = re.findall(r'nmod\:poss\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return poss

#determines whether there is a numeric modifier for the given noun in a dependency parse, and returns the number(s)
def getNumOfN(dep, noun):
	num = re.findall(r'nummod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	compnum = re.findall(r'compound\(%s*-[0-9]*, (\w*)-[0-9]*\)' % num, dep)
	num = compnum + num
	return num

#determines whether there is a case modifier for the given noun in a dependency parse, and returns the case(s)
def getCaseOfN(dep, noun):
	case = re.findall(r'case\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return case


#determines whether there is a adverbial modifier for the given noun in a dependency parse, and returns the adverb(s)
def getAdvOfN(dep, noun):
	adv = re.findall(r'advmod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return adv

#classifying denumerators
unit = ['a', 'an', 'one', '1'] #fall under determiners or numbers
fuzzy = ['several', 'many', 'few'] #fall under adjectives, excludes fuzzy numbers
typeO = ['each', 'every','either', 'both'] #fall under determiners, excludes concrete numbers

#determines whether the noun is modified by a denumerator, and returns a tuple of the denumerator and what type of denumerator it is, or nothing if there is no denumerator
def getDenOfN(dep, noun):
	dt = getDetOfN(dep, noun)
	jj = getAmodOfN(dep, noun)
	nm = getNumOfN(dep, noun)
	for n in nm: #listed first to avoid discrepancies like "a thousand" or "several hundred"
		if n in unit:
			return n, "unit"
		else:
			if not getAdvOfN(dep, n):
				return n, "typeO"
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
def isPluralN(tagged, noun, lemma):
	ntag = getTag(tagged, noun)
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
def isPluralV(tagged, verb):
	vtag = getTag(tagged, verb)
	if vtag == 'VBP':
		return "plural"
	elif vtag == 'VBZ':
		return "singular"
	else:
		return "ambiguous"

#looks at sentence to determine what allan test(s?) the sentence is modeled after for the given noun, and returns the name of the test(s?) the sentence fits 
def allanTests(tagged, dep, noun, lemma):
	den = getDenOfN(dep, noun)
	det = getDetOfN(dep, noun)
	pluN = isPluralN(tagged, noun, lemma)
	verb = getVerb(tagged, dep, noun)
	pluV = isPluralV(tagged, verb)
	test = ""
	#A+N test
	if den[1] == "unit" and pluN != "plural":
		test += "A+N"
	#F+Ns test
	if den[1] == "fuzzy" and pluN != "singular":
		test += "F+NS"
	#EX-PL test
	if pluN != "plural" and pluV == "plural":
		test += "EX-PL"
	#O-DEN test
	if den[1] == "other": 
		test += "O-DEN"
	#All+N test
	for d in det:
		if d == "all" and len(det) == 1:
			test+= "All+N"
	return test


def isCountable(tagged, dep, noun, lemma):
	tests = allanTests(tagged, dep, noun, lemma)
	if tests != "":
		if tests == "All+N":
			return "uncountable"
		else:
			return "countable"
	else: 
		return "unknown"


#test sentence 1: A darkness fell over the room
sentence1 = [
    "a/DT darkness/NNS fell/VBD over/IN the/DT room/NN", 
    "det(darkness-2, a-1) nsubj(fell-3, darkness-2) root(ROOT-0, fell-3) case(room-6, over-4) det(room-6, the-5) nmod(fell-3, room-6)", 
    "darkness"]
#test sentence 2: Several lambs ran from their pasture
sentence2 = [
    "several/JJ lambs/NNS ran/VBD from/IN their/PRP$ pasture/NN",
    "amod(lambs-2, several-1) nsubj(ran-3, lambs-2) root(ROOT-0, ran-3) case(pasture-6, from-4) nmod:poss(pasture-6, their-5) nmod(ran-3, pasture-6)", 
    "lamb"]
#test sentence 3: The cattle are grazing in the field
sentence3 = [
    "the/DT cattle/NNS are/VBP grazing/VBG in/IN the/DT field/NN",
    "det(cattle-2, the-1) nsubj(grazing-4, cattle-2) aux(grazing-4, are-3) root(ROOT-0, grazing-4) case(field-7, in-5) det(field-7, the-6) nmod(grazing-4, field-7)", 
    "cattle"]
#test sentence 4: Each kitten was fluffy 
sentence4 = [
    "each/DT kitten/NN was/VBD fluffy/JJ",
    "det(kitten-2, each-1) nsubj(fluffy-4, kitten-2) cop(fluffy-4, was-3) root(ROOT-0, fluffy-4)", 
    "kitten"]
#test sentence 5: All lightning is frightening to the child
sentence5 = [
    "all/DT lightning/NN is/VBZ frightening/JJ to/TO the/DT child/NN",
    "det(lightning-2, all-1) nsubj(frightening-4, lightning-2) cop(frightening-4, is-3) root(ROOT-0, frightening-4) case(child-7, to-5) det(child-7, the-6) nmod(frightening-4, child-7)", 
    "lightning"]

def listToString(alist):
	return "[" + ', '.join(alist) + "]"

def runNounTests(sentence):
	tagged = sentence[0]
	print "tagged = " + tagged 
	dep = sentence[1]
	print "dep = " + dep 
	lemma = sentence[2]
	print "lemma = " + lemma 
	noun = getNoun(tagged, lemma)
	print "noun = " + noun 
	nountag = getTag(tagged, noun)
	print "nountag = " + nountag 
	verbref = getVerb(tagged, dep, noun)
	print "verbref = " + verbref 
	verbtag = getTag(tagged, verbref)
	print "verbtag = " + verbtag 
	dets = getDetOfN(dep, noun)
	print "dets = " + listToString(dets) 
	adjs = getAmodOfN(dep, noun)
	print "adjs = " + listToString(adjs) 
	poss = getPossOfN(dep, noun)
	print "poss = " + listToString(poss) 
	num = getNumOfN(dep, noun)
	print "num = " + listToString(num) 
	case = getCaseOfN(dep, noun)
	print "case = " + listToString(case) 
	adv = getAdvOfN(dep, noun)
	print "adv = " + listToString(adv) 
	dens = getDenOfN(dep, noun)
	den = dens[0]
	print "den = " + den 
	dentype = dens[1]
	print "dentype = " + dentype 
	pluN = isPluralN(tagged, noun, lemma)
	print "pluN = " + pluN 
	pluV = isPluralV(tagged, verbref)
	print "pluV = " + pluV 
	passedT = allanTests(tagged, dep, noun, lemma)
	print "passedT = " + passedT 
	countable = isCountable(tagged, dep, noun, lemma)
	print "countable = " + countable 

runNounTests(sentence1)
runNounTests(sentence2)
runNounTests(sentence3)
runNounTests(sentence4)
runNounTests(sentence5)






