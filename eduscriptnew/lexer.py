# lexer.py

import ply.lex as lex
import textwrap

# listing all token types that the lexer will recognize.
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'SEMICOLON',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQ',
    'NEQ',
    'LT',
    'GT',
    'LE',
    'GE',
    'AND',
    'OR',
    'NOT'
]

# defined some specific keywords that have special meanings in EduScript these are also called Reserved keywords
reserved = {
    'function': 'FUNCTION',
    'if': 'IF',
    'else': 'ELSE',
    'repeat': 'REPEAT',
    'return': 'RETURN',
    'moveForward': 'MOVEFORWARD',
    'moveBackward': 'MOVEBACKWARD',
    'turnRight': 'TURNRIGHT',
    'turnLeft': 'TURNLEFT',
}

tokens += list(reserved.values()) #  appending the reserved keywords to the tokens list

# regular expression rules for simple tokens
# each token is associated with a regular expression that defines its pattern
# each line here is a definition to recognize a specific token
# example, t_PLUS = r'\+' tells the lexer to recognize the + symbol as a PLUS token
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_COMMA     = r','
t_SEMICOLON = r';'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_EQ        = r'=='
t_NEQ       = r'!='
t_LE        = r'<='
t_GE        = r'>='
t_LT        = r'<'
t_GT        = r'>'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'!'

def t_IDENTIFIER(t):
    # Matches any string that starts with a letter or underscore, followed by letters, digits, 
    # or underscores.
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # determine if the matched string is a reserved keyword. If so, assigns the corresponding token type; otherwise, treats it as an IDENTIFIER.
    return t

# matching integers (\d+) and floating-point numbers (\d+\.\d+).
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# matching one or more newline characters
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# characters to ignore during lexing. spaces and tabs are ignored.
t_ignore  = ' \t'

# catching any characters that do not match any defined token patterns
# it prints the illegal character along with its line and column number
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, column {find_column(t.lexer.lexdata, t)}")
    t.lexer.skip(1)

#  determining the column position of a token within the input string
# it searches for the last occurrence of a newline character before the token's position
# it subtracts the position of the last newline from the token's position to get the column number
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

# compiling the lexer with defined rules
def build_lexer():
    return lex.lex()

# testing the lexer
if __name__ == "__main__":
    lexer = build_lexer()
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

    lexer.input(data)
    for tok in lexer:
        column = find_column(data, tok)
        print(f"LexToken({tok.type},{tok.value!r},{tok.lineno},{column})")
