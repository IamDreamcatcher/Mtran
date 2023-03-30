class CustomToken:
    def __init__(self, value, token_type, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
