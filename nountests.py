import sys
import re
from nltk.stem import WordNetLemmatizer
import csv
import string

#returns a string of the relevant dependencies (those that contain the target noun)
def getRelDeps(dep, noun, index):
	reldep = ''
	reldepleft = re.findall(r'(\S*\(%s-%d, \S*-[0-9]*\))' % (noun, index), dep)
	reldepright = re.findall(r'(\S*\(\S*-[0-9]*, %s-%d\))' % (noun, index), dep)
	for r in reldepleft:
		reldep += r + ' '
	for r in reldepright:
		reldep += r + ' '
	return reldep

#returns a string of the 10 words surrounding the noun in a sentence
def getSentFrag(sent, index):
	arr = sent.split()
	if (index-6) < 0:
		startindex = 0
	else:
		startindex = index-6
	if (index+5) > len(arr):
		endindex = len(arr)
	else:
		endindex = index+5
	sentfragarr = arr[startindex:endindex]
	sentfrag = ' '.join(sentfragarr)
	return sentfrag


#returns a list of tuples of nouns, indeces, and tags from a tagged sentence for a given lemma
def getNouns(tagged, lemma):
	tokenized = tagged.split()
	nouns = []
	for i in range(len(tokenized)):
		noun = re.findall(r'(\S*)/N', tokenized[i])
		if len(noun) == 1:
			try:
				lmtz = WordNetLemmatizer().lemmatize(noun[0], 'n') 
				if lmtz == lemma:
					tag = re.findall(r'%s\/(\w*)' % noun[0], tokenized[i])
					nouns.append((noun[0], i+1, tag[0]))
			except UnicodeDecodeError:
				print 'LEMMATIZER ERROR: ' + noun[0]
	return nouns

def getIndex(tagged, n):
	tokenized = tagged.split()
	nouns = []
	for i in range(len(tokenized)):
		noun = re.findall(r'(\S*)/N', tokenized[i])
		if len(noun) == 1:
			if noun[0] == n:
				return i+1
	return False

#looks at tagged sentence to get the tag of a given word
def getTag(tagged, word):
	tag = re.findall(r'%s\/(\w*)' % word, tagged)
	return tag[0]

#looks to see if the noun is negated and returns the negation
def getNeg (dep, noun, index):
	neg = re.findall(r'neg\(%s-%d, (\w*)-[0-9]*' % (noun, index), dep)
	return neg

#classifying verbs
verbtag = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

#looks at tagged sentence to get the verb the noun refers to
def getVerb(tagged, dep, noun, index):
	nsubj = re.findall(r'nsubj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	nobj = re.findall(r'nsubj\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	nsubjpass = re.findall(r'nsubjpass\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	dobj = re.findall(r'dobj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	iobj = re.findall(r'iobj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	comp = re.findall(r'compound\((\w*)-([0-9]*), %s-%d\)' % (noun, index), dep)
	xcomp = re.findall(r'xcomp\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	ccomp = re.findall(r'ccomp\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	#handles cases where noun is the subject of the verb
	if len(nsubj) >= 1:
		stype = getTag(tagged, nsubj[0])
		#handles the copula case, in which the parser uses a non-verb(esp. adjectives) in the nsubj instead of the base verb
		if stype not in verbtag:
			verb = re.findall(r'cop\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
			verb += re.findall(r'cop\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
			if len(verb) >= 1:
				vtag = getTag(tagged, verb[0])
			else:
				verb = ['']
				vtag = ''		
		#handles the gerund case, in which the parser returns the gerund of the vp rather than the base verb
		elif stype == 'VBG':
			verb = re.findall(r'aux\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
			if len(verb) >= 1:
				neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
				vtag = getTag(tagged, verb[0])
				vlemma = WordNetLemmatizer().lemmatize(verb[0], 'v')
				return verb[0], vtag, 'subject', neg, vlemma
			else:
				verb = ['']
				vtag = ''
		#all other cases
		else:
			verb = nsubj
			vtag = stype
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % verb[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(verb[0], 'v')
		return verb[0], vtag , 'subject', neg, vlemma
	if len(nobj) >= 1:
		stype = getTag(tagged, nobj[0])
		#handles the copula case, in which the parser uses a non-verb(esp. adjectives) in the nsubj instead of the base verb
		if stype not in verbtag:
			verb = re.findall(r'cop\(%s-[0-9]*, (\w*)-[0-9]*\)' % nobj[0], dep)
			verb += re.findall(r'cop\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
			if len(verb) >= 1:
				vtag = getTag(tagged, verb[0])
			else:
				verb = ['']
				vtag = ''		
		#handles the gerund case, in which the parser returns the gerund of the vp rather than the base verb
		elif stype == 'VBG':
			verb = re.findall(r'aux\(%s-[0-9]*, (\w*)-[0-9]*\)' % nobj[0], dep)
			neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % nobj[0], dep)
			if len(verb) >= 1:
				vtag = getTag(tagged, verb[0])
				vlemma = WordNetLemmatizer().lemmatize(verb[0], 'v')
				return verb[0], vtag, 'object', neg, vlemma
			else:
				verb = ['']
				vtag = ''
		#all other cases
		else:
			verb = nobj
			vtag = stype
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % verb[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(verb[0], 'v')
		return verb[0], vtag , 'object', neg, vlemma
	elif len(nsubjpass) >=1:
		vtag = getTag(tagged, nsubjpass[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubjpass[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(nsubjpass[0], 'v')
		return nsubjpass[0], vtag, 'subject', neg, vlemma
	#handles cases where noun is the object of the verb
	elif len(dobj) >= 1:
		vtag = getTag(tagged, dobj[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % dobj[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(dobj[0], 'v')
		return dobj[0], vtag, 'object', neg, vlemma
	elif len(iobj) >= 1:
		vtag = getTag(tagged, iobj[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % iobj[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(iobj[0], 'v')
		return iobj[0], vtag, 'object', neg, vlemma
	elif len(xcomp) >= 1:
		vtag = getTag(tagged, xcomp[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % xcomp[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(xcomp[0], 'v')
		return xcomp[0], vtag, 'object', neg, vlemma
	elif len(ccomp) >= 1:
		vtag = getTag(tagged, ccomp[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % ccomp[0], dep)
		vlemma = WordNetLemmatizer().lemmatize(ccomp[0], 'v')
		return ccomp[0], vtag, 'object', neg, vlemma
	#handles compound case where noun modifies another noun (that is either the subject or object of the verb)
	elif len(comp) >= 1:
		verbtup = getVerb(tagged, dep, comp[0][0], int(comp[0][1]))
		return verbtup[0], verbtup[1], verbtup[2], verbtup[3], verbtup[4] 
	else:
		return '', '', '', '', ''

#determines whether the noun is included in a prep phrase, then returns a tuple of the position in the phrase(modifier vs. modified) with the rest of the phrase		
def getPrepOfN(dep, noun, index):
	nmod = re.findall(r'nmod\:(\w*)\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	modn = re.findall(r'nmod\:(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	preps = []
	objs = []
	subjs = []
	preplist = []
	for i in nmod:
		if i[0] != 'poss':
			preplist.append(i)
			preps.append(i[0])
			objs.append(i[1])
	for i in modn:
		if i[0] != 'poss':
			preplist.append(i)
			preps.append(i[0])
			subjs.append(i[1])
			
	return preplist, preps, subjs, objs

indef_articles = ['a','an','some']
def_articles = ['the']
demonstratives = ['this','that','those','these','which']
quantifiers = ['each','every','few','a few','many','much','some','any','all']

#determines whether there is a determiner for the given noun in a dependency parse, and returns the determiner(s)
def getDetOfN(dep, noun, index):
	det = re.findall(r'det\:*\w*\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	dettype = ''
	for i in det:
		if i in indef_articles:
			dettype ='indefinite article'
		elif i in def_articles:
			dettype ='definite article'
		elif i in demonstratives:
			dettype ='demonstrative'
		elif i in quantifiers:
			dettype ='quantifier'
		else:
			dettype ='other'
	return det, dettype

#determines whether the noun is compounded with another word, then returns the word it's compounded to 
def getCompOfN(dep, noun, index):
	compright = re.findall(r'compound\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	compleft = re.findall(r'compound\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	comp = compleft + compright
	return comp 

#determines whether the noun occurs in a list of other nouns, then returns a list of tuples of the other noun(s) and conjunction(s)
def getConjOfN(dep, noun, index):
	conjright = re.findall(r'conj\:*(\w*)\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	conjleft = re.findall(r'conj\:*(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	conjs = []
	conjd = []
	conjp = []
	for i in conjright:
		conjs.append(i[0])
		conjd.append(i[1])
		conjp.append(i)
	for i in conjleft:
		conjs.append(i[0])
		conjd.append(i[1])
		conjp.append(i)
	return conjp, conjs, conjd

def loadAdjTypes(): 
    adjdict = {}
    adjdf = open("words.predicted","r")
    for ln in adjdf:
        l = re.findall(r"(.*){", ln)[0].split("\t")
        adjdict[l[0]]=l[1]
    return adjdict

#determines whether there is an adjectival modifier for the given noun in a dependency parse, and returns the adjective(s)
def getAmodOfN(dep, noun, index):
	amod = re.findall(r'amod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return amod

def getAdjType(adj, adjdict):
    adjtype = []
    for i in adj:
        if i in adjdict:
            adjtype.append(adjdict[i])
    return adjtype
  

#determines whether there is a possesive pronoun or proper noun for the given noun in a dependency parse, and returns the pronoun(s) or noun(s) that are owned by the noun
def getPossdOfN(dep, noun, index):
	possd = re.findall(r'nmod\:poss\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	return possd

#determines whether there is a possesive pronoun or proper noun for the given noun in a dependency parse, and returns the pronoun(s) or noun(s) that own the noun
def getPossvOfN(dep, noun, index):
	possv = re.findall(r'nmod\:poss\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return possv

#determines whether there is a numeric modifier for the given noun in a dependency parse, and returns the number(s)
def getNumOfN(dep, noun, index):
	num = re.findall(r'nummod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	if len(num) >=1:
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

#determines whether there is a appositional modifier for the given noun in a dependency parse, and returns the noun(s) and whether they modify or are modified by the given noun
def getApposOfN(dep, noun, index):
	mfd = re.findall(r'appos\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	mfy = re.findall(r'appos\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	appos = []
	mfdappos = []
	mfyappos = []
	for i in mfd:
		appos += ('modified', i)
		mfdappos.append(i)
	for i in mfy:
		appos += ('modifier', i)
		mfyappos.append(i)
	return appos, mfyappos, mfdappos

def getModalOfN(dep, tagged, noun, index):
	aux = re.findall(r'aux\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	if len(aux) >= 1:
		atag = getTag(tagged, aux[0])
		if atag == 'MD':
			return aux
	return []

def getCondOfN(dep, tagged, noun, index, verb):
	mark = re.findall(r'mark\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	markv = re.findall(r'mark\(%s-[0-9]*, (\w*)-[0-9]*\)' % verb, dep)
	if len(mark) >= 1 :
		mtag = getTag(tagged, mark[0])
		if mtag == 'IN':
			return mark
	if len(markv) >= 1 :
		mtag = getTag(tagged, markv[0])
		if mtag == 'IN':
			return markv
	return []



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

def isBareN(extdep, tagged, plurality, dets, poss, nums, dens, adjs, conjd):
	bareconj = True
	if conjd != []:
		i = conjd[0]
		conjdi = getIndex(tagged, i)
		conjddep = getRelDeps(extdep, i, conjdi)
		conjdet = getDetOfN(conjddep, i, conjdi)[0]
		conjposs = getPossdOfN(conjddep, i, conjdi)
		conjnums = getNumOfN(extdep, i, conjdi)
		conjadj = getAmodOfN(conjddep, i, conjdi)
		conjadv = getAdvOfN(conjddep, i, conjdi)
		conjdens = getDenOfN(conjdet, conjadj, conjnums, conjadv)[0]
		if conjdet != [] or conjposs != [] or conjnums !=[] or conjdens != "":
			bareconj = False
	if plurality == 'plural' and dets == [] and poss == [] and nums == [] and dens[0] == "" and adjs == [] and bareconj:
		return 'bare plural'
	elif plurality == 'singular' and dets == [] and poss == [] and nums == [] and dens[0] == "" and adjs == [] and bareconj:
		return 'bare singular'
	else:
		return 'linked'

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
	test = []
	#A+N test
	if dent == "unit" and pluN != "plural":
		test.append("A+N")
	#F+Ns test
	if dent == "fuzzy" and pluN != "singular": 
		test.append("F+Ns")
	#EX-PL test
	if pluN != "plural" and pluV == "plural":
		test.append("EX-PL")
	#O-DEN test
	if dent == "other":  
		test.append("O-DEN")
	#All+N test
	for d in det:
		if d == "all" and len(det) == 1 and pluN == "singular":
			test.append("All+N")
	return test

#looks at sentence to determine whether the noun is countable in the given context based on the allan tests
def isCountable(tests):
	if tests != []:
		if 'All+N' in tests:
			return "uncountable"
		else:
			return "countable"
	else: 
		return "unknown"

def isVerdical(modl, cond, negn, negv):
	if len(negn) >= 1 or len(negv) >=1:
		return 'verdical'
	elif len(modl) >= 1:
		return 'nonverdical'
	elif len(cond) >= 1:
		return 'nonverdical'
	else:
		return 'unknown'

#takes in a sentence, tags, dependencies, and lemma and returns a list of the outputs to all noun tests
def returnNounTests(sentence, lemma, nountup, adjdict):
	sent = sentence[0]
	tagged = sentence[1]
	extdep = sentence[2]
	noun = nountup[0]
	index = nountup[1]
	dep = getRelDeps(extdep, noun, index)
	sfrag = getSentFrag(sent, index)
	nountag = nountup[2]
	neg = getNeg(dep, noun, index)
	verbtup = getVerb(tagged, extdep, noun, index)
	verbref = verbtup[0]
	verbtag = verbtup[1]
	verbrel = verbtup[2]
	verblemma = verbtup[4]
	if verbrel == 'subject':
		verbsubj = verbref
		verbsubjlemma = verblemma
		verbobj = ''
		verbobjlemma = ''
	elif verbrel == 'object':
		verbobj = verbref
		verbobjlemma = verblemma
		verbsubj = ''
		verbsubjlemma = ''
	else:
		verbsubj, verbsubjlemma, verbobj, verbobjlemma = '', '', '', ''
	verbneg = verbtup[3]
	preptup = getPrepOfN(dep, noun, index)
	prepphrs = preptup[0]
	preps = preptup[1]
	prepsubjs = preptup[2]
	prepobjs = preptup[3]
	dettup = getDetOfN(dep, noun, index)
	dets = dettup[0]
	dettype = dettup[1]
	conj = getConjOfN(dep, noun, index)
	conjp = conj[0]
	conjs = conj[1]
	conjd = conj[2]
	comps = getCompOfN(dep, noun, index)
	adjs = getAmodOfN(dep, noun, index)
	adjtype = getAdjType(adjs, adjdict)
        possd = getPossdOfN(dep, noun, index)
	possv = getPossvOfN(dep, noun, index)
	num = getNumOfN(extdep, noun, index)
	case = getCaseOfN(dep, noun, index)
	adv = getAdvOfN(dep, noun, index)
	appos = getApposOfN(dep, noun, index)
	app = appos[0]
	appmod = appos[1]
	modapp = appos[2]
	modl = getModalOfN(dep, tagged, noun, index)
	cond = getCondOfN(dep, tagged, noun, index, verbref)
	dens = getDenOfN(dets, adjs, num, adv) 
	den = dens[0]
	dentype = dens[1]
	pluN = isPluralN(noun, lemma, nountag)
	bareplu = isBareN(extdep, tagged, pluN, dets, possd, num, dens, adjs, conjd)
	pluV = isPluralV(verbtag)
	passedT = allanTests(dentype, dets, pluN, pluV)
	countable = isCountable(passedT)
	verdical = isVerdical(modl, cond, neg, verbneg)
	return [noun, index, dep, sfrag, nountag, neg, verbref, verbtag, verbrel, verbsubj, verbsubjlemma, verbobj, verbobjlemma, verbneg, prepphrs, preps, prepsubjs, prepobjs, dets, dettype, conjp, conjs, conjd, comps,  adjs, adjtype,  possd, possv, num, case, adv, app, appmod, modapp, modl, cond, den, dentype, pluN, bareplu, pluV, passedT, countable, verdical]


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
			row.extend(['Noun', 'Noun Tag', 'Verb', 'Verb Tag', 'Determiners', 'Adjectival Modifiers', 'Adjective Types', 'Possesives', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Plurality of Verb', 'Allan Tests Passed', 'Countability'])
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
        adjdict = loadAdjTypes()
	header = True
	for row in reader:
		if header:
			row.extend(['Noun', 'Index', 'Relevant Dependencies', 'Sentence Fragment', 'Noun Tag', 'Negation', 'Verb Reference', 'Verb Tag', 'Relation to Verb', 'Verb Subject', 'Verb Subject Lemma', 'Verb Object', 'Verb Object Lemma', 'Verb Negation', 'Prepositional Phrases', 'Prepositions', 'Prepositional Subjects', 'Prepositional Objects', 'Determiners', 'Determiner Type', 'Conjunction Phrases', 'Conjunctions', 'Conjoined', 'Compounds', 'Adjectival Modifiers', 'Adjective Types', 'Possesed owned by noun', 'Possesive owner of noun', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Appositionals', 'Appositional Modifiers', 'Modified Appositives', 'Modality', 'Conditional', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Bareness of Noun', 'Plurality of Verb', 'Allan Tests Passed', 'Countability', 'Verdicality'])
			header = False
			writer.writerow(row)
		else:
			nounoccs = getNouns(row[1], lemma)
			for i in range(len(nounoccs)):
				newrow = []
				newrow.extend([row[0], row[1], row[2]])
				newrow.extend(returnNounTests([row[0], row[1], row[2]], lemma, nounoccs[i], adjdict))
				writer.writerow(newrow)
	#csvifile.close()
	#csvofile.close()

#appendToCSV('brotherIn.csv', 'brotherOut.csv', 'brother')
# appendToCSV('harmIn.csv', 'harmOut.csv', 'harm')
#appendToCSV('crimeIn.csv', 'crimeOut.csv', 'crime')
#appendToCSV('testingIn.csv', 'testingOut.csv', 'testing')
lemma = sys.argv[1]
infilepath = 'infiles/'+ lemma + 'In.csv'
outfilepath = 'outfiles/' + lemma + 'Out.csv'
appendToCSV(infilepath, outfilepath, lemma)
print 'written to ' + outfilepath


