import re
from enum import Enum

class TokenType(Enum):
    INT = 'INT'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.regex_patterns = [
            (TokenType.INT, r'\d+'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
        ]

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        while self.pos < len(self.text):
            for token_type, pattern in self.regex_patterns:
                match = re.match(pattern, self.text[self.pos:])
                if match:
                    value = match.group(0)
                    self.pos += len(value)
                    return Token(token_type, value)

            if self.text[self.pos].isspace():
                self.pos += 1
                continue

            self.error()

        return Token(None, None)

class ASTNode:
    pass

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f'({self.left} {self.op} {self.right})'

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.regex_patterns = [
            (TokenType.INT, r'\d+'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
        ]

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        while self.pos < len(self.text):
            for token_type, pattern in self.regex_patterns:
                match = re.match(pattern, self.text[self.pos:])
                if match:
                    value = match.group(0)
                    self.pos += len(value)
                    if token_type == TokenType.INT:
                        return Token(token_type, int(value))
                    else:
                        return Token(token_type, value)

            if self.text[self.pos].isspace():
                self.pos += 1
                continue

            self.error()

        return Token(None, None)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return NumNode(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOpNode(left=node, op=token.value, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOpNode(left=node, op=token.value, right=self.term())

        return node

    def parse(self):
        self.current_token = self.tokens[self.index]
        return self.expr()

def main():
    text = input("Enter an expression: ")
    lexer = Lexer(text)

    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type is None:
            break
        tokens.append(token)

    print("Tokens:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAST:")
    print(ast)

if __name__ == "__main__":
    main()
