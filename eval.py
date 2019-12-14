import enum

from abc import ABC, abstractmethod

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
    UNARY_OP = 2
    FUNCTION = 3
    UNK_FUNC = 4
    LBRACKET = 5
    RBRACKET = 6
    UNKNOWNT = 7

class Token:
    def __init__(self, t_type, value):
        self.t_type = t_type
        self.value = value

class MiniLexer:
    def __init__(self, expr):
        self.expr = expr
        self.idx = -1
        self.peek = None
        self.ht = {}
        self._init_dict()
        self._advance()
        self.done = False
    
    def scan(self):
        if self.done:
            return
        
        while self.expr[self.idx] == " ":
            self.idx += 1
        self.peek = self.expr[self.idx]
        
        if self.peek in ["+", "-", "*", "/"]:
            token = None
            
            if self.expr[self.idx + 1] == "(" or self.expr[self.idx + 1].isalnum():
                token = Token(TokType.UNARY_OP, self.peek)
            else:
                token = Token(TokType.OPERATOR, self.peek)
            
            self._advance()
            
            return token
        
        if self.peek.isdigit():
            value = 0.0
             
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
        
        if self.peek.isalpha():
            func = ""
            
            while self.peek.isalnum():
                func += self.peek
                self._advance()
            
            if func in self.ht:
                return self.ht[func]
            
            return Token(TokType.UNK_FUNC, func)
        
        if self.peek is "(":
            token = Token(TokType.LBRACKET, self.peek)
            self._advance()
            return token
        
        if self.peek is ")":
            token = Token(TokType.RBRACKET, self.peek)
            self._advance()
            return token
        
        token = Token(TokType.UNKNOWNT, self.peek)
        self._advance()
        
        return token
    
    def _advance(self):
        self.idx += 1
        if self.idx == len(self.expr):
            self.done = True
            return
        self.peek = self.expr[self.idx]
    
    def _init_dict(self):
        for func in supported_funcs:
            self.ht[func] = Token(TokType.FUNCTION, func)

class Expression(ABC):
    def __init__(self):
        super.__init__()
    
    @abstractmethod
    def reduce(self):
        pass

class RealNumber(Expression):
    def __init__(self, fvalue):
        self.fvalue = fvalue
    
    def reduce(self):
        return self.fvalue

class FunctionCall(Expression):
    def __init__(self, fname, expr):
        self.fname = fname
        self.expr = expr
    
    def reduce(self):
        import math
        return math.__dict__[self.fname](expr.reduce())

class UnaryExpression(Expression):
    def __init__(self, is_minus, expr):
        self.is_minus = is_minus
        self.expr = expr
    
    def reduce(self):
        reduced_val = expr.reduce()
        return -reduced_val if is_minus else reduced_val

def BinaryExpression(Expression):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    def reduce(self):
        if op == "+":
            return left.reduce() + right.reduce()
        elif op == "-":
            return left.reduce() - right.reduce()
        elif op == "*":
            return left.reduce() * right.reduce()
        elif op == "/":
            return left.reduce() / right.reduce()

class ExpressionParser:
    def __init__(self, expr):
        self.lex = MiniLexer(expr)
    
    def parse(self, expr=None):
        if expr is None:
            expr = self.expr
        
        while not self.lex.done:
            token = self.lex.scan()
            
            if token.t_type is TokType.REAL_NUM:
                next_tok = self.lex.scan()
                
                if next_tok.t_type is TokType.OPERATOR:
                    return BinaryExpression(RealNumber(token.value), next_tok.value, parse()) # TODO