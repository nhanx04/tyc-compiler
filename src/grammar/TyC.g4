grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()

    if tk == self.UNCLOSE_STRING:
        txt = result.text
        if len(txt) > 0 and txt[0] == '"':
            txt = txt[1:]
        if len(txt) > 0 and txt[-1] == '\n':
            txt = txt[:-1]
        if len(txt) > 0 and txt[-1] == '\r':
            txt = txt[:-1]
        raise UncloseString(txt)
    elif tk == self.ILLEGAL_ESCAPE:
        txt = result.text
        if len(txt) > 0 and txt[0] == '"':
            txt = txt[1:]
        raise IllegalEscape(txt)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.STRINGLIT:
        txt = result.text
        if len(txt) >= 2 and txt[0] == '"' and txt[-1] == '"':
            result.text = txt[1:-1]
        return result
    else:
        return result
}

options{
	language=Python3;
}

// TODO: Define grammar rules here
program
    : topDeclList EOF
    ;

topDeclList
    : topDecl topDeclList
    |
    ;

topDecl
    : structDecl
    | funcDecl
    ;

structDecl
    : STRUCT ID LBRACE structMemberDeclList RBRACE SEMI
    ;

structMemberDeclList
    : structMemberDecl structMemberDeclList
    |
    ;

structMemberDecl
    : typeSpec ID SEMI
    ;

funcDecl
    : returnTypeOpt ID LPAREN paramListOpt RPAREN blockStmt
    ;

returnTypeOpt
    : returnType
    |
    ;

returnType
    : VOID
    | typeSpec
    ;

paramListOpt
    : paramList
    |
    ;

paramList
    : param paramListTail
    ;

paramListTail
    : COMMA param paramListTail
    |
    ;

param
    : typeSpec ID
    ;

typeSpec
    : INT
    | FLOAT
    | STRING
    | ID
    ;

stmt
    : varDeclStmt
    | blockStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    ;

blockStmt
    : LBRACE stmtList RBRACE
    ;

stmtList
    : stmt stmtList
    |
    ;

varDeclStmt
    : AUTO ID varDeclAutoInitOpt SEMI
    | typeSpec ID varDeclTypedInitOpt SEMI
    | typeSpec ID SEMI
    ;

varDeclAutoInitOpt
    : ASSIGN expr
    |
    ;

varDeclTypedInitOpt
    : ASSIGN expr
    | ASSIGN structInit
    |
    ;

structInit
    : LBRACE structInitListOpt RBRACE
    ;

structInitListOpt
    : structInitElem structInitListTail
    |
    ;

structInitListTail
    : COMMA structInitElem structInitListTail
    |
    ;

structInitElem
    : expr
    | structInit
    ;

ifStmt
    : IF LPAREN expr RPAREN stmt elseOpt
    ;

elseOpt
    : ELSE stmt
    |
    ;

whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;

forStmt
    : FOR LPAREN forInitOpt SEMI exprOpt SEMI forUpdateOpt RPAREN stmt
    ;

forInitOpt
    : forInit
    |
    ;

forInit
    : varDeclFor
    | assignExpr
    ;

exprOpt
    : expr
    |
    ;

varDeclFor
    : AUTO ID varDeclAutoInitOpt
    | typeSpec ID varDeclTypedInitOpt
    | typeSpec ID
    ;

forUpdateOpt
    : forUpdate
    |
    ;

forUpdate
    : assignExpr
    | postfixExpr
    | unaryExpr
    ;

switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchSectionList RBRACE
    ;

switchSectionList
    : switchSection switchSectionList
    |
    ;

switchSection
    : caseLabelPlus stmtList
    | defaultLabel stmtList
    ;

caseLabelPlus
    : caseLabel caseLabelStar
    ;

caseLabelStar
    : caseLabel caseLabelStar
    |
    ;

caseLabel
    : CASE expr COLON
    ;

defaultLabel
    : DEFAULT COLON
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN returnExprOpt SEMI
    ;

returnExprOpt
    : expr
    |
    ;

exprStmt
    : expr SEMI
    ;

//-------------------------------------------------------------------------

expr
  : assignExpr
  ;

assignExpr
  : lvalue ASSIGN assignExpr
  | orExpr
  ;

lvalue
  : ID (DOT ID)*
  ;
orExpr
  : andExpr orExprTail
  ;

orExprTail
  : OR andExpr orExprTail
  |
  ;

andExpr
  : eqExpr andExprTail
  ;

andExprTail
  : AND eqExpr andExprTail
  |
  ;

eqExpr
  : relExpr eqExprTail
  ;

eqExprTail
  : eqOp relExpr eqExprTail
  |
  ;

eqOp
  : EQ
  | NEQ
  ;

relExpr
  : addExpr relExprTail
  ;

relExprTail
  : relOp addExpr relExprTail
  |
  ;

relOp
  : LT
  | LE
  | GT
  | GE
  ;

addExpr
  : mulExpr addExprTail
  ;

addExprTail
  : addOp mulExpr addExprTail
  |
  ;

addOp
  : ADD
  | SUB
  ;

mulExpr
  : unaryExpr mulExprTail
  ;

mulExprTail
  : mulOp unaryExpr mulExprTail
  |
  ;

mulOp
  : MUL
  | DIV
  | MOD
  ;

unaryExpr
  : unaryOp unaryExpr
  | postfixExpr
  ;

unaryOp
  : INC
  | DEC
  | NOT
  | ADD
  | SUB
  ;

postfixExpr
  : primaryExpr postfixTailList
  ;

postfixTailList
  : postfixTail postfixTailList
  |
  ;

postfixTail
  : DOT ID
  | LPAREN argListOpt RPAREN
  | INC
  | DEC
  ;

argListOpt
  : argList
  |
  ;

argList
  : expr argListTail
  ;

argListTail
  : COMMA expr argListTail
  |
  ;

primaryExpr
  : literal
  | ID
  | LPAREN expr RPAREN
  ;

literal
  : INTLIT
  | FLOATLIT
  | STRINGLIT
  ;

//--------------------------------------------------------------------

AUTO: 'auto';
BREAK: 'break';
CASE: 'case';
CONTINUE: 'continue';
DEFAULT: 'default';
ELSE: 'else';
FLOAT: 'float';
FOR: 'for';
IF: 'if';
INT: 'int';
RETURN: 'return';
STRING: 'string';
STRUCT: 'struct';
SWITCH: 'switch';
VOID: 'void';
WHILE: 'while';

INC: '++';
DEC: '--';

EQ: '==';
NEQ: '!=';
LE: '<=';
GE: '>=';

AND: '&&';
OR: '||';

LT: '<';
GT: '>';
NOT: '!';
ASSIGN: '=';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

DOT: '.';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
SEMI: ';';
COMMA: ',';
COLON: ':';

ID: [_a-zA-Z] [_a-zA-Z0-9]*;

//------------------------------------------------------------------------------------------

INTLIT: [0-9]+;

fragment DIGIT: [0-9];
fragment EXP: [eE] [+-]? DIGIT+;

FLOATLIT
    : DIGIT+ '.' DIGIT* EXP?
    | '.' DIGIT+ EXP?
    | DIGIT+ EXP
    ;

//--------------------------------------------------------------------------------------------

fragment ESC: '\\' [bfrnt"\\];
fragment STR_CHAR: ~["\\\r\n] | ESC;

STRINGLIT
  : '"' STR_CHAR* '"'
  ;

ILLEGAL_ESCAPE
  : '"' (STR_CHAR)* '\\' ~[bfrnt"\\]
  ;

UNCLOSE_STRING
  : '"' STR_CHAR* ( '\r' | '\n' | EOF )
  ;


LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs, form feed

ERROR_CHAR: .;

/*
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;
*/
