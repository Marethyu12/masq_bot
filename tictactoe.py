class Board:
    def __init__(self, data=[["_"] * 3 for i in range(3)]):
        self.data = data
    
    def winner(self):
        if ((self.data[0][0] == self.data[1][1] and self.data[1][1] == self.data[2][2]) or
            (self.data[2][0] == self.data[1][1] and self.data[1][1] == self.data[0][2])) and self.data[1][1] is not "_":
            return self.data[1][1]
        
        for i in range(3):
            if self.data[i][0] == self.data[i][1] and self.data[i][1] == self.data[i][2] and self.data[i][0] is not "_":
                return self.data[i][0]
        
        for j in range(3):
            if self.data[0][j] == self.data[1][j] and self.data[1][j] == self.data[2][j] and self.data[0][j] is not "_":
                return self.data[0][j]
        
        b = True
        
        for i in range(3):
            for j in range(3):
                if self.data[i][j] == "_":
                    b = False
        
        return "T" if b else "N"
    
    def score(self, player):
        winner = self.winner()
        
        if winner is player:
            return 10
        elif winner is self._enemy(player):
            return -10
        else:
            return 0
    
    def reset(self):
        for i in range(3):
            for j in range(3):
                self.data[i][j] = "_"
    
    def __str__(self):
        return ("`-------------`\n"
                "`| " + self.data[0][0] + " | " + self.data[0][1] + " | " + self.data[0][2] + " |`\n"
                "`-------------`\n"
                "`| " + self.data[1][0] + " | " + self.data[1][1] + " | " + self.data[1][2] + " |`\n"
                "`-------------`\n"
                "`| " + self.data[2][0] + " | " + self.data[2][1] + " | " + self.data[2][2] + " |`\n"
                "`-------------`\n")
    
    def _enemy(self, player):
        if player is "X":
            return "O"
        elif player is "O":
            return "X"
        else:
            return "_"

class GameController:
    def __init__(self, human, difficulty):
        self.human = human
        self.computer = "O" if human is "X" else "X"
        self.max_depth = (2 ** difficulty) // 2
        self.board = Board()
        self.game_over = False
    
    def make_move(self, row, col):
        self.board.data[row][col] = self.human
        
        cmpt_mv = self._minimax()[1]
        
        if cmpt_mv is not None:
            self.board.data[cmpt_mv[0]][cmpt_mv[1]] = self.computer
    
    def check_win(self):
        status = self.board.winner()
        
        if status is not "N":
            self.game_over = True
            return status
        else:
            return None
    
    # TODO: Implement Alpha Beta Pruning
    def _minimax(self, max_player=True, depth=0):
        score = self.board.score(self.computer)
        
        if score == 10:
            return (10, None)
        
        if score == -10:
            return (-10, None)
        
        if self.board.winner() == "T":
            return (0, None)
        
        if depth == self.max_depth:
            return (0, None)
        
        best_val = -10000 if max_player else 10000
        best_mv = [0, 0]
        
        for i in range(3):
            for j in range(3):
                if self.board.data[i][j] == "_":
                    self.board.data[i][j] = self.computer if max_player else self.human
                    
                    tmp = self._minimax(False if max_player else True, depth + 1)
                    if (max_player and best_val < tmp[0]) or (not max_player and best_val > tmp[0]):
                        best_val = tmp[0]
                        best_mv[0] = i
                        best_mv[1] = j
                    
                    self.board.data[i][j] = "_"
        
        return (best_val, best_mv)