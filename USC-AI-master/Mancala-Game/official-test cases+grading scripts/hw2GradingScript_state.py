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

if len(actualLines)<4:
    print "Incorrect format of board state for input file."
    incorrect = 1
else:
    d = desiredLines[0].split()
    a = actualLines[0].split()
    for i in range(len(d)):
        if d[i]!=a[i]:
            incorrect = 1
            print "Incorrect state for Player-2 board."
            break

    d = desiredLines[1].split()
    a = actualLines[1].split()
    for i in range(len(d)):
        if d[i]!=a[i]:
            incorrect = 1
            print "Incorrect state for Player-1 board."
            break

    if desiredLines[2]!=actualLines[2]:
        print "Incorrect number of stones in Player-2's mancala."
        incorrect = 1
    
    if desiredLines[3]!=actualLines[3]:
        print "Incorrect number of stones in Player-1's mancala."
        incorrect = 1

if incorrect==0:
    print "Correct state."
else:
    print "Incorrect state."
