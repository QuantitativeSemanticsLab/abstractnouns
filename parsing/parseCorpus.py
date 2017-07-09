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
    ('properties', '{"annotators":"pos,lemma,ner,parse,openie, mention, coref", "coref.algorithm":"neural","outputFormat":"json",timeout:"900000"}'),
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
  nerList=[]
  for tags in pos_list:
    word=tags['word']
    index=str(tags['index'])
    lemma=tags['lemma']
    pos=tags['pos']
    ner=tags['ner']
    posList.append(word+'/'+lemma+'/'+pos)
    sentence.append(word)
    if ner!='O':
      # if ner=='DATE':
      #   # Since phrase like "mid of july" should be considered as time
      #   # together in stead of mid/time, of/time, july/time
      #   # the if loops here are to combine time phrases
      #   id=tags['timex']['tid']
      #   if id!=tid:
      #     if tid!=-1:
      #       # if we just had the first time fragment
      #       time=word
      #     else:
      #       # if we enconter another time fragment, we need to append the last one
      #       time+='/DATE'
      #       nerList.append(time)
      #       time=word

      #     tid=id
      #   else:
      #     # if the id matches the tid
      #     # that must means that a previous term has been added
      #     time+='-'+word
      # else:
      nerList.append(word+'/'+index+'/'+ner)

  return [' '.join(sentence),' '.join(posList), ' '.join(nerList)]



def parseOpenIE(openIEList):
  relationList=[]
  relation_index_list=[]
  for relation in openIEList:
    rel=relation['relation']
    obj=relation['object']
    sub=relation['subject']
    objSpan=relation['objectSpan']
    subSpan=relation['subjectSpan']
    relSpan=relation['relationSpan']

    relationList.append('('+rel+'('+sub+', '+obj+')'+')')
    relation_index_list.append("("+"-".join(str(x) for x in relSpan)+"("+"-".join(str(x) for x in subSpan)+", "+"-".join(str(x) for x in objSpan)+")")
  return [relationList, relation_index_list]




def parseSentence(sentence):
  # this function is to parse a sentence
  # so what I did is to send the sentence to local server
  # if you run the code I provided at the top,
  # then the port is 9000. You can of course 
  # use another one if port 9000 is busy
  rows=[]
  coref_rows=[]
  
  try: 
    # parsing to utf-8 is going to cause some problems in some lines
    # I have not done specific work to parse a single sentence each time
    # this is parsing a line in the text file
    # it is hard to tell where a sentence ends. It can be ?,.! or whatever
    # leave it to the stanford parser
    data=sentence.replace(u'\xa0', u' ').encode('utf-8')
    result= requests.post('http://localhost:9000/', params=params, data=data).content
    json_item = json.loads(result)
    for index, item in enumerate(json_item['sentences']):
      dep_list=item['enhancedPlusPlusDependencies']
      pos_list=item['tokens']
      openIE_list=item['openie']
      pos_result=parsePOS(pos_list)
      dependency_result=parseDependency(dep_list)
      openIE_result=parseOpenIE(openIE_list)
      rows.append([pos_result[0],pos_result[1]," ".join(dependency_result), pos_result[2], "; ".join(openIE_result[0]), "; ".join(openIE_result[1]), str(index+1)])
      # print " ".join(dependency_result)
    for group in json_item['corefs']:
      for refs in json_item['corefs'][group]:
        text=refs['text']
        representative=str(refs['isRepresentativeMention'])
        startIndex=str(refs['startIndex'])
        endIndex=str(refs['endIndex'])
        sentNum=str(refs['sentNum'])
        coref_rows.append([text, representative, startIndex, endIndex, sentNum])
    return [rows, coref_rows]

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
  coref_csv_name=path_name+"/"+filetup[0]+"_Coref"+'.csv'
  print "CSV path: %s"%csv_name
  with open(csv_name,'wb') as outcsv:
    print "CSV created"
    with open(coref_csv_name,'wb') as corcsv:
      print "Coreference CSV created"
      print "Start parsing"
      writer=csv.writer(outcsv)
      corwriter=csv.writer(corcsv)
      writer.writerow(['sent','tags','parse','ner','open IE','open IE index','sentence number', 'paragraph number'])
      corwriter.writerow(['text', 'is representative', 'start index', 'end index', 'sentence number', 'paragraph number'])
      line_num=1
      for line in f:
        result=parseSentence(line)
        if result:
          rows=result[0]
          coref_rows=result[1]
          for row in rows:
            row.append(str(line_num))
            writer.writerow(row)
          for row in coref_rows:
            row.append(str(line_num))
            corwriter.writerow(row)
        print "File %s line %d finished"%(file_name,line_num)
        line_num=line_num+1
  print "File Finished %s"%csv_name
  print "Coreference File Finished %s"%coref_csv_name



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
# mainWork(inFile)
directory_list=[]
for root, dirs, files in walk(inFile):
  directory_list.extend(dirs)
  # Added this line so that if there are text files in the directory
  # then it will also be parsed directly
  # I have not run tthis code with this specific line, but should be fine
  directory_list.extend(files)
  break
directory_list=map(lambda x: inFile+"/"+x, directory_list)
for dirs in directory_list:
  print "Start working in %s"%dirs
  mainWork(dirs)








