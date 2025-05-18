

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

    def export_to_txt(self, filename):
        state_id_map = {}
        current_id = 0

        # Assign unique numeric IDs to each state
        for state in self.transitions:
            if state not in state_id_map:
                state_id_map[state] = current_id
                current_id += 1
            for target in self.transitions[state].values():
                if target not in state_id_map:
                    state_id_map[target] = current_id
                    current_id += 1

        num_states = len(state_id_map)
        start_state_id = state_id_map[self.start_state]
        accept_state_ids = sorted(state_id_map[s] for s in self.accept_states)
        alphabet = set()

        # Collect transitions
        transition_lines = []
        for src, transitions in self.transitions.items():
            src_id = state_id_map[src]
            for symbol, dst in transitions.items():
                dst_id = state_id_map[dst]
                alphabet.add(symbol)
                transition_lines.append(f"{src_id},{symbol},{dst_id}")

        # Write to file
        with open(filename, 'w') as f:
            f.write(f"{num_states}\n")
            f.write(f"{start_state_id}\n")
            f.write(','.join(map(str, accept_state_ids)) + '\n')
            f.write(','.join(sorted(alphabet)) + '\n')
            for line in transition_lines:
                f.write(line + '\n')
