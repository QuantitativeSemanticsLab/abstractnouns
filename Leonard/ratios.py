import csv
'''
def getOneWay(reader, targetIndex, notwants):
	target = 0
	total = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			total += 1
			passPls = False 
			for index in notwants:
				if(row[index] != '[]'):
					passPls = True
			if(passPls):
				continue
			if(row[targetIndex] != '[]' and row[targetIndex] != ''):
				target += 1
	return target / float(total)

def getNeg(reader, notwants):
	target = 0
	total = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			total += 1
			passPls = False
			for index in notwants:
				if(row[index] != '[]'):
					passPls = True
			if(passPls):
				continue
			target += 1
	print target
	print total
	return target / float(total)

def getPos(reader, dowants):
	target = 0
	total = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			total += 1
			passPls = False
			for index in dowants:
				if(row[index] == '[]'):
					passPls = True
			if(passPls):
				continue
			target += 1
	return target / float(total)
def getTwoWay(reader, numIndex, demIndex, notwants):
	numCount = 0
	demCount = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			passPls = False
			for index in notwants:
				if(row[index] != '[]'):
					passPls = True
			if(passPls):
				continue
			if(row[demIndex] != '[]' and row[demIndex] != ''):
				demCount += 1
				if(row[numIndex] != '[]' and row[numIndex] != ''):
					print row[numIndex]
					numCount += 1
	return numCount / float(demCount)

def getTwoWayNeg(reader, numIndex, notwants):
	numCount = 0
	demCount = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			passPls = False
			for index in notwants:
				if(row[index] != '[]' or row[index] != ''):
					passPls = True
			if(passPls):
				continue
			demCount += 1
			if(row[numIndex] != '[]' and row[numIndex] != ''):
				numCount += 1
	return numCount / float(demCount)
'''

'''
def getTwoWayPos(reader, numIndex, demIndex, dowants):
	numCount = 0
	demCount = 0
	header = True
	for row in reader:
		if header:
			header = False
		else:
			passPls = 
			for index in dowants:
				if(row[index])
'''

def vpingGrabber(list):
	return [row for row in list if row[15] == '[]' and row[22] == '[]' and row[27] == '[]']

def compingGrabber(list):
	return [row for row in list if row[24] != '[]']

def detingGrabber(list):
	return [row for row in list if row[22] != '[]' and row[15] == '[]']

def ofingGrabber(list):
	return [row for row in list if row[15] != '[]' and row[22] == '[]' and row[27] == '[]']

def detofingGrabber(list):
	return [row for row in list if row[22] != '[]' and row[15] != '[]']

def possofingGrabber(list):
	return [row for row in list if row[15] != '[]' and row[27] != '[]']

def possingGrabber(list):
	return [row for row in list if row[27] != '[]' and row[15] == '[]']

def indexGrabber(list, index):
	return [row for row in list if row[index] != '[]']

def prepGrabber(list,prep,index):
	return [row for row in list if prep in row[index].lower()]

def getTheRatio(list, index):
	numer = 0
	denom = len(list)
	if denom == 0:
		denom = 1
	for row in list:
		if row[index] != '[]':
			numer += 1
	return numer / float(denom)

def getPrepRatio(list,prep,index):
	numer = 0
	denom = len(list)
	if denom == 0:
		denom = 1
	for row in list:
		if row[index].lower() == prep:
			numer += 1
	return numer / float(denom)

def getPreps(list, index):
	prepSet = set([])
	for row in list:
		if row[index] != '[]':
			prepSet.add(row[index].lower())
	return prepSet

def getRatio(numer, denom):
	if denom != 0:
		return numer / denom
	else:
		return numer / 1



'''
def getRatio(numList,denList):
	numCount = 0
	denCount = 0
	header = True
	for row in rowsList:
		if header:
			header = False
		else:
'''


colIndices = []
rowIndices = [24,]
vpNegs = [15,22,27]
rowsList= []
def tableMaker(ifile,ofile,ofile2):
	csvifile = open(ifile, 'rU')
	reader = list(csv.reader(csvifile))[1:]
	csvofile = open(ofile, 'w')
	csvofile2 = open(ofile2, 'w')
	writer = csv.writer(csvofile)
	writer2 = csv.writer(csvofile2)
	nums = [(24,'compound'),(36,'subject'),(37,"object"),(25,"adjectival modifier"),(30,"Adverbial Modifier")]
	'''
	header = True
	i = j = 0
	for row in reader:
		if(header):
			header = False
		else:
			for col in row[8:]:
				if (col != '[]' and col != ''):
					rowsList[i][j] = True
				else:
					rowsList[i][j] = False
				j += 1
			j = 0
	i += 1
	'''

	#print(reader)
	writer.writerow(['','VP-ing','of-ing','DET-ing','DET-of-ing','Poss-ing','Poss-of-ing','Total'])
	writer2.writerow(['','VP-ing','of-ing','DET-ing','DET-of-ing','Poss-ing','Poss-of-ing'])
	total = 0
	'''
	for index, name in nums:
		writer.writerow([name,getRatio(vpingGrabber(reader),index),getRatio(ofingGrabber(reader),index),getRatio(detingGrabber(reader),index),getRatio(detofingGrabber(reader),index),getRatio(possingGrabber(reader),index),getRatio(possofingGrabber(reader),index),getRatio(reader,index)])
		total += getRatio(reader,index)
	for prep in getPreps(reader,19):
		writer.writerow([prep,getPrepRatio(vpingGrabber(reader),prep,19),getPrepRatio(ofingGrabber(reader),prep,19),getPrepRatio(detingGrabber(reader),prep,19),getPrepRatio(detofingGrabber(reader),prep,19),getPrepRatio(possingGrabber(reader),prep,19),getPrepRatio(possofingGrabber(reader),prep,19),getPrepRatio(reader,prep,19)])
		total += getPrepRatio(reader, prep,19)
	for prep in getPreps(reader,16):
		writer.writerow([prep + ' -adv',getPrepRatio(vpingGrabber(reader),prep,16),getPrepRatio(ofingGrabber(reader),prep,16),getPrepRatio(detingGrabber(reader),prep,16),getPrepRatio(detofingGrabber(reader),prep,16),getPrepRatio(possingGrabber(reader),prep,16),getPrepRatio(possofingGrabber(reader),prep,16),getPrepRatio(reader,prep,16)])
		total += getPrepRatio(reader, prep,16)
	writer.writerow(["Total",len(vpingGrabber(reader))/float(len(reader)),len(ofingGrabber(reader))/float(len(reader)),len(detingGrabber(reader))/float(len(reader)),len(detofingGrabber(reader))/float(len(reader)),len(possingGrabber(reader))/float(len(reader)),len(possofingGrabber(reader))/float(len(reader)),total])
	'''
	for index, name in nums:

		numer = indexGrabber(reader,index)
		writer.writerow([name,getRatio(len(vpingGrabber(numer)),float(len(numer))),getRatio(len(ofingGrabber(numer)),float(len(numer))),getRatio(len(detingGrabber(numer)),float(len(numer))),getRatio(len(detofingGrabber(numer)),float(len(numer))),getRatio(len(possofingGrabber(numer)),float(len(numer))),getRatio(len(vpingGrabber(numer)),float(len(numer))),len(numer)/float(len(reader))])
		writer2.writerow([name, getRatio(len(indexGrabber(vpingGrabber(reader),index)),float(len(vpingGrabber(reader)))),getRatio(len(indexGrabber(ofingGrabber(reader),index)),float(len(ofingGrabber(reader)))),getRatio(len(indexGrabber(detingGrabber(reader),index)),float(len(detingGrabber(reader)))),getRatio(len(indexGrabber(detofingGrabber(reader),index)),float(len(detofingGrabber(reader)))),getRatio(len(indexGrabber(possingGrabber(reader),index)),float(len(possingGrabber(reader)))),getRatio(len(indexGrabber(possofingGrabber(reader),index)),float(len(possofingGrabber(reader))))])
		#total += getTheRatio(reader,index)
	for prep in getPreps(reader,19):
		numer = prepGrabber(reader,prep,19)
		writer.writerow([prep,getRatio(len(vpingGrabber(numer)),float(len(numer))),getRatio(len(ofingGrabber(numer)),float(len(numer))),getRatio(len(detingGrabber(numer)),float(len(numer))),getRatio(len(detofingGrabber(numer)),float(len(numer))),getRatio(len(possofingGrabber(numer)),float(len(numer))),getRatio(len(vpingGrabber(numer)),float(len(numer))),len(numer)/float(len(reader))])
		writer2.writerow([prep, getRatio(len(prepGrabber(vpingGrabber(reader),prep,19)),float(len(vpingGrabber(reader)))),getRatio(len(prepGrabber(ofingGrabber(reader),prep,19)),float(len(ofingGrabber(reader)))),getRatio(len(prepGrabber(detingGrabber(reader),prep,19)),float(len(detingGrabber(reader)))),getRatio(len(prepGrabber(detofingGrabber(reader),prep,19)),float(len(detofingGrabber(reader)))),getRatio(len(prepGrabber(possingGrabber(reader),prep,19)),float(len(possingGrabber(reader)))),getRatio(len(prepGrabber(possofingGrabber(reader),prep,19)),float(len(possofingGrabber(reader))))])
	for prep in getPreps(reader,16):
		numer = prepGrabber(reader,prep,16)
		writer.writerow([prep + ' -adv',getRatio(len(vpingGrabber(numer)),float(len(numer))),getRatio(len(ofingGrabber(numer)),float(len(numer))),getRatio(len(detingGrabber(numer)),float(len(numer))),getRatio(len(detofingGrabber(numer)),float(len(numer))),getRatio(len(possofingGrabber(numer)),float(len(numer))),getRatio(len(vpingGrabber(numer)),float(len(numer))),len(numer)/float(len(reader))])
		writer2.writerow([prep, getRatio(len(prepGrabber(vpingGrabber(reader),prep,16)),float(len(vpingGrabber(reader)))),getRatio(len(prepGrabber(ofingGrabber(reader),prep,16)),float(len(ofingGrabber(reader)))),getRatio(len(prepGrabber(detingGrabber(reader),prep,16)),float(len(detingGrabber(reader)))),getRatio(len(prepGrabber(detofingGrabber(reader),prep,16)),float(len(detofingGrabber(reader)))),getRatio(len(prepGrabber(possingGrabber(reader),prep,16)),float(len(possingGrabber(reader)))),getRatio(len(prepGrabber(possofingGrabber(reader),prep,16)),float(len(possofingGrabber(reader))))])

	writer2.writerow(['Total',len(vpingGrabber(reader))/float(len(reader)),len(ofingGrabber(reader))/float(len(reader)),len(detingGrabber(reader))/float(len(reader)),len(detofingGrabber(reader))/float(len(reader)),len(possingGrabber(reader))/float(len(reader)),len(possofingGrabber(reader))/float(len(reader))])
	#writer.writerow([str(getNeg(reader,vpNegs)),str(getOneWay(reader,22,[15])),str(getPos(reader,[15,22])),str(getOneWay(reader,27,[13,15])),str(getPos(reader, [27,13])),str(getPos(reader, [27,15])),'0' ])



tableMaker('sellingOut.csv', 'sellingTable.csv','sellingTable2.csv')
#print getOneWay('testingOut.csv', 27)

	

