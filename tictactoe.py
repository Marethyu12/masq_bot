class Board:
    valid_ch = ["X", "O", "_"]
    
    def __init__(self, data=[[["_" * 3]] for i in range(0, 3)]):
        self.data = data
        self._check()
    
    def set(self, row, col, ch):
        if ch not in valid_ch:
            raise ValueError("ch is invalid")
        
        self.data[row][col] = ch
    
    def winner(self):
        if ((self.data[0][0] == self.data[1][1] and self.data[1][1] == self.data[2][2]) or
            (self.data[2][0] == self.data[1][1] and self.data[1][1] == self.data[0][2])) and
            self.data[1][1] is not "_":
            return self.data[1][1]
        
        for i in range(0, 3):
            if self.data[i][0] == self.data[i][1] and self.data[i][1] == self.data[i][2] and self.data[i][0] is not "_":
                return self.data[i][0]
        
        for j in range(0, 3):
            if self.data[0][j] == self.data[1][j] and self.data[1][j] == self.data[2][j] and self.data[0][j] is not "_":
                return self.data[0][j]
        
        return "T"
    
    def score(self, player):
        winner = self.winner()
        
        if winner is player:
            return 10
        elif winner is self._enemy(player):
            return -10
        else:
            return 0
    
    def __str__(self):
        return ("-------------"
                "| " + self.data[0][0] + " | " + self.data[0][1] + " | " + self.data[0][2] + " |") # todo
    
    def _check(self):
        if len(self.data) is not 3 or len(self.data[0]) is not 3:
            raise ValueError("data isn't a 3x3 matrix")
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.data[i][j] not in valid_ch:
                    raise ValueError("The one of characters in data is not recognized")
    
    def _enemy(self, player):
        if player is "X":
            return "O":
        elif player is "O":
            return "X":
        else:
            raise ValueError("Unknown player (_ or something)")
