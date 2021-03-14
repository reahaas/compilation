from sly import Parser

from maman_16.lexer.cpl_lexer import CplLexer


class TreeSummingParser(Parser):
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



    @_("declarations stmt_block")
    def program(self, p):
        pass

    @_("declarations declaration")
    def declarations(self, p):
        pass

    @_("")  # epsilon
    def declarations(self, p):
        pass

    @_("idlist : type ;")
    def declaration(self, p):
        pass

    @_("INT")
    def type(self, p):
        pass

    @_("FLOAT")
    def type(self, p):
        pass

    @_("idlist , ID")
    def idlist(self, p):
        pass

    @_("ID")
    def idlist(self, p):
        pass

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
    @_("ID = expression ;")
    def assignment_stmt(self, p):
        pass

    @_("INPUT ( ID ) ;")
    def input_stmt(self, p):
        pass

    @_("OUTPUT ( expression ) ;")
    def output_stmt(self, p):
        pass

    @_("IF ) boolexpr ( stmt ELSE stmt")
    def if_stmt(self, p):
        pass

    @_("WHILE ) boolexpr ( stmt")
    def while_stmt(self, p):
        pass

    @_("SWITCH ( expression ) { caselist DEFAULT ':' stmtlist '}'")
    def switch_stmt(self, p):
        pass

    @_("caselist CASE NUM : stmtlist")
    def caselist(self, p):
        pass

    @_("")  # epsilon
    def caselist(self, p):
        pass

    @_("BREAK ;")
    def break_stmt(self, p):
        pass

    @_("{ stmtlist }")
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
    @_("NOT ( boolexpr )")
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
    @_("( expression )")
    def factor(self, p):
        pass

    @_("CAST ( expression )")
    def factor(self, p):
        pass

    @_("ID")
    def factor(self, p):
        pass

    @_("NUM")
    def factor(self, p):
        pass
