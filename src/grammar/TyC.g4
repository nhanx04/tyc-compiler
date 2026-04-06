grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// --- PARSER --- //

// TODO Literal Integer, floating-point, and string literals


// TODO Expressions
/*
| **Operator** | **Associativity** |
|--------------|-------------------|
| `++`, `--` (postfix) | left | 10
| `++`, `--` (prefix) | right | 9
| `!`, `-` (unary), `+` (unary) | right | 8
| `.` (member access) | left | 7
| `*`, `/`, `%` | left | 6
| `+`, `-` (binary) | left | 5
| `<`, `<=`, `>`, `>=` | left | 4
| `==`, `!=` | left | 3
| `&&` | left | 2
| `\|\|` | left | 1
| `=` | right | 0 
Primary expressions (identifiers, literals, parenthesized, member access), 
unary operations, binary operations following operator precedence, 
function calls, and postfix operations (increment/decrement)
*/

// CHECK HERE TOMORROW
list_expression: expression (COMMA expression)*;
expression  : (lhs) ASSIGN expression | expression1 | all_literal; // right associate
lhs: expression10 ACCESS ID | ID;
expression1 : expression1 OR expression2 | expression2; // left associate
expression2 : expression2 AND expression3 | expression3; // left associate
expression3 : expression3 (EQUAL | NOT_EQUAL) expression4 | expression4; // left associate
expression4 : expression4 (GT | LT | GEQ | LEQ) expression5 | expression5; // left associate
expression5 : expression5 (PLUS | MINUS) expression6 | expression6; // left associate
expression6 : expression6 (MUL | DIV | MODULUS) expression7 | expression7; // left associate
expression7 : (NOT | MINUS | PLUS) expression7 | expression8;
expression8 : (INCRE | DECRE) expression8 | expression9;
expression9 : expression9 (INCRE | DECRE) | expression10;
expression10: expression10 ACCESS ID | primary;
primary : LPAREN expression RPAREN | all_literal | ID | function_call;
function_call: ID (LPAREN (expression (COMMA expression)*)? RPAREN);
all_literal : INT_LIT | FLOAT_LIT | STRING_LIT | struct_literal;
struct_literal : LBRACE (expression (COMMA expression)*)? RBRACE; 

// TODO type `int`, `float`, `string`, `void`, struct types, and type inference using `auto`


// TODO Statements Variable declarations, assignments, control flow (if, while, for, switch-case), break, continue, return, expression statements, and blocks
list_statement: statement+;
statement: var_statement SEMI 
		| if_statement
		| while_statement
		| for_statement
        | switch_statement
		| break_statement
		| continue_statement
        | block_statement
        | expression_statement SEMI
		| return_statement
        | call_statement;
var_statement: (all_type) ID (ASSIGN expression)?; // lệnh khai báo
all_type: FLOAT | INT | STRING | AUTO | ID;
// hỗ trợ: khai báo có khởi tạo và không có khởi tạo
if_statement: IF LPAREN expression RPAREN statement (ELSE statement)?;
// OK
while_statement: WHILE LPAREN expression RPAREN statement;
// OK
for_statement: FOR LPAREN (first)? SEMI expression? SEMI (third)? RPAREN statement;
first: for_var_statement | assign;
for_var_statement: all_type ID (ASSIGN expression)?;
third: incre_decre | assign;
incre_decre: (INCRE | DECRE) lhs | lhs (INCRE | DECRE);
assign: lhs ASSIGN expression;
// OK
switch_statement: SWITCH LPAREN expression RPAREN LBRACE case_statement* default_statement? case_statement* RBRACE; 
case_statement: CASE expression COLON list_statement?;
default_statement: DEFAULT COLON list_statement?;
// OK
break_statement: BREAK SEMI; 
// OK
continue_statement: CONTINUE SEMI; 
block_statement: LBRACE list_statement? RBRACE;
// OK
expression_statement: expression;
// OK
return_statement: RETURN expression? SEMI;
call_statement: function_call SEMI;


// TODO Structs and Functions

program: (structs | functions)* EOF;
structs: STRUCT ID LBRACE (struct_var_statement)* RBRACE SEMI;
struct_var_statement: all_struct_type ID SEMI;
all_struct_type: (FLOAT | INT | STRING | ID); // không có void, auto
// không hỗ trợ member kiểu auto
// không được khai báo 2 struct lồng nhau
functions: all_func_type? ID (LPAREN params RPAREN) block_statement;
all_func_type: FLOAT | INT | STRING | VOID | ID; // tất cả kiểu trừ auto
all_param_type: (FLOAT | INT | STRING | ID); // kiểu tường minh
params: list_param | ; // có thể rỗng
list_param: all_param_type ID (COMMA all_param_type ID)*; // ngăn cách dấu , kiểu tham số tường minh


// --- LEXER --- //

// TODO Keywords: OK
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';

// TODO Operator: OK
PLUS        : '+';
MINUS       : '-';
MUL         : '*';
DIV         : '/';
MODULUS     : '%';
EQUAL       : '==';
NOT_EQUAL   : '!=';
LT          : '<';
GT          : '>';
LEQ         : '<=';
GEQ         : '>=';
OR          : '||';
AND         : '&&';
NOT         : '!';
INCRE       : '++';
DECRE       : '--';
ASSIGN      : '=';
ACCESS      : '.';

// TODO Separator: OK
LPAREN   : '(';
RPAREN   : ')';
LBRACE   : '{';
RBRACE   : '}';
COMMA    : ',';
SEMI     : ';';
COLON    : ':';

// TODO Identifiers: OK
ID       : [a-zA-Z_][a-zA-Z0-9_]*;

// TODO Literals
INT_LIT  : [0-9]+; // OK
FLOAT_LIT : [0-9]*'.'[0-9]+([Ee][+-]?[0-9]+)? | [0-9]+'.'[0-9]*([Ee][+-]?[0-9]+)? | [0-9]+[Ee][+-]?[0-9]+;
STRING_LIT : '"' STR_CHAR* '"' { self.text = self.text[1:-1] };
fragment STR_CHAR : ~ [\n\r"\\] | ESC_SEQ;
fragment ESC_SEQ : '\\' [bfnrt"\\];

// TODO Comment and WS
LINE_COMMENT: '//' ~ [\r\n]*  -> skip;
BLOCK_COMMENT: '/*' (.)*? '*/' -> skip;
// Comment không lồng nhau
WS: [ \f\t\r\n]+ -> skip;

// TODO ERROR: ILLEGAL_ESCAPE -> UNCLOSE_STRING
UNCLOSE_STRING: '"' STR_CHAR*  '\\'? ('\n' | '\r\n' | EOF) {
    if self.text[-1] == '\n' and self.text[-2] == '\r':
        raise UncloseString(self.text[1:-2])
    elif self.text[-1] == '\n':
        raise UncloseString(self.text[1:-1])
    else:
        raise UncloseString(self.text[1:])
};
ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL { raise IllegalEscape(self.text[1:]) };
fragment ESC_ILLEGAL : '\\' ~ [bfnrt"\\];
// đọc 1 xâu, thấy esc_seq lỗi, thì báo lỗi từ đầu xâu về sau
ERROR_CHAR: . {raise ErrorToken(self.text)}; // báo lỗi chính cái kí tự lỗi đó