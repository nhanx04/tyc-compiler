"""100-case semantic checker suite with explicit rule/error mapping."""

import pytest
from tests.utils import Checker

PASS = "Static checking passed"


def C(name, rule, why_first_failure, source, expected=PASS, mode="exact"):
    return (name, rule, why_first_failure, source, mode, expected)


CASES = [
    C("c001_valid_min", "entrypoint", "single valid main", "void main(){}"),
    C("c002_valid_builtin_io", "builtin", "all builtin signatures match", "void main(){ int a=readInt(); float b=readFloat(); string c=readString(); printInt(a); printFloat(b); printString(c);} "),
    C("c003_valid_arith_int", "expr arithmetic", "all ops int-valid", "void main(){ int a=1+2*3-4/2; int b=a%2; }"),
    C("c004_valid_arith_mix", "expr arithmetic", "promotion int/float valid", "void main(){ float a=1+2.0; float b=a/2; }"),
    C("c005_valid_rel_logic", "expr relational/logical", "relational returns int usable in if", "void main(){ int a=1<2; if(a&&1){} }"),
    C("c006_valid_unary", "expr unary", "unary +,-,! on valid operand types", "void main(){ int a=1; int b=+a; int c=-a; int d=!a; }"),
    C("c007_valid_incdec", "expr ++/--", "lvalue int for prefix/postfix", "void main(){ int a=1; ++a; a++; --a; a--; }"),
    C("c008_valid_func_call", "function call", "arity/type match", "int add(int x,int y){return x+y;} void main(){ int z=add(1,2);} "),
    C("c009_valid_inferred_return", "inferred return", "first return fixes int", "f(int x){ if(x) return 1; return 2; } void main(){ int a=f(1);} "),
    C("c010_valid_auto_init", "auto infer", "init gives concrete type", "void main(){ auto a=1; auto b=2.0; auto c=\"x\"; }"),
    C("c011_valid_auto_first_use_assign", "auto infer", "first assignment fixes type", "void main(){ auto a; a=1; int b=a; }"),
    C("c012_valid_auto_first_use_param", "auto infer", "function param fixes lone auto arg", "void f(int x){} void main(){ auto a; f(a);} "),
    C("c013_valid_struct_decl_var", "struct", "declared struct used as type", "struct P{int x;}; void main(){ P p; p.x=1; }"),
    C("c014_valid_struct_literal", "struct literal", "arity/type match member order", "struct P{int x; float y;}; void main(){ P p={1,2.0}; }"),
    C("c015_valid_member_from_call", "member access", "function returns struct then member", "struct P{int x;}; P g(){ P p={1}; return p;} void main(){ int a=g().x; }"),
    C("c016_valid_for_scope_persist", "for scope", "init variable visible after for per spec", "void main(){ for(int i=0;i<1;++i){} int a=i; }"),
    C("c017_valid_for_body_shadow", "for scope", "body inner scope shadows init var and outer remains visible", "void main(){ for(int i=0;i<1;++i){ int i=2; printInt(i);} printInt(i);} "),
    C("c018_valid_switch_empty", "switch", "empty switch allowed", "void main(){ int x=1; switch(x){} }"),
    C("c019_valid_switch_break", "switch", "break allowed in switch", "void main(){ int x=1; switch(x){ case 1: break; default: break;} }"),
    C("c020_valid_break_continue_loop", "loop control", "break/continue both in loop", "void main(){ for(int i=0;i<3;++i){ if(i) continue; break; } }"),
    C("c021_redeclared_var_same_block", "Redeclared", "second decl in same scope", "void main(){ int x=1; int x=2; }", "Redeclared(", "prefix"),
    C("c022_redeclared_param", "Redeclared", "duplicate parameter detected at function decl", "int f(int x,int x){return x;} void main(){}", "Redeclared(", "prefix"),
    C("c023_redeclared_func", "Redeclared", "global function name duplicated", "void f(){} int f(){return 1;} void main(){}", "Redeclared(", "prefix"),
    C("c024_redeclared_struct", "Redeclared", "global struct name duplicated", "struct A{}; struct A{}; void main(){}", "Redeclared(", "prefix"),
    C("c025_redeclared_member", "Redeclared", "member names duplicate in same struct", "struct A{int x; float x;}; void main(){}", "Redeclared(", "prefix"),
    C("c026_redeclared_param_name_in_block", "Redeclared param rule", "local cannot reuse parameter name", "int f(int x){ {int x=1;} return x;} void main(){}", "Redeclared(", "prefix"),
    C("c027_undeclared_identifier", "UndeclaredIdentifier", "y used before any declaration", "void main(){ int x=y+1; }", "UndeclaredIdentifier(", "prefix"),
    C("c028_undeclared_function", "UndeclaredFunction", "call to unknown function", "void main(){ foo(); }", "UndeclaredFunction(", "prefix"),
    C("c029_undeclared_struct", "UndeclaredStruct", "unknown struct type in variable decl", "void main(){ Point p; }", "UndeclaredStruct(", "prefix"),
    C("c030_undeclared_struct_member_type", "UndeclaredStruct", "member uses non-declared struct type", "struct A{B b;}; struct B{}; void main(){}", "UndeclaredStruct(", "prefix"),
    C("c031_undeclared_in_self_init", "UndeclaredIdentifier", "initializer checked before variable enters scope", "void main(){ int x=x+1; }", "UndeclaredIdentifier(", "prefix"),
    C("c032_undeclared_member_name", "TypeMismatchInExpression", "struct exists but member missing", "struct A{int x;}; void main(){ A a; int y=a.z; }", "TypeMismatchInExpression(", "prefix"),
    C("c033_cannot_infer_lonely_auto", "TypeCannotBeInferred", "auto never constrained", "void main(){ auto x; }", "TypeCannotBeInferred(", "prefix"),
    C("c034_cannot_infer_auto_assign_auto", "TypeCannotBeInferred", "x=y leaves both unknown", "void main(){ auto x; auto y; x=y; }", "TypeCannotBeInferred(", "prefix"),
    C("c035_cannot_infer_binary_two_auto", "TypeCannotBeInferred", "a+b has two unknown autos", "void main(){ auto a; auto b; auto c=a+b; }", "TypeCannotBeInferred(", "prefix"),
    C("c036_cannot_infer_return_auto", "TypeCannotBeInferred", "return unknown auto expression", "f(){ auto x; return x; } void main(){}", "TypeCannotBeInferred(", "prefix"),
    C("c037_cannot_infer_arg_compound", "TypeCannotBeInferred", "param type does not infer both leaves", "void f(int x){} void main(){ auto a; auto b; f(a+b);} ", "TypeCannotBeInferred(", "prefix"),
    C("c038_valid_auto_tiebreak_int_literal", "auto infer tie-break", "unknown + int literal fixed to int", "void main(){ auto a; a=1+a; printInt(a);} "),
    C("c039_stmt_mismatch_if_cond", "TypeMismatchInStatement", "if condition must be int", "void main(){ float x=1.2; if(x){} }", "TypeMismatchInStatement(", "prefix"),
    C("c040_stmt_mismatch_while_cond", "TypeMismatchInStatement", "while condition must be int", "void main(){ string s=\"a\"; while(s){} }", "TypeMismatchInStatement(", "prefix"),
    C("c041_stmt_mismatch_for_cond", "TypeMismatchInStatement", "for condition must be int", "void main(){ for(int i=0; 1.5; ++i){} }", "TypeMismatchInStatement(", "prefix"),
    C("c042_stmt_mismatch_return_void_with_expr", "TypeMismatchInStatement", "void function cannot return value", "void f(){ return 1; } void main(){}", "TypeMismatchInStatement(", "prefix"),
    C("c043_stmt_mismatch_return_nonvoid_empty", "TypeMismatchInStatement", "non-void function requires expr return", "int f(){ return; } void main(){}", "TypeMismatchInStatement(", "prefix"),
    C("c044_stmt_mismatch_return_conflict_inferred", "TypeMismatchInStatement", "first return infers int then float conflicts", "f(){ return 1; return 2.0; } void main(){}", "TypeMismatchInStatement(", "prefix"),
    C("c045_stmt_mismatch_assign_stmt", "TypeMismatchInStatement", "assignment stmt incompatible rhs", "void main(){ int x=1; x=2.0; }", "TypeMismatchInStatement(", "prefix"),
    C("c046_stmt_mismatch_switch_expr", "TypeMismatchInStatement", "switch selector must be int", "void main(){ float x=1.0; switch(x){case 1: break;} }", "TypeMismatchInStatement(", "prefix"),
    C("c047_stmt_mismatch_switch_case", "TypeMismatchInStatement", "case expression must be int", "void main(){ int x=1; switch(x){ case 1.5: break; } }", "TypeMismatchInStatement(", "prefix"),
    C("c048_stmt_mismatch_main_signature_param", "entrypoint", "main must have no params", "void main(int x){}", "TypeMismatchInStatement(", "prefix"),
    C("c049_stmt_mismatch_main_signature_ret", "entrypoint", "main must return void", "int main(){ return 1; }", "TypeMismatchInStatement(", "prefix"),
    C("c050_expr_mismatch_add_string", "TypeMismatchInExpression", "string not allowed in +", "void main(){ int x=1+\"a\"; }", "TypeMismatchInExpression(", "prefix"),
    C("c051_expr_mismatch_mod_float", "TypeMismatchInExpression", "% requires int", "void main(){ int x=3.0%2; }", "TypeMismatchInExpression(", "prefix"),
    C("c052_expr_mismatch_rel_string", "TypeMismatchInExpression", "relational not for string", "void main(){ int x=\"a\"<\"b\"; }", "TypeMismatchInExpression(", "prefix"),
    C("c053_expr_mismatch_logic_float", "TypeMismatchInExpression", "logical requires int", "void main(){ int x=1.0&&2.0; }", "TypeMismatchInExpression(", "prefix"),
    C("c054_expr_mismatch_not_float", "TypeMismatchInExpression", "! requires int", "void main(){ int x=!1.0; }", "TypeMismatchInExpression(", "prefix"),
    C("c055_expr_mismatch_unary_minus_string", "TypeMismatchInExpression", "unary - requires numeric", "void main(){ int x=-\"a\"; }", "TypeMismatchInExpression(", "prefix"),
    C("c056_expr_mismatch_prefix_inc_float", "TypeMismatchInExpression", "++ requires int lvalue", "void main(){ float x=1.0; ++x; }", "TypeMismatchInExpression(", "prefix"),
    C("c057_expr_mismatch_postfix_dec_float", "TypeMismatchInExpression", "-- requires int lvalue", "void main(){ float x=1.0; x--; }", "TypeMismatchInExpression(", "prefix"),
    C("c058_expr_mismatch_inc_non_lvalue", "TypeMismatchInExpression", "cannot increment non-lvalue", "void main(){ int x=1; ++(x+1); }", "TypeMismatchInExpression(", "prefix"),
    C("c059_expr_mismatch_call_arity", "TypeMismatchInExpression", "arg count mismatch", "int f(int x){return x;} void main(){ int a=f(1,2);} ", "TypeMismatchInExpression(", "prefix"),
    C("c060_expr_mismatch_call_arg_type", "TypeMismatchInExpression", "arg type mismatch", "int f(int x){return x;} void main(){ int a=f(1.0);} ", "TypeMismatchInExpression(", "prefix"),
    C("c061_expr_mismatch_call_void_in_expr", "TypeMismatchInStatement", "void call in typed var init is reported at statement", "void f(){} void main(){ int x=f(); }", "TypeMismatchInStatement(", "prefix"),
    C("c062_expr_mismatch_member_on_nonstruct", "TypeMismatchInExpression", "dot lhs must be struct", "void main(){ int x=1; int y=x.z; }", "TypeMismatchInExpression(", "prefix"),
    C("c063_expr_mismatch_struct_eq", "TypeMismatchInExpression", "struct has no relational ops", "struct P{int x;}; void main(){ P a={1}; P b={2}; int c=a==b; }", "TypeMismatchInExpression(", "prefix"),
    C("c064_mustinloop_cross_function_break", "MustInLoop", "loop context does not cross function boundary", "void helper(){ break; } void main(){ for(int i=0;i<1;++i){ helper(); } }", "MustInLoop(", "prefix"),
    C("c065_missing_main", "entrypoint", "program must contain void main()", "int f(){ return 1; }", "UndeclaredFunction(main)", "exact"),
    C("c066_expr_mismatch_assign_rhs_type", "TypeMismatchInExpression", "assignment expr checks rhs type", "void main(){ int a=1; int b=(a=\"s\"); }", "TypeMismatchInExpression(", "prefix"),
    C("c067_expr_mismatch_struct_literal_arity", "TypeMismatchInExpression", "literal element count must match", "struct P{int x; int y;}; void main(){ P p={1}; }", "TypeMismatchInExpression(", "prefix"),
    C("c068_expr_mismatch_struct_literal_type", "TypeMismatchInExpression", "literal member type mismatch", "struct P{int x;}; void main(){ P p={1.0}; }", "TypeMismatchInExpression(", "prefix"),
    C("c069_expr_mismatch_nested_struct_literal", "TypeMismatchInExpression", "nested member literal wrong", "struct A{int x;}; struct B{A a;}; void main(){ B b={{1.5}}; }", "TypeMismatchInExpression(", "prefix"),
    C("c070_mustinloop_break_outside", "MustInLoop", "break outside loop/switch", "void main(){ break; }", "MustInLoop(", "prefix"),
    C("c071_mustinloop_continue_outside", "MustInLoop", "continue outside loop", "void main(){ continue; }", "MustInLoop(", "prefix"),
    C("c072_mustinloop_continue_in_switch", "MustInLoop", "switch is not loop for continue", "void main(){ int x=1; switch(x){ case 1: continue; } }", "MustInLoop(", "prefix"),
    C("c073_valid_break_in_switch", "MustInLoop", "break allowed in switch", "void main(){ int x=1; switch(x){ case 1: break; } }"),
    C("c074_valid_nested_loop_break", "MustInLoop", "break in nested loop legal", "void main(){ while(1){ for(int i=0;i<1;++i){ break; } break; } }"),
    C("c075_valid_shadow_local", "scope", "inner local shadows outer local", "void main(){ int x=1; {int x=2; printInt(x);} printInt(x);} "),
    C("c076_valid_function_struct_same_name", "namespace", "function/struct namespaces separate", "struct A{}; int A(){return 1;} void main(){ int x=A(); }"),
    C("c077_valid_forward_builtin", "builtin", "builtin available globally", "void main(){ printString(readString()); }"),
    C("c078_valid_assignment_chain", "assignment expr", "right-associative compatible chain", "void main(){ int a=0; int b=0; int c=0; a=b=c=1; }"),
    C("c079_valid_member_assignment_expr", "assignment expr", "member as valid lvalue", "struct P{int x;}; void main(){ P p={1}; int y=(p.x=2); }"),
    C("c080_valid_struct_copy", "struct assignment", "same struct assignment allowed", "struct P{int x;}; void main(){ P a={1}; P b; b=a; }"),
    C("c081_valid_return_void_inferred", "inferred return", "no return expr infers void", "f(){ int x=1; } void main(){ f(); }"),
    C("c082_valid_return_inferred_float", "inferred return", "first valued return is float", "f(){ return 1.0; } void main(){ float x=f(); }"),
    C("c083_valid_call_with_struct_arg", "function call struct", "arg struct type matches param", "struct P{int x;}; void f(P p){} void main(){ P p={1}; f(p);} "),
    C("c084_valid_struct_literal_in_call", "function call struct literal", "context gives literal struct type", "struct P{int x;}; void f(P p){} void main(){ f({1}); }"),
    C("c085_valid_switch_cases_expr", "switch", "case int constant expressions valid", "void main(){ int x=1; switch(x){ case 1+2: break; case (3): break; default: break;} }"),
    C("c086_valid_if_else_blocks", "if", "both branches well typed", "void main(){ int x=1; if(x){int a=1;} else {int b=2;} }"),
    C("c087_valid_while_with_assign_expr", "while", "condition int from relational", "void main(){ int x=0; while((x=x+1)<3){} }"),
    C("c088_valid_for_missing_parts", "for", "optional init/cond/update accepted", "void main(){ int i=0; for(;i<2;){ i=i+1; } }"),
    C("c089_valid_parenthesized_member", "member access", "parenthesized struct expr member", "struct P{int x;}; void main(){ P p={1}; int a=(p).x; }"),
    C("c090_valid_complex_expr", "precedence", "mixed precedence still type-correct", "void main(){ int a=1; int b=2; int c=3; int d=a+b*c==7||0; }"),
    C("c091_first_failure_redecl_before_body", "visit order", "duplicate function found before stmt checks", "int f(){return 1;} int f(){return 2;} void main(){ int x=\"s\"; }", "Redeclared(", "prefix"),
    C("c092_first_failure_undeclared_before_mismatch", "visit order", "undeclared id appears before outer mismatch", "void main(){ int x=y+\"s\"; }", "UndeclaredIdentifier(", "prefix"),
    C("c093_first_failure_stmt_before_expr_inside", "visit order", "if cond mismatch surfaced at stmt level", "void main(){ if(1.2){ int x=1+\"a\"; } }", "TypeMismatchInStatement(", "prefix"),
    C("c094_first_failure_mustinloop_before_inner", "visit order", "break outside loop raised immediately", "void main(){ break; int x=1+\"a\"; }", "MustInLoop(", "prefix"),
    C("c095_first_failure_return_conflict", "visit order", "first return fixes type then second conflicts", "f(){ return 1; return \"s\"; } void main(){}", "TypeMismatchInStatement(", "prefix"),
    C("c096_expr_call_unknown_vs_arg", "visit order", "unknown function reported before arg typing", "void main(){ foo(1+\"a\"); }", "UndeclaredFunction(", "prefix"),
    C("c097_struct_use_before_decl", "decl-before-use", "struct must be declared before use", "void main(){ A a; } struct A{int x;};", "UndeclaredStruct(", "prefix"),
    C("c098_func_use_before_decl", "decl-before-use", "function must be declared before call", "void main(){ f(); } void f(){}", "UndeclaredFunction(", "prefix"),
    C("c099_valid_recursive_after_decl", "function", "self recursive call in declared function", "int f(int n){ if(n) return f(n-1); return 0; } void main(){ int x=f(2);} "),
    C("c100_valid_nested_struct_init", "struct literal nested", "nested struct literal correct", "struct P{int x;}; struct Q{P p; int y;}; void main(){ Q q={{1},2}; }"),
]


assert len(CASES) == 100


@pytest.mark.parametrize("name,rule,why_first_failure,source,mode,expected", CASES)
def test_checker_cases(name, rule, why_first_failure, source, mode, expected):
    result = Checker(source).check_from_source()
    note = f"[{name}] rule={rule}; first_failure={why_first_failure}; got={result}"
    if mode == "exact":
        assert result == expected, note
    else:
        assert result.startswith(expected), note
