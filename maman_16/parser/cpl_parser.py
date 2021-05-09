from sly import Parser

from maman_16.lexer.cpl_lexer import CplLexer, print_err
from maman_16.parser.consts import QUAD_OPCODES


def parser_error(message, p):
    line_number = p.lineno if hasattr(p, "lineno") else "compilier code"
    print_err(f"PARSER error: line number: {line_number}, {message}, {p}")


def generate_temp_variable_name():
    """
    A generator for temporary variable names.
    :str return: a new temp variable name.
    """
    counter = 0
    while True:
        counter += 1
        yield f"t_{counter}"


g_generate_temp_variable_name = generate_temp_variable_name()


class Expression():
    def __init__(self, type, temp):
        self.type = type
        self.temp = temp


temp_variables_values_dict = {}
variables_type_dict = {}


def quad_code(code_operation):
    """
    This method warp the print function to prints the code operation that we want to generate.
    :param code_operation:
    :return:
    """
    def validate_quad_syntax():
        if type(code_operation) is not str:
            parser_error("code_operation should be string", code_operation)
            return False
        elif len(code_operation.split()) > 4:
            parser_error("code_operation can't be longer than 4 words", code_operation)
            return False
        elif code_operation.split()[0] not in QUAD_OPCODES:
            parser_error(f"OPCODE {code_operation.split()[0]} is not define", code_operation)
            return False
        else:
            return True

    if validate_quad_syntax():
        print(code_operation)


def cast_type(expression, to_type):
    if to_type not in ["int", "float"]:
        parser_error(f"coding error, can't cast to value: {to_type}", expression)
        raise

    # If there is no need for casting, return the original expression.
    if expression.type == to_type:
        return expression

    convert_opcode = "RTOI" if to_type == "int" else "ITOR"
    temp = next(g_generate_temp_variable_name)
    quad_code(f"{convert_opcode} {temp} {expression.temp}")

    return Expression(to_type, temp)


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
        #print(f"declarations: {variables_type_dict}")
        pass

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
                parser_error("variable already declared, can't declare it again.", id)

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
            parser_error(f"Variable not defined: {p.ID}", p)
        elif variables_type_dict[p.ID] == p.expression.type:
            opdoce = "IASN" if variables_type_dict[p.ID] == "int" else "RASN"
            quad_code(f"{opdoce} {p.ID} {p.expression.temp}")
        elif variables_type_dict[p.ID] == "float":
            if p.expression.type == "int":
                convert_opcode = "ITOR"
                temp_real = next(g_generate_temp_variable_name)
                quad_code(f"{convert_opcode} {temp_real} {p.expression.temp}")
            else:
                temp_real = p.expression.temp
            quad_code(f"RASN {p.ID} {temp_real}")
        else:
            parser_error(f"Can't assign float value {p.expression.temp} to int variable {p.ID}", p)

    @_("INPUT '(' ID ')' ';'")
    def input_stmt(self, p):
        if p.ID not in variables_type_dict:
            parser_error(f"Variable not defined: {p.ID}")
        else:
            opdoce = "IINP" if variables_type_dict[p.ID] == "int" else "RINP"
            quad_code(f"{opdoce} {p.ID}")

    @_("OUTPUT '(' expression ')' ';'")
    def output_stmt(self, p):
        opdoce = "IPRT" if p.expression.type == "int" else "RPRT"
        value = temp_variables_values_dict[p.expression.temp]
        quad_code(f"{opdoce} {value}")

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
        """
        Each expression return the type and a name of a temporary variable to save the data to.
        :param p:
        :return:
        """
        if p.expression.type == p.term.type:
            num_type = p.expression.type
            first, second = p.expression.temp, p.term.temp
        else:
            num_type = "float"
            if p.expression.type == "int":
                to_convert = cast_type(p.expression, "float").temp
                first, second = to_convert, p.term.temp
            else:
                to_convert = cast_type(p.term, "float").temp
                first, second = p.expression.temp, to_convert

        opcode_type = "I" if num_type == "int" else "R"
        opcode_action = "ADD" if p.ADDOP == "+" else "SUB"
        opcode = opcode_type + opcode_action

        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = temp

        quad_code(f"{opcode} {temp} {first} {second}")
        return Expression(num_type, temp)

    @_("term")
    def expression(self, p):
        return p.term

    @_("term MULOP factor")
    def term(self, p):
        if p.term.type == p.factor.type:
            num_type = p.term.type
            first, second = p.term.temp, p.factor.temp
        else:
            num_type = "float"
            if p.term.type == "int":
                to_convert = cast_type(p.term, "float").temp
                first, second = to_convert, p.factor.temp
            else:
                to_convert = cast_type(p.factor, "float").temp
                first, second = p.term.temp, to_convert

        opcode_type = "I" if num_type == "int" else "R"
        opcode_action = "MLT" if p.MULOP == "*" else "DIV"
        opcode = opcode_type + opcode_action

        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = temp

        quad_code(f"{opcode} {temp} {first} {second}")
        return Expression(num_type, temp)

    @_("factor")
    def term(self, p):
        return p.factor

    @_("'(' expression ')'")
    def factor(self, p):
        return p.expression

    @_("CAST '(' expression ')'")
    def factor(self, p):
        num_type = "int" if p.CAST =="static_cast<int>" else "float"
        return cast_type(p.expression, num_type)

    @_("ID")
    def factor(self, p):
        num_type = variables_type_dict[p.ID]

        value = p.ID
        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = value

        opdoce = "IASN" if num_type == "int" else "RASN"
        quad_code(f"{opdoce} {temp} {value}")
        return Expression(num_type, temp)

    @_("NUM")
    def factor(self, p):
        num_type = "float" if "." in p.NUM else "int"
        value = int(p.NUM) if num_type == "int" else float(p.NUM)
        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = value

        opdoce = "IASN" if num_type == "int" else "RASN"
        quad_code(f"{opdoce} {temp} {value}")
        return Expression(num_type, temp)
