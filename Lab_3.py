import re

# Define token types
TOKEN_INT = 'INT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLY'
TOKEN_DIVIDE = 'DIVIDE'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'

# Define regular expressions for each token type
TOKEN_REGEX = [
    (TOKEN_INT, r'\d+'),
    (TOKEN_PLUS, r'\+'),
    (TOKEN_MINUS, r'-'),
    (TOKEN_MULTIPLY, r'\*'),
    (TOKEN_DIVIDE, r'/'),
    (TOKEN_LPAREN, r'\('),
    (TOKEN_RPAREN, r'\)'),
]

# Token class to represent individual tokens
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Lexer class to tokenize input text
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(None, None)

        for token_type, regex_pattern in TOKEN_REGEX:
            regex = re.compile('^' + regex_pattern)
            match = regex.match(self.text[self.pos:])
            if match:
                value = match.group(0)
                token = Token(token_type, value)
                self.pos += len(value)
                return token

        self.error()

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

if __name__ == "__main__":
    main()
