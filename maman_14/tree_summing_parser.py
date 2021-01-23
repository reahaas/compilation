import sys

from sly import Parser

from maman_14.tree_summing_lexer import TreeSummingLexer, print_err


def size_of_tree(tree):
    if type(tree) == TreeSumming:
        return tree.size

    return 1 + sum([size_of_tree(son) for son in tree])


def sum_parity_tree(tree_list, parity):
    # if not tree_list:
    #     return 0
    # if len(tree_list) == 1 and tree_list[0] is None:
    #     return 1
    return sum([son.value for son in tree_list if son.value % 2 == parity])


def sum_odd_tree(tree_list):
    ODD = 1
    return sum_parity_tree(tree_list, parity=ODD)


def sum_even_tree(tree_list):
    EVEN = 0
    return sum_parity_tree(tree_list, parity=EVEN)


class TreeSumming():
    def __init__(self, value, size):
        self.value = value
        self.size = size


class TreeSummingParser(Parser):
    """
    This class parse the summing tree defined in maman_14 question 2.
    The parsing define

    The translation scheme is:

    Built features:
    value: The value of the tree.
    size: The size of the tree.

    Inherited features:
    None

    0. S' -> S                       { if S.value == ignore:
                                           raise exception
                                       else:
                                           print(S.value)
                                     }

    1. S -> tree                     { S.value = tree.value
                                       S.size = tree.size
                                     }

    2. tree -> SUM_ODD ( treelist )  { tree.value = sum(tree.value for tree in treelist if
                                                        is_odd(tree.value))
                                       tree.size = sum(tree.size for tree in treelist)
                                     }

    3. tree -> SUM_EVEN ( treelist ) { tree.value = sum(tree.value for tree in treelist if
                                                        is_even(tree.value))
                                       tree.size = sum(tree.size for tree in treelist)
                                     }

    4. tree -> SIZE ( treelist )     { tree.value = sum(tree.size for tree in treelist)
                                       tree.size = sum(tree.size for tree in treelist)
                                     }

    5. tree -> IGNORE ( treelist )   { tree.value = 0
                                       tree.size = sum(tree.size for tree in treelist)
                                     }

    6. tree -> NUMBER                { tree.value = NUMBER.value
                                       tree.size = 1
                                     }

    7. treelist -> treelist_1 tree   { treelist.value = treelist_1 + [tree] }

    8. treelist -> tree              { treelist.value = [tree] }
    """

    # Get the token list from the lexer (required)
    tokens = TreeSummingLexer.tokens

    # Grammar rules and actions
    @_('tree')
    def S(self, p):
        return p.tree.value

    @_('IGNORE LPAREN tree_list RPAREN')
    def S(self, p):
        raise Exception("The head of the tree can't be of type IGNORE")

    @_('SUM_ODD LPAREN tree_list RPAREN')
    def tree(self, p):
        results = TreeSumming(value=sum_odd_tree(p.tree_list), size=size_of_tree(p.tree_list))
        print(f"value: {results.value}, size: {results.size}, "
              f"tree: {p.SUM_ODD + p.LPAREN + str([t. value for t in p.tree_list]) + p.RPAREN}")
        return results

    @_('SUM_EVEN LPAREN tree_list RPAREN')
    def tree(self, p):
        results = TreeSumming(value=sum_even_tree(p.tree_list), size=size_of_tree(p.tree_list))
        print(f"value: {results.value}, size: {results.size}, "
              f"tree: {p.SUM_EVEN + p.LPAREN + str([t.value for t in p.tree_list]) + p.RPAREN}")
        return results

    @_('SIZE LPAREN tree_list RPAREN')
    def tree(self, p):
        tree_list_size = size_of_tree(p.tree_list)
        print(f"value: {tree_list_size}, size: {tree_list_size}, "
              f"tree: {p.SIZE + p.LPAREN + str([t.value for t in p.tree_list]) + p.RPAREN}")
        return TreeSumming(value=tree_list_size, size=tree_list_size)

    @_('IGNORE LPAREN tree_list RPAREN')
    def tree(self, p):
        results = TreeSumming(value=0, size=size_of_tree(p.tree_list))
        print(f"value: {results.value}, size: {results.size}, "
              f"tree: {p.IGNORE + p.LPAREN + str([t.value for t in p.tree_list]) + p.RPAREN}")
        return results

    @_('NUMBER')
    def tree(self, p):
        return TreeSumming(value=int(p.NUMBER), size=1)

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

    original_stdout = sys.stdout  # Save a reference to the original standard output

    file_name_w = file_name.rstrip(".txt") + ".par"
    with open(file_name_w, 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.

        result = parser.parse(lexer.tokenize(input_text))
        f.write(f"Results: {str(result)}")

        sys.stdout = original_stdout  # Reset the standard output to its original value
        print(result)
        print("Student: Rea Haas")


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
