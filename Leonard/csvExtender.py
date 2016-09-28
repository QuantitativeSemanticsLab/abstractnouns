import re
import csv
from nltk.corpus import wordnet
import nltk
from nltk import WordNetLemmatizer

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
		noun = re.findall(r'(\S*)/', tokenized[i])
		try:
			if len(noun) == 1 and WordNetLemmatizer().lemmatize(noun[0], 'n') == lemma:
				tag = re.findall(r'%s\/(\w*)' % noun[0], tokenized[i])
				nouns.append((noun[0], i+1, tag[0]))
				break
		except UnicodeDecodeError:
			tag = re.findall(r'%s\/(\w*)' % noun[0], tokenized[i])
			nouns.append((noun[0], i+1, tag[0]))
	return nouns

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

def getSubj(dep, noun, index):
	nsubj = re.findall(r'nsubj\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	nsubj += re.findall(r'nsubjpass\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return nsubj

def getDObj(dep, noun, index):
	dobj = re.findall(r'dobj\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return dobj
def getisObj(dep, noun, index):
	obj = re.findall(r'dobj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	return obj
def getisSubj(dep, noun, index):
	nsubj = re.findall(r'nsubj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	nsubj += re.findall(r'nsubjpass\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	return nsubj

def getOfObj(dep, noun, index):
	ofObj = re.findall(r'nmod\:of\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return ofObj

def getIObj(dep, noun, index):
	iobj = re.findall(r'iobj\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return iobj

#looks at tagged sentence to get the verb the noun refers to
def getVerb(tagged, dep, noun, index):
	nsubj = re.findall(r'nsubj\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	nsubj += re.findall(r'nsubjpass\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	
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
			if len(verb) >= 1:
				vtag = getTag(tagged, verb[0])
			else:
				verb = ['']
				vtag = ''
		#handles the gerund case, in which the parser returns the gerund of the vp rather than the base verb
		elif stype == 'VBG':
			verb = re.findall(r'aux\(%s-[0-9]*, (\w*)-[0-9]*\)' % nsubj[0], dep)
			if len(verb) >= 1:
				vtag = getTag(tagged, verb[0])
			else:
				verb = ['']
				vtag = ''
		#all other cases
		else:
			verb = nsubj
			vtag = stype
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % verb[0], dep)
		return verb[0], vtag , 'subject', neg
	#handles cases where noun is the object of the verb
	elif len(dobj) >= 1:
		vtag = getTag(tagged, dobj[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % dobj[0], dep)
		return dobj[0], vtag, 'object', neg
	elif len(iobj) >= 1:
		vtag = getTag(tagged, iobj[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % iobj[0], dep)
		return iobj[0], vtag, 'object', neg
	elif len(xcomp) >= 1:
		vtag = getTag(tagged, xcomp[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % xcomp[0], dep)
		return xcomp[0], vtag, 'object', neg
	elif len(ccomp) >= 1:
		vtag = getTag(tagged, ccomp[0])
		neg = re.findall(r'neg\(%s-[0-9]*, (\w*)-[0-9]*\)' % ccomp[0], dep)
		return ccomp[0], vtag, 'object', neg
	else:
		return '', '', '', ''
	#handles compound case where noun modifies another noun (that is either the subject or object of the verb)
	'''
	elif len(comp) >= 1:
		print comp[0][0]
		split = str(comp[0]).split(',')
		if split != noun:
			count = 0
			for tuple in tagged.split(' '):
				print(tuple)
			verbtup = getVerb(tagged, dep, split, getNouns(tagged, split)[0][1])
		return verbtup[0], verbtup[1], verbtup[2], verbtup[3]
	'''

#determines whether the noun is included in a prep phrase, then returns a tuple of the position in the phrase(modifier vs. modified) with the rest of the phrase
def getPrepOfN(dep, noun, index):
	#nmod = re.findall(r'nmod\:(\w*)\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	modn = re.findall(r'nmod\:(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	modn += re.findall(r'advcl\:(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun,index), dep)
	preps = []
	objs = []
	subjs = []
	preplist = []
	'''
	for i in nmod:
		if i[0] != 'poss':
			preplist.append(i)
			preps.append(i[0])
			objs.append(i[1])
	'''
	for i in modn:
		if i[0] != 'poss':
			preplist.append(i)
			preps.append(i[0])
			subjs.append(i[1])
    
	return preplist, preps, subjs, objs


#determines whether there is a determiner for the given noun in a dependency parse, and returns the determiner(s)
def getDetOfN(dep, noun, index):
	det = re.findall(r'det\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return det

def getMarkofN(dep, noun, index):
	mark = re.findall(r'mark\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	return mark

#determines whether the noun is compounded with another word, then returns the word it's compounded to
def getCompOfN(dep, noun, index):
	compright = re.findall(r'compound\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	#compleft = re.findall(r'compound\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	comp =compright
	return comp

#determines whether the noun occurs in a list of other nouns, then returns a list of tuples of the other noun(s) and conjunction(s)
def getConjOfN(dep, noun, index):
	conjright = re.findall(r'conj\:*(\w*)\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	conjleft = re.findall(r'conj\:*(\w*)\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	conj = conjright + conjleft
	return conj

#determines whether there is an adjectival modifier for the given noun in a dependency parse, and returns the adjective(s)
def getAmodOfN(dep, noun, index):
	amodright = re.findall(r'amod\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	#amodleft = re.findall(r'amod\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	amod = amodright
	return amod

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

def getadvclOfN(dep,noun,index):
	advcl = re.findall(r'advcl\((\w*)-[0-9]*, %s-%d\)' % (noun,index), dep)

	return advcl

#determines whether there is a appositional modifier for the given noun in a dependency parse, and returns the noun(s) and whether they modify or are modified by the given noun
def getApposOfN(dep, noun, index):
	mfd = re.findall(r'appos\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep)
	mfy = re.findall(r'appos\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep)
	mfdappos = []
	mfyappos = []
	for i in mfd:
		mfdappos += ('modified', i)
	for i in mfy:
		mfyappos += ('modifier', i)
	appos = mfdappos + mfyappos
	return appos

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

#takes in a sentence, tags, dependencies, and lemma and returns a list of the outputs to all noun tests
def returnNounTests(sentence, lemma, nountup):
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
	verbneg = verbtup[3]
	mark = getMarkofN(dep, noun, index)
	preptup = getPrepOfN(dep, noun, index)
	prepphrs = preptup[0]
	preps = preptup[1]
	prepsubjs = preptup[2]
	prepobjs = preptup[3]
	dets = getDetOfN(dep, noun, index)
	conjs = getConjOfN(dep, noun, index)
	comps = getCompOfN(dep, noun, index)
	adjs = getAmodOfN(dep, noun, index)
	possd = getPossdOfN(dep, noun, index)
	possv = getPossvOfN(dep, noun, index)
	num = getNumOfN(extdep, noun, index)
	case = getCaseOfN(dep, noun, index)
	adv = getAdvOfN(dep, noun, index)
	appos = getApposOfN(dep, noun, index)
	dens = getDenOfN(dets, adjs, num, adv)
	den = dens[0]
	dentype = dens[1]
	pluN = isPluralN(noun, lemma, nountag)
	pluV = isPluralV(verbtag)
	nsubj = getSubj(dep, noun, index)
	dobj = getDObj(dep, noun, index)
	iobj = getIObj(dep, noun, index)
	ofObj = getOfObj(dep, noun, index)
	sub = getisSubj(dep, noun, index)
	ob = getisObj(dep,noun,index)
	advcl = getadvclOfN(dep,noun,index)
	#passedT = allanTests(dentype, dets, pluN, pluV)
	#countable = isCountable(passedT)
	return [noun, index, dep, sfrag, nountag, neg, verbref, verbtag, verbrel, verbneg, dobj, iobj, ofObj, mark, nsubj, prepphrs, preps, prepsubjs, prepobjs, dets, conjs, comps, adjs, possd, possv, num, case, adv, appos, den, dentype, pluN, pluV, sub, ob]

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
			row.extend(['Noun', 'Noun Tag', 'Verb', 'Verb Tag', 'Determiners', 'Adjectival Modifiers', 'Possesives', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Plurality of Verb', 'subject', 'object'])
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
			row.extend(['Noun', 'Index', 'Relevant Dependencies', 'Sentence Fragment', 'Noun Tag', 'Negation', 'Verb Reference', 'Verb Tag', 'Relation to Verb', 'Verb Negation', 'Direct Object', 'Indirect Object', '"Of" Object', 'Adverbial Preposition', 'Subject', 'Prepositional Phrases', 'Prepositions', 'Prepositional Subjects', 'Prepositional Objects', 'Determiners', 'Conjunctions', 'Compounds', 'Adjectival Modifiers', 'Possesed (owned by noun)', 'Possesive (owner of noun)', 'Numeric Modifiers', 'Case Modifiers', 'Adverbial Modifiers', 'Appositional Modifiers', 'Denumerator', 'Type of Denumerator', 'Plurality of Noun', 'Plurality of Verb', 'subject', 'object','advcl'])
			header = False
			writer.writerow(row)
		else:
			nounoccs = getNouns(row[1], lemma)
			for i in range(len(nounoccs)):
				newrow = []
				newrow.extend([row[0], row[1], row[2]])
				newrow.extend(returnNounTests([row[0], row[1], row[2]], lemma, nounoccs[i]))
				writer.writerow(newrow)

appendToCSV('sellingIn1.csv', 'sellingOut.csv', 'selling')