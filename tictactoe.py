class Board:
    def __init__(self, mat):
        self.mat = mat
        
        if len(mat) is not 3 or len(mat[0]) is not 3:
            raise ValueError("mat isn't a 3x3 matrix")
    
    def winner(self):
        if self.mat[0][0] == self.mat[1][1] and self.mat[1][1] == self.mat[2][2] or
           self.mat[2][0] == self.mat[1][1] and self.mat[0][2]:
            return self.mat[1][1]
        
        for i in range(0, 3):
            if self.mat[i][0] == self.mat[i][1] and self.mat[i][1] == self.mat[i][2]:
                return self.mat[i][0]
        
        for j in range(0, 3):
            if self.mat[0][j] == self.mat[1][j] and self.mat[1][j] == self.mat[2][j]:
                return self.mat[0][j]
        
        return "T"
    
    def score(self, player):
        winner = self.winner()
        
        if winner is player:
            return 10
        elif winner
    # todo: add set method, handle _, and to_str
    def _enemy(self, player):
        if player is "X":
            return "O":
        elif player is "O":
            return "X":
        else:
            raise ValueError("Unknown player")

