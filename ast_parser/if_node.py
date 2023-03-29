from ast_parser.node import Node


class IfNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.condition = None
