import regular_expression as re

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

    print("")
    print("VALIDATION")
    print("")

    for i in regular_expressions:
        print(i.to_postfix(i.pattern))

if __name__ == "__main__":
    main()