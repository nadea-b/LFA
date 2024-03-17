# Define token types
TOKEN_INT = 'INT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULTIPLY = 'MULTIPLY'
TOKEN_DIVIDE = 'DIVIDE'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'

# Define a function to check if a character is a digit
def is_digit(char):
    return '0' <= char <= '9'

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
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            if current_char.isspace():
                self.pos += 1
                continue

            if is_digit(current_char):
                start_pos = self.pos
                while self.pos < len(self.text) and is_digit(self.text[self.pos]):
                    self.pos += 1
                return Token(TOKEN_INT, self.text[start_pos:self.pos])

            if current_char == '+':
                self.pos += 1
                return Token(TOKEN_PLUS, current_char)

            if current_char == '-':
                self.pos += 1
                return Token(TOKEN_MINUS, current_char)

            if current_char == '*':
                self.pos += 1
                return Token(TOKEN_MULTIPLY, current_char)

            if current_char == '/':
                self.pos += 1
                return Token(TOKEN_DIVIDE, current_char)

            if current_char == '(':
                self.pos += 1
                return Token(TOKEN_LPAREN, current_char)

            if current_char == ')':
                self.pos += 1
                return Token(TOKEN_RPAREN, current_char)

            self.error()

        return Token(None, None)

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
