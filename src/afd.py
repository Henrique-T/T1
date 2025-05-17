

class AFD:
    def __init__(self, start_state, accept_states, transitions):
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions  # Dict[frozenset, Dict[symbol, frozenset]]

    def __str__(self):
        lines = ["AFD:"]
        lines.append(f"Start state: {self.start_state}")
        lines.append(f"Accept states: {self.accept_states}")
        lines.append("Transitions:")
        for state, trans in self.transitions.items():
            for symbol, target in trans.items():
                lines.append(f"  {set(state)} -- {symbol} --> {set(target)}")
        return "\n".join(lines)


# class AFD:
#     def __init__(self):
#         self.states = set()
#         self.alphabet = set()
#         self.start_state = None
#         self.accept_states = set()
#         self.transitions = dict()  # (state, symbol) -> state

#     def add_transition(self, from_state, symbol, to_state):
#         self.transitions[(frozenset(from_state), symbol)] = frozenset(to_state)
#         self.states.add(frozenset(from_state))
#         self.states.add(frozenset(to_state))
#         self.alphabet.add(symbol)

#     def __str__(self):
#         lines = ["AFD:"]
#         lines.append(f"Start state: {self.start_state}")
#         lines.append(f"Accept states: {self.accept_states}")
#         lines.append("Transitions:")
#         for (state, symbol), to_state in self.transitions.items():
#             lines.append(f"  {set(state)} -- {symbol} --> {set(to_state)}")
#         return "\n".join(lines)
