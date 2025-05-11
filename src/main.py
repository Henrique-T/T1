import regular_expression as re
import syntax_tree as st

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
        print(i.to_postfix(i.pattern))

    print("\nStack")
    for i in regular_expressions:
        tree = st.SyntaxTree(i.to_postfix(i.pattern))
        print(tree.build_syntax_tree().symbol)

if __name__ == "__main__":
    main()