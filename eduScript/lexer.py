# lexer.py

import ply.lex as lex
import textwrap

# List of token names
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

# Reserved keywords
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
    'pickUpObject': 'PICKUPOBJECT',
    'dropObject': 'DROPOBJECT',
    #'detectObstacle': 'DETECTOBSTACLE',
    #'measureDistance': 'MEASUREDISTANCE'
}

tokens += list(reserved.values())

# Regular expression rules for simple tokens
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

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, column {find_column(t.lexer.lexdata, t)}")
    t.lexer.skip(1)

# Function to find the column number
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

# Build the lexer
def build_lexer():
    return lex.lex()

# Test the lexer
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
                pickUpObject();
                moveBackward(5);
            }
        }
        ''')

    lexer.input(data)
    for tok in lexer:
        column = find_column(data, tok)
        print(f"LexToken({tok.type},{tok.value!r},{tok.lineno},{column})")
