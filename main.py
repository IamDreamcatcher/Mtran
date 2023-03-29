from ast_parser.tree import build_tree, print_ast
from lexer.lexer import Lexer


def get_list_tree(tokens_list):
    tree_list = []
    func_table = {}
    for token in tokens_list:
        func_table[token[0]] = True
        tree_list.append((token[0], build_tree(token[1])))

    return tree_list


def print_errors(errors_list):
    for error in errors_list:
        print(error)


def print_tok(tokens_list):
    for token in tokens_list:
        print(token[0])
        for item in token[1]:
            print(item)


if __name__ == "__main__":
    cpp_file = "example.cpp"
    with open(cpp_file, "r") as file:
        code = (file.read())
    custom_lexer = Lexer()
    tokens, errors = custom_lexer.get_tokens(code)
    if len(errors) != 0:
        print_errors(errors)
        exit()
    functions_tree_list = get_list_tree(tokens)

    for token in functions_tree_list:
        print(f"Function: {token[0]}")
        print_ast(token[1], 0)
