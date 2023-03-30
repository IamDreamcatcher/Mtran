import copy
import sys

from ast_parser.assign_node import AssignNode
from ast_parser.build_in_node import BuildInNode
from ast_parser.compare_node import CompareNode
from ast_parser.expression_node import ExpressionNode
from ast_parser.for_node import ForNode
from ast_parser.func_declaration_node import FuncDeclarationNode
from ast_parser.func_node import FuncNode
from ast_parser.if_node import IfNode
from ast_parser.node import Node
from ast_parser.variable_node import VariableNode


def parse_statement(parent_node, statement, variable_table, cur_line):

    new_node = build_expression_tree(statement, variable_table, cur_line)

    if new_node is not None:
        new_node.parent = parent_node
    return new_node


def build_expression_tree(expression, variable_table, cur_line):
    if not expression:
        return None
    min_operator = None
    parentheses_count = 0
    maximum_parentheses = 100
    for i in range(len(expression) - 1, -1, -1):
        if expression[i].value == ')':
            parentheses_count += 1
        elif expression[i].value == '(':
            parentheses_count -= 1
        elif parentheses_count < maximum_parentheses:
            if expression[i].token_type == "ARITHMETIC_OPERATION":
                min_precedence = get_priority(expression[i].value)
                min_operator = i
                maximum_parentheses = parentheses_count
        elif parentheses_count == maximum_parentheses:
            if expression[i].token_type == "ARITHMETIC_OPERATION" and get_priority(expression[i].value) < min_precedence:
                min_precedence = get_priority(expression[i].value)
                min_operator = i

    if min_operator is not None:
        root = ExpressionNode("Expression_node", expression[min_operator].value)

        root.right_value = build_expression_tree(expression[min_operator + 1:], variable_table, cur_line)
        root.left_value = build_expression_tree(expression[:min_operator], variable_table, cur_line)

        if root.left_value is not None and root.right_value is not None:
            if root.left_value.expression_result_type != "Const" and root.right_value.expression_result_type != "Const":
                if root.left_value.expression_result_type != root.right_value.expression_result_type:
                    print(
                        f"Semantic error: the types of l_value and r_value are not equal '{expression}' at line {expression[0].line} column {expression[0].column}")
                    sys.exit()

        root.expression_result_type = root.left_value.expression_result_type
    else:
        root = ExpressionNode("Expression_node", "")
        root.left_value = VariableNode("Variable_node")
        if expression[0].value == "(":
            expression = expression[1:]

        if expression[0].token_type == "VARIABLE":
            if expression[0].value not in variable_table:
                print(
                    f"Semantic error: undefined variable '{expression[0].value}' at line {expression[0].line} column {expression[0].column}")
                sys.exit()

            root.left_value = copy.deepcopy(variable_table[expression[0].value])

            if len(expression) > 1 and expression[1].value == "[":
                index = 1
                statement = []
                while expression[index].value != "]":
                    statement.append(expression[index])
                    index += 1

                root.left_value.array_index = parse_statement(root.left_value.array_index, statement, variable_table, cur_line)

            root.expression_result_type = root.left_value.variable_type
        else:
            root.left_value.variable_type = expression[0].token_type
            root.left_value.cur_value = expression[0].value
            root.left_value.variable_name = "Const"
            root.expression_result_type = root.left_value.variable_name
    return root


def get_priority(operator):
    if operator in ['+', '-', '+=', '-=']:
        return 1
    elif operator in ['*', '/', '/=', '*=']:
        return 2
    else:
        return float('inf')


def parse_compare_statement(parent_node, statement, variable_table, cur_line):
    new_node = CompareNode("Compare_node")
    operator_pos = 0

    for i in range(len(statement)):

        if statement[i].token_type == "COMPARISON_SIGN":
            operator_pos = i

    new_node.compare_sign = statement[operator_pos].value
    new_node.left_value = parse_statement(new_node, statement[:operator_pos], variable_table, cur_line)
    new_node.right_value = parse_statement(new_node, statement[operator_pos + 1:], variable_table, cur_line)
    new_node.parent = parent_node

    return new_node


def build_tree(tokens):
    root = Node("Block_node")
    cur_node = root
    variable_table = {}
    index = 0
    while index < len(tokens):
        cur_line = tokens[index].line
        if tokens[index].token_type == "DATA_TYPE":
            if tokens[index + 1].token_type == "FUNCTION":

                new_node = FuncDeclarationNode("Func_declaration_node")
                new_node.return_value = tokens[index].value
                new_node.parent = cur_node

                index += 2
                if tokens[index].value != "(":
                    print(
                        f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                    sys.exit()
                index += 1

                while tokens[index].value != ")":
                    if tokens[index].token_type != "DATA_TYPE":
                        print(
                            f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                        sys.exit()
                    if tokens[index + 1].token_type != "VARIABLE":
                        print(
                            f"Semantic error: l_value could be non constant '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                        sys.exit()
                    if tokens[index + 1].value in variable_table:
                        print(
                            f"Syntax error: variable redeclaration '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                        sys.exit()
                    var_node = VariableNode("Variable_node")
                    var_node.variable_type = tokens[index].value
                    var_node.variable_name = tokens[index + 1].value

                    new_node.arguments.append(var_node)
                    variable_table[tokens[index + 1].value] = var_node
                    index += 2
                    if tokens[index].value == ')':
                        break
                    index += 1

                cur_node.children.append(new_node)
                index += 1
                cur_node = new_node
            elif tokens[index + 1].token_type == "VARIABLE":
                if tokens[index + 1].value in variable_table:
                    print(
                        f"Syntax error: variable redeclaration '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                    sys.exit()

                new_node = VariableNode("Variable_node")
                new_node.variable_type = tokens[index].value
                new_node.variable_name = tokens[index + 1].value
                if tokens[index + 2].value == "[":
                    new_node.is_array = True
                new_node.parent = cur_node
                variable_table[tokens[index + 1].value] = new_node
                cur_node.children.append(new_node)
                index += 1
            else:
                if tokens[index + 1].token_type == "ARITHMETIC_OPERATION":
                    print(
                        f"Syntax error: expected variable but found '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                    sys.exit()
                else:
                    print(
                        f"Semantic error: l_value could be non constant '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                    sys.exit()

        elif tokens[index].value == "for":
            new_node = ForNode("For_node", VariableNode("Variable_node"), ExpressionNode("Expression_node", ""),
                               CompareNode("Compare_node"), ExpressionNode("Expression_node", ""))

            index += 2
            new_node.token = tokens[index]
            if tokens[index].token_type != "DATA_TYPE":
                print(
                    f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
            if tokens[index + 1].token_type != "VARIABLE":
                print(
                    f"Semantic error: l_value could be non constant '{tokens[index + 1].value}' at line {tokens[index + 1].line}, column {tokens[index + 1].column}")
                sys.exit()

            new_node.variable_node.variable_type = tokens[index].value
            new_node.variable_node.variable_name = tokens[index + 1].value
            variable_table[tokens[index + 1].value] = new_node.variable_node
            index += 2
            if tokens[index].value != "=":
                print(
                    f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
            index += 1

            statement = []
            while tokens[index].value != ";":
                statement.append(tokens[index])
                index += 1
            index += 1
            new_node.start_value_node = parse_statement(new_node.start_value_node, statement, variable_table, cur_line)
            statement = []
            while tokens[index].value != ";":
                statement.append(tokens[index])
                index += 1
            index += 1
            new_node.compare_node = parse_compare_statement(new_node.compare_node, statement, variable_table, cur_line)

            statement = []
            while tokens[index].value != ")":
                statement.append(tokens[index])
                index += 1

            new_node.expression_node = parse_statement(new_node.expression_node, statement, variable_table, cur_line)
            index += 1

            new_node.parent = new_node
            cur_node.children.append(new_node)
            cur_node = new_node
        elif tokens[index].value == "[":
            index += 1
            statement = []
            while tokens[index].value != "]":
                statement.append(tokens[index])
                index += 1

            new_node = parse_statement(cur_node, statement, variable_table, cur_line)
            cur_node.children[-1].array_index = new_node
            new_node.parent = cur_node.children[-1]
            index += 1
        elif tokens[index].token_type == "VARIABLE":
            new_node = AssignNode("Assign_node")

            if tokens[index].value not in variable_table:
                print(
                    f"Semantic error: undefined variable '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
            new_node.left_value = copy.deepcopy(variable_table[tokens[index].value])

            index += 1
            if tokens[index].value == "[":
                index += 1
                statement = []
                while tokens[index].value != "]":
                    statement.append(tokens[index])
                    index += 1

                new_node.left_value.array_index = parse_statement(new_node.left_value.array_index, statement,
                                                                  variable_table, cur_line)
                index += 1

            if tokens[index].token_type == "ARITHMETIC_OPERATION":
                new_node.arithmetic_sign = tokens[index].value
                index += 1

            statement = []
            while tokens[index - 1].line == tokens[index].line and tokens[index].value != ";":
                statement.append(tokens[index])
                index += 1

            if tokens[index].value != ";":
                print(
                    f"Syntax error: expected ; but found '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
            new_node.right_value = parse_statement(new_node, statement, variable_table, cur_line)
            new_node.parent = cur_node
            cur_node.children.append(new_node)
            index += 1
        elif tokens[index].value == "if":
            new_node = IfNode("If_node")

            index += 2

            statement = []
            while tokens[index].value != ")":
                statement.append(tokens[index])
                index += 1

            new_node.condition = parse_compare_statement(new_node, statement, variable_table, cur_line)
            index += 1
            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "else":
            if len(cur_node.children) == 0 or (cur_node.children[-1].node_type != "If_node" and (len(cur_node.children) > 1 and cur_node.children[-2].node_type != "If_node")):
                print(
                    f"Syntax error: expected if before but found '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
            new_node = IfNode("If_node")

            index += 1

            if tokens[index].value == "if":
                statement = []
                while tokens[index].value != ")":
                    statement.append(tokens[index])
                    index += 1
                new_node.condition = parse_compare_statement(new_node, statement, variable_table, cur_line)
                index += 1

            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "cout":
            new_node = BuildInNode("Build_in_node")

            new_node.function_name = "cout"
            index += 1

            while tokens[index].value != ";":
                index += 1
                new_node.arguments.append(tokens[index])
                index += 1

            index += 1

            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "break":
            new_node = BuildInNode("Build_in_node")

            new_node.function_name = "break"
            index += 2

            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "continue":
            new_node = BuildInNode("Build_in_node")

            new_node.function_name = "continue"
            index += 2

            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "return":
            new_node = BuildInNode("Build_in_node")

            new_node.function_name = "return"
            index += 1

            new_node.arguments.append(tokens[index])
            index += 2

            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].token_type == "FUNCTION":
            new_node = FuncNode("Func_node")

            new_node.function_name = tokens[index].value
            index += 2

            while tokens[index].value != ")":
                var_node = copy.deepcopy(variable_table[tokens[index].value])
                var_node.children = []
                new_node.arguments.append(var_node)
                index += 1

            index += 2
            new_node.parent = cur_node
            cur_node.children.append(new_node)
        elif tokens[index].value == "{":
            new_node = Node("Block_node")

            new_node.parent = cur_node
            cur_node.children.append(new_node)
            cur_node = new_node
            index += 1

        elif tokens[index].value == "}":
            cur_node = cur_node.parent
            index += 1
        elif tokens[index].value == ";":
            if cur_node.node_type == "Variable_node" or cur_node.node_type == "Func_node":
                cur_node = cur_node.parent
            else:
                print(
                    f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
                sys.exit()
        else:
            print(
                f"Syntax error: unexpected character '{tokens[index].value}' at line {tokens[index].line}, column {tokens[index].column}")
            sys.exit()
    return root


def print_ast(node, indent):
    if node is None:
        print(f"{indent * '-'}None")
        return
    print(f"{indent * '-'}{node.node_type}")
    if node.node_type == "Assign_node":
        print_ast(node.left_value, indent + 2)
        print(f"{(indent + 2) * '-'}Sign {node.arithmetic_sign}")
        print_ast(node.right_value, indent + 2)
    if node.node_type == "Build_in_node":
        print(f"{(indent + 2) * '-'}Build in function with name: {node.function_name}")
        print(f"{(indent + 2) * '-'}Arguments:")
        for arg in node.arguments:
            print(f"{(indent + 4) * '-'}Type: {arg.token_type} Value: {arg.value}")
    if node.node_type == "Compare_node":
        print(f"{(indent + 2) * '-'}Left value:")
        print_ast(node.left_value, indent + 4)
        print(f"{(indent + 2) * '-'}Sign: {node.compare_sign}")
        print(f"{(indent + 2) * '-'}Right value:")
        print_ast(node.right_value, indent + 4)
    if node.node_type == "Expression_node":
        print(f"{(indent + 2) * '-'}Left value:")
        print_ast(node.left_value, indent + 4)
        print(f"{(indent + 2) * '-'}Sign: {node.operator}")
        print(f"{(indent + 2) * '-'}Right value:")
        print_ast(node.right_value, indent + 4)
    if node.node_type == "For_node":
        print(f"{(indent + 2) * '-'}Variable args:")
        print_ast(node.variable_node, indent + 4)
        print(f"{(indent + 2) * '-'}Starting value:")
        print_ast(node.start_value_node, indent + 4)
        print(f"{(indent + 2) * '-'}Exit condition:")
        print_ast(node.compare_node, indent + 4)
        print(f"{(indent + 2) * '-'}Args changes:")
        print_ast(node.expression_node, indent + 4)
    if node.node_type == "Func_declaration_node":
        print(f"{(indent + 2) * '-'}Return value: {node.return_value}")
        print(f"{(indent + 2) * '-'}Args:")
        for item in node.arguments:
            print_ast(item, indent + 4)
    if node.node_type == "Func_node":
        print(f"{(indent + 2) * '-'}Function name: {node.function_name}")
        print(f"{(indent + 2) * '-'}Input args:")
        for item in node.arguments:
            print_ast(item, indent + 4)
    if node.node_type == "If_node":
        print(f"{(indent + 2) * '-'}if condition:")
        if node.condition is None:
            print(f"{(indent + 2) * '-'}None")
        else:
            print_ast(node.condition, indent + 4)
    if node.node_type == "Variable_node":
        print(f"{(indent + 2) * '-'}Name: {node.variable_name}")
        print(f"{(indent + 2) * '-'}Type: {node.variable_type}")
        if node.is_array:
            print(f"{(indent + 2) * '-'}Type: array ")
            print(f"{(indent + 2) * '-'}Values: {node.cur_array}")
        else:
            print(f"{(indent + 2) * '-'}Type: simple variable")
            print(f"{(indent + 2) * '-'}Value: {node.cur_value}")

        return node.variable_type
    for child in node.children:
        # print(f"{node.node_type} {child.node_type}")
        print_ast(child, indent + 2)

    if node.node_type == "Block_node":
        print(f"{indent * '-'}{node.node_type} ends")
