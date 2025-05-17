import regular_expression as re
import syntax_tree as st
from syntax_tree import build_afd

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

if __name__ == "__main__":
    main()