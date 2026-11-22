from board import HUMAN, AGENT
from tree_node import Node
from heuristic import evaluate


# hena han handle el agent


INF = 100000000

nodes = 0

def get_nodes():
    # Other files read the counter through this function
    return nodes


#Nasi7a, lw hanakhod K kebera aw bn7sb time, TURN THESE OFF!
build_tree = False
tree_root = None


def set_tree_building(on):
    global build_tree
    build_tree = on


def get_tree():
    #Hatrg3le None lw ana mesh 3yza el tree t build
    return tree_root


def make_root(node_type): # Called by the choose_move functions at the start of a turn

    global tree_root
    if build_tree:
        tree_root = Node(None, node_type)
    else:
        tree_root = None
    return tree_root


def mark_pruned(parent, board, col, node_type):

    if parent is None:
        return
    valid = board.valid_columns()
    for c in valid[valid.index(col) + 1:]:
        skipped = make_child(parent, c, node_type)
        skipped.ispruned = True


def make_child(parent, col, node_type, prob=None):
    if parent is None:
        return None
    child = Node(None, node_type)
    child.move = col
    parent.add_child(child, prob)
    return child


def minimax(board, depth, is_agent_turn, node=None):
    global nodes
    nodes = nodes + 1   # count this node
    if board.is_full() or depth == 0:
        value = evaluate(board)
        if node is not None:
            node.value = value      # leaf: the heuristic value
        return value

    if is_agent_turn:
       
        best = -INF #el alpha btkon negative infinity
        for col in board.valid_columns(): #hena m3ana el valid coloumns
            child = board.copy()                 
            child.drop(col, AGENT)
            child_node = make_child(node, col, "min")   # next level is the human's
            value = minimax(child, depth - 1, False, child_node)   
            if value > best:
                best = value
        if node is not None:
            node.value = best
        return best #maximum woooo
    else:
        best = INF #Beta btkon infinity
        for col in board.valid_columns():
            child = board.copy()
            child.drop(col, HUMAN)
            child_node = make_child(node, col, "max")   # next level is the agent's
            value = minimax(child, depth - 1, True, child_node)    
            if value < best:
                best = value
        if node is not None:
            node.value = best
        return best #el minimum woooo


def choose_move(board, k): #han-call de fel main
    global nodes
    nodes = 0           # turn gdid fa n3ed mn el awel
    root = make_root("max")     # None when tree building is off
    best_value = -INF
    best_col = None
    for col in board.valid_columns():
        child = board.copy()
        child.drop(col, AGENT)
        child_node = make_child(root, col, "min")
        value = minimax(child, k - 1, False, child_node)     
        if value > best_value:
            best_value = value
            best_col = col
    if root is not None:
        root.value = best_value
    return best_col









def alphabeta(board, depth, alpha, beta, is_agent_turn, node=None):
    global nodes
    nodes = nodes + 1   # count this node
    if node is not None:
        node.alpha = alpha     
        node.beta = beta
    if board.is_full() or depth == 0:
        value = evaluate(board)
        if node is not None:
            node.value = value      # leaf: the heuristic value
        return value

    if is_agent_turn:
        best = -INF
        for col in board.valid_columns():
            child = board.copy()
            child.drop(col, AGENT)
            child_node = make_child(node, col, "min")
            value = alphabeta(child, depth - 1, alpha, beta, False, child_node)
            if value > best:
                best = value
            if best > alpha:
                alpha = best
            #pruning hena vv
            if alpha >= beta:
                mark_pruned(node, board, col, "min")
                break
        if node is not None:
            node.value = best
        return best
    else:
        best = INF
        for col in board.valid_columns():
            child = board.copy()
            child.drop(col, HUMAN)
            child_node = make_child(node, col, "max")
            value = alphabeta(child, depth - 1, alpha, beta, True, child_node)
            if value < best:
                best = value
            if best < beta:
                beta = best
            #pruning hena vv
            if alpha >= beta:
                mark_pruned(node, board, col, "max")
                break
        if node is not None:
            node.value = best
        return best


def choose_move_alphabeta(board, k):
    global nodes
    nodes = 0          
    root = make_root("max")    
    alpha = -INF
    beta = INF
    if root is not None:
        root.alpha = alpha
        root.beta = beta
    best_value = -INF
    best_col = None
    for col in board.valid_columns():
        child = board.copy()
        child.drop(col, AGENT)
        child_node = make_child(root, col, "min")
        value = alphabeta(child, k - 1, alpha, beta, False, child_node)
        if value > best_value:
            best_value = value
            best_col = col
        if best_value > alpha:
            alpha = best_value
    if root is not None:
        root.value = best_value
    return best_col








def landing_options(board, col):
    left = col - 1
    right = col + 1
    left_ok = left >= 0 and not board.is_column_full(left)
    right_ok = right < board.cols and not board.is_column_full(right)

    if left_ok and right_ok:
        return [(col, 0.6), (left, 0.2), (right, 0.2)]
    if left_ok:
        return [(col, 0.6), (left, 0.4)]
    if right_ok:
        return [(col, 0.6), (right, 0.4)]
    return [(col, 1.0)]          


def chance_value(board, col, player, depth, next_is_agent, node=None):
    total = 0
    for landing_col, prob in landing_options(board, col):
        child = board.copy()
        child.drop(landing_col, player)
        next_type = "max" if next_is_agent else "min"
        child_node = make_child(node, landing_col, next_type, prob)
        value = expected_minimax(child, depth - 1, next_is_agent, child_node)
        total = total + prob * value
    if node is not None:
        node.value = total
    return total


def expected_minimax(board, depth, is_agent_turn, node=None):
    global nodes
    nodes = nodes + 1  
    if board.is_full() or depth == 0:
        value = evaluate(board)
        if node is not None:
            node.value = value      # leaf: the heuristic value
        return value

    if is_agent_turn:
        best = -INF
        for col in board.valid_columns():
            chance_node = make_child(node, col, "chance")
            value = chance_value(board, col, AGENT, depth, False, chance_node)
            if value > best:
                best = value
        if node is not None:
            node.value = best
        return best
    else:
        best = INF
        for col in board.valid_columns():
            chance_node = make_child(node, col, "chance")
            value = chance_value(board, col, HUMAN, depth, True, chance_node)
            if value < best:
                best = value
        if node is not None:
            node.value = best
        return best


def choose_move_expected(board, k):
    global nodes
    nodes = 0           
    root = make_root("max")     
    best_value = -INF
    best_col = None
    for col in board.valid_columns():
        chance_node = make_child(root, col, "chance")
        value = chance_value(board, col, AGENT, k, False, chance_node)
        if value > best_value:
            best_value = value
            best_col = col
    if root is not None:
        root.value = best_value
    return best_col