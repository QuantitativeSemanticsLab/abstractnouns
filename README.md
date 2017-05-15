# abstractnouns
## Parsing COCA

COCA text files are parsed and saved in hdf5 files for each type of COCA sample (academic, fiction, magazine, newspaper, and spoken). Each file is parsed in parallel, the script detects the number of cpu cores available then creates that many threads to run on. For each sentence, a testfile is created and filled with the sample sentence and the stanford parser is run on that file. The resulting output is a string of the tagged sentence and the dependency parse, which are split and stored as a pandas series which is appended to a pandas dataframe for the whole COCA file. Once the entire file is parsed, it is stored in the corresponding hdf5 file for its type

To parse an individual text file, run this command:
```bash
python c2h5multi.py <filepath>
```
The COCA files can't be stored here due to liscensing, so the commands to run depend on how the COCA files are structured and where they are stored. For nested files with folders for each type, run this command:
```bash
for f in COCA_Corpus/*/*; do python c2h5multi.py $f; done
```

---
## Creating Infiles

Infiles are created by pulling sentences stored in hdf5 files for each COCA type to extract all sentences that contain a given word, along with their given tags and parses. These sentences are stored as a pandas dataframe that is then converted to a csv file.
To create an infile for a given word run this command:
```bash
python H5toCSV.py <word lemma>
```

To create infiles for all of the nouns in nounlist run these commands:
```bash
while read f; do python H5toCSV.py $f; done < regularnouns.txt
```

edit H5toCSV.py ln32 to be csvname = 'infiles/' + word + '1In.csv'
```bash
while read f; do python H5toCSV.py $f; done < nonregularnouns_sep.txt
while read f; do $f; done <nonregularnouns_tup.txt 
```

The first command creates infiles for all regular nouns w/ +s plural constructions. The second command creates separate infiles for plural and nonplural versions of non-regular nouns (with -y+ies, -s+es, etc.) plural constructions. The third command merges the singular and plural non-regular noun infiles into one infile (named for the singular version of the noun)

## Creating Outfiles

Outfiles are created through a series of noun tests based on the dependency parse pairings that include the noun. The relevant wods are pulled from the dependency parse using a regex. Some tests are more complicated, but the basic tests follow a similar format:

```python
def get<feature>OfN(dep, noun, index): #more features can be passed in if they've been previously stored
  #the format of the regex is determined by the dependency structure 
  #check online stanford parses to determine whether the target noun is on the right/left, and if the dependency is otherwise abnormal 
  <feat> = re.findall(r'<feat>\(%s-%d, (\w*)-[0-9]*\)' % (noun, index), dep) #target noun on left side of dependency
  <feat> = re.findall(r'<feat>\((\w*)-[0-9]*, %s-%d\)' % (noun, index), dep) #target noun on right side of dependency
  #extra functions can be performed on the extracted word(s) here
  return <feat>
```

Other more complicated tests have more explanation in comments and outfileFormat.txt. All tests must be run in returnNounTests, added to the return array, and named in appendToCSV. In appendToCSV, the tests are run on each line of the infile and stored in new columns for each row in the outfile.

To create outfiles for a given word run this command:
```bash
python nountests.py <word lemma>
```

To create outfiles for all the nouns in nounlist, run this command:
```bash
while read f; do python nountests.py $f; done < nounlist.txt
```

## Creating Postfiles/Master

Postfiles are cleaned versions of Outfiles, and in the process of cleaning, postprocess calculates percentages for each column of each outfile to compress the outfile into a row of a master csv. Each column is considered seperately within postprocess, but all columns get a subset of 6 methods applied to them. fixEmpty replaces null cells with the empty string, listCol converts strings of lists into iterable python lists, freqCol creates a frequency list for all of the words in the column, stripCol cleans list columns to a nicer format, lowerCol turns a column to lowercase (so that freqCol is more acccurate), and getPercent converts the count of a column and the total of a column into a ratio. The functions for each column are detailed within the comments.

To create a postfile for a given word, run this command:
```bash
python postprocess.py <word lemma>
```

To create postfiles for all the nouns in nounlist and create the master, run these commands:
```bash
python writeheader.py
while read f; do python postprocess.py $f; done < nounlist.txt
```

---
## Using the Adjective Supersense Classifier
To produce the "Adjtype: x" features, use the adjective_supersense_classifier from 
<i class="icon-share"></i> http://www.cs.cmu.edu/~ytsvetko/papers/adj-lrec14.pdf

'''bash
git clone https://github.com/ytsvetko/adjective_supersense_classifier. 
'''

Instead of using the provided data file, run gensim word2vec on combined COCA corpus text using the python interface for 2ord2vec 

'''bash
git clone https://github.com/danielfrg/word2vec
'''

Combine the coca corpus text files into one using the command

''' bash
cat * > coca.txt
'''

in the directory of COCA txt files. 
Then copy runw2v.py into the pulled word2vec directory, run, then convert the resulting .bin file into a txt file

'''bash
python runw2vec.py
git clone https://github.com/marekrei/convertvec
./convertvec bin2txt cocavec.bin cocavec.txt
'''

The resulting file is cocavec.txt, which should replace the eacl14-faruqui-en-svd-de-64.adj.txt.gz file in adjective_supersense_classifier/data/VSM

Then run the classifier according to it's documentation

'''bash
./adj_supersense_tagger.sh
'''

use the words.predicted file from the predicted_supersenses directory to run nountests.py normally.

runw2v.py, and words.predicted can be found in this repo, but intermediary files must be run independently. 

---
## Clustering

master.csv can be clustered using k-means and plotted in 2 or 3 dimensions by running testplot.py and changing variables to determine the number of dimensions and their content, as well as the number of clusters. Edit lines 17-19 to change the columns to focus on, line 20 to determine the number of dimensions, and 21 for the number of clusters. 

To cluster and plot data, run this command:
```bash
python testplot.py
```
