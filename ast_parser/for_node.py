from ast_parser.node import Node


class ForNode(Node):
    def __init__(self, node_type, variable_node, start_value_node, compare_node, expression_node):
        super().__init__(node_type)
        self.variable_node = variable_node
        self.start_value_node = start_value_node
        self.compare_node = compare_node
        self.expression_node = expression_node
