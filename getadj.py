import re
d = {}
f = open("words.predicted","r")
for ln in f:
    l = re.findall(r"(.*){", ln)[0].split("\t")
    d[l[0]]=l[1]
print d
if "kitten" in d:
    print "yay!"
if "meaningless" in d:
    print d["meaningless"]
