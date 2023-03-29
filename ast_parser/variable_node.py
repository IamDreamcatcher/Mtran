from ast_parser.expression_node import ExpressionNode
from ast_parser.node import Node


class VariableNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.variable_name = ""
        self.variable_type = ""
        self.cur_value = "-"
        self.is_array = False
        self.cur_array = []
        self.array_index = ExpressionNode("Expression_node", "")
