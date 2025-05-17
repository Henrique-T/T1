from afd import AFD

class SyntaxTree():
    def __init__(self, postfix_tokens):
        self.stack = []
        self.postfix_tokens = postfix_tokens
        self.leaf_positions = {}  # Mapeia posição -> símbolo

    def build_syntax_tree(self):
        position_counter = 1

        for token in self.postfix_tokens:
            if token.isalnum() or token == '#':
                node = Leaf(token, position_counter)
                self.leaf_positions[position_counter] = token  # <-- adiciona isso
                position_counter += 1
                self.stack.append(node)
            elif token in ['*', '+', '?']:
                if len(self.stack) < 1:
                    raise ValueError("Invalid postfix expression: missing operand for unary operator")
                child = self.stack.pop()
                self.stack.append(UnaryNode(token, child))
            elif token in ['|', '.']:
                if len(self.stack) < 2:
                    raise ValueError("Invalid postfix expression: missing operands for binary operator")
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(BinaryNode(token, left, right))
            else:
                raise ValueError(f"Unknown token: {token}")

        if len(self.stack) != 1:
            raise ValueError("Invalid postfix expression")

        return self.stack[0]

    
    def compute_nullable_first_last_follow(self, root):
        followpos = dict()

        def traverse(node):
            if isinstance(node, Leaf):
                node.nullable = False
                node.firstpos = {node.position}
                node.lastpos = {node.position}
                followpos[node.position] = set()

            elif isinstance(node, UnaryNode):
                traverse(node.child)

                if node.symbol == '*':
                    node.nullable = True
                    node.firstpos = node.child.firstpos
                    node.lastpos = node.child.lastpos
                    for p in node.lastpos:
                        followpos[p].update(node.firstpos)
                elif node.symbol == '+':
                    node.nullable = node.child.nullable
                    node.firstpos = node.child.firstpos
                    node.lastpos = node.child.lastpos
                    for p in node.lastpos:
                        followpos[p].update(node.firstpos)
                elif node.symbol == '?':
                    node.nullable = True
                    node.firstpos = node.child.firstpos
                    node.lastpos = node.child.lastpos

            elif isinstance(node, BinaryNode):
                traverse(node.left)
                traverse(node.right)

                if node.symbol == '.':
                    node.nullable = node.left.nullable and node.right.nullable
                    node.firstpos = node.left.firstpos if not node.left.nullable else node.left.firstpos | node.right.firstpos
                    node.lastpos = node.right.lastpos if not node.right.nullable else node.left.lastpos | node.right.lastpos

                    for p in node.left.lastpos:
                        followpos[p].update(node.right.firstpos)

                elif node.symbol == '|':
                    node.nullable = node.left.nullable or node.right.nullable
                    node.firstpos = node.left.firstpos | node.right.firstpos
                    node.lastpos = node.left.lastpos | node.right.lastpos

        traverse(root)
        return followpos

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

def build_afd(root, followpos, leaf_positions):
    from collections import deque, defaultdict

    # Encontra a posição que tem o símbolo '#'
    hash_position = None
    for pos, symbol in leaf_positions.items():
        if symbol == '#':
            hash_position = pos
            break

    if hash_position is None:
        raise ValueError("Símbolo '#' não encontrado na expressão regular.")

    # Estado inicial: firstpos da raiz
    start_state = frozenset(root.firstpos)
    dstates = [start_state]
    unmarked_states = deque([start_state])
    transitions = {}
    accept_states = set()

    while unmarked_states:
        current = unmarked_states.popleft()
        transitions[current] = {}

        symbol_to_positions = defaultdict(set)

        for pos in current:
            symbol = leaf_positions[pos]
            if symbol == '#':
                continue  # ignorar o símbolo especial
            for follow in followpos.get(pos, []):
                symbol_to_positions[symbol].add(follow)

        for symbol, new_positions in symbol_to_positions.items():
            new_state = frozenset(new_positions)
            if new_state not in dstates:
                dstates.append(new_state)
                unmarked_states.append(new_state)
            transitions[current][symbol] = new_state

        for state in dstates:
            if hash_position in state:
                accept_states.add(state)

        return AFD(start_state, accept_states, transitions)


# def build_afd(root, followpos):
#     afd = AFD()
#     state_id_map = dict()  # frozenset of positions -> state name (optional, for printing)

#     # Encontra a posição do símbolo terminal '#'
#     hash_position = None
#     for pos in followpos:
#         if root.symbol == '#' or (hasattr(root, 'position') and root.symbol == '#'):
#             hash_position = root.position
#             break
#         if isinstance(root, BinaryNode):
#             if isinstance(root.right, Leaf) and root.right.symbol == '#':
#                 hash_position = root.right.position
#                 break

#     # Estado inicial
#     start = frozenset(root.firstpos)
#     afd.start_state = start
#     unmarked_states = [start]
#     marked_states = set()

#     while unmarked_states:
#         current = unmarked_states.pop()
#         marked_states.add(current)

#         symbols_to_positions = dict()

#         for pos in current:
#             # Encontrar o símbolo associado a esta posição
#             symbol_node = find_leaf_by_position(root, pos)
#             if symbol_node.symbol == '#':
#                 continue  # não cria transição com #
#             if symbol_node.symbol not in symbols_to_positions:
#                 symbols_to_positions[symbol_node.symbol] = set()
#             symbols_to_positions[symbol_node.symbol].update(followpos[pos])

#         for symbol, next_positions in symbols_to_positions.items():
#             next_state = frozenset(next_positions)
#             afd.add_transition(current, symbol, next_state)
#             if next_state not in marked_states and next_state not in unmarked_states:
#                 unmarked_states.append(next_state)

#     # Estados de aceitação: contém a posição do '#'
#     for state in afd.states:
#         if hash_position in state:
#             afd.accept_states.add(state)

#     return afd


def find_leaf_by_position(node, pos):
    if isinstance(node, Leaf):
        if node.position == pos:
            return node
    elif isinstance(node, UnaryNode):
        return find_leaf_by_position(node.child, pos)
    elif isinstance(node, BinaryNode):
        left_result = find_leaf_by_position(node.left, pos)
        if left_result:
            return left_result
        return find_leaf_by_position(node.right, pos)
    return None

