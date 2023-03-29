from ast_parser.node import Node


class ExpressionNode(Node):
    def __init__(self, node_type, operator):
        super().__init__(node_type)
        self.left_value = None
        self.operator = operator
        self.right_value = None
