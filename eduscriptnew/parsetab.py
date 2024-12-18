
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftORleftANDleftEQNEQleftLTLEGTGEleftPLUSMINUSleftMULTIPLYDIVIDErightNOTAND COMMA DIVIDE ELSE EQ FUNCTION GE GT IDENTIFIER IF LBRACE LE LPAREN LT MINUS MOVEBACKWARD MOVEFORWARD MULTIPLY NEQ NOT NUMBER OR PLUS RBRACE REPEAT RETURN RPAREN SEMICOLON TURNLEFT TURNRIGHTprogram : function_def_listfunction_def_list : function_def_list function_def\n                         | function_deffunction_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACEstatement_list : statement_list statement\n                      | statement : command_statement\n                 | if_statement\n                 | loop_statement\n                 | function_call\n                 | return_statementcommand_statement : ROBOT_COMMAND LPAREN arguments RPAREN SEMICOLONif_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_clauseelse_clause : ELSE LBRACE statement_list RBRACE\n                   | loop_statement : REPEAT LPAREN expression RPAREN LBRACE statement_list RBRACEfunction_call : IDENTIFIER LPAREN arguments RPAREN SEMICOLONreturn_statement : RETURN expression SEMICOLONexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression MULTIPLY expression\n                  | expression DIVIDE expression\n                  | expression EQ expression\n                  | expression NEQ expression\n                  | expression LT expression\n                  | expression LE expression\n                  | expression GT expression\n                  | expression GE expression\n                  | expression AND expression\n                  | expression OR expressionexpression : NOT expressionexpression : LPAREN expression RPARENexpression : NUMBERexpression : IDENTIFIERexpression : function_call_exprfunction_call_expr : IDENTIFIER LPAREN arguments RPARENarguments : arguments COMMA expression\n                 | expression\n                 | ROBOT_COMMAND : MOVEFORWARD\n                     | MOVEBACKWARD\n                     | TURNRIGHT\n                     | TURNLEFT'
    
_lr_action_items = {'FUNCTION':([0,2,3,5,12,],[4,4,-3,-2,-4,]),'$end':([1,2,3,5,12,],[0,-1,-3,-2,-4,]),'IDENTIFIER':([4,9,10,13,14,15,16,17,18,22,27,28,29,30,32,33,42,43,44,45,46,47,48,49,50,51,52,53,54,57,59,77,79,80,81,83,84,85,86,87,89,90,91,],[6,-6,11,-5,-7,-8,-9,-10,-11,35,35,35,35,35,35,35,-18,35,35,35,35,35,35,35,35,35,35,35,35,35,35,-17,-12,-6,-6,11,11,-15,-16,-13,-6,11,-14,]),'LPAREN':([6,11,19,20,21,22,23,24,25,26,27,28,29,30,32,33,35,43,44,45,46,47,48,49,50,51,52,53,54,57,59,],[7,27,28,29,30,33,-40,-41,-42,-43,33,33,33,33,33,33,57,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'RPAREN':([7,27,28,34,35,36,37,38,39,40,41,55,56,57,63,64,65,66,67,68,69,70,71,72,73,74,75,76,78,82,],[8,-39,-39,-33,-34,-35,58,-38,60,61,62,-31,75,-39,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-32,82,-37,-36,]),'LBRACE':([8,61,62,88,],[9,80,81,89,]),'RBRACE':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,12,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,85,86,-15,-16,-13,-6,91,-14,]),'IF':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,20,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,20,20,-15,-16,-13,-6,20,-14,]),'REPEAT':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,21,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,21,21,-15,-16,-13,-6,21,-14,]),'RETURN':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,22,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,22,22,-15,-16,-13,-6,22,-14,]),'MOVEFORWARD':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,23,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,23,23,-15,-16,-13,-6,23,-14,]),'MOVEBACKWARD':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,24,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,24,24,-15,-16,-13,-6,24,-14,]),'TURNRIGHT':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,25,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,25,25,-15,-16,-13,-6,25,-14,]),'TURNLEFT':([9,10,13,14,15,16,17,18,42,77,79,80,81,83,84,85,86,87,89,90,91,],[-6,26,-5,-7,-8,-9,-10,-11,-18,-17,-12,-6,-6,26,26,-15,-16,-13,-6,26,-14,]),'NOT':([22,27,28,29,30,32,33,43,44,45,46,47,48,49,50,51,52,53,54,57,59,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'NUMBER':([22,27,28,29,30,32,33,43,44,45,46,47,48,49,50,51,52,53,54,57,59,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'COMMA':([27,28,34,35,36,37,38,39,55,57,63,64,65,66,67,68,69,70,71,72,73,74,75,76,78,82,],[-39,-39,-33,-34,-35,59,-38,59,-31,-39,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-32,59,-37,-36,]),'SEMICOLON':([31,34,35,36,55,58,60,63,64,65,66,67,68,69,70,71,72,73,74,75,82,],[42,-33,-34,-35,-31,77,79,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-32,-36,]),'PLUS':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[43,-33,-34,-35,43,43,43,-31,43,-19,-20,-21,-22,43,43,43,43,43,43,43,43,-32,43,-36,]),'MINUS':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[44,-33,-34,-35,44,44,44,-31,44,-19,-20,-21,-22,44,44,44,44,44,44,44,44,-32,44,-36,]),'MULTIPLY':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[45,-33,-34,-35,45,45,45,-31,45,45,45,-21,-22,45,45,45,45,45,45,45,45,-32,45,-36,]),'DIVIDE':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[46,-33,-34,-35,46,46,46,-31,46,46,46,-21,-22,46,46,46,46,46,46,46,46,-32,46,-36,]),'EQ':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[47,-33,-34,-35,47,47,47,-31,47,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,47,47,-32,47,-36,]),'NEQ':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[48,-33,-34,-35,48,48,48,-31,48,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,48,48,-32,48,-36,]),'LT':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[49,-33,-34,-35,49,49,49,-31,49,-19,-20,-21,-22,49,49,-25,-26,-27,-28,49,49,-32,49,-36,]),'LE':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[50,-33,-34,-35,50,50,50,-31,50,-19,-20,-21,-22,50,50,-25,-26,-27,-28,50,50,-32,50,-36,]),'GT':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[51,-33,-34,-35,51,51,51,-31,51,-19,-20,-21,-22,51,51,-25,-26,-27,-28,51,51,-32,51,-36,]),'GE':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[52,-33,-34,-35,52,52,52,-31,52,-19,-20,-21,-22,52,52,-25,-26,-27,-28,52,52,-32,52,-36,]),'AND':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[53,-33,-34,-35,53,53,53,-31,53,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,53,-32,53,-36,]),'OR':([31,34,35,36,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,75,78,82,],[54,-33,-34,-35,54,54,54,-31,54,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-32,54,-36,]),'ELSE':([85,],[88,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'function_def_list':([0,],[2,]),'function_def':([0,2,],[3,5,]),'statement_list':([9,80,81,89,],[10,83,84,90,]),'statement':([10,83,84,90,],[13,13,13,13,]),'command_statement':([10,83,84,90,],[14,14,14,14,]),'if_statement':([10,83,84,90,],[15,15,15,15,]),'loop_statement':([10,83,84,90,],[16,16,16,16,]),'function_call':([10,83,84,90,],[17,17,17,17,]),'return_statement':([10,83,84,90,],[18,18,18,18,]),'ROBOT_COMMAND':([10,83,84,90,],[19,19,19,19,]),'expression':([22,27,28,29,30,32,33,43,44,45,46,47,48,49,50,51,52,53,54,57,59,],[31,38,38,40,41,55,56,63,64,65,66,67,68,69,70,71,72,73,74,38,78,]),'function_call_expr':([22,27,28,29,30,32,33,43,44,45,46,47,48,49,50,51,52,53,54,57,59,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'arguments':([27,28,57,],[37,39,76,]),'else_clause':([85,],[87,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> function_def_list','program',1,'p_program','parser.py',111),
  ('function_def_list -> function_def_list function_def','function_def_list',2,'p_function_def_list','parser.py',115),
  ('function_def_list -> function_def','function_def_list',1,'p_function_def_list','parser.py',116),
  ('function_def -> FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statement_list RBRACE','function_def',7,'p_function_def','parser.py',123),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',127),
  ('statement_list -> <empty>','statement_list',0,'p_statement_list','parser.py',128),
  ('statement -> command_statement','statement',1,'p_statement','parser.py',135),
  ('statement -> if_statement','statement',1,'p_statement','parser.py',136),
  ('statement -> loop_statement','statement',1,'p_statement','parser.py',137),
  ('statement -> function_call','statement',1,'p_statement','parser.py',138),
  ('statement -> return_statement','statement',1,'p_statement','parser.py',139),
  ('command_statement -> ROBOT_COMMAND LPAREN arguments RPAREN SEMICOLON','command_statement',5,'p_command_statement','parser.py',143),
  ('if_statement -> IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_clause','if_statement',8,'p_if_statement','parser.py',147),
  ('else_clause -> ELSE LBRACE statement_list RBRACE','else_clause',4,'p_else_clause','parser.py',151),
  ('else_clause -> <empty>','else_clause',0,'p_else_clause','parser.py',152),
  ('loop_statement -> REPEAT LPAREN expression RPAREN LBRACE statement_list RBRACE','loop_statement',7,'p_loop_statement','parser.py',159),
  ('function_call -> IDENTIFIER LPAREN arguments RPAREN SEMICOLON','function_call',5,'p_function_call','parser.py',163),
  ('return_statement -> RETURN expression SEMICOLON','return_statement',3,'p_return_statement','parser.py',167),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','parser.py',171),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','parser.py',172),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression_binop','parser.py',173),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','parser.py',174),
  ('expression -> expression EQ expression','expression',3,'p_expression_binop','parser.py',175),
  ('expression -> expression NEQ expression','expression',3,'p_expression_binop','parser.py',176),
  ('expression -> expression LT expression','expression',3,'p_expression_binop','parser.py',177),
  ('expression -> expression LE expression','expression',3,'p_expression_binop','parser.py',178),
  ('expression -> expression GT expression','expression',3,'p_expression_binop','parser.py',179),
  ('expression -> expression GE expression','expression',3,'p_expression_binop','parser.py',180),
  ('expression -> expression AND expression','expression',3,'p_expression_binop','parser.py',181),
  ('expression -> expression OR expression','expression',3,'p_expression_binop','parser.py',182),
  ('expression -> NOT expression','expression',2,'p_expression_unary','parser.py',186),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parser.py',190),
  ('expression -> NUMBER','expression',1,'p_expression_number','parser.py',194),
  ('expression -> IDENTIFIER','expression',1,'p_expression_identifier','parser.py',198),
  ('expression -> function_call_expr','expression',1,'p_expression_function_call','parser.py',202),
  ('function_call_expr -> IDENTIFIER LPAREN arguments RPAREN','function_call_expr',4,'p_function_call_expr','parser.py',206),
  ('arguments -> arguments COMMA expression','arguments',3,'p_arguments','parser.py',210),
  ('arguments -> expression','arguments',1,'p_arguments','parser.py',211),
  ('arguments -> <empty>','arguments',0,'p_arguments','parser.py',212),
  ('ROBOT_COMMAND -> MOVEFORWARD','ROBOT_COMMAND',1,'p_ROBOT_COMMAND','parser.py',228),
  ('ROBOT_COMMAND -> MOVEBACKWARD','ROBOT_COMMAND',1,'p_ROBOT_COMMAND','parser.py',229),
  ('ROBOT_COMMAND -> TURNRIGHT','ROBOT_COMMAND',1,'p_ROBOT_COMMAND','parser.py',230),
  ('ROBOT_COMMAND -> TURNLEFT','ROBOT_COMMAND',1,'p_ROBOT_COMMAND','parser.py',231),
]
