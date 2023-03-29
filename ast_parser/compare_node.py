from ast_parser.node import Node


class CompareNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.left_value = None
        self.compare_sign = ""
        self.right_value = None
