from optparse import OptionParser
import mancGame as game
import mancParam as param
class Driver:
    def __init__(self, inputFile):
        self.file = inputFile
        self.fobj = None
        self.linecount = 1
        self.methodId = 0
        self.player_turn = 0
        self.depth = 0
        self.pitsCount = 0
        self.players = {}
        
    def run(self):
        self.fobj = open(self.file, 'r')
        self.method = self.__getObjNum()
        self.player_turn = self.__getObjNum() #pl1->id=1, pl2->id=2
        self.depth = self.__getObjNum()
        
        #get player 2 state
        ply2_list = self.__getPitsDetails()
        
        #get player 1 state
        ply1_list = self.__getPitsDetails()
        
        #get player 2 mancala score
        ply2_score = self.__getObjNum()
        
        #get player 2 mancala score
        ply1_score = self.__getObjNum()
        
        #create player objects
        ply1 = game.GamePlayer(param.PLAYER_ID1, ply1_list, ply1_score)
        self.players[param.PLAYER_ID1] = ply1
        ply2 = game.GamePlayer(param.PLAYER_ID2, ply2_list, ply2_score)
        self.players[param.PLAYER_ID2] = ply2
        
        #create State object
        state = game.GameState(self.players)
        
        #play On
        gameObj = game.Game(state, self.method, self.player_turn, self.depth, self.pitsCount)
        gameObj.play();
        self.fobj.close()
        
        
    def __getObjNum(self):
        line = self.fobj.readline()
        self.linecount+=1
        return int(line.split()[0])
    
    #returns the dictionary of pitlists
    def __getPitsDetails(self):
        line = self.fobj.readline()
        self.linecount+=1
        pits = line.split()
        self.pitsCount = len(pits)
        pit_list = {}
        for i in range(self.pitsCount):
            pit_list[i+1] = (int(pits[i]))
        return pit_list 

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="Specify input file")
    (options, args) = parser.parse_args()
    dobj = Driver(options.input)
    dobj.run()