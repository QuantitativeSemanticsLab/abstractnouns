import re
import ast
d = {}
f = open("words.predicted","r")
for ln in f:
    l = re.findall(r"(.*)({.*})", ln)#[0].split("\t")
    word = l[0][0].split("\t")[0]
    vec = ast.literal_eval(l[0][1]).values()
    d[word]= vec
print d
if "kitten" in d:
    print "yay!"
if "meaningless" in d:
    print d["meaningless"]
