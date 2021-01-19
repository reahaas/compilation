import sys

from sly import Parser

from maman_14.tree_summing_lexer import TreeSummingLexer, print_err


def size_of_tree(tree):
    if type(tree) == int:
        return 1

    return 1 + sum([size_of_tree(son) for son in tree])


def sum_parity_tree(tree_list, parity):
    # if not tree_list:
    #     return 0
    # if len(tree_list) == 1 and tree_list[0] is None:
    #     return 1
    return sum([son for son in tree_list if son % 2 == parity])


def sum_odd_tree(tree_list):
    ODD = 1
    return sum_parity_tree(tree_list, parity=ODD)


def sum_even_tree(tree_list):
    EVEN = 1
    return sum_parity_tree(tree_list, parity=EVEN)


class TreeSumming():
    def __init__(self, value, size):
        self.value = value
        self.size = size


class TreeSummingParser(Parser):
    # Get the token list from the lexer (required)
    tokens = TreeSummingLexer.tokens

    # Grammar rules and actions
    @_('tree')
    def S(self, p):
        return p.tree

    @_('IGNORE LPAREN tree_list RPAREN')
    def S(self, p):
        raise Exception("The head of the tree can't be of type IGNORE")

    @_('SUM_ODD LPAREN tree_list RPAREN')
    def tree(self, p):
        return sum_odd_tree(p.tree_list)

    @_('SUM_EVEN LPAREN tree_list RPAREN')
    def tree(self, p):
        return sum_even_tree(p.tree_list)

    @_('SIZE LPAREN tree_list RPAREN')
    def tree(self, p):
        return size_of_tree(p.tree_list)

    @_('IGNORE LPAREN tree_list RPAREN')
    def tree(self, p):
        return 0

    @_('NUMBER')
    def tree(self, p):
        return int(p.NUMBER)  # TreeSumming(value=p.NUMBER, size=1)

    @_('tree_list tree')
    def tree_list(self, p):
        return p.tree_list + [p.tree]

    @_('tree')
    def tree_list(self, p):
        return [p.tree]


def main(file_name):
    try:
        with open(file_name) as input_file:
            input_text = input_file.read()
    except IOError as e:
        print(f"can't read {file_name}")
        raise e

    lexer = TreeSummingLexer()
    parser = TreeSummingParser()

    # original_stdout = sys.stdout  # Save a reference to the original standard output

    file_name_w = file_name.rstrip(".txt") + ".par"
    with open(file_name_w, 'w') as f:
        # sys.stdout = f  # Change the standard output to the file we created.
        # for tok in lexer.tokenize(input_text):
        #     print('type=%r, value=%r' % (tok.type, tok.value))

        result = parser.parse(lexer.tokenize(input_text))
        print(result)
        print("Student: Rea Haas")

        # sys.stdout = original_stdout  # Reset the standard output to its original value


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
