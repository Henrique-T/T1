

INPUT_RE_FILE = "../example_input_RE.txt"

def main():
    try:
        with open(INPUT_RE_FILE, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_RE_FILE}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()