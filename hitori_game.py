from boardgame import BoardGame
from re import sub

class HitoriGame(BoardGame):
    def __init__(self, f: str):
        self._cols = 0
        self._rows = 0
        self._starting_matrix = []
        self._populate_starting_matrix(f)
        self.clear_board()
        self.test = True
    
    def cols(self):
        return self._cols
    
    def rows(self):
        return self._rows
    
    def _populate_starting_matrix(self, f):
        with open(f, "r") as f1:
            for line in f1:
                self._cols += 1
                l = line.strip()
                l = l.split(",")
                self._rows = len(l)
                for c in l:
                    self._starting_matrix.append(int(c))
    
    def clear_board(self):
        self._user_matrix = ['CLEAR' for _ in range(self._cols * self._rows)]
        self._help_counter = 0
    
    def play_at(self, x, y):
        if self._user_matrix[y * self._cols + x] != 'BLACK':
            self._user_matrix[y * self._cols + x] = 'BLACK'
        else:
            self._user_matrix[y * self._cols + x] = 'CLEAR'
    
    def flag_at(self, x, y):
        if self._user_matrix[y * self._cols + x] != 'CIRCLE':
            self._user_matrix[y * self._cols + x] = 'CIRCLE'
        else:
            self._user_matrix[y * self._cols + x] = 'CLEAR'
    
    def auto_flag(self):
        for i in range(self._cols * self._rows):
            y = i // self._cols
            x = i % self._cols

            if self._user_matrix[y * self._cols + x] == 'BLACK':
                if y * self._cols + x - 1 >= y * self._cols and self._user_matrix[y * self._cols + x - 1] != 'BLACK':
                    self._user_matrix[y * self._cols + x - 1] = 'CIRCLE'
                if y * self._cols + x + 1 < (y * self._cols) + self._cols and self._user_matrix[y * self._cols + x + 1] != 'BLACK':
                    self._user_matrix[y * self._cols + x + 1] = 'CIRCLE'
                if y * self._cols + x + self._cols < self._cols * self._rows and self._user_matrix[y * self._cols + self._cols + x] != 'BLACK':
                    self._user_matrix[y * self._cols + self._cols + x] = 'CIRCLE'
                if y * self._cols + x - self._cols >= 0 and self._user_matrix[y * self._cols - self._cols + x] != 'BLACK':
                    self._user_matrix[y * self._cols - self._cols + x] = 'CIRCLE'
    
    def auto_play(self):
        for i in range(self._cols * self._rows):
            y = i // self._cols
            x = i % self._cols

            if self._user_matrix[y * self._cols + x] == 'CIRCLE':
                # For row
                for r in range(y * self._cols, y * self._cols + self._cols):
                    if r != y * self._cols + x:
                        if self._starting_matrix[r] == self._starting_matrix[y * self._cols + x]:
                            self._user_matrix[r] = 'BLACK'  
                
                # For column
                y2 = x
                while y2 < self._cols * self._rows:
                    if y2 != y * self._cols + x:
                        if self._starting_matrix[y2] == self._starting_matrix[y * self._cols + x]:
                            self._user_matrix[y2] = 'BLACK'
                    
                    y2 += self._cols
    
    def value_at(self, x, y):
        if self._user_matrix[y * self._cols + x] == 'CIRCLE':
            return str(self._starting_matrix[y * self._cols + x]) + '!'
        elif self._user_matrix[y * self._cols + x] == 'BLACK':
            return str(self._starting_matrix[y * self._cols + x]) + '#'
        else:
            return str(self._starting_matrix[y * self._cols + x]) + ' '

    def finished(self) -> bool:
        if self._check_value_repetition() and self._check_black_cells(self._user_matrix) and self._check_white_cells_connection(self._user_matrix):
            return True
        else:
            return False
    
    def message(self):
        return 'You won'
    
    def _check_value_repetition(self) -> bool:
        start = 0
        
        # For rows
        while start < self._cols * self._rows:
            for r in range(start, start + self._cols):
                if self._user_matrix[r] != 'BLACK':
                    for x in range(r + 1, self._cols + start):
                        if self._user_matrix[x] != 'BLACK':
                            if self._starting_matrix[r] == self._starting_matrix[x]:
                                return False
            start += self._cols
        
        # For columns
        for c in range(self._cols):
            y = c

            while y < self._cols * self._rows:
                if self._user_matrix[y] != 'BLACK':
                    y2 = y + self._cols
                    while y2 < self._cols * self._rows:
                        if self._user_matrix[y2] != 'BLACK':
                            if self._starting_matrix[y] == self._starting_matrix[y2]:
                                return False
                        y2 += self._cols
                y += self._cols
        
        return True
    
    """
        If the cell is black check the next cell and the cell below.
        Not the cell above or the previous one because is redundant
    """
    def _check_black_cells(self, matrix) -> bool:
        for m in range(self._cols * self._rows - 1):
            if matrix[m] == 'BLACK': 
                if m + self._cols < self._cols * self._rows and matrix[m + self._cols] == 'BLACK':
                    return False
                elif matrix[m + 1] == 'BLACK':
                    return False
        
        return True
    
    def _check_white_cells_connection(self, matrix):
        boolean_matrix = [False for _ in range(self._cols * self._rows)]
        cnt1 = 0
        pos = 0
        start = 0

        # Find first white cell
        while matrix[pos] == 'BLACK':
            pos += 1
        
        boolean_matrix[pos] = True

        # Check how many contiguous cells there are
        self._check_adjacent_cells(boolean_matrix, pos, start, matrix)

        # Count how many contiguous white cells there are
        for x in boolean_matrix:
            if x == True:
                cnt1 += 1

        cnt2 = self._expected_white_cells(matrix)

        if cnt2 == cnt1:
            return True
        else:
            return False
    
    def _check_adjacent_cells(self, b_matrix: list, pos: int, start: int, matrix: list) -> int:
        if pos + 1 < start + self._cols:
            if b_matrix[pos + 1] != True and matrix[pos + 1] != 'BLACK':
                b_matrix[pos + 1] = True
                self._check_adjacent_cells(b_matrix, pos + 1, start, matrix)
        if pos - 1 >= start:
            if b_matrix[pos - 1] != True and matrix[pos - 1] != 'BLACK':
                b_matrix[pos - 1] = True
                self._check_adjacent_cells(b_matrix, pos - 1, start, matrix)
        if pos - self._cols >= 0:
            if b_matrix[pos - self._cols] != True and matrix[pos - self._cols] != 'BLACK':
                b_matrix[pos - self._cols] = True
                self._check_adjacent_cells(b_matrix, pos - self._cols, start - self._cols, matrix)
        if pos + self._cols < self._cols * self._rows:
            if b_matrix[pos + self._cols] != True and matrix[pos + self._cols] != 'BLACK':
                b_matrix[pos + self._cols] = True
                self._check_adjacent_cells(b_matrix, pos + self._cols, start + self._cols, matrix)

    def wrong(self, matrix) -> bool:
        if not (self._check_black_cells(matrix) and self._check_white_cells_connection(matrix) and self._check_flagged_cells(matrix)):
            return True
        else:
            return False 

    def _expected_white_cells(self, matrix) -> int:
        cnt = 0

        for m in matrix:
            if m != 'BLACK':
                cnt += 1
        
        return cnt
    
    def _check_flagged_cells(self, matrix) -> bool:
        y = 0

        while y < self._cols * self._rows:
            for x in range(y, y + self._cols):
                if matrix[x] == 'CIRCLE':
                    # Search if there is the same circled value on the same row
                    for r in range(x + 1, y + self._cols):
                        if matrix[r] == 'CIRCLE' and self._starting_matrix[x] == self._starting_matrix[r]:
                            return False
                    # Search if there is the same circled value on the same column
                    y_flag = x - y
                    while y_flag < self._cols * self._rows:
                        if y_flag != x:
                            if matrix[y_flag] == 'CIRCLE' and self._starting_matrix[y_flag] == self._starting_matrix[x]:
                                return False
                        y_flag += self._cols
            y += self._cols

        return True
    
    def _try_play_at(self, matrix, x, y):
        backup_matrix = matrix.copy()

        matrix[y * self._cols + x] = 'BLACK'
        self.mark_auto()

        if self.wrong(matrix):
            matrix = backup_matrix
            matrix[y * self._cols + x] = 'CIRCLE'
        else:
            matrix = backup_matrix
        
        return matrix
    
    def _try_flag_at(self, matrix, x, y):
        backup_matrix = matrix.copy()

        matrix[y * self._cols + x] = 'CIRCLE'
        self.mark_auto()

        if self.wrong(matrix):
            matrix = backup_matrix
            matrix[y * self._cols + x] = 'BLACK'
        else:
            matrix = backup_matrix
        
        return matrix
    
    def user_helper(self):
        m_play = []
        m_flag = []
        saved = self._user_matrix.copy()

        while not self._user_matrix[self._help_counter] == 'CLEAR':
            self._help_counter += 1
        
        y = self._help_counter // self._cols
        x = self._help_counter % self._cols

        # Try blacken
        self._user_matrix[y * self._cols + x] = 'BLACK'
        self.mark_auto()
        m_play = self._user_matrix.copy()
        
        self._user_matrix = saved
        # Try circle
        self._user_matrix[y * self._cols + x] = 'CIRCLE'
        self.mark_auto()
        m_flag = self._user_matrix.copy()
        
        self._user_matrix = saved
        
        for c in range(self._rows * self._cols):
            if m_play[c] == 'BLACK' and m_flag[c] == 'BLACK':
                self._user_matrix[c] = 'BLACK'
            elif m_play[c] == 'CIRCLE' and m_flag[c] == 'CIRCLE':
                self._user_matrix[c] = 'CIRCLE'
    
    def mark_auto(self):
        self.auto_play()
        self.auto_flag()


    def solve_recursive(self, i: int) -> bool:
        self.mark_auto()  # mark all obvious cells
        if self.wrong(self._user_matrix): return False  # unsolvable
    # find first undecided cell, starting from i
        while i < len(self._user_matrix) and self._user_matrix[i] != 'CLEAR':
            i += 1
        if i < len(self._user_matrix):
            saved = self._user_matrix[:]  # save current status
            for a in ('BLACK', 'CIRCLE'):
                self._user_matrix[i] = a
                if self.solve_recursive(i + 1):
                    return True
                self._user_matrix = saved  # backtracking
        return self.finished()




    
