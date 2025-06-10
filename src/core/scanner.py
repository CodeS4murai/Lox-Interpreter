from src.core.token_type import TokenType
from src.core.token1 import Token

class Scanner:
    keywords = {                  # mapping keywords to their token types
        "and":    TokenType.AND,
        "class":  TokenType.CLASS,
        "else":   TokenType.ELSE,
        "false":  TokenType.FALSE,
        "for":    TokenType.FOR,
        "fun":    TokenType.FUN,
        "if":     TokenType.IF,
        "nil":    TokenType.NIL,
        "or":     TokenType.OR,
        "print":  TokenType.PRINT,
        "return": TokenType.RETURN,
        "super":  TokenType.SUPER,
        "this":   TokenType.THIS,
        "true":   TokenType.TRUE,
        "var":    TokenType.VAR,
        "while":  TokenType.WHILE
    }

    def __init__(self, source):
        self.source = source # source code to be scanned
        self.tokens = []  # list to store tokens
        self.start = 0   # start index of the current token
        self.current = 0   # current index in the source code
        self.line = 1   # current line number in the source code

    def scan_tokens(self):  
        while not self.is_at_end():  #scans tokens until the end of the source code
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))  # add EOF token at the end
        return self.tokens

    def is_at_end(self): # checks if the current index is at the end of the source code
        return self.current >= len(self.source) # returns true if finishes scanning all characters

    def scan_token(self):  
        c = self.advance() # gets the current character and move to the next one
        if c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '!':    #here on checks for the respective token types
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in (' ', '\r', '\t'): 
            pass  # Ignore whitespace
        elif c == '\n':   
            self.line += 1  # Increment line number
        elif c == '"': # Start of a string literal
            self.string()
        elif c.isdigit(): #start of a number literal
            self.number()
        elif c.isalpha() or c == '_':   # start of an identifier
            self.identifier()
        else:
            print(f"[line {self.line}] Unexpected character: {c}")

    def advance(self): #moves one character forward and returns the current character
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None): # adds a token to the list of tokens
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected): # checks if the next character matches the expected character
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self): # returns the current character without moving forward
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self): # look at next character after the current one
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def string(self): # handles string literals
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end(): # if we reach the end of the source code without finding a closing quote
            print(f"[line {self.line}] Unterminated string.")
            return

        self.advance()  # closing "
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self): # handles number literals(int and float)
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self): # handles identifiers and keywords
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
