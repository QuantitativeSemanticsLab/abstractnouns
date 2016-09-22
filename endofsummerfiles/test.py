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

print academic
print fiction 
print magazine
print newspaper
print spoken

print magazine['w_mag_1991']




