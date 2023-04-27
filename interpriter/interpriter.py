return_flag = 0


def execute_program(node, function_tree_list, variable_table):
    global return_flag
    if node.node_type == "Assign_node":
        if node.arithmetic_sign == "=":
            variable_table[node.left_value.name] = execute_program(node.right_value, function_tree_list, variable_table)
        elif node.arithmetic_sign == "+=":
            variable_table[node.left_value.name] += execute_program(node.right_value, function_tree_list,
                                                                    variable_table)
        elif node.arithmetic_sign == "/=":
            variable_table[node.left_value.name] /= execute_program(node.right_value, function_tree_list,
                                                                    variable_table)
        elif node.arithmetic_sign == "*=":
            variable_table[node.left_value.name] *= execute_program(node.right_value, function_tree_list,
                                                                    variable_table)
        else:
            variable_table[node.left_value.name] = None
    if node.node_type == "Build_in_node":
        if node.function_name == "return":
            return node.arguments[0]
        if node.function_name == "continue":
            return_flag = 1
        if node.function_name == "break":
            return_flag = 2
        if node.function_name == "cout":
            for arg in node.arguments:
                print(arg, end='')
    if node.node_type == "Compare_node":
        compare_left_value = execute_program(node.left_value, function_tree_list, variable_table)
        compare_right_value = execute_program(node.right_value, function_tree_list, variable_table)
        if node.compare_sign == "<":
            return compare_left_value < compare_right_value
        if node.compare_sign == ">":
            return compare_left_value > compare_right_value
        if node.compare_sign == "<=":
            return compare_left_value <= compare_right_value
        if node.compare_sign == ">=":
            return compare_left_value >= compare_right_value
        if node.compare_sign == "==":
            return compare_left_value == compare_right_value
        if node.compare_sign == "!=":
            return compare_left_value != compare_right_value
    if node.node_type == "Expression_node":
        expr_left_value = execute_program(node.left_value, function_tree_list, variable_table)
        expr_right_value = execute_program(node.right_value, function_tree_list, variable_table)
        if node.operator == "+":
            return expr_left_value + expr_right_value
        elif node.operator == "-":
            return expr_left_value - expr_right_value
        elif node.operator == "/":
            return expr_left_value / expr_right_value
        elif node.operator == "*":
            return expr_left_value * expr_right_value
        elif node.operator == "++":
            return expr_left_value + 1
        elif node.operator == "--":
            return expr_left_value - 1
        elif node.operator == "%":
            return expr_left_value % expr_right_value
        elif node.operator == "/":
            return expr_left_value / expr_right_value
        else:
            return expr_left_value
    if node.node_type == "For_node":
        start_value = execute_program(node.start_value_node, function_tree_list, variable_table)
        variable_table[node.variable_node.name] = start_value
        while True:
            if not execute_program(node.compare_node, function_tree_list, variable_table):
                break
            for child in node.children:
                execute_program(child, function_tree_list, variable_table)
                if return_flag == 1:
                    return_flag = 0
                    break
                elif return_flag == 2 or return_flag == 3:
                    break

            if return_flag == 2:
                return_flag = 0
                break

            variable_table[node.variable_node.name] = execute_program(node.expression_node, function_tree_list,
                                                                      variable_table)

    if node.node_type == "Func_declaration_node":
        new_variable_table = {}
        for val, arg2 in zip(variable_table, node.arguments):
            new_variable_table[arg2] = val

        func_result = None
        for child in node.children:
            func_result = execute_program(child, function_tree_list, new_variable_table)

        return func_result
    if node.node_type == "Func_node":
        for func in function_tree_list:
            if func[0] == node.function_name:
                return execute_program(func[1], function_tree_list, node.arguments)
    if node.node_type == "If_node":
        if node.condition is None or execute_program(node.condition, function_tree_list, variable_table):
            for child in node.children:
                execute_program(child, function_tree_list, variable_table)

    if node.node_type == "Variable_node":
        if node.is_array:
            return node.cur_array
        else:
            return node.cur_array

    if node.node_type == "Block_node":
        for child in node.children:
            execute_program(child, function_tree_list, variable_table)
