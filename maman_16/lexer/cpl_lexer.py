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

    # operators:
    RELOP = r'==|!=|>=|<=|<|>'
    ADDOP = r'\+|-'
    MULOP = r'\*|/'
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'!'
    CAST = r'static_cast<int>|static_cast<float>'

    # more tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUM = r'\d+(\.\d*)?'

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
    ID['switch'] = SWITCH
    ID['while'] = WHILE


    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling rule
    def error(self, t):
        print_err("LEXER error: line: '{l}', Illegal character '{c}'".format(l=self.lineno, c=t.value[0]))
        self.index += 1
