import regular_expression as re
import syntax_tree as st
import afn
import automaton_operations as ao

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

    # Debug output of parsed regex objects
    print("\nParsed Regular Expressions:")
    for regex in regular_expressions:
        print(regex)

    print("\nPostfix notation")
    for i in regular_expressions:
        postfix = i.to_postfix(i.pattern)
        print(postfix)

    print("\nStack - root of syntax tree")
    for i in regular_expressions:
        postfix = i.to_postfix(i.pattern)
        tree = st.SyntaxTree(postfix)
        print(tree.build_syntax_tree().symbol)

    print("\nNullable, First, Last, Follow")
    for i in regular_expressions:
        postfix = i.to_postfix(i.pattern)
        tree = st.SyntaxTree(postfix)
        root = tree.build_syntax_tree()
        followpos = tree.compute_nullable_first_last_follow(root)
        print(followpos)

    print("\nAFD")
    for i in regular_expressions:
        postfix = i.to_postfix(i.pattern)
        tree = st.SyntaxTree(postfix)
        root = tree.build_syntax_tree()
        followpos = tree.compute_nullable_first_last_follow(root)
        afd = st.build_afd(root, followpos, tree.leaf_positions)
        print(afd)
    
    print("\nAFD export")
    for i in regular_expressions:
        postfix = i.to_postfix(i.pattern)
        tree = st.SyntaxTree(postfix)
        root = tree.build_syntax_tree()
        followpos = tree.compute_nullable_first_last_follow(root)
        afd = st.build_afd(root, followpos, tree.leaf_positions)
        afd.export_to_txt("../afd_output_%s.txt" % regular_expressions.index(i))

    print("\nUnion with epsilon")
    afn1 = afn.AFN.load_afd_from_file("../afd_output_0.txt")
    afn2 = afn.AFN.load_afd_from_file("../afd_output_1.txt")
    union_afn = ao.AutomatonOperations.union(afn1, afn2)
    print(union_afn)

    print("\nAFN to AFD")
    afn1 = afn.AFN.load_afd_from_file("../afd_output_0.txt")
    afn2 = afn.AFN.load_afd_from_file("../afd_output_1.txt")
    union_afn = ao.AutomatonOperations.union(afn1, afn2)
    afd = union_afn.to_afd()
    print(afd)


if __name__ == "__main__":
    main()