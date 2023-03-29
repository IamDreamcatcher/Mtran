from ast_parser.node import Node


class FuncDeclarationNode(Node):
    def __init__(self, node_type):
        super().__init__(node_type)
        self.arguments = []
        self.return_value = ""
