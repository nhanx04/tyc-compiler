"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = "void greet() { printString(\"Hello\"); }"
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. While statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. For statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"

# ========== Extended Test Cases (Additional 100 cases) ==========

# --- Program / Top-level ---

def test_program_struct_then_main():
    source = "struct A { int x; }; void main() {}"
    assert Parser(source).parse() == "success"


def test_program_two_functions():
    source = "void a() {} void b() {}"
    assert Parser(source).parse() == "success"


def test_program_multiple_structs_and_funcs():
    source = "struct A { int x; }; struct B { float y; }; void main() {}"
    assert Parser(source).parse() == "success"


def test_struct_empty():
    source = "struct Empty { };"
    assert Parser(source).parse() == "success"


def test_struct_nested_type_member():
    source = "struct P { int x; }; struct Q { P p; };"
    assert Parser(source).parse() == "success"


# --- Function declarations ---

def test_function_inferred_return_type():
    source = "add(int x, int y) { return x + y; }"
    assert Parser(source).parse() == "success"


def test_function_many_params():
    source = "void f(int a, float b, string c) { return; }"
    assert Parser(source).parse() == "success"


def test_function_returns_expression():
    source = "int f() { return 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_function_call_statement():
    source = "void main() { printInt(1); }"
    assert Parser(source).parse() == "success"


def test_function_call_with_args():
    source = "void main() { printFloat(1.0); printString(\"hi\"); }"
    assert Parser(source).parse() == "success"


# --- Variable declarations ---

def test_var_decl_auto_no_init():
    source = "void main() { auto x; x = 1; }"
    assert Parser(source).parse() == "success"


def test_var_decl_explicit_no_init():
    source = "void main() { int x; float y; string s; }"
    assert Parser(source).parse() == "success"


def test_var_decl_explicit_with_init_expr():
    source = "void main() { int x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_var_decl_struct_no_init():
    source = "struct P { int x; int y; }; void main() { P p; }"
    assert Parser(source).parse() == "success"


def test_var_decl_struct_with_init():
    source = "struct P { int x; int y; }; void main() { P p = {1, 2}; }"
    assert Parser(source).parse() == "success"


def test_var_decl_struct_with_nested_init():
    source = "struct A { int x; int y; }; struct B { A a; int z; }; void main() { B b = {{1,2}, 3}; }"
    assert Parser(source).parse() == "success"


# --- Blocks / If ---

def test_block_empty():
    source = "void main() { { } }"
    assert Parser(source).parse() == "success"


def test_if_else_blocks():
    source = "void main() { if (1) { printInt(1); } else { printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_dangling_else_association():
    source = "void main() { if (1) if (1) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


# --- While ---

def test_while_with_block():
    source = "void main() { while (1) { break; } }"
    assert Parser(source).parse() == "success"


def test_while_nested():
    source = "void main() { while (1) while (0) break; }"
    assert Parser(source).parse() == "success"


# --- For ---

def test_for_missing_init():
    source = "void main() { int i; for (; i < 10; ++i) { } }"
    assert Parser(source).parse() == "success"


def test_for_missing_cond():
    source = "void main() { int i; for (i = 0; ; ++i) { break; } }"
    assert Parser(source).parse() == "success"


def test_for_missing_update():
    source = "void main() { int i; for (i = 0; i < 10; ) { i = i + 1; } }"
    assert Parser(source).parse() == "success"


def test_for_all_missing_parts():
    source = "void main() { for (;;){ break; } }"
    assert Parser(source).parse() == "success"


def test_for_init_assignment():
    source = "void main() { int i; for (i = 0; i < 10; i = i + 1) { } }"
    assert Parser(source).parse() == "success"


def test_for_update_postfix():
    source = "void main() { int i; for (i = 0; i < 10; i++) { } }"
    assert Parser(source).parse() == "success"


def test_for_update_prefix():
    source = "void main() { int i; for (i = 0; i < 10; ++i) { } }"
    assert Parser(source).parse() == "success"


def test_for_init_auto_decl():
    source = "void main() { for (auto i = 0; i < 10; ++i) { } }"
    assert Parser(source).parse() == "success"


def test_for_init_explicit_decl():
    source = "void main() { for (int i = 0; i < 10; ++i) { } }"
    assert Parser(source).parse() == "success"


# --- Switch (case expr: mẫu 1) ---

def test_switch_empty_body():
    source = "void main() { switch (1) { } }"
    assert Parser(source).parse() == "success"


def test_switch_default_only():
    source = "void main() { switch (1) { default: break; } }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases_fallthrough():
    source = "void main() { switch (x) { case 1: case 2: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_switch_case_negative_literal_expr():
    source = "void main() { switch (1) { case -1: break; } }"
    assert Parser(source).parse() == "success"


def test_switch_case_parenthesized_expr():
    source = "void main() { switch (1) { case (1+2): break; } }"
    assert Parser(source).parse() == "success"


def test_switch_case_complex_expr():
    source = "void main() { switch (1) { case 1+2*3: break; } }"
    assert Parser(source).parse() == "success"


def test_switch_default_in_middle():
    source = "void main() { switch (1) { case 1: break; default: break; case 2: break; } }"
    assert Parser(source).parse() == "success"


# --- Break/Continue/Return ---

def test_return_no_expr():
    source = "void main() { return; }"
    assert Parser(source).parse() == "success"


# --- Member access / assignment LHS ---

def test_member_access_read():
    source = "struct P { int x; }; void main() { P p; auto y = p.x; }"
    assert Parser(source).parse() == "success"


def test_member_access_assign():
    source = "struct P { int x; }; void main() { P p; p.x = 1; }"
    assert Parser(source).parse() == "success"


def test_member_access_chain_assign():
    source = "struct A { int x; }; struct B { A a; }; void main() { B b; b.a.x = 1; }"
    assert Parser(source).parse() == "success"


def test_assignment_chain_simple():
    source = "void main() { int a; int b; int c; a = b = c = 1; }"
    assert Parser(source).parse() == "success"


# --- Calls in expressions (postfixTail includes call) ---

def test_call_no_args_expr_stmt():
    source = "void f() {} void main() { f(); }"
    assert Parser(source).parse() == "success"


def test_call_many_args():
    source = "void f(int a, float b, string c) {} void main() { f(1, 2.0, \"hi\"); }"
    assert Parser(source).parse() == "success"


def test_call_nested_args():
    source = "int g() { return 1; } void main() { printInt(g()); }"
    assert Parser(source).parse() == "success"


# --- Expression precedence sanity ---

def test_expr_precedence_mul_over_add():
    source = "void main() { auto x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_expr_parentheses_override():
    source = "void main() { auto x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"


def test_expr_logical_and_or():
    source = "void main() { auto x = 1 && 0 || 1; }"
    assert Parser(source).parse() == "success"


def test_expr_relational_equality():
    source = "void main() { auto x = 1 < 2 == 0 != 1; }"
    assert Parser(source).parse() == "success"


def test_expr_unary_prefix_chain():
    source = "void main() { int x; x = ---1; }"
    assert Parser(source).parse() == "success"


def test_expr_postfix_inc_member():
    source = "struct P { int x; }; void main() { P p; p.x++; }"
    assert Parser(source).parse() == "success"


def test_expr_prefix_inc_member():
    source = "struct P { int x; }; void main() { P p; ++p.x; }"
    assert Parser(source).parse() == "success"


# --- Negative syntax cases (should fail) ---

def test_error_missing_semi_in_vardecl():
    source = "void main() { auto x = 1 }"
    assert Parser(source).parse() != "success"


def test_error_missing_rparen_if():
    source = "void main() { if (1 { } }"
    assert Parser(source).parse() != "success"


def test_error_missing_rbrace_func():
    source = "void main() { auto x = 1; "
    assert Parser(source).parse() != "success"


def test_error_struct_missing_semi():
    source = "struct A { int x; }"
    assert Parser(source).parse() != "success"


def test_error_switch_case_missing_colon():
    source = "void main() { switch (1) { case 1 break; } }"
    assert Parser(source).parse() != "success"


def test_error_assignment_non_lvalue():
    source = "void main() { int a; (a + 1) = 2; }"
    assert Parser(source).parse() != "success"


def test_error_for_missing_semis():
    source = "void main() { for (i=0 i<10 ++i) { } }"
    assert Parser(source).parse() != "success"


def test_error_unexpected_token():
    source = "void main() { $$$ }"
    assert Parser(source).parse() != "success"

# --- More programs / structs ---

def test_program_only_structs():
    source = "struct A { int x; }; struct B { string s; };"
    assert Parser(source).parse() == "success"


def test_struct_many_members():
    source = "struct S { int a; int b; int c; float d; string e; };"
    assert Parser(source).parse() == "success"


def test_struct_member_struct_of_struct():
    source = "struct A { int x; }; struct B { A a; }; struct C { B b; };"
    assert Parser(source).parse() == "success"


# --- More functions ---

def test_function_param_struct_type():
    source = "struct P { int x; }; void f(P p) { return; }"
    assert Parser(source).parse() == "success"


def test_function_void_without_return_stmt():
    source = "void main() { auto x = 1; }"
    assert Parser(source).parse() == "success"


def test_function_inferred_void():
    source = "greet(string name) { printString(name); }"
    assert Parser(source).parse() == "success"


def test_function_multiple_returns_syntax_ok():
    source = "int f(int x) { if (x) return 1; else return 2; }"
    assert Parser(source).parse() == "success"


# --- More statements ---

def test_nested_blocks_with_shadowing_syntax():
    source = "void main() { int x; { int x; x = 1; } x = 2; }"
    assert Parser(source).parse() == "success"


def test_empty_statement_not_allowed_negative():
    source = "void main() { ; }"
    assert Parser(source).parse() != "success"


def test_return_in_block():
    source = "int f() { { return 1; } }"
    assert Parser(source).parse() == "success"


def test_if_with_expr_stmt():
    source = "void main() { if (1) 1+2; }"
    assert Parser(source).parse() == "success"


def test_while_with_continue():
    source = "void main() { while (1) { continue; } }"
    assert Parser(source).parse() == "success"


def test_for_body_single_stmt():
    source = "void main() { int i; for (i = 0; i < 3; ++i) i = i + 1; }"
    assert Parser(source).parse() == "success"


# --- More switch cases ---

def test_switch_case_with_assignment_expr():
    source = "void main() { int x; switch (x) { case (x = 1): break; } }"
    assert Parser(source).parse() == "success"


def test_switch_case_with_logical_expr():
    source = "void main() { int x; switch (x) { case (1 && 0): break; } }"
    assert Parser(source).parse() == "success"


def test_switch_multiple_sections_with_default():
    source = "void main() { switch (1) { case 1: break; case 2: break; default: break; } }"
    assert Parser(source).parse() == "success"


# --- More expressions ---

def test_expr_assignment_as_subexpr():
    source = "void main() { int x; int y; y = (x = 5) + 7; }"
    assert Parser(source).parse() == "success"


def test_expr_member_in_parens_postfix():
    source = "struct P { int x; }; void main() { P p; (p.x)++; }"
    assert Parser(source).parse() == "success"


def test_expr_complex_chain():
    source = "void main() { int a; int b; int c; a = b = (c = 1); }"
    assert Parser(source).parse() == "success"


def test_expr_unary_mix():
    source = "void main() { int x; x = !--++x; }"
    assert Parser(source).parse() == "success"


def test_expr_call_in_chain():
    source = "int f() { return 1; } void main() { auto x = f() + 2; }"
    assert Parser(source).parse() == "success"


# --- More negative syntax ---

def test_error_missing_rparen_call():
    source = "void main() { printInt(1; }"
    assert Parser(source).parse() != "success"


def test_error_missing_lbrace_block():
    source = "void main()  auto x = 1; }"
    assert Parser(source).parse() != "success"


def test_error_for_missing_rparen():
    source = "void main() { for (auto i = 0; i < 10; ++i { } }"
    assert Parser(source).parse() != "success"


def test_error_switch_missing_rbrace():
    source = "void main() { switch (1) { case 1: break; "
    assert Parser(source).parse() != "success"


def test_error_struct_missing_rbrace():
    source = "struct A { int x; ;"
    assert Parser(source).parse() != "success"


def test_error_member_access_missing_id():
    source = "struct P { int x; }; void main() { P p; p.; }"
    assert Parser(source).parse() != "success"


def test_error_double_comma_args():
    source = "void main() { printInt(1,,2); }"
    assert Parser(source).parse() != "success"


def test_error_unexpected_case_in_block():
    source = "void main() { case 1: break; }"
    assert Parser(source).parse() != "success"


def test_error_bad_struct_init_commas():
    source = "struct P { int x; int y; }; void main() { P p = {1,,2}; }"
    assert Parser(source).parse() != "success"


def test_error_bad_struct_init_missing_rbrace():
    source = "struct P { int x; int y; }; void main() { P p = {1,2; }"
    assert Parser(source).parse() != "success"