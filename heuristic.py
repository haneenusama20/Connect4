from board import HUMAN, AGENT


_WINDOW_CACHE = {} # cache to compute it only once
def _windows(board):
    key = (board.rows, board.cols)
    if key not in _WINDOW_CACHE:
        wins = []
        rows, cols = board.rows, board.cols
        for r in range(rows):
            for c in range(cols - 3):
                wins.append([(r, c + i) for i in range(4)])
        for r in range(rows - 3):
            for c in range(cols):
                wins.append([(r + i, c) for i in range(4)])
        for r in range(rows - 3):
            for c in range(cols - 3):
                wins.append([(r + i, c + i) for i in range(4)])
        for r in range(rows - 3):
            for c in range(3, cols):
                wins.append([(r + i, c - i) for i in range(4)])
        _WINDOW_CACHE[key] = wins
    return _WINDOW_CACHE[key]

def _count_windows_k(board, player, k): #el windows bt3ty eli feha 3add k mn el discs
    opp = HUMAN if player == AGENT else AGENT
    total = 0
    for w in _windows(board):
        own = 0
        blocked = False
        for r, c in w:
            v = board.grid[r][c]
            if v == player:
                own += 1
            elif v == opp:
                blocked = True
                break
        if not blocked and own == k:
            total += 1
    return total

def _candidate_cells(board, player): #el cells eli feha 3 discs, w empty space wahda. Momken tekon el connect four!
    opp = HUMAN if player == AGENT else AGENT
    cells = set()
    for w in _windows(board):
        own = 0
        empty = None
        blocked = False
        for r, c in w:
            v = board.grid[r][c]
            if v == player:
                own += 1
            elif v == opp:
                blocked = True
                break
            else:
                empty = (r, c)
        if not blocked and own == 3 and empty is not None:
            cells.add(empty)
    return cells

def _double_threat_cells(board, player): #el cells eli mwgoda f aktr mn window, fa hat722le 3add akbr mn el connect 4
    opp = HUMAN if player == AGENT else AGENT
    counts = {}
    for w in _windows(board):
        own = 0
        empty = None
        blocked = False
        for r, c in w:
            v = board.grid[r][c]
            if v == player:
                own += 1
            elif v == opp:
                blocked = True
                break
            else:
                empty = (r, c)
        if not blocked and own == 3 and empty is not None:
            counts[empty] = counts.get(empty, 0) + 1
    return sum(1 for v in counts.values() if v >= 2)

def _center_control(board, player): #weights, fel nos ahsn mn el hrof, more connect fours
    mid = board.cols // 2
    weights = [mid + 1 - abs(c - mid) for c in range(board.cols)]
    total = 0
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == player:
                total += weights[c]
    return total

def _future_capacity(board, player): # 3add el discs bta3ty elly gowa window wahda 3al a2al mfish feha human
    opp = HUMAN if player == AGENT else AGENT
    alive = set()
    for w in _windows(board):
        blocked = False
        for r, c in w:
            if board.grid[r][c] == opp:
                blocked = True
                break
        if not blocked:
            for r, c in w:
                if board.grid[r][c] == player:
                    alive.add((r, c))
    return len(alive)


def h1(board):
    return board.scores[AGENT] - board.scores[HUMAN]

# H2 ->	Current fours + "who's about to complete a four"
def h2(board):
    return (100 * (board.scores[AGENT] - board.scores[HUMAN])
            +   1 * (len(_candidate_cells(board, AGENT))
                      - len(_candidate_cells(board, HUMAN))))

# H3 ->	Current fours + counts of 3-in-a-row, 2-in-a-row, 1-in-a-row setups (weighted)
def h3(board):
    return (10000 * (board.scores[AGENT] - board.scores[HUMAN])
            +   100 * (_count_windows_k(board, AGENT, 3)
                       - _count_windows_k(board, HUMAN, 3))
            +     5 * (_count_windows_k(board, AGENT, 2)
                       - _count_windows_k(board, HUMAN, 2))
            +     1 * (_count_windows_k(board, AGENT, 1)
                       - _count_windows_k(board, HUMAN, 1)))

# H4 ->	H3 + danger cells + center control
def h4(board):
    return (1000 * (board.scores[AGENT] - board.scores[HUMAN])
            +  500 * (len(_candidate_cells(board, AGENT))
                      - len(_candidate_cells(board, HUMAN)))
            +   50 * (_count_windows_k(board, AGENT, 3)
                       - _count_windows_k(board, HUMAN, 3))
            +    5 * (_count_windows_k(board, AGENT, 2)
                       - _count_windows_k(board, HUMAN, 2))
            +    1 * (_count_windows_k(board, AGENT, 1)
                       - _count_windows_k(board, HUMAN, 1))
            +   20 * (_center_control(board, AGENT)
                       - _center_control(board, HUMAN)))

# H5 ->	H4 + "double threats" (cells that complete TWO fours at once) + "future capacity"
def h5(board):
    return (10000 * (board.scores[AGENT] - board.scores[HUMAN])
            +  2000 * (len(_candidate_cells(board, AGENT))
                       - len(_candidate_cells(board, HUMAN)))
            +   800 * (_double_threat_cells(board, AGENT)
                       - _double_threat_cells(board, HUMAN))
            +   150 * (_count_windows_k(board, AGENT, 3)
                       - _count_windows_k(board, HUMAN, 3))
            +    10 * (_count_windows_k(board, AGENT, 2)
                       - _count_windows_k(board, HUMAN, 2))
            +     1 * (_count_windows_k(board, AGENT, 1)
                       - _count_windows_k(board, HUMAN, 1))
            +    30 * (_center_control(board, AGENT)
                       - _center_control(board, HUMAN))
            +    15 * (_future_capacity(board, AGENT)
                       - _future_capacity(board, HUMAN)))

HEURISTICS = {
    "h1": h1,
    "h2": h2,
    "h3": h3,
    "h4": h4,
    "h5": h5,
}

def evaluate(board, name="h3"):
    return HEURISTICS[name](board)