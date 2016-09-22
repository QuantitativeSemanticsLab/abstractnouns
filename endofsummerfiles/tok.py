import sys

import numpy as np

import pandas as pd
#from pandas import DataFrame

import nltk
from nltk.tokenize import *
from nltk.tokenize import sent_tokenize

filepath = sys.argv[1]
f = open(filepath)
text = f.read()

sent_tokenize_list = sent_tokenize(text)
listlen = len(sent_tokenize_list)
dftok = pd.DataFrame(sent_tokenize_list)
dftok.to_csv('dftok.csv')
