"""AST Generation test cases for TyC compiler."""

from tests.utils import ASTGenerator


def check_ast(source: str, expected: str):
    assert str(ASTGenerator(source).generate()) == expected


def test_empty_main():
    check_ast("void main() {}", "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])")


def test_struct_decl():
    src = "struct Point { int x; int y; };"
    exp = "Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)])])"
    check_ast(src, exp)


def test_func_with_params():
    src = "int add(int a, int b) { return a + b; }"
    exp = "Program([FuncDecl(IntType(), add, [Param(IntType(), a), Param(IntType(), b)], BlockStmt([ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))]))])"
    check_ast(src, exp)


def test_auto_var_decl():
    src = "void main() { auto x = 10; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = IntLiteral(10))]))])"
    check_ast(src, exp)


def test_typed_var_decl_no_init():
    src = "void main() { int x; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x)]))])"
    check_ast(src, exp)


def test_if_else_stmt():
    src = "void main() { if (1) x = 2; else x = 3; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2))), else ExprStmt(AssignExpr(Identifier(x) = IntLiteral(3))))]))])"
    check_ast(src, exp)


def test_while_stmt():
    src = "void main() { while (x < 10) x = x + 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while BinaryOp(Identifier(x), <, IntLiteral(10)) do ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(x), +, IntLiteral(1)))))]))])"
    check_ast(src, exp)


def test_for_stmt():
    src = "void main() { for (auto i = 0; i < 3; i++) printInt(i); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(3)); PostfixOp(Identifier(i)++) do ExprStmt(FuncCall(printInt, [Identifier(i)])))]))])"
    check_ast(src, exp)


def test_return_without_expr():
    src = "void main() { return; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return)]))])"
    check_ast(src, exp)


def test_member_access_assign():
    src = "struct P { int x; }; void main() { P p; p.x = 5; }"
    exp = "Program([StructDecl(P, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(P), p), ExprStmt(AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(5)))]))])"
    check_ast(src, exp)


def test_operator_precedence():
    src = "void main() { int x = 1 + 2 * 3; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))))]))])"
    check_ast(src, exp)


def test_prefix_and_postfix():
    src = "void main() { int x; ++x; x--; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), ExprStmt(PrefixOp(++Identifier(x))), ExprStmt(PostfixOp(Identifier(x)--))]))])"
    check_ast(src, exp)


def test_switch_case_default():
    src = "void main() { switch (x) { case 1: break; default: continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])], default DefaultStmt(default: [ContinueStmt()]))]))])"
    check_ast(src, exp)


def test_nested_blocks():
    src = "void main() { { int x = 1; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([VarDecl(IntType(), x = IntLiteral(1))])]))])"
    check_ast(src, exp)


def test_struct_literal_init():
    src = "struct P { int x; int y; }; void main() { P p = {1, 2}; }"
    exp = "Program([StructDecl(P, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(P), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))]))])"
    check_ast(src, exp)
