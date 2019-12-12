class Board:
    valid_ch = ["X", "O", "_"]
    
    def __init__(self, data=[["_"] * 3 for i in range(0, 3)]):
        self.data = data
        self._check()
    
    def winner(self):
        if ((self.data[0][0] == self.data[1][1] and self.data[1][1] == self.data[2][2]) or
            (self.data[2][0] == self.data[1][1] and self.data[1][1] == self.data[0][2])) and self.data[1][1] is not "_":
            return self.data[1][1]
        
        for i in range(0, 3):
            if self.data[i][0] == self.data[i][1] and self.data[i][1] == self.data[i][2] and self.data[i][0] is not "_":
                return self.data[i][0]
        
        for j in range(0, 3):
            if self.data[0][j] == self.data[1][j] and self.data[1][j] == self.data[2][j] and self.data[0][j] is not "_":
                return self.data[0][j]
        
        b = True
        
        for i in range(0, 3):
            for j in range(0, 3):
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
    
    def __str__(self):
        return ("-------------\n"
                "| " + self.data[0][0] + " | " + self.data[0][1] + " | " + self.data[0][2] + " |\n"
                "-------------\n"
                "| " + self.data[1][0] + " | " + self.data[1][1] + " | " + self.data[1][2] + " |\n"
                "-------------\n"
                "| " + self.data[2][0] + " | " + self.data[2][1] + " | " + self.data[2][2] + " |\n"
                "-------------\n")
    
    def _check(self):
        if len(self.data) is not 3 or len(self.data[0]) is not 3:
            raise ValueError("data isn't a 3x3 matrix")
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.data[i][j] not in self.valid_ch:
                    raise ValueError("The one of characters in data is not recognized")
    
    def _enemy(self, player):
        if player is "X":
            return "O"
        elif player is "O":
            return "X"
        else:
            raise ValueError("Unknown player (_ or something)")

class GameController:
    def __init__(self, human):
        self.computer = "O" if human is "X" else "X"
        self.board = Board()
    
    def _minimax(self, max_player):
        score = self.board.score(computer)
        
        if score == 10:
            return 10
        
        if score == -10
            return -10
        
        if self.board.winner() == "T":
            return 0
        
        best = (0, 0, 0)
        
        if max_player:
            best[0] = -10000
            
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board.data[i][j] == "_":
                        self.board.data[i][j] = computer
                        
                        tmp = self._minimax(False)
                        if best < tmp[0]:
                            best = tmp[0]
                            best[1] = i
                            best[2] = j
                        
                        self.board.data[i][j] = "_"
            
            return best
        else:
            best[1] = 10000
            
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board.data[i][j] == "_":
                        self.board.data[i][j] = human
                        
                        tmp = self._minimax(True)
                        if best > tmp[0]:
                            best = tmp[0]
                            best[1] = i
                            best[2] = j
                        
                        self.board.data[i][j] = "_"
            
            return best
