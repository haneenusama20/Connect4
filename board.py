#initial comment
#grid 7x6 rowsxcoloumns NOT FIXED!
#list which coloumns are not full
#at each play, is there a connect four? to who?
#During search, each agent search algo will have a copy, not the real

#t7t howa el 0, TAHT HA

EMPTY = 0
HUMAN = 1
AGENT = 2

DIRECTIONS = [
    (0, 1),    # horizontal
    (1, 0),    # vertical
    (1, 1),    # diagonal up-right
    (1, -1),   # diagonal up-left
]


class Board:
    def __init__(self, rows=6, cols=7): #hanghyar el sizes HANGHYR EL SIZE 3ADY
        
        self.rows = rows
        self.cols = cols
        
        self.grid = []
        for r in range(rows):
            one_row = []
            for c in range(cols):
                one_row.append(EMPTY)
            self.grid.append(one_row)

        #f kol coloumn hanhot counter, ysa3dna fel decisions
        self.heights = []
        for c in range(cols):
            self.heights.append(0)

        # Number of connected-fours each player has made so far
        self.scores = {HUMAN: 0, AGENT: 0}

    def is_column_full(self, col):
        return self.heights[col] == self.rows

    def valid_columns(self):
        valid = []
        for c in range(self.cols):
            if not self.is_column_full(c):
                valid.append(c)
        return valid

    def drop(self, col, player):
        if self.is_column_full(col):
            return None

        row = self.heights[col]

        self.grid[row][col] = player
        self.heights[col] = self.heights[col] + 1

        new_fours = self.count_new_fours(row, col, player)
        self.scores[player] = self.scores[player] + new_fours

        return row

    def is_inside(self, row, col):
        #bn check el edges bs
        return 0 <= row < self.rows and 0 <= col < self.cols

    def count_same_in_direction(self, row, col, row_step, col_step, player):
        count = 0
        r = row + row_step
        c = col + col_step
        while self.is_inside(r, c) and self.grid[r][c] == player:
            count = count + 1
            r = r + row_step
            c = c + col_step
        return count

    def count_new_fours(self, row, col, player):
        total = 0

        for row_step, col_step in DIRECTIONS:
            before = self.count_same_in_direction(row, col, -row_step, -col_step, player)
            after = self.count_same_in_direction(row, col, row_step, col_step, player)

            for start in range(-3, 1):
                end = start + 3
                if start >= -before and end <= after:
                    total = total + 1

        return total

    def copy(self):
        new_board = Board(self.rows, self.cols)

        for r in range(self.rows):
            for c in range(self.cols):
                new_board.grid[r][c] = self.grid[r][c]

        for c in range(self.cols):
            new_board.heights[c] = self.heights[c]

        new_board.scores[HUMAN] = self.scores[HUMAN]
        new_board.scores[AGENT] = self.scores[AGENT]

        return new_board

    def is_full(self):
        for c in range(self.cols):
            if not self.is_column_full(c):
                return False
        return True



    
