import csv
import re
import os
import sys
# increase the field size so that reading a large
# file will not lead to crush
csv.field_size_limit(sys.maxsize)

# this is the place where parsed files are
file_directory='/scratch/sgrimm3_lab/0617_parsedfiles'

# create the infile folder at where the parsed files are
infile_directory=file_directory+'/'+'infile'

# a noun list specify which nouns you want to get
nounfile=open('/scratch/sgrimm3_lab/0617_parsedfiles/nounlist.txt','r')
nounlist=set([])
for noun in nounfile:
    nounlist.add(noun.strip('\n'))

# if the infile directory does not exist, create it
if not os.path.exists(infile_directory):
    os.makedirs(infile_directory)

# find all the nouns in the tags
# this will exclude strange symbols like ##
# and will find singular and plural nouns
def findNoun(x):
    nouns=set([])
    nounList=re.findall(r'\w*\/\w*\/NN',x)
    for x in nounList:
        lemma=(x.split('/')[1])
        if lemma in nounlist:
            nouns.add(lemma)
    return nouns

# process each file to a infile

def process_file(raw_file):
    with open(raw_file,'r') as raw:
        raw_reader=csv.reader(raw)
        next(raw_reader)
        for row in raw_reader:
            tags=row[1]
            nouns=findNoun(tags)
            for noun in nouns:
                infile=infile_directory+"/"+noun+".csv"
                if not os.path.isfile(infile):
                    with open(infile, 'wb') as outcsv:
                        writer = csv.writer(outcsv)
                        writer.writerow(['sent','tags','parse','ner','open IE'])
                        writer.writerow(row)
                else:
                    with open(infile, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
    print "Finished parsing %s"%raw_file

raw_data_dir=[]
for root, dirs, files in os.walk(file_directory):
    raw_data_dir.extend(dirs)
raw_data_dir.remove('infile')
raw_data_dir=map(lambda x: file_directory+'/'+x, raw_data_dir)


for dirs in raw_data_dir:
    directory=dirs
    raw_files=[]
    for root, dirs, files in os.walk(dirs):
        raw_files.extend(files)
    
    raw_files=filter(lambda x: x.endswith('.csv'), raw_files)
    raw_files=map(lambda x: directory+'/'+x, raw_files)
    # print raw_files
    for raw in raw_files:
        process_file(raw)
