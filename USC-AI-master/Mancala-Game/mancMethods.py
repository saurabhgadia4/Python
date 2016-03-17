import mancParam as param

def get_node_name(playerId, pit_id):
    return param.PLAYER_LABEL[playerId] + str(pit_id+1)
 
def return_opposite_type(nodeType, return_list):
    if nodeType == param.MAX_NODE:
        return min(return_list);
    else:
        return max(return_list);

def return_same_type(nodeType, return_list):
    if nodeType == param.MAX_NODE:
        return max(return_list)
    else:
        return min(return_list)

def write_title(fobj, title):
    fobj.write(title)

def get_opponent_id(playId):
    #check whether removal makes changes in param.PLAYER_LIST
    if playId == param.PLAYER_ID1:
        return param.PLAYER_ID2
    else:
        return param.PLAYER_ID1

def alternate_type(nodeType):
    if nodeType == param.MAX_NODE:
        return param.MIN_NODE
    else:
        return param.MAX_NODE
        
def should_prune(alpha, beta):
    if beta > alpha:
        return False
    return True

def print_alphabeta(value):
    if value == param.PLUS_INFINITY:
        return param.NODE_TYPE_STR[param.MIN_NODE]
    elif value == param.MINUS_INFINITY:
        return param.NODE_TYPE_STR[param.MAX_NODE]
    else:
        return value
'''
 def return_alphabeta(returnValList, nodeType):
    if nodeType == param.MAX_NODE:
        return 
'''

def get_eval(nodeType, alpha, beta, isFreeturn):
    if not isFreeturn:
        if nodeType == param.MAX_NODE:
            return alpha
        else:
            return beta
    else:
        if nodeType == param.MAX_NODE:
            return beta
        else:
            return alpha

def intermediate_value(nodeType, isFreeturn):
    val = ''
    if isFreeturn:
        if nodeType == param.MAX_NODE:
            val = param.NODE_TYPE_STR[param.MIN_NODE]
        else:
            val = param.NODE_TYPE_STR[param.MAX_NODE]
    else:
        if nodeType == param.MAX_NODE:
            val = param.NODE_TYPE_STR[param.MAX_NODE]
        else:
            val = param.NODE_TYPE_STR[param.MIN_NODE]
    return val

def write_entry_log(fobj, method, nodeName, nodeType, max_depth, current_depth, isFreeturn, eval_val=None, alpha=None, beta=None, game_end=False):
    if game_end and current_depth==max_depth and not isFreeturn:
        return
    if (current_depth<max_depth):
        eval_val = intermediate_value(nodeType, isFreeturn)
    elif current_depth==max_depth and isFreeturn:
        eval_val = intermediate_value(nodeType, isFreeturn)


    # if current_depth == max_depth and game_end and not isFreeturn:
    #     fobj.write('continuing\n')
    #     return
    #if not ((max_depth == current_depth) and (not isFreeturn)):
    #    eval_val = intermediate_value(nodeType, isFreeturn)

    if method == param.TASK_OPTION['ALPHABETA']:
        str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(eval_val) + ',' + str(print_alphabeta(alpha)) + ',' + str(print_alphabeta(beta)) + '\n'
    elif method == param.TASK_OPTION['MINIMAX']:
        str_arr = str(nodeName) + ',' + str(current_depth) + ',' + str(eval_val) + '\n'
        #print str_arr
    #print 'nodeName', nodeName, 'current_depth', current_depth, 'eval_val', eval_val
    fobj.write(str_arr)

'''            
what to do on??
1. Endgame, lastdepth, freeturn  -->Do we need to print infinity or evaluate it 2 times
2. Endgame, lastdepth not freeturn
3. Endgame not lastdepth freeturn
4. Endgame not lastdepth not freeturn '''          