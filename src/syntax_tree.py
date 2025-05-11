

class SyntaxTree():
    def __init__(self, postfix_tokens):
        self.stack = []
        self.postfix_tokens = postfix_tokens

    def build_syntax_tree(self):
        position_counter = 1  # Assign unique position to each leaf

        for token in self.postfix_tokens:
            if token.isalnum() or token == '#':  # symbol
                node = Leaf(token, position_counter)
                position_counter += 1
                self.stack.append(node)
            elif token in ['*', '+', '?']:  # unary ops
                child = self.stack.pop()
                self.stack.append(UnaryNode(token, child))
            elif token in ['|', '.']:  # binary ops
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(BinaryNode(token, left, right))
            else:
                raise ValueError(f"Unknown token: {token}")

        if len(self.stack) != 1:
            raise ValueError("Invalid postfix expression")

        return self.stack[0]

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

class Leaf(Node):
    def __init__(self, symbol, position):
        super().__init__(symbol)
        self.position = position

class UnaryNode(Node):
    def __init__(self, symbol, child):
        super().__init__(symbol)
        self.child = child

class BinaryNode(Node):
    def __init__(self, symbol, left, right):
        super().__init__(symbol)
        self.left = left
        self.right = right