from sly import Parser

from maman_16.lexer.cpl_lexer import CplLexer, print_err
from maman_16.parser.consts import QUAD_OPCODES, RELOP


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


class BoolListsObject():
    def __init__(self, next_list, true_list, false_list, break_list):
        self.next_list = next_list
        self.true_list = true_list
        self.false_list = false_list
        self.break_list = break_list



temp_variables_values_dict = {}
variables_type_dict = {}
BACKPATCH = "__"

qaud_lineno = 1

qaud_code_structure = []


def qaud_code(code_operation):
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
        qaud_code_structure.append(code_operation)
        # print(code_operation)
        global qaud_lineno
        qaud_lineno += 1


def cast_type(expression, to_type):
    if to_type not in ["int", "float"]:
        parser_error(f"coding error, can't cast to value: {to_type}", expression)
        raise

    # If there is no need for casting, return the original expression.
    if expression.type == to_type:
        return expression

    convert_opcode = "RTOI" if to_type == "int" else "ITOR"
    temp = next(g_generate_temp_variable_name)
    qaud_code(f"{convert_opcode} {temp} {expression.temp}")

    return Expression(to_type, temp)


def backpatch(instructions_list, jump_value):
    for instructions in instructions_list:
        asdf = qaud_code_structure[instructions - 1]
        qaud_code_structure[instructions - 1] = qaud_code_structure[instructions - 1].replace(f"{BACKPATCH}", str(jump_value))


def get_type_first_second_of_binary_operation(first_expression, second_expression):
    """
    This function take two Expressions objects, and detect the type of the return value:
    1. int & int: int
    2. int & float or float & int: float
    :param first_expression:
    :param second_expression:
    :return: A tuple of three elemets:
             1. num_type: the type of the value of the operations: int or float.
             2. first: Expression object, that is the given first or a converted value of it.
             3. second: Expression object, that is the given second or a converted value of it.
    """
    if first_expression.type == second_expression.type:
        num_type = first_expression.type
        first, second = first_expression.temp, second_expression.temp
    else:
        num_type = "float"
        if first_expression.type == "int":
            to_convert = cast_type(first_expression, "float").temp
            first, second = to_convert, second_expression.temp
        else:
            to_convert = cast_type(second_expression, "float").temp
            first, second = first_expression.temp, to_convert
    return num_type, first, second


def I_for_int_R_for_float(num_type):
    return "I" if num_type == "int" else "R"


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
        for line in qaud_code_structure:
            print(line)

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
        # return empty lists
        return BoolListsObject([], [], [], [])

    @_("input_stmt")
    def stmt(self, p):
        # return empty lists
        return BoolListsObject([], [], [], [])

    @_("output_stmt")
    def stmt(self, p):
        return BoolListsObject([], [], [], [])

    @_("if_stmt M")
    def stmt(self, p):
        backpatch(p.if_stmt.next_list, p.M)
        return p.if_stmt

    @_("while_stmt M")
    def stmt(self, p):
        backpatch(p.while_stmt.next_list, p.M)
        return p.while_stmt

    @_("switch_stmt")
    def stmt(self, p):
        pass

    @_("break_stmt")
    def stmt(self, p):
        return p.break_stmt

    @_("stmt_block")
    def stmt(self, p):
        return p.stmt_block

    @_("ID '=' expression ';'")
    def assignment_stmt(self, p):
        if p.ID not in variables_type_dict:
            parser_error(f"Variable not defined: {p.ID}", p)
        elif variables_type_dict[p.ID] == p.expression.type:
            opdoce = "IASN" if variables_type_dict[p.ID] == "int" else "RASN"
            qaud_code(f"{opdoce} {p.ID} {p.expression.temp}")
        elif variables_type_dict[p.ID] == "float":
            if p.expression.type == "int":
                convert_opcode = "ITOR"
                temp_real = next(g_generate_temp_variable_name)
                qaud_code(f"{convert_opcode} {temp_real} {p.expression.temp}")
            else:
                temp_real = p.expression.temp
            qaud_code(f"RASN {p.ID} {temp_real}")
        else:
            parser_error(f"Can't assign float value {p.expression.temp} to int variable {p.ID}", p)

    @_("INPUT '(' ID ')' ';'")
    def input_stmt(self, p):
        if p.ID not in variables_type_dict:
            parser_error(f"Variable not defined: {p.ID}")
        else:
            opdoce = "IINP" if variables_type_dict[p.ID] == "int" else "RINP"
            qaud_code(f"{opdoce} {p.ID}")

    @_("OUTPUT '(' expression ')' ';'")
    def output_stmt(self, p):
        opdoce = "IPRT" if p.expression.type == "int" else "RPRT"
        value = temp_variables_values_dict[p.expression.temp]
        qaud_code(f"{opdoce} {value}")

    # Good link for backpatching:
    # Credit giving: I used this with some adjustment to implement my code.
    # https://www.ques10.com/p/9481/explain-back-patching-with-an-example-1/?
    @_("IF '(' boolexpr ')' M stmt N ELSE M stmt")
    def if_stmt(self, p):
        # Notice!:
        # I swapped the true_list/false_list backpatching from the guide I pasted,
        # since the jump commands in the QAUD language not working as:
        #     if boolexpr then goto ADDRESS_TRUE;
        #     goto ADDRESS_FALSE;
        # but they working as:
        #     JMPZ ADDRESS_FALSE boolexpr
        #     JUMP ADDRESS_TRUE
        backpatch(p.boolexpr.true_list, p.M0)
        backpatch(p.boolexpr.false_list, p.M1)
        next_list = p.N.next_list + p.stmt0.next_list + p.stmt1.next_list

        # To support BREAK statements:
        break_list = p.stmt0.break_list + p.stmt1.break_list

        return BoolListsObject(next_list, [], [], break_list)

    @_("")
    def M(self, p):
        return qaud_lineno

    @_("")
    def N(self, p):
        current_quad_lineno = qaud_lineno
        qaud_code(f'JUMP {BACKPATCH}')
        return BoolListsObject([current_quad_lineno], [], [], [])

    @_("WHILE M '(' boolexpr ')' M stmt")
    def while_stmt(self, p):
        backpatch(p.stmt.next_list, p.M0)
        backpatch(p.boolexpr.true_list, p.M1)
        # To support BREAK statements:
        backpatch(p.stmt.break_list, p.M0)

        qaud_code(f"JUMP {p.M0}")
        return BoolListsObject(p.boolexpr.false_list, [], [], [])

    @_("SWITCH '(' expression ')' '{' caselist DEFAULT ':' stmtlist '}'")
    def switch_stmt(self, p):
        pass

    @_("caselist CASE NUM ':' stmtlist")
    def caselist(self, p):
        pass

    @_("")  # epsilon
    def caselist(self, p):
        pass

    @_("N BREAK ';'")
    def break_stmt(self, p):
        return BoolListsObject([], [], [], p.N.next_list)

    @_("'{' stmtlist '}'")
    def stmt_block(self, p):
        return p.stmtlist

    @_("stmtlist M stmt")
    def stmtlist(self, p):
        backpatch(p.stmtlist.next_list, p.M)

        # To support BREAK statements:
        break_list = p.stmtlist.break_list + p.stmt.break_list

        return BoolListsObject(p.stmt.next_list,
                               p.stmt.true_list,
                               p.stmt.false_list,
                               break_list)

    @_("")  # epsilon
    def stmtlist(self, p):
        # return empty lists
        return BoolListsObject([], [], [], [])

    @_("boolexpr OR M boolterm")
    def boolexpr(self, p):
        backpatch(p.boolexpr.false_list, p.M)

        true_list = p.boolexpr.true_list + p.boolterm.true_list
        false_list = p.boolterm.false_list
        return BoolListsObject([], true_list, false_list, [])

    @_("boolterm")
    def boolexpr(self, p):
        return p.boolterm

    @_("boolterm AND M boolfactor")
    def boolterm(self, p):
        backpatch(p.boolterm.true_list, p.M)

        true_list = p.boolfactor.true_list
        false_list = p.boolterm.false_list + p.boolfactor.false_list
        return BoolListsObject([], true_list, false_list, [])


    @_("boolfactor")
    def boolterm(self, p):
        return p.boolfactor

    @_("NOT '(' boolexpr ')'")
    def boolfactor(self, p):
        return BoolListsObject([], p.boolexpr.false_list, p.boolexpr.true_list, [])

    @_("expression RELOP expression")
    def boolfactor(self, p):

        num_type, first, second = get_type_first_second_of_binary_operation(p.expression0, p.expression1)

        temp_bool = next(g_generate_temp_variable_name)
        opcode_type = I_for_int_R_for_float(num_type)
        opcode_relation = RELOP[p.RELOP]
        opcode = opcode_type + opcode_relation
        qaud_code(f"{opcode} {temp_bool} {first} {second}")

        false_list = [qaud_lineno]
        true_list = [qaud_lineno + 1]
        return_list = BoolListsObject([], true_list, false_list, [])

        qaud_code(f"JMPZ {BACKPATCH} {temp_bool}")  # {false_list}
        qaud_code(f"JUMP {BACKPATCH}")  # {true_list}

        return return_list


    @_("expression ADDOP term")
    def expression(self, p):
        """
        Each expression return the type and a name of a temporary variable to save the data to.
        :param p:
        :return:
        """
        num_type, first, second = get_type_first_second_of_binary_operation(p.expression, p.term)

        opcode_type = I_for_int_R_for_float(num_type)
        opcode_action = "ADD" if p.ADDOP == "+" else "SUB"
        opcode = opcode_type + opcode_action

        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = temp

        qaud_code(f"{opcode} {temp} {first} {second}")
        return Expression(num_type, temp)

    @_("term")
    def expression(self, p):
        return p.term

    @_("term MULOP factor")
    def term(self, p):

        first_expression = p.term
        second_expression = p.factor
        first, num_type, second = get_type_first_second_of_binary_operation(first_expression, second_expression)

        opcode_type = I_for_int_R_for_float(num_type)
        opcode_action = "MLT" if p.MULOP == "*" else "DIV"
        opcode = opcode_type + opcode_action

        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = temp

        qaud_code(f"{opcode} {temp} {first} {second}")
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
        qaud_code(f"{opdoce} {temp} {value}")
        return Expression(num_type, temp)

    @_("NUM")
    def factor(self, p):
        num_type = "float" if "." in p.NUM else "int"
        value = int(p.NUM) if num_type == "int" else float(p.NUM)
        temp = next(g_generate_temp_variable_name)
        temp_variables_values_dict[temp] = value

        opdoce = "IASN" if num_type == "int" else "RASN"
        qaud_code(f"{opdoce} {temp} {value}")
        return Expression(num_type, temp)
