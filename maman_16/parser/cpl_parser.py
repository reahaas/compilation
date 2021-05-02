from sly import Parser

from maman_16.lexer.cpl_lexer import CplLexer, print_err
from maman_16.parser.consts import QUAD_OPCODES


def parser_error(message, p):
    print_err(f"PARSER error: line number: {p.lineno}, {message}, {p}")


class expression():
    def __init__(self, type, value):
        self.type = type
        self.value = value


variables_type_dict = {}


def quad_code(code_operation):
    """
    This method warp the print function to prints the code operation that we want to generate.
    :param code_operation:
    :return:
    """
    def validate_quad_syntax():
        if type(code_operation) is not str:
            print_err("code_operation should be string")
            return False
        elif len(code_operation.split()) > 3:
            print_err("code_operation can't be longer than 3 words")
            return False
        elif code_operation.split()[0] not in QUAD_OPCODES:
            print_err(f"OPCODE {code_operation.split()[0]} is not define")
            return False
        else:
            return True

    if validate_quad_syntax():
        print(code_operation)


class CplParser(Parser):
    """
    This class parse the CPL language defined in maman_16.

    The translation scheme is:

    Built features:
    value: The value of the tree.
    size: The size of the tree.

    Inherited features:
    None
    """

    # Get the token list from the lexer (required)
    tokens = CplLexer.tokens

    # tokens.union(CplLexer.literals)
    # literals = CplLexer.literals

    @_("declarations stmt_block")
    def program(self, p):
        # todo remove the print.
        print(f"declarations: {variables_type_dict}")

    @_("declarations declaration")
    def declarations(self, p):
        pass

    @_("")  # epsilon
    def declarations(self, p):
        pass

    @_("idlist ':' type ';'")
    def declaration(self, p):
        if p.type in ["int", "float"]:
            variable_type = p.type
        else:
            parser_error(f"type is not defined: {p.type}", p)
            return

        for id in p.idlist:
            if id not in variables_type_dict:
                variables_type_dict[id] = variable_type
            else:
                parser_error("variable already declared, can't declare it again.")

    @_("INT")
    def type(self, p):
        return "int"

    @_("FLOAT")
    def type(self, p):
        return "float"

    @_("idlist ',' ID")
    def idlist(self, p):
        return p.idlist + [p.ID]

    @_("ID")
    def idlist(self, p):
        return [p.ID]

    @_("assignment_stmt")
    def stmt(self, p):
        pass

    @_("input_stmt")
    def stmt(self, p):
        pass

    @_("output_stmt")
    def stmt(self, p):
        pass

    @_("if_stmt")
    def stmt(self, p):
        pass

    @_("while_stmt")
    def stmt(self, p):
        pass

    @_("switch_stmt")
    def stmt(self, p):
        pass

    @_("break_stmt")
    def stmt(self, p):
        pass

    @_("stmt_block")
    def stmt(self, p):
        pass

    @_("ID '=' expression ';'")
    def assignment_stmt(self, p):
        if p.ID not in variables_type_dict:
            print_err(f"Variable not defined: {p.ID}")
        elif variables_type_dict[p.ID] == p.expression.type:
            opdoce = "IASN" if variables_type_dict[p.ID] == "int" else "RASN"
            quad_code(f"{opdoce} {p.ID} {p.expression.value}")
        elif variables_type_dict[p.ID] == "float":
            quad_code(f"IASN {p.ID} {float(p.expression.value)}")
        else:
            print_err(f"Can't assign float value {p.expression.value} to int variable {p.ID}")

    @_("INPUT '(' ID ')' ';'")
    def input_stmt(self, p):
        if p.ID not in variables_type_dict:
            print_err(f"Variable not defined: {p.ID}")
        else:
            opdoce = "IINP" if variables_type_dict[p.ID] == "int" else "RINP"
            quad_code(f"{opdoce} {p.ID}")

    @_("OUTPUT '(' expression ')' ';'")
    def output_stmt(self, p):
        pass

    @_("IF '(' boolexpr ')' stmt ELSE stmt")
    def if_stmt(self, p):
        pass

    @_("WHILE '(' boolexpr ')' stmt")
    def while_stmt(self, p):
        pass

    @_("SWITCH '(' expression ')' '{' caselist DEFAULT ':' stmtlist '}'")
    def switch_stmt(self, p):
        pass

    @_("caselist CASE NUM ':' stmtlist")
    def caselist(self, p):
        pass

    @_("")  # epsilon
    def caselist(self, p):
        pass

    @_("BREAK ';'")
    def break_stmt(self, p):
        pass

    @_("'{' stmtlist '}'")
    def stmt_block(self, p):
        pass

    @_("stmtlist stmt")
    def stmtlist(self, p):
        pass

    @_("")  # epsilon
    def stmtlist(self, p):
        pass

    @_("boolexpr OR boolterm")
    def boolexpr(self, p):
        pass

    @_("boolterm")
    def boolexpr(self, p):
        pass

    @_("boolterm AND boolfactor")
    def boolterm(self, p):
        pass

    @_("boolfactor")
    def boolterm(self, p):
        pass

    @_("NOT '(' boolexpr ')'")
    def boolfactor(self, p):
        pass

    @_("expression RELOP expression")
    def boolfactor(self, p):
        pass

    @_("expression ADDOP term")
    def expression(self, p):
        pass

    @_("term")
    def expression(self, p):
        pass

    @_("term MULOP factor")
    def term(self, p):
        pass

    @_("factor")
    def term(self, p):
        pass

    @_("'(' expression ')'")
    def factor(self, p):
        pass

    @_("CAST '(' expression ')'")
    def factor(self, p):
        pass

    @_("ID")
    def factor(self, p):
        pass

    @_("NUM")
    def factor(self, p):
        pass
