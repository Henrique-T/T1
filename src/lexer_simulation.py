

def simulate_dfa_on_text(dfa, token_map, text):
    """
    Simulates DFA on input text and returns list of (lexeme, token) tuples.
    
    Parameters:
    - dfa: dict with {state, transitions, accepting states}
    - token_map: dict {state: token_name} from regex order
    - text: str, entire input program
    
    Returns: list of (lexeme, token) or (lexeme, "erro!")
    """
    i = 0
    tokens = []

    while i < len(text):
        state = dfa.start_state
        last_accepting = None
        last_accepting_index = i
        current_index = i

        while current_index < len(text):
            symbol = text[current_index]
            print(f"Reading symbol: '{symbol}' from state {state}")

            if symbol not in dfa.transitions.get(state, {}):
                print(f" No transition for symbol '{symbol}' from state {state}")
                break

            state = dfa.transitions[state][symbol]
            print(f"  ✅ Transition to state {state}")

            if state in dfa.accept_states:
                last_accepting = state
                last_accepting_index = current_index + 1

            current_index += 1

        if last_accepting is not None:
            lexeme = text[i:last_accepting_index]

            token = None
            for substate in sorted(last_accepting):
                if substate in token_map:
                    token = token_map[substate]
                    break

            if token is None:
                token = "erro!"

            tokens.append((lexeme, token))
            i = last_accepting_index
        else:
            tokens.append((text[i], "erro!"))
            i += 1

    return tokens

def simulate_dfa_on_line(dfa, token_map, line):
    """
    Simulates DFA on a single line of input and returns (lexeme, token).
    If the entire line is accepted by DFA, it returns the corresponding token.
    Otherwise, it returns (line, "erro!").
    """
    state = dfa.start_state
    i = 0
    while i < len(line):
        symbol = line[i]
        if symbol not in dfa.transitions.get(state, {}):
            return (line, "erro!")
        state = dfa.transitions[state][symbol]
        i += 1

    if state in dfa.accept_states:
        # Token resolution: check which original substate this final DFA state includes
        token = None
        for substate in sorted(state):
            if substate in token_map:
                token = token_map[substate]
                break
        return (line, token or "erro!")
    else:
        return (line, "erro!")

def run_lexer(dfa, token_map, input_text_path, output_token_path):
    with open(input_text_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    tokens = []
    for line in lines:
        result = simulate_dfa_on_line(dfa, token_map, line)
        tokens.append(result)

    with open(output_token_path, 'w') as out:
        for lexeme, token in tokens:
            out.write(f"<{lexeme}, {token}>\n")


# def run_lexer(dfa, token_map, input_text_path, output_token_path):
#     with open(input_text_path, 'r') as f:
#         text = f.read().replace('\n', '')

#     tokens = simulate_dfa_on_text(dfa, token_map, text)

#     with open(output_token_path, 'w') as out:
#         for lexeme, token in tokens:
#             out.write(f"<{lexeme}, {token}>\n")
