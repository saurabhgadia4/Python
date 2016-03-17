import mancParam as param
import copy
import mancMethods as method
import os

class Game:
    def __init__(self, state, method, player_turn, depth, totalPits):
        self.currentState = state
        self.method = method
        self.playTurn = player_turn
        self.totalPits = totalPits
        self.maxDepth = depth
        self.nsfobj = None
        self.tlfobj = None
        self.__create_fobj()

    def __create_fobj(self):
        try:
            os.remove(param.NEXT_STATE_FILE_NAME)
            #print 'successfully removed next state file'
        except Exception:
            pass

        try:
            os.remove(param.TRAVERSE_LOG_NAME)
            #print 'successfully removed traverse log'
        except Exception:
            pass    
        
        self.nsfobj = open(param.NEXT_STATE_FILE_NAME,'w')
        if self.method >1:
            self.tlfobj = open(param.TRAVERSE_LOG_NAME,'w')
        else:
            self.tlfobj = None
        self.__write_title()

    def __write_title(self):
        if self.method == param.TASK_OPTION['MINIMAX']:
            self.tlfobj.write(param.TRAV_MINIMAX_TITLE)
        elif self.method == param.TASK_OPTION['ALPHABETA']:
            self.tlfobj.write(param.TRAV_ALPHABETA_TITLE)

    def __write_state(self, stateObj):
        line = self.__output_pits_state(stateObj, param.PLAYER_ID2)
        #print line + 'end'
        self.nsfobj.write(line + '\n')
        line = self.__output_pits_state(stateObj, param.PLAYER_ID1)
        #print line + 'end'
        self.nsfobj.write(line + '\n')
        self.__output_score(stateObj, param.PLAYER_ID2)
        self.__output_score(stateObj, param.PLAYER_ID1)
        self.__close_files()

    def __close_files(self):
        if self.nsfobj:
            self.nsfobj.close()
        if self.tlfobj:
            self.tlfobj.close()

    def play(self):
        stateObj = self.call_method(self.currentState, self.playTurn)
        #print '\nnew state selected\n'
        #stateObj.print_info()
        #print output state
        self.__write_state(stateObj)
        
    def __output_score(self, state, playerId):
        score = state.players[playerId].score
        line = str(score) + '\n'
        self.nsfobj.write(line)
        
        
    def __output_pits_state(self, state, playerId):
        line = ''
        pitsDict = state.players[playerId].pitsList
        pitsKeyList = sorted(pitsDict)
        for key in pitsKeyList:
            line=line+str(pitsDict[key]) + ' '
        line = line.strip()
        # print 'stripping:', line+end
        # print 'board state - player id:', playerId, ' :',line
        return line
        
    
    def call_method(self, stateObj, play_turn, nodeName=None):
        valid_pits_list = stateObj.players[play_turn].get_valid_list()
        newState = None
        if self.method == param.TASK_OPTION['GREEDY']:
            newState = self.nxtGreedyMv(stateObj, valid_pits_list)
        elif self.method == param.TASK_OPTION['MINIMAX']:
            if nodeName == None:
                nodeName = 'root'
            score, newState = self.nxtMnmxMv(nodeName, stateObj, param.MAX_NODE, 0, valid_pits_list, play_turn)
            
        elif self.method == param.TASK_OPTION['ALPHABETA']:
            if nodeName == None:
                nodeName = 'root'
            score, newState, is_pruned = self.nxtABMv(nodeName, stateObj, param.MAX_NODE, 0, valid_pits_list, play_turn, param.MINUS_INFINITY, param.PLUS_INFINITY)
        else:
            return None, None
        return newState
    
    def nextState(self, stateObj, play_turn, pitid):    
        total_pits = self.totalPits
        (free_turn, next_pit_id, playerId, pl_list, pl_score) = self.distribute(stateObj, play_turn, pitid)
            
        if not free_turn:
            #check if the last updated pit has count == 1
            if next_pit_id == 0:
                if playerId ==1:
                    last_filled_pit = total_pits
                elif playerId ==2:
                    last_filled_pit = 1
            else:
                if playerId == 1:
                    last_filled_pit = next_pit_id -1
                elif playerId == 2:
                    last_filled_pit = next_pit_id + 1
        
            #Now check if last update was in same half and count ==1
            valid_players = [1,2]
            if playerId == play_turn:
                real_id = playerId
                valid_players.remove(real_id)
                opp_id = valid_players[0]
                if pl_list[real_id][last_filled_pit] == 1:
                    pl_score[real_id]= pl_score[real_id] + pl_list[opp_id][last_filled_pit] + 1
                    pl_list[opp_id][last_filled_pit] = 0
                    pl_list[real_id][last_filled_pit] = 0

        #Now check for end game condition
        is_player1_empty = pl_list[param.PLAYER_ID1] 
        pl_list, pl_score, is_empty = self.__check_board_empty(pl_list, pl_score) 

                    
        #create new pseudostate and recur
        #1. Create Player objects
        pl1 = GamePlayer(param.PLAYER_ID1, pl_list[param.PLAYER_ID1], pl_score[param.PLAYER_ID1])
        pl2 = GamePlayer(param.PLAYER_ID2, pl_list[param.PLAYER_ID2], pl_score[param.PLAYER_ID2])
        players = {}
        players[param.PLAYER_ID1] = pl1
        players[param.PLAYER_ID2] = pl2
        pseudoState = GameState(players)
        if free_turn and (self.method ==  param.TASK_OPTION['MINIMAX'] or self.method ==  param.TASK_OPTION['ALPHABETA']):
            pseudoState.freeTurn = True
            
            
        if free_turn and self.method ==  param.TASK_OPTION['GREEDY'] and (not is_empty):
            #print 'free turn'
            #pseudoState.print_info()
            pseudoState = self.call_method(pseudoState, play_turn)
            #print 'state after free turn'
            #pseudoState.print_info()
            return pseudoState
        return pseudoState
    
    #it will check for whether any side of board is empty. If it is empty it will update the score and pl_list
    def __check_board_empty(self, pl_list, pl_score):
        pid1 = param.PLAYER_ID1
        pid2 = param.PLAYER_ID2
        is_empty = False
        pl_empty = {}
        pl_empty[pid1] = True
        pl_empty[pid2] = True
        for pid in pl_empty:
            for key in pl_list[pid]:
                if pl_list[pid][key]!=0:
                    pl_empty[pid] = False
                    break

        if pl_empty[pid1]:
            #empty pl_list[pid2]
            is_empty = True
            for key in pl_list[pid2]:
                pl_score[pid2] += pl_list[pid2][key]
                pl_list[pid2][key] = 0

        if pl_empty[pid2]:
            #empty pl_list[pid2]
            is_empty = True
            for key in pl_list[pid1]:
                pl_score[pid1] += pl_list[pid1][key]
                pl_list[pid1][key] = 0
                 
        return pl_list, pl_score, is_empty

        
    def nxtGreedyMv(self, stateObj, valid_pits_list):
        next_pstate = {}
        #get only valid moves
        for pit_id in valid_pits_list:
            #print 'greedy pit_id:', pit_id
            next_pstate[pit_id] = self.nextState(stateObj, self.playTurn, pit_id)
        #print '\noriginal state before evaluating'
        #stateObj.print_info()
        pit_id = self.batch_evaluate(next_pstate)
        #print 'pit selcted by greedy',pit_id
        #next_pstate[pit_id].print_info()
        return next_pstate[pit_id] 
    
    def batch_evaluate(self, stateList):
        #print 'stateList', stateList
        if self.playTurn == param.PLAYER_ID1:
            keyList = sorted(stateList)
        else:
            keyList = sorted(stateList, reverse=True)
        max_val = 0
        max_pid = 0
        for key in keyList:
            #print '\nbatch evaluating key:',key
            #stateList[key].print_info()
            score = self.evaluate(self.playTurn, stateList[key])
            if score > max_val:
                max_val = score
                max_pid = key
        if max_pid == 0:
            max_pid = keyList[0]
        return max_pid
    
    #1. If free turn then
           #case 1.a: if node_type == Min then return Max
           #case 1.b: if node_type == Max then return Min
        #2. If not free turn then
            #case 2.a: if node_type == Min then return Min
            #case 2.b: if node_type == Max then return Max
        #print '\n\nNodename:',nodeName, 'valid list:', valid_pits_list, 'current_depth',current_depth,'freeTurn',currentState.freeTurn, \
                #'play_turn',play_turn
    
    def nxtMnmxMv(self, nodeName, currentState, nodeType, current_depth, valid_pits_list, play_turn):
        #print nodeName, currentState.print_info()
        returnValList = []
        returnStateList = []
        currentState.depth = current_depth
        eval_val = self.evaluate(self.playTurn, currentState)
        ret_val = eval_val
        ret_state = currentState
        game_end = False
        if not valid_pits_list:
            game_end = True
            #self.tlfobj.write('endgame\n')
        '''        
        if current_depth ==self.maxDepth and currentState.freeTurn:
            self.tlfobj.write('last depth and freeturn\n')
        elif current_depth==self.maxDepth and not currentState.freeTurn:
            self.tlfobj.write('last depth and not freeturn\n')
        elif current_depth<self.maxDepth and currentState.freeTurn:
            self.tlfobj.write('intr depth and freeturn\n')
        elif current_depth<self.maxDepth and not currentState.freeTurn:
            self.tlfobj.write('intr depth and not freeturn\n')
        '''        
        method.write_entry_log(self.tlfobj, param.TASK_OPTION['MINIMAX'], nodeName, nodeType, self.maxDepth, current_depth, currentState.freeTurn, eval_val, alpha=None, beta=None, game_end = game_end)
        if not valid_pits_list:
            #self.tlfobj.write('gameend\n')
            return eval_val, currentState
        if current_depth == self.maxDepth:
            if not currentState.freeTurn:
                return eval_val, currentState
            else:
                for pit_id in valid_pits_list:
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    child_valid_pits_list = []
                    next_depth = current_depth
                    #if child_state.freeTurn:
                        #calculate the valid_pits_list for the child
                    child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), \
                        child_state, nodeType, next_depth, child_valid_pits_list, play_turn)

                    if not child_valid_pits_list:
                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        #print the state
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + '\n'
                        #self.tlfobj.write('freeturn\n')
                        #method.write_entry_log(self.tlfobj, param.TASK_OPTION['MINIMAX'], nodeName, nodeType, self.maxDepth, current_depth, currentState.freeTurn, eval_val, alpha=None, beta=None)
                        self.tlfobj.write(str_arr)

                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    #print nodeName, ',',current_depth, ',', method.return_opposite_type(nodeType, returnValList)
                    #printing opposite because its freeturn
                    str_arr = str(nodeName) + ',' + str(current_depth) +','+ str(method.return_opposite_type(nodeType, returnValList)) + '\n'
                    #print str_arr
                    self.tlfobj.write(str_arr)

                #if not returnValList:
                #    returnValList.append(ret_val)
                #    returnStateList.append(currentState)
                ret_val = method.return_opposite_type(nodeType, returnValList)
                idx = returnValList.index(ret_val) 
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
        
        else:
        
            if currentState.freeTurn:
                #it will pass same nodetype, depth to child
                #valid pit list should from the same play_turn as it will now be extended
                for pit_id in valid_pits_list:
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                    next_depth = current_depth
                    next_node_type = nodeType
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
  
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn

                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), child_state, next_node_type,\
                                next_depth, child_valid_pits_list, next_play_turn)

                    if not child_valid_pits_list:
                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        #print the state
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + '\n'
                        #self.tlfobj.write('freeturn\n')
                        #method.write_entry_log(self.tlfobj, param.TASK_OPTION['MINIMAX'], nodeName, nodeType, self.maxDepth, current_depth, currentState.freeTurn, eval_val, alpha=None, beta=None)
                        self.tlfobj.write(str_arr)
                    #else:    
                        # val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), child_state, next_node_type,\
                        #         next_depth, child_valid_pits_list, next_play_turn)
                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    str_arr = str(nodeName) + ',' + str(current_depth) +','+ str(method.return_opposite_type(nodeType, returnValList)) + '\n'
                    #print str_arr
                    self.tlfobj.write(str_arr)

                ret_val = method.return_opposite_type(nodeType, returnValList)
                idx = returnValList.index(ret_val)
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
                
            else:
                #valid_pits_list should be the opponents valid pit list
                for pit_id in valid_pits_list:
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #print 'child_state\n',child_state.print_info()
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
                        next_depth = current_depth+1
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn
                        next_depth = current_depth+1

                    val, ret_state = self.nxtMnmxMv(method.get_node_name(play_turn, pit_id), child_state, method.alternate_type(nodeType),\
                                 next_depth, child_valid_pits_list, next_play_turn)
                    if not child_valid_pits_list:

                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        #method.write_entry_log(self.tlfobj, param.TASK_OPTION['MINIMAX'], nodeName, nodeType, self.maxDepth, next_depth, child_state.freeTurn, eval_val, alpha=None, beta=None, game_end = True)
                        #print the state
                        #print 'check'
                        #self.tlfobj.write('game-end\n')
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + '\n'
                        self.tlfobj.write(str_arr)
                    #else:
                        
                    returnValList.append(val)
                    returnStateList.append(ret_state)
                    str_arr = str(nodeName) + ',' + str(current_depth) +','+ str(method.return_same_type(nodeType, returnValList)) + '\n'
                    #print str_arr
                    self.tlfobj.write(str_arr)

                ret_val = method.return_same_type(nodeType, returnValList)
                idx = returnValList.index(ret_val)
                if (returnStateList[idx].depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                else:
                    ret_state = returnStateList[idx]
                return ret_val,ret_state
        
    def nxtABMv(self, nodeName, currentState, nodeType, current_depth, valid_pits_list, play_turn, alpha, beta):
        returnValList = []
        returnStateList = []
        currentState.depth = current_depth
        global_ret_state = currentState
        eval_val = self.evaluate(self.playTurn, currentState)
        game_end = False
        if not valid_pits_list:
            game_end = True
            #self.tlfobj.write('endgame\n')
        '''
        if current_depth ==self.maxDepth and currentState.freeTurn:
            self.tlfobj.write('last depth and freeturn\n')
        elif current_depth==self.maxDepth and not currentState.freeTurn:
            self.tlfobj.write('last depth and not freeturn\n')
        elif current_depth<self.maxDepth and currentState.freeTurn:
            self.tlfobj.write('intr depth and freeturn\n')
        elif current_depth<self.maxDepth and not currentState.freeTurn:
            self.tlfobj.write('intr depth and not freeturn\n')'''
        

        method.write_entry_log(self.tlfobj, param.TASK_OPTION['ALPHABETA'], nodeName, nodeType, self.maxDepth, current_depth, currentState.freeTurn, eval_val, alpha, beta, game_end)
        if not valid_pits_list:
            #self.tlfobj.write('gameend\n')
            return eval_val, currentState, param.NOT_PRUNED
        if current_depth == self.maxDepth:
            # as lst depth evaluate and print
            if not currentState.freeTurn:
                return eval_val, currentState, param.NOT_PRUNED
            else:
                if nodeType == param.MAX_NODE:
                    v = param.PLUS_INFINITY
                else:
                    v = param.MINUS_INFINITY

                for pit_id in valid_pits_list:
                    alpha_update_pending = False
                    beta_update_pending = False
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    child_valid_pits_list = []
                    next_depth = current_depth
                    #if child_state.freeTurn:
                        #calculate the valid_pits_list for the child
                    child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                            
                    val, ret_child_state, is_pruned = self.nxtABMv(method.get_node_name(play_turn, pit_id), child_state, nodeType, \
                                                        next_depth, child_valid_pits_list, play_turn, alpha, beta)
                    
                    if nodeType == param.MAX_NODE:
                        #v = min(v, val)  #as freeturn doing opposite
                        if val < v:
                            v = val
                            ret_state = ret_child_state
                    else:
                        #v = max(v, val)
                        if val > v:
                            v = val
                            ret_state = ret_child_state

                    if not child_valid_pits_list:
                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        #print the state
                        #check for alpha beta values
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + ','+ str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        #self.tlfobj.write('freeturn\n')
                        #method.write_entry_log(self.tlfobj, param.TASK_OPTION['MINIMAX'], nodeName, nodeType, self.maxDepth, current_depth, currentState.freeTurn, eval_val, alpha=None, beta=None)
                        self.tlfobj.write(str_arr)

                    #check for pruning!!
                    if nodeType == param.MAX_NODE:
                            #as it is free turn we will update its beta value
                        prune_needed = method.should_prune(alpha, v)
                        beta_update_pending = True
                    else:
                        prune_needed = method.should_prune(v, beta)
                        alpha_update_pending = True
                    
                    if prune_needed:
                        str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        self.tlfobj.write(str_arr)
                        if alpha_update_pending:
                            alpha = v
                        else:
                            beta = v
                        return method.get_eval(nodeType, alpha, beta, currentState.freeTurn), None, param.PRUNED
                    else:                                                                          
                        if nodeType == param.MAX_NODE:
                            # buts its a freeturn so update beta
                            if beta > v:
                                beta = v
                                global_ret_state = ret_state
                        else:
                            if alpha < v:
                                alpha = v
                                global_ret_state = ret_state   

                    str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                    self.tlfobj.write(str_arr)
                #If code reaches here then we will return the correct value
                ret_state = global_ret_state
                if (global_ret_state.depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                elif (global_ret_state == currentState) and currentState.depth!=0:
                    ret_state = currentState
                return v, ret_state, param.NOT_PRUNED
                     
        #if it is a intermediatory node
        else:
            
            if currentState.freeTurn:
                #print 'inter free turn'
                if nodeType == param.MAX_NODE:
                    v = param.PLUS_INFINITY
                else:
                    v = param.MINUS_INFINITY
                
                for pit_id in valid_pits_list:
                    alpha_update_pending = False
                    beta_update_pending = False
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                    next_depth = current_depth
                    next_node_type = nodeType
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
  
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn

                    val, ret_child_state, is_pruned = self.nxtABMv(method.get_node_name(play_turn, pit_id), child_state, next_node_type,\
                                next_depth, child_valid_pits_list, next_play_turn, alpha, beta)
                    
                    #self.tlfobj.write('value got '+str(val)+'\n')
                    if nodeType == param.MAX_NODE:
                        #v = min(v, val)  #as freeturn doing opposite
                        if val < v:
                            v = val
                            ret_state = ret_child_state
                    else:
                        #v = max(v, val)
                        if val > v:
                            v = val
                            ret_state = ret_child_state

                    #self.tlfobj.write('value chosen '+str(v)+'\n')
                    if not child_valid_pits_list:
                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        is_pruned = False
                        #print the state
                        #str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + '\n'
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        self.tlfobj.write(str_arr)
                    
                    #check for pruning!!
                    if nodeType == param.MAX_NODE:
                            #as it is free turn we will update its beta value
                        prune_needed = method.should_prune(alpha, v)
                        beta_update_pending = True
                    else:
                        prune_needed = method.should_prune(v, beta)
                        alpha_update_pending = True
                    
                    if prune_needed:
                        #print nodeName, ',', current_depth, ',', val, ',',method.print_alphabeta(alpha),',', method.print_alphabeta(beta)
                        str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        self.tlfobj.write(str_arr)
                        if alpha_update_pending:
                            alpha = v
                        else:
                            beta = v
                        return method.get_eval(nodeType, alpha, beta, currentState.freeTurn), None, param.PRUNED
                    
                    else:                                                                          
                        if nodeType == param.MAX_NODE:
                            # buts its a freeturn so update beta
                            if beta > v:
                                beta = v
                                global_ret_state = ret_state
                        else:
                            if alpha < v:
                                alpha = v
                                global_ret_state = ret_state                       
                    #print nodeName, ',', current_depth, ',', method.print_alphabeta(method.get_eval(nodeType, alpha, beta, currentState.freeTurn)), ',',method.print_alphabeta(alpha),',', method.print_alphabeta(beta)
                    str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                    self.tlfobj.write(str_arr)
                    
                ret_state = global_ret_state
                if (global_ret_state.depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                elif (global_ret_state == currentState) and currentState.depth!=0:
                    ret_state = currentState
                return v, ret_state, param.NOT_PRUNED    
                    
            
            else:
                if nodeType == param.MAX_NODE:
                    v = param.MINUS_INFINITY
                else:
                    v = param.PLUS_INFINITY

                for pit_id in valid_pits_list:
                    alpha_update_pending = False
                    beta_update_pending = False
                    opponent_turn = method.get_opponent_id(play_turn)
                    child_state = self.nextState(currentState, play_turn, pit_id)
                    #print 'child_state\n',child_state.print_info()
                    if child_state.freeTurn:
                        child_valid_pits_list = child_state.players[play_turn].get_valid_list()
                        next_play_turn = play_turn
                        next_depth = current_depth+1
                    else:
                        child_valid_pits_list = child_state.players[opponent_turn].get_valid_list()
                        next_play_turn = opponent_turn
                        next_depth = current_depth+1


                    val, ret_child_state, is_pruned = self.nxtABMv(method.get_node_name(play_turn, pit_id), child_state, method.alternate_type(nodeType),\
                                next_depth, child_valid_pits_list, next_play_turn, alpha, beta)
                    
                    if nodeType == param.MAX_NODE:
                        #v = max(v, val)
                        if val> v:
                            v = val
                            ret_state = ret_child_state
                    else:
                        #v = min(v, val)
                        if val<v:
                            v = val
                            ret_state = ret_child_state 

                    if not child_valid_pits_list:
                        val = self.evaluate(self.playTurn, child_state)
                        ret_state = child_state
                        is_pruned = False
                        #print the state
                        #str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + '\n'
                        str_arr = str(method.get_node_name(play_turn, pit_id)) + ',' + str(next_depth) + ',' + str(val) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        self.tlfobj.write(str_arr)

                    
                    if nodeType == param.MAX_NODE:
                            #as it is not free turn we will update its alpha value
                        prune_needed = method.should_prune(v, beta)
                        alpha_update_pending = True
                    else:
                        prune_needed = method.should_prune(alpha, v)
                        beta_update_pending = True
                    
                    if prune_needed:
                        #print nodeName, ',', current_depth, ',', val, ',',method.print_alphabeta(alpha),',', method.print_alphabeta(beta)
                        str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                        self.tlfobj.write(str_arr)
                        if alpha_update_pending:
                            alpha = v
                        else:
                            beta = v
                        return method.get_eval(nodeType, alpha, beta, currentState.freeTurn), None, param.PRUNED
                    else:                                                                          
                        if nodeType == param.MAX_NODE:
                            # buts it is not a freeturn so update beta
                            #self.tlfobj.write(str(val) + 'updating alpha\n')
                            if alpha < v:
                                #self.tlfobj.write('updated')
                                alpha = v
                                global_ret_state = ret_state
                        else:
                            #self.tlfobj.write(str(val) + 'updating beta\n')
                            if beta > v:
                            #    self.tlfobj.write('updated')
                                beta = v                     
                                global_ret_state = ret_state
                    #print nodeName, ',', current_depth, ',', method.print_alphabeta(method.get_eval(nodeType, alpha, beta, currentState.freeTurn)), ',',method.print_alphabeta(alpha),',', method.print_alphabeta(beta)
                    str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(v) + ',' + str(method.print_alphabeta(alpha)) + ',' + str(method.print_alphabeta(beta)) + '\n'
                    self.tlfobj.write(str_arr)

                # after visiting all child and no pruning done
                ret_state = global_ret_state
                if (global_ret_state.depth > currentState.depth) and currentState.depth!=0:
                    ret_state = currentState
                elif (global_ret_state == currentState) and currentState.depth!=0:
                    ret_state = currentState
                #return method.get_eval(nodeType, alpha, beta, currentState.freeTurn), ret_state, param.NOT_PRUNED
                return v, ret_state, param.NOT_PRUNED
            
    
    def print_state(self):
        self.currentState.print_info()
    
    #for 2 player game it will be playerId - other_playerId
    def evaluate(self, plyId, pseudoStateObj):
        players = pseudoStateObj.players
        valid_players = [1,2]
        valid_players.remove(plyId)
        othrPlyId = valid_players[0]
        return players[plyId].score - players[othrPlyId].score
    
    def distribute(self, pseudoState, play_turn, pitid):
        pl_list = {}
        pl_score = {}
        free_turn = False
        totalPits = self.totalPits + 1
        pl_list[param.PLAYER_ID1] = copy.deepcopy(pseudoState.players[param.PLAYER_ID1].pitsList)
        pl_score[param.PLAYER_ID1] = pseudoState.players[param.PLAYER_ID1].score        
        pl_list[param.PLAYER_ID2] = copy.deepcopy(pseudoState.players[param.PLAYER_ID2].pitsList)
        pl_score[param.PLAYER_ID2] = pseudoState.players[param.PLAYER_ID2].score
        
        if play_turn == 1:
            step = 1
            playerId = 1
        elif play_turn == 2:
            step = -1
            playerId = 2
        
        stone_count = pl_list[play_turn][pitid]
        #print 'pitid ',pitid, ' stones:',stone_count
        
        #emptying the stones from selected pitid
        pl_list[play_turn][pitid] = 0
        next_pit_id = (pitid + step) % totalPits 
        while stone_count!=0:
            free_turn = False
            while next_pit_id!=0 and stone_count!=0:
                pl_list[playerId][next_pit_id]+=1
                stone_count-=1
                next_pit_id = (next_pit_id + step) % totalPits
            if stone_count==0:
                break
            else:
                if playerId == play_turn:
                    pl_score[play_turn]+=1
                    stone_count-=1
                    free_turn = True
                if playerId == param.PLAYER_ID2:
                    next_pit_id = 1
                    playerId = 1
                    step = 1
                else:
                    next_pit_id = totalPits -1
                    playerId = 2
                    step = -1
        return (free_turn, next_pit_id, playerId, pl_list, pl_score) 
    
    def get_pits_valid_state(self, stateObj, play_turn):
        player = stateObj.players[play_turn]
        return player.get_valid_list()
        
class GameState:
    def __init__(self, players):
        self.players = players  #dictionary for holding player objects against their ID
        self.freeTurn = False #indicates whether we have to continue playing 
        self.depth = None
        
    def print_info(self):
        for pid in sorted(self.players,reverse=True):
            self.players[pid].print_info() 
    
class GamePlayer:
    def __init__(self, id, pitsList, score):
        self.id = id
        self.pitsList = pitsList
        self.score = score
        self.pitsCount = len(pitsList)
    
    def hasValidMoves(self):
        return len(self.get_valid_list()) == 0
        
    def get_valid_list(self):
        valid = []
        for i in range(self.pitsCount):
            if self.pitsList[i+1]!=0:
                valid.append(i+1)
        return valid
    
    def print_info(self):
        #print 'Player Id:', self.id
        print 'score', self.score
        #print 'pits count', len(self.pitsList)
        print 'Player Id:', self.id, 'pitlist:', self.pitsList
