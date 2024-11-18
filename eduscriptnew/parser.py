# parser.py

import ply.yacc as yacc
from lexer import tokens, build_lexer
import textwrap

# Each class represents a different construct in EduScript, 
# in a format of hierarchical representation 
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self): # __repr__ methods provide us the readable string representations of each node, helping in debugging and testing
        return f"Program(functions={self.functions})"

class FunctionDef(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"FunctionDef(name={self.name}, body={self.body})"

class Command(ASTNode):
    def __init__(self, command, args):
        self.command = command
        self.args = args

    def __repr__(self):
        return f"Command(command={self.command}, args={self.args})"

class IfStatement(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, if_body={self.if_body}, else_body={self.else_body})"

class RepeatLoop(ASTNode):
    def __init__(self, times, body):
        self.times = times
        self.body = body

    def __repr__(self):
        return f"RepeatLoop(times={self.times}, body={self.body})"

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall(name={self.name}, args={self.args})"

class ReturnStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ReturnStatement(expression={self.expression})"

class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp(op={self.op}, left={self.left}, right={self.right})"

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp(op={self.op}, operand={self.operand})"

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number(value={self.value})"

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name})"


# parsing rules
# defining the order in which operations are parsed, 
# resolving ambiguities in expressions
# OR has the lowest precedence.
# AND is higher.
# Equality operators (EQ, NEQ) come next.
# Relational operators (LT, LE, GT, GE).
# Arithmetic operators (PLUS, MINUS, MULTIPLY, DIVIDE).
# NOT has the highest precedence among defined operators.
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'NOT'),
)

def p_program(p):
    # a program consists of a list of function definitions
    # it creates a Program AST node with the list of functions
    '''program : function_def_list'''
    p[0] = Program(p[1])

def p_function_def_list(p):
    # a function_def_list can be extended by adding another function_def
    # it basically accumulates the deifinitions to a list
    '''function_def_list : function_def_list function_def
                         | function_def'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_function_def(p):
    # defininf a function with the function keyword, an identifier (name), empty parameters (), and a body enclosed in {}
    # it basically creates a FunctionDef AST Node with the functions name and body
    '''function_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE'''
    p[0] = FunctionDef(p[2], p[6])

def p_statement_list(p):
    # list of statements can be extended by adding another statement.
    # it basically ccumulates statements into a list
    '''statement_list : statement_list statement
                      | '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_statement(p):
    # a statement can be a command, an if statement, a loop, a function call, or a return statement
    '''statement : command_statement
                 | if_statement
                 | loop_statement
                 | function_call
                 | return_statement'''
    p[0] = p[1]

def p_command_statement(p):
    # robot command followed by arguments within () and terminated by a semicolon ;
    # it basically creates a Command AST node with the command name and its arguments
    '''command_statement : ROBOT_COMMAND LPAREN arguments RPAREN SEMICOLON'''
    p[0] = Command(p[1], p[3])

def p_if_statement(p):
    # an if keyword followed by a condition in (), a body in {}, and an optional else claus
    '''if_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_clause'''
    p[0] = IfStatement(p[3], p[6], p[8])

def p_else_clause(p):
    '''else_clause : ELSE LBRACE statement_list RBRACE
                   | '''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = None

def p_loop_statement(p):
    '''loop_statement : REPEAT LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = RepeatLoop(p[3], p[6])

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN arguments RPAREN SEMICOLON'''
    p[0] = FunctionCall(p[1], p[3])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ReturnStatement(p[2])

def p_expression_binop(p):
    # an expression combined with another expression via a binary operator
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_expression_unary(p):
    '''expression : NOT expression'''
    p[0] = UnaryOp(p[1], p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Number(p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = Identifier(p[1])

def p_expression_function_call(p):
    '''expression : function_call_expr'''
    p[0] = p[1]

def p_function_call_expr(p):
    '''function_call_expr : IDENTIFIER LPAREN arguments RPAREN'''
    p[0] = FunctionCall(p[1], p[3])

def p_arguments(p):
    '''arguments : arguments COMMA expression
                 | expression
                 | '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# Define ROBOT_COMMAND as a reserved word
def p_ROBOT_COMMAND(p):
    '''ROBOT_COMMAND : MOVEFORWARD
                     | MOVEBACKWARD
                     | TURNRIGHT
                     | TURNLEFT'''
    p[0] = p[1]

def traverse_ast(node, indent=0):
    spacer = '  ' * indent
    if isinstance(node, Program):
        print(f"{spacer}Program")
        for func in node.functions:
            traverse_ast(func, indent + 1)
    elif isinstance(node, FunctionDef):
        print(f"{spacer}FunctionDef: {node.name}")
        for stmt in node.body:
            traverse_ast(stmt, indent + 1)
    elif isinstance(node, Command):
        print(f"{spacer}Command: {node.command}, Args: {node.args}")
    elif isinstance(node, IfStatement):
        print(f"{spacer}IfStatement:")
        traverse_ast(node.condition, indent + 1)
        print(f"{spacer}  If Body:")
        for stmt in node.if_body:
            traverse_ast(stmt, indent + 2)
        if node.else_body:
            print(f"{spacer}  Else Body:")
            for stmt in node.else_body:
                traverse_ast(stmt, indent + 2)
    elif isinstance(node, RepeatLoop):
        print(f"{spacer}RepeatLoop: {node.times}")
        for stmt in node.body:
            traverse_ast(stmt, indent + 1)
    elif isinstance(node, FunctionCall):
        print(f"{spacer}FunctionCall: {node.name}, Args: {node.args}")
    elif isinstance(node, Number):
        print(f"{spacer}Number: {node.value}")
    elif isinstance(node, Identifier):
        print(f"{spacer}Identifier: {node.name}")
    else:
        print(f"{spacer}Unknown node type: {type(node)}")


# Build the parser
def build_parser():
    lexer = build_lexer()
    return yacc.yacc()

# At the end of parser.py
if __name__ == "__main__":
    parser = build_parser()
    data = textwrap.dedent('''\
        function main() {
            moveForward(10);
            if (detectObstacle()) {
                turnRight(90);
            } else {
                moveForward(5);
            }
            repeat(3) {
                moveBackward(5);
            }
        }
    ''')
    ast = parser.parse(data)
    if ast:
        traverse_ast(ast)
    else:
        print("Parsing failed.")
