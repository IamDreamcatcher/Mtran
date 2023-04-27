import re

from lexer.custom_token import CustomToken
from lexer.lexer_constants import regex_map, syntax_types


class Lexer:
    def __init__(self):
        self.func_list = []
        self.tokens = []
        self.errors = []
        self.line_num = 1
        self.col_num = 1
        self.cur_func = ""

    def get_tokens(self, code):
        self.tokens = []
        self.errors = []
        self.line_num = 1
        self.col_num = 1
        self.cur_func = ""
        i = 0
        while i < len(code):
            match = None
            for key, value in regex_map.items():
                tag, pattern = key, value
                regex = re.compile(pattern)
                match = regex.match(code[i:])
                if match:
                    text = match.group(0)
                    if tag == "function":
                        text = text.split()
                        if len(self.tokens) != 0:
                            self.func_list.append((self.cur_func, self.tokens))
                            self.tokens = []
                        token = CustomToken(text[0], syntax_types[text[0]], self.line_num, self.col_num)
                        self.tokens.append(token)
                        self.col_num += len(text[0])
                        token = CustomToken(text[1], syntax_types[tag], self.line_num, self.col_num)
                        self.tokens.append(token)
                        self.col_num += len(text[1])
                        self.cur_func = text[1]
                    elif tag == "whitespace":
                        if '\n' in text:
                            self.line_num += 1
                            self.col_num = 1
                    elif tag == "operator":
                        if len(text) > 2 or self.tokens[-1].token_type == "ARITHMETIC_OPERATION" or text not in syntax_types:
                            self.errors.append(
                                f"Syntax error: unexpected operator '{text}' at line {self.line_num}, column {self.col_num}")
                            self.col_num += len(text)
                        else:
                            token = CustomToken(text, syntax_types[text], self.line_num, self.col_num)
                            self.tokens.append(token)
                            self.col_num += len(text)
                    elif tag == "string_value":
                        token = CustomToken(text, syntax_types[tag], self.line_num, self.col_num)
                        self.tokens.append(token)
                        self.col_num += len(text)
                    elif tag == "identifier":
                        if text[0] == "*":
                            text = text[1:]
                        token = CustomToken(text, syntax_types[tag], self.line_num, self.col_num)
                        for item in self.func_list:
                            if item[0] == text:
                                token.token_type = "FUNCTION"
                        self.tokens.append(token)
                        self.col_num += len(text)
                    elif tag == "const":
                        if text.count('.') > 1:
                            self.errors.append(
                                f"Syntax error: unexpected value '{text}' at line {self.line_num}, column {self.col_num}")
                            self.col_num += len(text)
                        else:
                            token = CustomToken(text, syntax_types[tag], self.line_num, self.col_num)
                            self.tokens.append(token)
                            self.col_num += len(text)
                    else:
                        token = CustomToken(text, syntax_types[text], self.line_num, self.col_num)
                        self.tokens.append(token)
                        self.col_num += len(text)
                    break
            if not match:
                self.errors.append(
                    f"Syntax error: unexpected character '{code[i]}' at line {self.line_num}, column {self.col_num}")
                self.col_num += 1
                i += 1
            else:
                i += len(match.group(0))

        self.func_list.append((self.cur_func, self.tokens))

        return self.func_list, self.errors
