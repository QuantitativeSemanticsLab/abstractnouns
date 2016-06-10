import re
from nltk.stem import WordNetLemmatizer

#returns a list of nouns from a tagged sentence
def findNounsT(tagged):
	noun = re.findall(r'\s(\S*)/N', tagged)
	return noun
#print findNounsT("all/DT pretty/JJ oak/NNS is/VBZ deciduous/JJ")

#returns a list of nouns from a parse
def findNounsP(parse):
	noun = re.findall(r'\(NN (\w*)\)', parse)
	return noun
#print findNounsP("(ROOT (S (NP (DT all) (JJ pretty) (NN oak)) (VP (VBZ is) (NP (DT a) (JJ deciduous) (NN tree)))))")

#determines whether there is a determiner for the given noun in a dependency parse, and returns the determiner(s)
def getDetOfN(dep, noun):
	det = re.findall(r'det\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return det
#print getDetOfN("det(oak-3, all-1) amod(oak-3, pretty-2) nsubj(tree-7, oak-3)", "oak")

#determines whether there is an adjectival modifier for the given noun in a dependency parse, and returns the adjective(s)
def getAmodOfN(dep, noun):
	amod = re.findall(r'amod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return amod
#print getAmodOfN("amod(cattle-3, several-1) amod(cattle-3, pretty-2) nsubj(grazing-5, cattle-3) cop(grazing-5, were-4) root(ROOT-0, grazing-5)", "cattle")

#determines whether there is a possesive pronoun or proper noun for the given noun in a dependency parse, and returns the pronoun(s) or noun(s)
def getPossOfN(dep, noun):
	poss = re.findall(r'nmod\:poss\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return poss
#print getPossOfN("nmod:poss(cattle-3, Sarah-1) (case(Sarah-1, 's-2) amod(cattle-4, pretty-3) nsubj(grazing-6, cattle-4) cop(grazing-6, were-5) root(ROOT-0, grazing-6)", "cattle")

#determines whether there is a numeric modifier for the given noun in a dependency parse, and returns the number(s)
def getNumOfN(dep, noun):
	num = re.findall(r'nummod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	compnum = re.findall(r'compound\(%s*-[0-9]*, (\w*)-[0-9]*\)' % num, dep)
	num = compnum + num
	return num

#print getNumOfN("compound(thousand-2, four-1) nummod(people-3, thousand-2) nsubj(came-4, people-3) root(ROOT-0, came-4) case(party-7, to-5) det(party-7, to-5) nmod(came-4, party-7)", "people")

#determines whether there is a case modifier for the given noun in a dependency parse, and returns the case(s)
def getCaseOfN(dep, noun):
	case = re.findall(r'case\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return case
#print getCaseOfN("nsubj(grazing-6, all-1) case(cattle-4, of-2) det(cattle-4, the-3) nmod(all-1, cattle-4) cop(grazing-6, were-5) root(ROOT-0, grazing-6)", "cattle")

def getAdvOfN(dep, noun):
	adv = re.findall(r'advmod\(%s-[0-9]*, (\w*)-[0-9]*\)' % noun, dep)
	return adv
#print getAdvOfN("advmod(thousand-2, several-1) nummod(cattle-3, thousand-2) nsubj(jumped-4, cattle-3) root(ROOT-0, jumped-4)", "thousand")

#classifying denumerators
unit = ['a', 'an', 'one', '1'] #fall under determiners or numbers
fuzzy = ['several', 'many', 'few'] #fall under adjectives, excludes fuzzy numbers
typeO = ['each', 'every','either', 'both'] #fall under determiners, excludes concrete numbers

#determines whether the noun is modified by a denumerator, and returns what type of denumerator it is, or nothing if there is no denumerator
def getDenOfN(dep, noun):
	dt = getDetOfN(dep, noun)
	jj = getAmodOfN(dep, noun)
	nm = getNumOfN(dep, noun)
	for n in nm: #listed first to avoid discrepancies like "a thousand" or "several hundred"
		if n in unit:
			return "unit"
		else:
			if not getAdvOfN(dep, n):
				return "typeO"
			else:
				return "fuzzy"
	for d in dt:
		if d in unit:
			return "unit"
		if d in typeO:
			return "other"
	for j in jj:
		if j in fuzzy:
			return "fuzzy"
	return 
#print getDenOfN("det(cattle-3, a-1) nummod(cattle-3, thousand-2) nsubj(jumped-4, cattle-3) root(ROOT-0, jumped-4)", "cattle")

#looks at tagged sentence to get the type of noun
def getNounTag(tagged, noun):
	ntag = re.findall(r'%s\/(\w*)' % noun, tagged)
	return ntag
#print getNounTag("all/DT pretty/JJ oak/NNS is/VBZ deciduous/JJ", "oak")

#classifying noun types
singulartag = ['NN', 'NNP']
pluraltag = ['NNS', 'NNPS']

#gets the lemma of the given noun
def getLemma(noun):
	lemma = WordNetLemmatizer().lemmatize(noun, 'n')
	return lemma

#determines whether a noun is concretely plural, concretely singular, or ambiguous(mixed results) and returns the plurality of the noun
def isPluralN(tagged, noun):
	ntag = getNounTag(tagged, noun)
	if ntag[0] in singulartag:
		lemma = getLemma(noun)
		if noun is not lemma:
			return "ambiguous"
		else:
			return "singular"
	if ntag[0] in pluraltag:
		lemma = getLemma(noun)
		if noun is not lemma:
			return "plural"
		else:
			return "ambiguous"
#print isPluralN("all/DT pretty/JJ oak/NN is/VBZ deciduous/JJ", "oak")

#looks at tagged sentence to get the tag of the verb the noun refers to
def getVerbTag(tagged, noun): #dep, noun):
	vtag = re.findall(r'/(V\w*)', tagged)
	return vtag
	#toss up - above might not capture the right verb the noun acts on, below disregards cases in which dependency between noun-verb are undefined
	#		 - above is more faulty, but does not encounter bugs, below is more foolproof, but when it breaks, it breaks the program. would require lots of hand coding to get right
	#	verb = re.findall(r'nsubj\((\w*)-[0-9]*, %s-[0-9]*\)' % noun, dep)
	#	print verb
	#	vtag = re.findall(r'%s\/(\w*)' % verb, tagged)
	#	print vtag
	#	if re.search(r'V\w*', vtag):
	#		verb = re.findall(r'cop\(%s-[0-9]*, (\w*)-[0-9]*\)' % verb, dep)
	#		vtag = re.findall(r'%s\/(\w*)' % verb, tagged)
	#	return vtag
#print getVerbTag("all/DT of/IN the/DT cattle/NNS were/VBD grazing/NN", "cattle")

#determines whether a verb is concretely plural, concretely singular, or ambiguous(in the past tense) and returns the plurality of the verb
def isPluralV(tagged, noun):
	vtag = getVerbTag(tagged, noun)
	if vtag[0] == 'VBP':
		return "plural"
	elif vtag[0] == 'VBZ':
		return "singular"
	else:
		return "ambiguous"
#print isPluralV("all/DT pretty/JJ oak/NN is/VBZ deciduous/JJ", "oak")

#looks at sentence to determine what allan test(s?) the sentence is modeled after for the given noun, and returns the name of the test(s?) the sentence fits 
def allanTests(tagged, dep, noun):
	den = getDenOfN(dep, noun)
	det = getDetOfN(dep, noun)
	pluN = isPluralN(tagged, noun)
	pluV = isPluralV(tagged, noun)
	test = ""
	#A+N test
	if den == "unit" and pluN != "plural":
		test += "A+N"
	#F+Ns test
	if den == "fuzzy" and pluN != "singular":
		test += "F+NS"
	#EX-PL test
	if pluN != "plural" and pluV == "plural":
		test += "EX-PL"
	#O-DEN test
	if den == "other": 
		test += "O-DEN"
	#All+N test
	for d in det:
		if d == "all" and len(det) == 1:
			test+= "All+N"
	return test
#test sentence 1: A darkness fell over the room
	# print allanTests(
	# 	"a/DT darkness/NNS fell/VBD over/IN the/DT room/NN", 
	# 	"det(darkness-2, a-1) nsubj(fell-3, darkness-2) root(ROOT-0, fell-3) case(room-6, over-4) det(room-6, the-5) nmod(fell-3, room-6)",
	# 	"darkness")
#test sentence 2: Several lambs ran from their pasture
	# print allanTests(
	# 	"several/JJ lambs/NNS ran/VBD from/IN their/PRP$ pasture/NN",
	# 	"amod(lambs-2, several-1) nsubj(ran-3, lambs-2) root(ROOT-0, ran-3) case(pasture-6, from-4) nmod:poss(pasture-6, their-5) nmod(ran-3, pasture-6)",
	# 	"lambs")
#test sentence 3: The cattle are grazing in the field
	# print allanTests(
	# 	"the/DT cattle/NNS are/VBP grazing/VBG in/IN the/DT field/NN",
	# 	"det(cattle-2, the-1) nsubj(grazing-4, cattle-2) aux(grazing-4, are-3) root(ROOT-0, grazing-4) case(field-7, in-5) det(field-7, the-6) nmod(grazing-4, field-7)",
	# 	"cattle")
#test sentence 4: Each kitten was fluffy 
	# print allanTests(
	# 	"each/DT kitten/NN was/VBD fluffy/JJ",
	# 	"det(kitten-2, each-1) nsubj(fluffy-4, kitten-2) cop(fluffy-4, was-3) root(ROOT-0, fluffy-4)", 
	# 	"kitten")
#test sentence 5: All lightning is frightening to the child
	# print allanTests(
	# 	"all/DT lightning/NN is/VBZ frightening/JJ to/TO the/DT child/NN",
	# 	"det(lightning-2, all-1) nsubj(frightening-4, lightning-2) cop(frightening-4, is-3) root(ROOT-0, frightening-4) case(child-7, to-5) det(child-7, the-6) nmod(frightening-4, child-7)", 
	# 	"lightning")

def isCountable(tagged, dep, noun):
	tests = allanTests(tagged, dep, noun)
	if tests != "":
		if tests == "All+N":
			return "uncountable"
		else:
			return "countable"
	else: 
		return "unknown"
#test sentence 1: A darkness fell over the room
	# print isCountable(
	#     "a/DT darkness/NNS fell/VBD over/IN the/DT room/NN", 
	#     "det(darkness-2, a-1) nsubj(fell-3, darkness-2) root(ROOT-0, fell-3) case(room-6, over-4) det(room-6, the-5) nmod(fell-3, room-6)",
	#     "darkness")
#test sentence 2: Several lambs ran from their pasture
	# print isCountable(
	#     "several/JJ lambs/NNS ran/VBD from/IN their/PRP$ pasture/NN",
	#     "amod(lambs-2, several-1) nsubj(ran-3, lambs-2) root(ROOT-0, ran-3) case(pasture-6, from-4) nmod:poss(pasture-6, their-5) nmod(ran-3, pasture-6)",
	#     "lambs")
#test sentence 3: The cattle are grazing in the field
	# print isCountable(
	#     "the/DT cattle/NNS are/VBP grazing/VBG in/IN the/DT field/NN",
	#     "det(cattle-2, the-1) nsubj(grazing-4, cattle-2) aux(grazing-4, are-3) root(ROOT-0, grazing-4) case(field-7, in-5) det(field-7, the-6) nmod(grazing-4, field-7)",
	#     "cattle")
#test sentence 4: Each kitten was fluffy 
	# print isCountable(
	#     "each/DT kitten/NN was/VBD fluffy/JJ",
	#     "det(kitten-2, each-1) nsubj(fluffy-4, kitten-2) cop(fluffy-4, was-3) root(ROOT-0, fluffy-4)", 
	#     "kitten")
#test sentence 5: All lightning is frightening to the child
	# print isCountable(
	#     "all/DT lightning/NN is/VBZ frightening/JJ to/TO the/DT child/NN",
	#     "det(lightning-2, all-1) nsubj(frightening-4, lightning-2) cop(frightening-4, is-3) root(ROOT-0, frightening-4) case(child-7, to-5) det(child-7, the-6) nmod(frightening-4, child-7)", 
	#     "lightning")