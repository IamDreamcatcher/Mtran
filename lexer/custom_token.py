class CustomToken:
    def __init__(self, value, token_type, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"token with value: {self.value}, type: {self.token_type}, line {self.line}, column {self.column}"
