from optparse import OptionParser
import inferRule as Rule
import inferParam as param
import inferUtil as util

class Driver:
    def __init__(self, inputFile):
        self.file = inputFile
        self.fin = None
        self.linecount = 1
        self.queryCount = 0
        self.queries = []
        self.kbCount = 0
        self.KB = __builtins__.KB

    def run(self):
    	self.fin = open(self.file, 'r')
        self.fout = open('output.txt','w')
        self.queryCount = self.__getCount()
        self.__getQueries()
        self.kbCount = self.__getCount()
        self.__getKB()
        self.__inferQueries()
        self.fout.close()
        self.fin.close()
        

    def __inferQueries(self):
        for query in self.queries:
            q = Rule.Query(query)
            res = q.infer()
            #print res
            self.fout.write(res)

    def __getQueries(self):
        self.queries = []
        for i in range(self.queryCount):
            self.queries.append(self.fin.readline())

    def __getCount(self):
        self.linecount+=1
        return int(self.fin.readline())
    
    def __getKB(self):
        for i in range(self.kbCount):
            self.__processRule(self.fin.readline())

    def __processRule(self, rule):
        rule = rule.split('=>')
        #If rule is inference rule
        premise = ''
        if len(rule) == 2:
            premise = rule[0]
            ptype = param.PREDICATE_TYPE['PREMISE']
            conclusion = rule[1]
            ctype = param.PREDICATE_TYPE['CC']

        elif len(rule) == 1:
            premise = ''
            ptype = param.PREDICATE_TYPE['EMPTY']
            conclusion = rule[0]
            ctype = param.PREDICATE_TYPE['FACT']

        cobj = util.get_pred_object(conclusion, ctype)
        util.pop_premise_objList(premise, cobj)

    def printKB(self):
        facts = self.KB[param.PREDICATE_TYPE['FACT']]
        cc = self.KB[param.PREDICATE_TYPE['CC']]
        print 'Fact List-->'
        for key in facts:
            flist = facts[key]
            for fobj in flist:
                print fobj.printPredicate()

        print 'Inference Rule -->'
        for key in cc:
            flist = cc[key]
            for fobj in flist:
                print fobj.printPredicate()
                

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="Specify input file")
    (options, args) = parser.parse_args()
    __builtins__.KB = {
                                param.PREDICATE_TYPE['FACT']:{},
                                param.PREDICATE_TYPE['CC']:{}
                            }
    dobj = Driver(options.input)
    
    dobj.run()
    #dobj.printKB()