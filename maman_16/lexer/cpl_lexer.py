# Author: Rea Haas
# This file is a CPL lexical analyzer (cla).
# It is the requirements for maman 12 question 1.
import sys
from sys import stderr

from sly import Lexer


def print_err(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


class CplLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
        # keywords:
        BREAK,
        CASE,
        DEFAULT,
        ELSE,
        FLOAT,
        IF,
        INPUT,
        INT,
        OUTPUT,
        STATIC_CAST,
        SWITCH,
        WHILE,

        # operators:
        RELOP,  # == | != | < | > | >= | <=
        ADDOP,  # + | -
        MULOP,  # * | /
        OR,  # ||
        AND,  # &&
        NOT,  # !
        CAST,  # static_cast<int> static_cast<float>

        # more tokens
        ID,  # letter(letter|digit)*
        NUM,  # digit+ | digit+.digit*
        # COMMENT  # /* java style comments */
    }

    literals = {
        '(',
        ')',
        '{',
        '}',
        ',',
        ':',
        ';',
        '='
    }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Other ignored patterns
    # ignore_comment
    ignore_comment = r'\/\*.*\*\/'

    # Regular expression rules for tokens

    # more tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUM = r'\d+ |\d\.\d* '

    # keywords:
    ID['break'] = BREAK
    ID['case'] = CASE
    ID['default'] = DEFAULT
    ID['else'] = ELSE
    ID['float'] = FLOAT
    ID['if'] = IF
    ID['input'] = INPUT
    ID['int'] = INT
    ID['output'] = OUTPUT
    ID['static_cast'] = STATIC_CAST
    ID['switch'] = SWITCH
    ID['while'] = WHILE

    # operators:
    RELOP = r'==|!=|<|>|>=|<='
    ADDOP = r'\+|-'
    MULOP = r'\*|/'
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'!'
    CAST = r'static_cast<int>|static_cast<float>'

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

    lexer = CplLexer()

    original_stdout = sys.stdout  # Save a reference to the original standard output

    file_name_w = file_name.rstrip(".ou") + ".tok"
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
    if not file_name.endswith(".ou"):
        print(f"The input file name must ends with \".ou\" given: {file_name}")
        exit(1)

    main(file_name)
    print_err("Student: Rea Haas")
