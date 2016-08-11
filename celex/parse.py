import pandas as pd
import numpy as np

header = ['index', 'word', 'occurences', 'classNum', 'C_N', 'Unc_N', 'Sing_N', 'Plu_N', 'GrC_N', 'GrUnc_N', 'Attr_N', 'PostPos_N', 'Voc_N', 'Proper_N', 'Exp_N', 'Trans_V', 'TransComp_V', 'Intrans_V', 'Ditrans_V', 'Link_V', 'Phr_V', 'Prep_V', 'PhrPrep_V', 'Exp_V', 'Ord_A', 'Attr_A', 'Pred_A', 'PostPos_A', 'Exp_A', 'Ord_ADV', 'Pred_ADV', 'PostPos_ADV', 'Comb_ADV', 'Exp_ADV', 'Card_NUM', 'Ord_NUM', 'Exp_NUM', 'Pers_PRON', 'Dem_PRON', 'Poss_PRON', 'Refl_PRON', 'Wh_PRON', 'Det_PRON', 'Pron_PRON', 'Exp_PRON', 'Cor_C', 'Sub_C']

esl = pd.read_csv('esl.cd', delimiter = '\\', index_col = 0, header = None, names = header)
eslNouns = esl[esl['classNum']== 1]
eslNouns = eslNouns.iloc[:, 0:14]

#print eslNouns 
eslNouns.to_csv('celex.csv', index = False)