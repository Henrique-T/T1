import re as re_

class RegularExpression:
    def __init__(self, name: str, pattern: str):
        self.name = name
        self.pattern = pattern.strip()
        #self.postfix = self.to_postfix(pattern)
    
    def __repr__(self):
        return f"<RegularExpression name='{self.name}' pattern='{self.pattern}'>"

    @staticmethod
    def from_definition_line(line: str):
        """
        Parses a line like 'id: [a-zA-Z]([a-zA-Z] | [0-9])*' into a RegularExpression object.
        """
        if ':' not in line:
            raise ValueError(f"Invalid regular expression definition: {line}")
        name, pattern = line.split(':', 1)
        return RegularExpression(name.strip(), pattern.strip())
    
    @staticmethod
    def is_operator(c):
        return c in {'|', '.', '*', '+', '?'}
    
    def is_operand(token):
        return (
            (token.startswith('[') and token.endswith(']'))  # character class
            or token.isalnum()  # single letter/digit
        )

    
    @staticmethod
    def precedence(op):
        if op in {'*', '+', '?'}:
            return 3
        elif op == '.':
            return 2
        elif op == '|':
            return 1
        return 0
    
    def starts_expr(token):
        return token in {'(',} or token.startswith('[') or token.isalnum()


    def add_concatenation_symbols(self, pattern):
        result = []
        i = 0

        def is_character_class(token):
            return len(token) >= 3 and token[0] == '[' and token[-1] == ']'

        def is_literal(token):
            return len(token) == 1 and token.isalnum()

        def is_operand(token):
            return (
                is_character_class(token)
                or is_literal(token)
                or token == ')'
            )

        def is_prefix(token):
            return token in ['*', '+', '?']

        def is_open_group(token):
            return token == '('

        def is_closing_group(token):
            return token == ')'

        def read_token():
            nonlocal i
            if pattern[i] == '[':
                j = i + 1
                while j < len(pattern) and pattern[j] != ']':
                    j += 1
                token = pattern[i:j + 1]
                i = j + 1
            else:
                token = pattern[i]
                i += 1
            return token

        tokens = []
        while i < len(pattern):
            tokens.append(read_token())

        output = []
        for j in range(len(tokens)):
            token = tokens[j]
            output.append(token)

            # Lookahead to decide if we should insert a concatenation
            if j + 1 < len(tokens):
                curr = token
                next_tok = tokens[j + 1]

                if (
                    (is_operand(curr) or is_closing_group(curr) or is_prefix(curr))
                    and (is_operand(next_tok) or is_open_group(next_tok))
                    and curr != '|'
                    and next_tok not in {'|', '*', '+', '?', ')'}
                ):
                    output.append('.')

        self.pattern = ''.join(output)
        transformed = ''.join(output)
        return transformed
    
    def to_postfix(self, pattern):
        pattern = self.add_concatenation_symbols(self.expand_character_classes(pattern))
        output = []
        stack = []
        for token in self.tokenize(pattern):
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # pop '('
            elif self.is_operator(token):
                while (stack and stack[-1] != '(' and
                       ((self.precedence(token) < self.precedence(stack[-1])) or
                        (self.precedence(token) == self.precedence(stack[-1]) and token != '*'))):
                    output.append(stack.pop())
                stack.append(token)
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def expand_character_classes(self, pattern):
        """Converts character ranges like [a-zA-Z] into (a|b|...|Z)"""
        def expand_class(match):
            chars = []
            content = match.group(1)
            i = 0
            while i < len(content):
                if i + 2 < len(content) and content[i+1] == '-':
                    start, end = content[i], content[i+2]
                    chars.extend([chr(c) for c in range(ord(start), ord(end)+1)])
                    i += 3
                else:
                    chars.append(content[i])
                    i += 1
            return '(' + '|'.join(chars) + ')'
        return re_.sub(r'\[([^\]]+)\]', expand_class, pattern)
    
    def tokenize(self, pattern):
        """Splits a pattern into tokens (characters, operators, parentheses)"""
        tokens = []
        i = 0
        while i < len(pattern):
            if pattern[i] in {'(', ')', '|', '*', '+', '?', '.'}:
                tokens.append(pattern[i])
                i += 1
            elif not pattern[i].isspace():  # skip space characters
                tokens.append(pattern[i])  # add non-space characters to the tokens
                i += 1               
            else:
                i += 1
        return tokens