import requests
import json
import re
import csv
import sys
import os
from os import walk
from multiprocessing import Pool, cpu_count
import timeit

# The idea of this parsin
# is that we create our own server on local port
# and then implement multi-proecssing
# even though the multi-processing work here seem to be light
# as a matter of fact, if you look at activity monitor, each
# python workload will only be 2%, however, the java work will be
# around 400% if you have 4 cores.
# don't worry about that it does not mean we put too much work on one
# core, it means that all the cores are working at their best
# I think java can distribute the workload to cpu on its own
# to build the port, go to where the corenlp direcory is,
# run java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 
# in commend line
# more information can be found here
# https://stanfordnlp.github.io/CoreNLP/corenlp-server.html

params = (
    ('properties', '{"annotators":"pos,depparse","outputFormat":"json"}'),
)

# data = "Life and Letters <p> In the house of literature there are many anterooms . Let 's suppose , for instance , that we find ourselves in the most public of this stately house 's rooms , the parlor . While the great writer is busy working upstairs , here , milling around , are the various people who play subsidiary roles in that writer 's life : in one corner stand family members and close friends ; in another , deep in conference , are editors , publishers , agents ; also present are journalists , photographers , proteges , miscellaneous admirers and hangers-on , and , perhaps , taking notes in an alcove , the writer 's official biographer . <p>"




# print temp['sentences'][1]


def parseDependency(dep_list):
  # We are reading from a list, where all the items are 
  # dictionaries, we just have to extract all the information
  # from the dictionaries

  parsedDependencyList=[]
  for dependency in dep_list:
    dep=dependency['dep']
    dependent=dependency['dependent']
    dependentGloss=dependency['dependentGloss']
    governorGloss=dependency['governorGloss']
    governor=dependency['governor']
    dependencyText=str(dep)+'('+str(governorGloss)+'-'+str(governor)+', '+str(dependentGloss)+'-'+str(dependent)+')'
    parsedDependencyList.append(dependencyText)
  return parsedDependencyList


def parsePOS(pos_list):
  # parsing the part of speech tags
  sentence=[]
  posList=[]
  for tags in pos_list:
    word=tags['word']
    pos=tags['pos']
    posList.append(word+'/'+pos)
    sentence.append(word)
  return [' '.join(sentence),' '.join(posList)]

def parseSentence(sentence):
  # this function is to parse a sentence
  # so what I did is to send the sentence to local server
  # if you run the code I provided at the top,
  # then the port is 9000. You can of course 
  # use another one if port 9000 is busy
  rows=[]
  
  try: 
    # parsing to utf-8 is going to cause some problems in some lines
    # I have not done specific work to parse a single sentence each time
    # this is parsing a line in the text file
    # it is hard to tell where a sentence ends. It can be ?,.! or whatever
    # leave it to the stanford parser
    data=sentence.replace(u'\xa0', u' ').encode('utf-8')
    result= requests.post('http://localhost:9000/', params=params, data=data).content
    json_item = json.loads(result)
    for item in json_item['sentences']:
      dep_list=item['enhancedPlusPlusDependencies']
      pos_list=item['tokens']
      pos_result=parsePOS(pos_list)
      dependency_result=parseDependency(dep_list)
      rows.append([pos_result[0],pos_result[1]," ".join(dependency_result)])
      # print " ".join(dependency_result)
    return rows
  except:
    print "Error parsing sentence"
    return False

def parseFile(file):
  # this function parses a file
  file_name=os.path.basename(file)
  path_name=os.path.dirname(file)
  f=open(file,'r')
  print "File read"
  filetup = re.findall(r'(\w*).txt', file_name)
  csv_name=path_name+"/"+filetup[0]+'.csv'
  print "CSV path: %s"%csv_name
  with open(csv_name,'wb') as outcsv:
    print "CSV created"
    print "Start parsing"
    writer=csv.writer(outcsv)
    writer.writerow(['sent','tags','parse'])
    line_num=1
    for line in f:
      rows=parseSentence(line)
      if rows:
        for row in rows:
          writer.writerow(row)
      print "File %s line %d finished"%(file_name,line_num)
      line_num=line_num+1
  print "File finished %s"%csv_name



def mainWork(inFile):
  # Check the input. if it is a directory, then parse each file in the directory
  # if it is a directory, then it will browse all files in it
  if os.path.isfile(inFile):
    parseFile(inFile)
  else:
    print inFile
    f=[]
    for (dirpath, dirnames, filenames) in walk(inFile):
      f.extend(filenames)
      break
    f=filter(lambda x: x.endswith('.txt'),f)
    f=map(lambda x: inFile+'/'+x, f)
    pool=Pool(cpu_count())
    print "Start multi processing"
    start = timeit.default_timer()
    pool.map(parseFile,f)
    stop = timeit.default_timer()

    print stop - start 


inFile=sys.argv[1]
directory_list=[]
for root, dirs, files in walk(inFile):
  directory_list.extend(dirs)
  # Added this line so that if there are text files in the directory
  # then it will also be parsed directly
  # I have not run tthis code with this specific line, but should be fine       
  directory_list.exted(files)
  break
directory_list=map(lambda x: inFile+"/"+x, directory_list)
for dirs in directory_list:
  print "Start working in %s"%dirs
  mainWork(dirs)








