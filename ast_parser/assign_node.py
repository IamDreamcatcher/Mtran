from ast_parser.node import Node


class AssignNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.left_value = None
        self.arithmetic_sign = "="
        self.right_value = None
