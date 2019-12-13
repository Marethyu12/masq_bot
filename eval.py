import enum

supported_funcs = ["pow",
                   "sqrt",
                   "abs",
                   "floor",
                   "ceil",
                   "log2",
                   "log10",
                   "exp",
                   "sin",
                   "cos",
                   "tan",
                   "asin",
                   "acos",
                   "atan",]

class TokType(enum.Enum):
    REAL_NUM = 0
    OPERATOR = 1
    FUNCTION = 2
    UNK_FUNC = 3
    LBRACKET = 4
    RBRACKET = 5
    UNKNOWN= 6

class Token:
    def __init__(self, t_type, value):
        self.t_type = t_type
        self.value = value

class MiniLexer:
    def __init__(self, expr):
        self.expr = expr
        self.idx = 0
        self.peek = " "
        self.ht = {}
        self._init_dict()
    
    def scan(self):
        while self.expr[self.idx] == " ":
            self.idx += 1
        self.peek = self.expr[self.idx]
        
        if self.peek in ["+", "-", "*", "/"]:
            return Token(TokType.OPERATOR, self.peek)
        
        if self.peek.isdigit():
            value = float(self.peek)
            self._advance()
            
            while self.peek.isdigit():
                value = 10 * value + float(self.peek)
                self._advance()
            
            if self.peek is not ".":
                return Token(TokType.REAL_NUM, str(value))
            
            x = 10.0
            
            while True:
                self._advance()
                
                if not self.peek.isdigit():
                    break
                
                value += float(self.peek) / x
                x *= 10.0
            
            return Token(TokType.REAL_NUM, str(value))
        
        if self.peek.isidentifier():
            func = self.peek
            self._advance()
            
            while self.peek.isidentifier():
                func += self.peek
                self._advance()
            
            if func in ht:
                return ht[func]
            
            return Token(TokType.UNK_FUNC, func)
        
        if self.peek is "(":
            return Token(TokType.LBRACKET, self.peek)
        
        if self.peek is ")":
            return Token(TokType.RBRACKET, self.peek)
        
        return Token(TokType.UNKNOWN, self.peek)
    
    def _advance(self):
        self.peek = self.expr[self.idx]
        self.idx += 1
    
    def _init_dict(self):
        for func in supported_funcs:
            self.ht[func] = Token(TokType.FUNCTION, func)

class Expression:
    def __init__(self):
        pass

class ExpressionParser:
    def __init__(self, expr):
        self.lex = MiniLexer(expr)
        self.look = None
        self._next()
    
    def eval_expr(self):
        pass
    
    def _next(self):
        self.look = self.lex.scan()
