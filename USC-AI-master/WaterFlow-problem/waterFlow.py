from optparse import OptionParser
import flowParam as param
import graph

class Driver:
    def __init__(self, inputFile):
        self.file = inputFile
        self.fobj = None
        self.totalTest = 0
        self.method = None
        self.graph = None
        self.nodes = {}
        self.fout = None
        self.linecount = 1

    def run(self):
        ##print 'input file',self.file
        self.fobj = open(self.file, "r")
        self.fout = open('output.txt','w')
        self.totalTest = self.__getCount()
        for i in range(self.totalTest):
            #print 'TestCase: ',i+1, ' Line:',self.linecount
            self.nodes = {}
            self.__getMethod()
            startNode = self.__getStartNode()
            dstList = self.__getNodeList()
            mnodeList = self.__getNodeList()

            numEdges = self.__getCount()
            ##print 'numedges',numEdges
            edges = {}
            for j in range(numEdges):
                edge = self.__getEdge()
                if not edges.get(edge.startNode.label, None):
                    edges[edge.startNode.label] = {} 
                edges[edge.startNode.label][edge.endNode.label] = edge
            ##print 'Edges',edges
            start_time = self.__getCount()
            self.graph = graph.Graph(startNode, dstList, mnodeList, numEdges, edges, start_time, self.fout,i+1)
            self.graph.run(self.method)
            self.fobj.readline()
            self.linecount+=1
        self.fout.close()
        self.fobj.close()

    def __getEdge(self):
        line = self.fobj.readline()
        self.linecount+=1
        pipe_info = line.split()
        start = pipe_info[param.EDGE_INPUT['SRC']]
        ##print 'start-e',start
        dst = pipe_info[param.EDGE_INPUT['DST']]
        ##print 'dst-e',dst
        wt = int(pipe_info[param.EDGE_INPUT['WT']])
        off_period = int(pipe_info[param.EDGE_INPUT['NOFF']])
        j = param.EDGE_INPUT['NOFF']+1
        off_list = []
        for i in range(off_period):
            off_list.append(pipe_info[j+i])
        return graph.Edge(self.nodes[start], self.nodes[dst], wt, off_period, off_list)


    def __getNodeList(self):
        line = self.fobj.readline()
        self.linecount+=1
        nlist = line.split()
        ##print 'nlist',nlist
        nobjList = []
        for node in nlist:
            if not self.nodes.get(node, None):
                self.nodes[node] = graph.Node(node)
                nobjList.append(self.nodes[node])
        return nobjList

    def __getStartNode(self):
        line = self.fobj.readline()
        self.linecount+=1
        node = line.split()[0]
        ##print 'start node',node
        if not self.nodes.get(node, None):
            self.nodes[node] = graph.Node(node)
        return self.nodes[node]
        
    def __getCount(self):
        line = self.fobj.readline()
        self.linecount+=1
        return int(line.split()[0])

    def __getMethod(self):
        line = self.fobj.readline()
        self.linecount+=1
        self.method = param.SEARCH_METHOD[line.split()[0]]

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="Specify input file")
    (options, args) = parser.parse_args()
    dobj = Driver(options.input)
    dobj.run()
