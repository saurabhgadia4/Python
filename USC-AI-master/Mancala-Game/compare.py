from optparse import OptionParser
class Compare:
    def __init__(self, source, target):
        self.sfobj = open(source,'r')
        self.tfobj = open(target, 'r')
        self.source = source
        self.target = target

    def match_files(self):
        pass_count = 0
        total_count = 0
        fail_count=0
        pass_tests = []
        fail_tests = []
        loop=1
        while loop:
            l1 = self.sfobj.readline()
            l2 = self.tfobj.readline()
            if l1 == '':
                loop = 0
                break
            total_count+=1
            # print 'l1',l1
            # print 'l2',l2
            if l1==l2:
                pass_count+=1
                pass_tests.append(total_count)
            else:
                fail_count+=1
                fail_tests.append(total_count)

        print 'total_Count',total_count,'pass Count:',pass_count,'fail_count',fail_count
        print 'pass testcases',pass_tests
        print 'fail testcases',fail_tests

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-s", "--src",action="store", type="string", dest="source", help="Specify source input file")
    parser.add_option("-t", "--dst",action="store", type="string", dest="target", help="Specify target input file")
    (options, args) = parser.parse_args()
    dobj = Compare(options.source, options.target)
    dobj.match_files()