import re

# Define token types
TOKEN_INT = r'INT'
TOKEN_PLUS = r'PLUS'
TOKEN_MINUS = r'MINUS'
TOKEN_MULTIPLY = r'MULTIPLY'
TOKEN_DIVIDE = r'DIVIDE'
TOKEN_LPAREN = r'LPAREN'
TOKEN_RPAREN = r'RPAREN'

# Token class to represent individual tokens
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Define patterns for token identification
patterns = [
    (TOKEN_INT, r'\d+'),
    (TOKEN_PLUS, r'\+'),
    (TOKEN_MINUS, r'\-'),
    (TOKEN_MULTIPLY, r'\*'),
    (TOKEN_DIVIDE, r'/'),
    (TOKEN_LPAREN, r'\('),
    (TOKEN_RPAREN, r'\)'),
]

# Lexer class to tokenize input text
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        while self.pos < len(self.text):
            current_text = self.text[self.pos:]
            for token_type, pattern in patterns:
                match = re.match(pattern, current_text)
                if match:
                    value = match.group(0)
                    self.pos += len(value)
                    return Token(token_type, value)

            # If no match found, raise an error
            self.error()

        return Token(None, None)

# Define AST node types
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
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)

# Parser class to build AST from tokens
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()

        while self.current_token and self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            token = self.current_token
            if token.type == TOKEN_PLUS:
                self.advance()
            elif token.type == TOKEN_MINUS:
                self.advance()
            right = self.term()
            node = BinOpNode(node, token.value, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token and self.current_token.type in (TOKEN_MULTIPLY, TOKEN_DIVIDE):
            token = self.current_token
            if token.type == TOKEN_MULTIPLY:
                self.advance()
            elif token.type == TOKEN_DIVIDE:
                self.advance()
            right = self.factor()
            node = BinOpNode(node, token.value, right)

        return node

    def factor(self):
        token = self.current_token

        if token.type == TOKEN_INT:
            self.advance()
            return NumNode(token)
        elif token.type == TOKEN_LPAREN:
            self.advance()
            node = self.expr()
            if self.current_token.type != TOKEN_RPAREN:
                raise Exception('Expected RPAREN')
            self.advance()
            return node
        else:
            raise Exception('Invalid syntax')

# Sample usage
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
