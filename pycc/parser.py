from funcparserlib.parser import *
from lexer import *

expression = forward_decl()
assignment_expression = forward_decl()

primary_expression  = IDENTIFIER 
primary_expression |= CONSTANT 
primary_expression |= STRING_LITERAL 
primary_expression |= LEFT_PAREN + expression + RIGHT_PAREN

postfix_expression  = primary_expression 
postfix_expression |= postfix_expression + OPEN_INDEX + expression + CLOSE_INDEX
postfix_expression |= postfix_expression + LEFT_PAREN + RIGHT_PAREN
postfix_expression |= postfix_expression + LEFT_PAREN + argument_expression_list + RIGHT_PAREN
postfix_expression |= postfix_expression + DOT + IDENTIFIER
postfix_expression |= postfix_expression + PTR_OP + IDENTIFIER
postfix_expression |= postfix_expression + INC_OP
postfix_expression |= postfix_expression + DEC_OP

argument_expression_list  = assignment_expression
argument_expression_list |= argument_expression_list + COMMA + assignment_expression

unary_expression  = postfix_expression
unary_expression |= INC_OP + unary_expression
unary_expression |= DEC_OP + unary_expression
unary_expression |= unary_operator + cast_expression
unary_expression |= SIZEOF + LEFT_PAREN + type_name + RIGHT_PAREN

unary_operator = AND | MUL | ADD | SUB | INVERT | NOT

cast_expression  = unary_expression
cast_expression |= LEFT_PAREN + type_name + RIGHT_PAREN + cast_expression

multiplicative_expression  = cast_expression
multiplicative_expression |= multiplicative_expression + '*' + cast_expression
multiplicative_expression |= multiplicative_expression + '/' + cast_expression
multiplicative_expression |= multiplicative_expression + '%' + cast_expression

additive_expression  = multiplicative_expression
additive_expression |= additive_expression + '+' + multiplicative_expression
additive_expression |= additive_expression + '-' + multiplicative_expression

shift_expression  = additive_expression
shift_expression |= shift_expression + LEFT_OP + additive_expression
shift_expression |= shift_expression + RIGHT_OP + additive_expression

relational_expression  = shift_expression
relational_expression |= relational_expression + LT + shift_expression
relational_expression |= relational_expression + GT + shift_expression
relational_expression |= relational_expression + LE_OP + shift_expression
relational_expression |= relational_expression + GE_OP + shift_expression

equality_expression  = relational_expression
equality_expression |= equality_expression + EQ_OP + relational_expression
equality_expression |= equality_expression + NE_OP + relational_expression

and_expression  = equality_expression
and_expression |= and_expression + AND + equality_expression

exclusive_or_expression  = and_expression
exclusive_or_expression |= exclusive_or_expression + XOR + and_expression

inclusive_or_expression  = exclusive_or_expression
inclusive_or_expression |= inclusive_or_expression + OR + exclusive_or_expression

logical_and_expression  = inclusive_or_expression
logical_and_expression |= logical_and_expression + AND_OP + inclusive_or_expression

logical_or_expression  = logical_and_expression
logical_or_expression |= logical_or_expression + OR_OP + logical_or_expression

conditional_expression  = logical_or_expression
conditional_expression |= logical_or_expression + QMARK + expression + COLON + conditional_expression

assignment_operator = EQ | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | ADD_ASSIGN | SUB_ASSIGN | LEFT_ASSIGN | RIGHT_ASSIGN | AND_ASSIGN | XOR_ASSIGN | OR_ASSIGN

assignment_expression.define(conditional_expression | (unary_expression + assignment_operator + assignment_expression))

expression.define(assignment_expression | (expression + COMMA + assignment_expression))

constant_expression = conditional_expression

storage_class_specifier = TYPEDEF | EXTERN | STATIC | AUTO | REGISTER

declarator = forward_decl()

type_qualifier = CONST | VOLATILE

struct_or_union = STRUCT | UNION

parameter_list  = parameter_declaration
parameter_list |= parameter_list + COMMA + parameter_declaration

parameter_type_list  = parameter_list
parameter_type_list |= parameter_list + COMMA + ELLIPSIS

type_qualifier_list  = type_qualifier
type_qualifier_list |= type_qualifier_list + type_qualifier

pointer  = MUL
pointer |= MUL + type_qualifier_list
pointer |= MUL + pointer
pointer |= MUL + type_qualifier_list + pointer

direct_declarator  = IDENTIFIER
direct_declarator |= LEFT_PAREN + declarator + RIGHT_PAREN
direct_declarator |= direct_declarator + OPEN_INDEX + constant_expression + CLOSE_INDEX
direct_declarator |= direct_declarator + OPEN_INDEX + CLOSE_INDEX
direct_declarator |= direct_declarator + LEFT_PAREN + parameter_type_list + RIGHT_PAREN
direct_declarator |= direct_declarator + LEFT_PAREN + identifier_list + RIGHT_PAREN
direct_declarator |= direct_declarator + LEFT_PAREN + RIGHT_PAREN

declarator.define((pointer + direct_declarator) | direct_declarator)

enumerator  = IDENTIFIER
enumerator |= IDENTIFIER + EQ + constant_expression

enumerator_list  = enumerator
enumerator_list |= enumerator_list + COMMA + enumerator

enum_specifier  = ENUM + OPEN_BLOCK + enumerator_list + CLOSE_BLOCK
enum_specifier |= ENUM + IDENTIFIER + OPEN_BLOCK + enumerator_list + CLOSE_BLOCK
enum_specifier |= ENUM + IDENTIFIER 

struct_declarator  = declarator
struct_declarator |= COLON + constant_expression
struct_declarator |= declarator + COLON + constant_expression

struct_declarator_list  = struct_declarator
struct_declarator_list |= struct_declarator_list + COMMA + struct_declarator

specifier_quantifier_list  = type_specifier + specifier_quantifier_list
specifier_quantifier_list |= type_specifier
specifier_quantifier_list |= type_qualifier + specifier_quantifier_list
specifier_quantifier_list |= type_qualifier 

struct_declaration = specifier_quantifier_list + struct_declarator_list + SEMI

struct_declaration_list  = struct_declaration
struct_declaration_list |= struct_declaration_list + struct_declaration

struct_or_union_specifier  = struct_or_union + IDENTIFIER + OPEN_BLOCK + struct_declaration_list + CLOSE_BLOCK
struct_or_union_specifier |= struct_or_union + OPEN_BLOCK + struct_declaration_list + CLOSE_BLOCK
struct_or_union_specifier |= struct_or_union + IDENTIFIER 

type_specifier = VOID | CHAR | SHORT | INT | LONG | FLOAT | DOUBLE | SIGNED | UNSIGNED | struct_or_union_specifier | enum_specifier | TYPE_NAME

init_declarator  = declarator
init_declarator |= declarator + EQ + initializer

init_declarator_list  = init_declarator
init_declarator_list |= init_declarator_list + COMMA + init_declarator

declaration_specifiers  = storage_class_specifier
declaration_specifiers |= storage_class_specifier + declaration_specifiers
declaration_specifiers |= type_specifier
declaration_specifiers |= type_specifier + declaration_specifiers
declaration_specifiers |= type_qualifier
declaration_specifiers |= type_qualifier + declaration_specifiers

declaration  = declaration_specifiers + SEMI
declaration |= declaration_specifiers + init_declarator_list + SEMI

