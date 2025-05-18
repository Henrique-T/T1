import afn

class AutomatonOperations:
    @staticmethod
    def union(afn1: afn.AFN, afn2: afn.AFN) -> afn.AFN:
        # Offset afn2 states to avoid collision
        offset = max(afn1.states) + 1
        afn2 = afn2.offset_states(offset)

        # Create new start state
        new_start = max(afn2.states) + 1
        new_states = afn1.states | afn2.states | {new_start}
        new_finals = afn1.final_states | afn2.final_states
        new_alphabet = afn1.alphabet | afn2.alphabet

        # Merge transitions
        new_transitions = {**afn1.transitions}
        for state, trans in afn2.transitions.items():
            if state not in new_transitions:
                new_transitions[state] = {}
            for symbol, dests in trans.items():
                if symbol not in new_transitions[state]:
                    new_transitions[state][symbol] = set()
                new_transitions[state][symbol].update(dests)

        # Add epsilon transitions from new start to both automata
        if new_start not in new_transitions:
            new_transitions[new_start] = {}
        new_transitions[new_start]['ε'] = {afn1.start_state, afn2.start_state}

        return afn.AFN(new_states, new_start, new_finals, new_transitions, new_alphabet | {'ε'})

