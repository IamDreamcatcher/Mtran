from ast_parser.tree import print_ast, get_tree
from lexer.lexer import Lexer
from lexer.lexer_constants import execute_program


def print_errors(errors_list):
    for error in errors_list:
        print(error)


if __name__ == "__main__":
    cpp_file = "example.cpp"
    with open(cpp_file, "r") as file:
        code = (file.read())
    custom_lexer = Lexer()
    tokens, errors = custom_lexer.get_tokens(code)
    if len(errors) != 0:
        print_errors(errors)
        exit()
    functions_tree_list = get_tree(tokens)
    # for token in functions_tree_list:
    #     print(f"Function: {token[0]}")
    #     print_ast(token[1], 0)

    variable_table = {}
    for token in functions_tree_list:
        if token[0] == "main":
            execute_program(token[1], functions_tree_list, variable_table)
