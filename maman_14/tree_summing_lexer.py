import sys
from sys import stderr

from sly import Lexer


def print_err(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


class TreeSummingLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
        # keywords:
        SUM_ODD,
        SUM_EVEN,
        SIZE,
        IGNORE,

        # more tokens
        NUMBER,  # digit+ | digit+.digit*
        # COMMENT  # /* java style comments */

        # literals:
        LPAREN,
        RPAREN
    }


    # String containing ignored characters between tokens
    ignore = ' \t'

    # Other ignored patterns
    # ignore_comment
    ignore_comment = r'\/\*.*\*\/'

    # Regular expression rules for tokens

    # more tokens
    SUM_ODD = r"sum_odd"
    SUM_EVEN = r"sum_even"
    SIZE = r"size"
    IGNORE = r"ignore"
    NUMBER = r'\d+|\d\.\d* '

    # literals:
    LPAREN = r"\("
    RPAREN = r"\)"

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling rule
    def error(self, t):
        print_err("line: '{l}', Illegal character '{c}'".format(l=self.lineno, c=t.value[0]))
        self.index += 1


def main(file_name):
    try:
        with open(file_name) as input_file:
            input_text = input_file.read()
    except IOError as e:
        print(f"can't read {file_name}")
        raise e

    lexer = TreeSummingLexer()

    original_stdout = sys.stdout  # Save a reference to the original standard output

    file_name_w = file_name.rstrip(".txt") + ".tok"
    with open(file_name_w, 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.

        for tok in lexer.tokenize(input_text):
            print('type=%r, value=%r' % (tok.type, tok.value))
        print("Student: Rea Haas")

        sys.stdout = original_stdout  # Reset the standard output to its original value


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("The program expect a single parameter, which is the input file name")
        exit(1)
    file_name = sys.argv[1]
    if not file_name.endswith(".txt"):
        print(f"The input file name must ends with \".txt\" given: {file_name}")
        exit(1)

    main(file_name)
    print_err("Student: Rea Haas")
