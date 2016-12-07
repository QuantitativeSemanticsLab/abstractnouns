import pandas as pd
import numpy as np

header = ['index', 'word', 'occurences', "MorphStatus","Lang","MorphCnt","MorphNum","NVAffComp","Der","Comp","DerComp","Def","Imm","ImmClass","ImmSubCat","ImmSA","ImmAllo","ImmSubst","ImmOpac","TransDer","ImmInfix","ImmRevers","Flat","FlatClass","FlatSA","Struc","StrucLab","StrucBrackLab","StrucAllo","StrucSubst","StrucOpac","CompCnt","MorCnt","LevelCnt","ExampleName","Sing","Plu","Pos","Comp","Sup","Inf","Part","Pres","Past","Sin1","Sin2","Sin3","Rare","FlectType","TransInfl"]

eml = pd.read_csv('eml.cd', delimiter = '\\', index_col=0, header = None, names = header)

eml.to_csv('celexmorph.csv', index = False)
