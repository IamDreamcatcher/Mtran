from ast_parser.node import Node


class FuncNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.function_name = ""
        self.arguments = []
