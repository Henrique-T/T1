import regular_expression as re
import syntax_tree as st
import afn
import automaton_operations as ao
from lexer_simulation import run_lexer
from functools import reduce

INPUT_RE_FILE = "../example_input_RE.txt"

def main():
    regular_expressions = []
    try:
        with open(INPUT_RE_FILE, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if line:
                    print(f"Parsing line {line_number}: {line}")
                regular_expressions.append(re.RegularExpression.from_definition_line(line))
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_RE_FILE}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    names = []
    afns = []
    for i, regex in enumerate(regular_expressions):
        names.append(regex.name)
        postfix = regex.to_postfix(regex.pattern)
        tree = st.SyntaxTree(postfix)
        root = tree.build_syntax_tree()
        followpos = tree.compute_nullable_first_last_follow(root)
        afd = st.build_afd(root, followpos, tree.leaf_positions)
        afd.export_to_txt(f"../afd_output_{i}.txt")

    for i, name in enumerate(names):
        afns.append(afn.AFN.load_afd_from_file(f"../afd_output_{i}.txt", token_type=name))

    union_afn = reduce(lambda a1, a2: ao.AutomatonOperations.union(a1, a2), afns)
    afd, token_map = union_afn.to_afd()

    print("\nLexer Analysis")
    # print("DFA start state:", afd.start_state)
    # print("DFA accepting states:", afd.accept_states)
    # print("DFA transitions:")
    # for state, trans in afd.transitions.items():
    #     print(f"  From state {state}:")
    #     for symbol, target in trans.items():
    #         print(f"    On '{symbol}' -> {target}")

    run_lexer(afd, token_map, "../example_test_input.txt", "../token_list_output.txt")
    print("Token list written to: ../token_list_output.txt")


if __name__ == "__main__":
    main()