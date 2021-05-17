import sys

from maman_16.lexer.cpl_lexer import CplLexer, print_err
from maman_16.parser.cpl_parser import CplParser

cpl_file_suffix = ".ou"


def strip_end(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def main(file_name):
    try:
        with open(file_name) as input_file:
            input_text = input_file.read()
    except IOError as e:
        print(f"can't read {file_name}")
        raise e

    lexer = CplLexer()
    parser = CplParser()

    original_stdout = sys.stdout  # Save a reference to the original standard output

    file_name_w = strip_end(file_name, cpl_file_suffix) + ".par"
    with open(file_name_w, 'w') as f:
        sys.stdout = f  # Change the standard output to the file we created.

        result = parser.parse(lexer.tokenize(input_text))
        # f.write(f"Results: {str(result)}")
        f.write("HALT\n")
        f.write("Student: Rea Haas")

        sys.stdout = original_stdout  # Reset the standard output to its original value
        print(result)
        print("Student: Rea Haas")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("The program expect a single parameter, which is the input file name")
        exit(1)
    file_name = sys.argv[1]
    if not file_name.endswith(cpl_file_suffix):
        print(f"The input file name must ends with \"{cpl_file_suffix}\" given: {file_name}")
        exit(1)

    main(file_name)
    print_err("Student: Rea Haas")
