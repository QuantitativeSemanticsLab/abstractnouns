import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from pandas import HDFStore


academic = HDFStore('COCA_Corpus/COCAStore_academic_rpe.h5')
fiction = HDFStore('COCA_Corpus/COCAStore_fiction_awq.h5')
magazine = HDFStore('COCA_Corpus/COCAStore_magazine_qhk.h5')
newspaper = HDFStore('COCA_Corpus/COCAStore_newspaper_lsp.h5')
spoken = HDFStore('COCA_Corpus/COCAStore_spoken_kde.h5')

catlist = [['acad', academic],['fic', fiction],['mag', magazine],['news', newspaper],['spok', spoken]]

def extractword(word):
	df_word = pd.DataFrame(columns=['sent', 'tags', 'parse'])
	for cat in catlist:
		for year in range(1990, 2013):
			storename = '/w_' + cat[0] + '_' + str(year)
			h5name = cat[1]
			try:
				df = h5name[storename]
				print storename
				df_small = df[df['sent'].str.contains(word) == True]
				#df_word.append(df_small, ignore_index = True)
				df_word = pd.concat([df_word, df_small])
				#print df_word
			except KeyError:
				print 'filename not found'
	csvname = 'infiles/' + word + 'In.csv'
	df_word.to_csv(csvname, index = False)

word = sys.argv[1]
extractword(word)


