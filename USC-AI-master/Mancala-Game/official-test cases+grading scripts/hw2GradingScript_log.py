#Siddharth Jain
#Grading script to compare traverse log

import sys

f = open(sys.argv[1])
g = open(sys.argv[2])

desiredLines = []
actualLines = []

for line in f:
    desiredLines.append(line.strip())
f.close()

for line in g:
    actualLines.append(line.strip())
g.close()

incorrect = 0
total = len(desiredLines)
n = len(actualLines)
i = 0
j = 0
while i<total:
    d = desiredLines[i].split(',')
    if j==len(actualLines):
        print "Incorrect format of log file."
        incorrect = 1
        break
    a = actualLines[j].split(',')
    if len(a)<3:
        print "Incorrect format of log file."
        incorrect = 1
        break

    optional = False
    if "OPTIONAL" in d[-1]:
        optional = True

    if optional==True:
        if "Infinity" in a[2]:
            i += 1
            j += 1
            continue
        else:
            i += 1
            d = desiredLines[i].split(',')
    
    for k in range(len(d)):
        if k==len(a) or d[k]!=a[k]:
            print "Log incorrect at line-"+str(i+1)+" of standard file that corresponds to line-"+str(j+1)+" of student file."
            incorrect = 1
            break
    
    if incorrect==1:
	break

    i += 1
    j += 1

if incorrect==0:
    print "Correct log."
else:
    print "Incorrect log."
