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



def test_empty_program():
    check_ast("", "Program([])")


def test_struct_empty():
    src = "struct Empty { };"
    exp = "Program([StructDecl(Empty, [])])"
    check_ast(src, exp)


def test_struct_three_members():
    src = "struct S { int a; float b; string c; };"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), a), MemberDecl(FloatType(), b), MemberDecl(StringType(), c)])])"
    check_ast(src, exp)


def test_function_auto_return():
    src = "sum(int a) { return a; }"
    exp = "Program([FuncDecl(auto, sum, [Param(IntType(), a)], BlockStmt([ReturnStmt(return Identifier(a))]))])"
    check_ast(src, exp)


def test_function_no_params_no_return():
    src = "void foo() { }"
    exp = "Program([FuncDecl(VoidType(), foo, [], BlockStmt([]))])"
    check_ast(src, exp)


def test_function_struct_param():
    src = "struct P { int x; }; void f(P p) { return; }"
    exp = "Program([StructDecl(P, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), f, [Param(StructType(P), p)], BlockStmt([ReturnStmt(return)]))])"
    check_ast(src, exp)


def test_multi_top_decls():
    src = "struct A { int x; }; struct B { float y; }; void main() {}"
    exp = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(FloatType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    check_ast(src, exp)


def test_var_decl_float_init():
    src = "void main() { float x = 1.5; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), x = FloatLiteral(1.5))]))])"
    check_ast(src, exp)


def test_var_decl_string_init():
    src = "void main() { string s = \"hi\"; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), s = StringLiteral('hi'))]))])"
    check_ast(src, exp)


def test_var_decl_auto_no_init():
    src = "void main() { auto x; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x)]))])"
    check_ast(src, exp)


def test_block_with_two_stmts():
    src = "void main() { int x; x = 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))]))])"
    check_ast(src, exp)


def test_if_without_else():
    src = "void main() { if (x) y = 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(x) then ExprStmt(AssignExpr(Identifier(y) = IntLiteral(1))))]))])"
    check_ast(src, exp)


def test_if_nested():
    src = "void main() { if (a) if (b) c = 1; else c = 2; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then IfStmt(if Identifier(b) then ExprStmt(AssignExpr(Identifier(c) = IntLiteral(1))), else ExprStmt(AssignExpr(Identifier(c) = IntLiteral(2)))))]))])"
    check_ast(src, exp)


def test_while_with_block():
    src = "void main() { while (1) { break; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([BreakStmt()]))]))])"
    check_ast(src, exp)


def test_for_missing_init():
    src = "void main() { int i; for (; i < 5; i++) { } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for None; BinaryOp(Identifier(i), <, IntLiteral(5)); PostfixOp(Identifier(i)++) do BlockStmt([]))]))])"
    check_ast(src, exp)


def test_for_missing_cond():
    src = "void main() { int i; for (i = 0; ; i++) { break; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); None; PostfixOp(Identifier(i)++) do BlockStmt([BreakStmt()]))]))])"
    check_ast(src, exp)


def test_for_missing_update():
    src = "void main() { int i; for (i = 0; i < 2; ) i = i + 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(2)); None do ExprStmt(AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1)))))]))])"
    check_ast(src, exp)


def test_for_all_missing():
    src = "void main() { for (;;){ continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; None do BlockStmt([ContinueStmt()]))]))])"
    check_ast(src, exp)


def test_switch_multiple_cases():
    src = "void main() { switch (x) { case 1: x = 1; case 2: x = 2; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))]), CaseStmt(case IntLiteral(2): [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))])])]))])"
    check_ast(src, exp)


def test_switch_with_default_only():
    src = "void main() { switch (x) { default: break; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [], default DefaultStmt(default: [BreakStmt()]))]))])"
    check_ast(src, exp)


def test_return_with_expr():
    src = "int f() { return 1 + 2; }"
    exp = "Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])"
    check_ast(src, exp)


def test_expr_stmt_func_call():
    src = "void main() { printInt(1); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(printInt, [IntLiteral(1)]))]))])"
    check_ast(src, exp)


def test_expr_stmt_multi_args():
    src = "void main() { foo(1, 2, 3); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(foo, [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))]))])"
    check_ast(src, exp)


def test_member_access_chain():
    src = "void main() { a.b.c = 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier(a).b).c) = IntLiteral(1)))]))])"
    check_ast(src, exp)



def test_logical_ops():
    src = "void main() { if (a && b || c) return; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, Identifier(c)) then ReturnStmt(return))]))])"
    check_ast(src, exp)


def test_eq_ops():
    src = "void main() { x = a == b; y = a != b; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(a), ==, Identifier(b)))), ExprStmt(AssignExpr(Identifier(y) = BinaryOp(Identifier(a), !=, Identifier(b))))]))])"
    check_ast(src, exp)


def test_rel_ops():
    src = "void main() { x = a <= b; y = a >= b; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(a), <=, Identifier(b)))), ExprStmt(AssignExpr(Identifier(y) = BinaryOp(Identifier(a), >=, Identifier(b))))]))])"
    check_ast(src, exp)


def test_add_sub_chain():
    src = "void main() { x = a - b + c; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), -, Identifier(b)), +, Identifier(c))))]))])"
    check_ast(src, exp)


def test_mul_div_chain():
    src = "void main() { x = a * b / c; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), *, Identifier(b)), /, Identifier(c))))]))])"
    check_ast(src, exp)


def test_unary_ops():
    src = "void main() { x = -a; y = !b; z = +c; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PrefixOp(-Identifier(a)))), ExprStmt(AssignExpr(Identifier(y) = PrefixOp(!Identifier(b)))), ExprStmt(AssignExpr(Identifier(z) = PrefixOp(+Identifier(c))))]))])"
    check_ast(src, exp)


def test_prefix_inc_dec():
    src = "void main() { ++x; --y; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++Identifier(x))), ExprStmt(PrefixOp(--Identifier(y)))]))])"
    check_ast(src, exp)


def test_postfix_inc_dec():
    src = "void main() { x++; y--; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(Identifier(x)++)), ExprStmt(PostfixOp(Identifier(y)--))]))])"
    check_ast(src, exp)


def test_call_no_args():
    src = "void main() { foo(); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(foo, []))]))])"
    check_ast(src, exp)


def test_call_nested_args():
    src = "void main() { foo(1, bar(2)); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(foo, [IntLiteral(1), FuncCall(bar, [IntLiteral(2)])]))]))])"
    check_ast(src, exp)


def test_member_access_read():
    src = "void main() { x = p.x; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = MemberAccess(Identifier(p).x)))]))])"
    check_ast(src, exp)


def test_member_access_chain_expr():
    src = "void main() { x = a.b.c; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = MemberAccess(MemberAccess(Identifier(a).b).c)))]))])"
    check_ast(src, exp)


def test_struct_literal_empty():
    src = "struct S { int x; }; void main() { S s = {}; }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({}))]))])"
    check_ast(src, exp)


def test_struct_literal_nested():
    src = "struct A { int x; }; struct B { A a; int y; }; void main() { B b = {{1}, 2}; }"
    exp = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(StructType(A), a), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(B), b = StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)}))]))])"
    check_ast(src, exp)


def test_return_expr_binary():
    src = "int f() { return a * (b + c); }"
    exp = "Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return BinaryOp(Identifier(a), *, BinaryOp(Identifier(b), +, Identifier(c))))]))])"
    check_ast(src, exp)


def test_for_update_assign():
    src = "void main() { int i; for (i = 0; i < 3; i = i + 1) { } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(3)); AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1))) do BlockStmt([]))]))])"
    check_ast(src, exp)


def test_for_init_typed_decl():
    src = "void main() { for (int i = 0; i < 1; i++) { } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(1)); PostfixOp(Identifier(i)++) do BlockStmt([]))]))])"
    check_ast(src, exp)


def test_switch_case_multiple_labels():
    src = "void main() { switch (x) { case 1: x = 3; break; case 2: x = 4; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(3))), BreakStmt()]), CaseStmt(case IntLiteral(2): [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(4)))])])]))])"
    check_ast(src, exp)


def test_nested_blocks_two_levels():
    src = "void main() { { { int x = 1; } } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([BlockStmt([VarDecl(IntType(), x = IntLiteral(1))])])]))])"
    check_ast(src, exp)



def test_chained_assignment():
    src = "void main() { x = y = 3; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(3))))]))])"
    check_ast(src, exp)


def test_assignment_in_parens():
    src = "void main() { x = (y = 2); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(2))))]))])"
    check_ast(src, exp)


def test_call_in_binary():
    src = "void main() { x = foo(1) + 2; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(FuncCall(foo, [IntLiteral(1)]), +, IntLiteral(2))))]))])"
    check_ast(src, exp)


def test_binary_with_member_access():
    src = "void main() { x = p.x + 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(MemberAccess(Identifier(p).x), +, IntLiteral(1))))]))])"
    check_ast(src, exp)


def test_postfix_member_access():
    src = "void main() { p.x++; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(MemberAccess(Identifier(p).x)++))]))])"
    check_ast(src, exp)


def test_prefix_member_access():
    src = "void main() { ++p.x; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++MemberAccess(Identifier(p).x)))]))])"
    check_ast(src, exp)


def test_struct_var_decl_no_init():
    src = "struct S { int x; }; void main() { S s; }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s)]))])"
    check_ast(src, exp)


def test_struct_assign_literal():
    src = "struct S { int x; int y; }; void main() { S s = {1, 2}; }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1), IntLiteral(2)}))]))])"
    check_ast(src, exp)


def test_nested_function_calls():
    src = "void main() { foo(bar(1), baz(2, 3)); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(foo, [FuncCall(bar, [IntLiteral(1)]), FuncCall(baz, [IntLiteral(2), IntLiteral(3)])]))]))])"
    check_ast(src, exp)


def test_string_literal_empty():
    src = "void main() { string s = \"\"; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), s = StringLiteral(''))]))])"
    check_ast(src, exp)


def test_float_literal_simple():
    src = "void main() { float f = 0.5; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), f = FloatLiteral(0.5))]))])"
    check_ast(src, exp)


def test_int_literal_zero():
    src = "void main() { int z = 0; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), z = IntLiteral(0))]))])"
    check_ast(src, exp)


def test_while_continue_block():
    src = "void main() { while (1) { continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([ContinueStmt()]))]))])"
    check_ast(src, exp)


def test_if_else_blocks():
    src = "void main() { if (x) { return; } else { return; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(x) then BlockStmt([ReturnStmt(return)]), else BlockStmt([ReturnStmt(return)]))]))])"
    check_ast(src, exp)


def test_if_else_if():
    src = "void main() { if (a) return; else if (b) return; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then ReturnStmt(return), else IfStmt(if Identifier(b) then ReturnStmt(return)))]))])"
    check_ast(src, exp)


def test_for_init_expr_stmt():
    src = "void main() { int i; for (i = 0; i < 2; i = i + 1) { continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(2)); AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1))) do BlockStmt([ContinueStmt()]))]))])"
    check_ast(src, exp)


def test_switch_case_default_combo():
    src = "void main() { switch (x) { case 1: break; default: x = 2; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])], default DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))]))]))])"
    check_ast(src, exp)


def test_nested_while_if():
    src = "void main() { while (x) if (y) break; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(x) do IfStmt(if Identifier(y) then BreakStmt()))]))])"
    check_ast(src, exp)


def test_return_struct_literal():
    src = "struct S { int x; int y; }; S f() { S s = {1, 2}; return s; }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(StructType(S), f, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1), IntLiteral(2)})), ReturnStmt(return Identifier(s))]))])"
    check_ast(src, exp)


def test_var_decl_binary_init():
    src = "void main() { int x = (1 + 2) * 3; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3)))]))])"
    check_ast(src, exp)



def test_block_empty_inner():
    src = "void main() { { } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([])]))])"
    check_ast(src, exp)


def test_multiple_var_decls():
    src = "void main() { int a = 1; int b = 2; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), a = IntLiteral(1)), VarDecl(IntType(), b = IntLiteral(2))]))])"
    check_ast(src, exp)


def test_return_no_expr_in_int():
    src = "int f() { return; }"
    exp = "Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return)]))])"
    check_ast(src, exp)


def test_prefix_paren_expr():
    src = "void main() { x = -(a + b); }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PrefixOp(-BinaryOp(Identifier(a), +, Identifier(b)))))]))])"
    check_ast(src, exp)


def test_postfix_in_expr():
    src = "void main() { x = i++; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PostfixOp(Identifier(i)++)))]))])"
    check_ast(src, exp)


def test_prefix_in_expr():
    src = "void main() { x = ++i; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PrefixOp(++Identifier(i))))]))])"
    check_ast(src, exp)


def test_func_decl_mixed_params():
    src = "float mix(int a, float b, string c) { return b; }"
    exp = "Program([FuncDecl(FloatType(), mix, [Param(IntType(), a), Param(FloatType(), b), Param(StringType(), c)], BlockStmt([ReturnStmt(return Identifier(b))]))])"
    check_ast(src, exp)


def test_struct_member_structtype():
    src = "struct A { int x; }; struct B { A a; }; void main() {}"
    exp = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(StructType(A), a)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    check_ast(src, exp)


def test_return_call():
    src = "int f() { return foo(1); }"
    exp = "Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return FuncCall(foo, [IntLiteral(1)]))]))])"
    check_ast(src, exp)


def test_for_with_continue():
    src = "void main() { for (int i = 0; i < 1; i++) { continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(1)); PostfixOp(Identifier(i)++) do BlockStmt([ContinueStmt()]))]))])"
    check_ast(src, exp)


def test_logical_rel_combo():
    src = "void main() { if (a < b && c > d) return; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if BinaryOp(BinaryOp(Identifier(a), <, Identifier(b)), &&, BinaryOp(Identifier(c), >, Identifier(d))) then ReturnStmt(return))]))])"
    check_ast(src, exp)



def test_assign_member_to_member():
    src = "void main() { a.b = c.d; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(Identifier(a).b) = MemberAccess(Identifier(c).d)))]))])"
    check_ast(src, exp)


def test_multi_member_assignment():
    src = "void main() { a.b.c = d.e; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier(a).b).c) = MemberAccess(Identifier(d).e)))]))])"
    check_ast(src, exp)


def test_return_member_access():
    src = "int f() { return p.x; }"
    exp = "Program([FuncDecl(IntType(), f, [], BlockStmt([ReturnStmt(return MemberAccess(Identifier(p).x))]))])"
    check_ast(src, exp)


def test_expr_stmt_identifier():
    src = "void main() { x; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(Identifier(x))]))])"
    check_ast(src, exp)


def test_var_decl_assign_expr():
    src = "void main() { int x = y = 1; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = AssignExpr(Identifier(y) = IntLiteral(1)))]))])"
    check_ast(src, exp)


def test_call_with_struct_literal():
    src = "struct S { int x; }; void main() { S s = {1}; foo(s); }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1)})), ExprStmt(FuncCall(foo, [Identifier(s)]))]))])"
    check_ast(src, exp)


def test_struct_literal_in_binary():
    src = "struct S { int x; int y; }; void main() { S s = {1, 2}; S t = {1, 2}; }"
    exp = "Program([StructDecl(S, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1), IntLiteral(2)})), VarDecl(StructType(S), t = StructLiteral({IntLiteral(1), IntLiteral(2)}))]))])"
    check_ast(src, exp)


def test_for_body_single_stmt():
    src = "void main() { for (auto i = 0; i < 1; i++) break; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(1)); PostfixOp(Identifier(i)++) do BreakStmt())]))])"
    check_ast(src, exp)


def test_while_single_stmt():
    src = "void main() { while (x) break; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(x) do BreakStmt())]))])"
    check_ast(src, exp)


def test_if_single_stmt():
    src = "void main() { if (x) y; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(x) then ExprStmt(Identifier(y)))]))])"
    check_ast(src, exp)


def test_switch_case_with_block():
    src = "void main() { switch (x) { case 1: { int a = 1; } break; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BlockStmt([VarDecl(IntType(), a = IntLiteral(1))]), BreakStmt()])])]))])"
    check_ast(src, exp)



def test_if_body_is_for_stmt():
    src = "void main() { if (x) for (auto i = 0; i < 2; i++) break; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(x) then ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(2)); PostfixOp(Identifier(i)++) do BreakStmt()))]))])"
    check_ast(src, exp)


def test_while_body_is_switch_stmt():
    src = "void main() { while (x) switch (y) { case 1: break; default: continue; } }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(x) do SwitchStmt(switch Identifier(y) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])], default DefaultStmt(default: [ContinueStmt()])))]))])"
    check_ast(src, exp)


def test_for_body_is_while_stmt():
    src = "void main() { int i; for (i = 0; i < 1; ++i) while (j) break; }"
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), i), ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(1)); PrefixOp(++Identifier(i)) do WhileStmt(while Identifier(j) do BreakStmt()))]))])"
    check_ast(src, exp)


def test_for_update_prefix_member_access():
    src = "struct P { int x; }; void main() { P p; for (; ; ++p.x) break; }"
    exp = "Program([StructDecl(P, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(P), p), ForStmt(for None; None; PrefixOp(++MemberAccess(Identifier(p).x)) do BreakStmt())]))])"
    check_ast(src, exp)


def test_for_update_postfix_member_access():
    src = "struct P { int x; }; void main() { P p; for (; ; p.x--) break; }"
    exp = "Program([StructDecl(P, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(P), p), ForStmt(for None; None; PostfixOp(MemberAccess(Identifier(p).x)--) do BreakStmt())]))])"
    check_ast(src, exp)



def test_required_struct_point_decl_exact():
    src = """struct Point {
    int x;
    int y;
};"""
    exp = "Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)])])"
    check_ast(src, exp)


def test_required_void_main_empty_exact():
    src = """void main() {
}"""
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    check_ast(src, exp)


def test_required_int_add_exact():
    src = """int add(int x, int y) {
    return x + y;
}"""
    exp = "Program([FuncDecl(IntType(), add, [Param(IntType(), x), Param(IntType(), y)], BlockStmt([ReturnStmt(return BinaryOp(Identifier(x), +, Identifier(y)))]))])"
    check_ast(src, exp)


def test_required_auto_return_add_exact():
    src = """add(int x, int y) {
    return x + y;
}"""
    exp = "Program([FuncDecl(auto, add, [Param(IntType(), x), Param(IntType(), y)], BlockStmt([ReturnStmt(return BinaryOp(Identifier(x), +, Identifier(y)))]))])"
    check_ast(src, exp)


def test_required_main_auto_x_exact():
    src = """void main() {
    auto x = 10;
}"""
    exp = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = IntLiteral(10))]))])"
    check_ast(src, exp)
