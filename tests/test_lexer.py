"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


# ========== Simple Test Cases (10 types) ==========
def test_keyword_auto():
    """1. Keyword"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_operator_assign():
    """2. Operator"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_separator_semi():
    """3. Separator"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_integer_single_digit():
    """4. Integer literal"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_float_decimal():
    """5. Float literal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_string_simple():
    """6. String literal"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_identifier_simple():
    """7. Identifier"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_line_comment():
    """8. Line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_integer_in_expression():
    """9. Mixed: integers and operator"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


def test_complex_expression():
    """10. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"

# ========== Extended Test Cases (Additional 100 cases) ==========

def test_keyword_all_basic():
    tokenizer = Tokenizer("auto break case continue default else float for if int return string struct switch void while")
    assert tokenizer.get_tokens_as_string() == "auto,break,case,continue,default,else,float,for,if,int,return,string,struct,switch,void,while,<EOF>"


def test_keyword_vs_identifier_1():
    tokenizer = Tokenizer("auto1")
    assert tokenizer.get_tokens_as_string() == "auto1,<EOF>"


def test_keyword_vs_identifier_2():
    tokenizer = Tokenizer("_auto")
    assert tokenizer.get_tokens_as_string() == "_auto,<EOF>"


def test_keyword_vs_identifier_3_case_sensitive():
    tokenizer = Tokenizer("Auto")
    assert tokenizer.get_tokens_as_string() == "Auto,<EOF>"


def test_identifier_many_forms_1():
    tokenizer = Tokenizer("a A _a a0 a_0 _0A")
    assert tokenizer.get_tokens_as_string() == "a,A,_a,a0,a_0,_0A,<EOF>"


def test_identifier_many_forms_2():
    tokenizer = Tokenizer("__")
    assert tokenizer.get_tokens_as_string() == "__,<EOF>"


def test_identifier_single_underscore():
    tokenizer = Tokenizer("_")
    assert tokenizer.get_tokens_as_string() == "_,<EOF>"


def test_identifier_long():
    tokenizer = Tokenizer("________x________")
    assert tokenizer.get_tokens_as_string() == "________x________,<EOF>"


def test_separator_all():
    tokenizer = Tokenizer("(){}[];,:.")
    assert tokenizer.get_tokens_as_string() == "(,),{,},[,],;,,,:,.,<EOF>"


def test_operator_arithmetic_basic():
    tokenizer = Tokenizer("+ - * / %")
    assert tokenizer.get_tokens_as_string() == "+,-,*,/,%,<EOF>"


def test_operator_relational_basic():
    tokenizer = Tokenizer("< <= > >= == !=")
    assert tokenizer.get_tokens_as_string() == "<,<=,>,>=,==,!=,<EOF>"


def test_operator_logical_basic():
    tokenizer = Tokenizer("&& || !")
    assert tokenizer.get_tokens_as_string() == "&&,||,!,<EOF>"


def test_operator_inc_dec_basic():
    tokenizer = Tokenizer("++ --")
    assert tokenizer.get_tokens_as_string() == "++,--,<EOF>"


def test_operator_longest_match_le_lt():
    tokenizer = Tokenizer("<=<")
    assert tokenizer.get_tokens_as_string() == "<=,<,<EOF>"


def test_operator_longest_match_ge_gt():
    tokenizer = Tokenizer(">=>")
    assert tokenizer.get_tokens_as_string() == ">=,>,<EOF>"


def test_operator_longest_match_eq_assign():
    tokenizer = Tokenizer("===")
    assert tokenizer.get_tokens_as_string() == "==,=,<EOF>"


def test_operator_longest_match_neq_not():
    tokenizer = Tokenizer("!=!")
    assert tokenizer.get_tokens_as_string() == "!=,!,<EOF>"


def test_operator_longest_match_inc_plus():
    tokenizer = Tokenizer("+++")
    assert tokenizer.get_tokens_as_string() == "++,+,<EOF>"


def test_operator_longest_match_dec_minus():
    tokenizer = Tokenizer("---")
    assert tokenizer.get_tokens_as_string() == "--,-,<EOF>"


def test_operator_chain_1():
    tokenizer = Tokenizer("a+++b")
    assert tokenizer.get_tokens_as_string() == "a,++, +,b,<EOF>".replace(" ", "")


def test_operator_chain_2():
    tokenizer = Tokenizer("a----b")
    assert tokenizer.get_tokens_as_string() == "a,--,--,b,<EOF>"


def test_integer_zero():
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"


def test_integer_many_digits():
    tokenizer = Tokenizer("1234567890")
    assert tokenizer.get_tokens_as_string() == "1234567890,<EOF>"


def test_integer_leading_zeroes():
    tokenizer = Tokenizer("0012")
    assert tokenizer.get_tokens_as_string() == "0012,<EOF>"


def test_integer_sequence_whitespace():
    tokenizer = Tokenizer("1 2 3")
    assert tokenizer.get_tokens_as_string() == "1,2,3,<EOF>"


def test_float_simple():
    tokenizer = Tokenizer("0.0")
    assert tokenizer.get_tokens_as_string() == "0.0,<EOF>"


def test_float_trailing_dot():
    tokenizer = Tokenizer("1.")
    assert tokenizer.get_tokens_as_string() == "1.,<EOF>"


def test_float_leading_dot():
    tokenizer = Tokenizer(".5")
    assert tokenizer.get_tokens_as_string() == ".5,<EOF>"


def test_float_exponent_lower():
    tokenizer = Tokenizer("1e4")
    assert tokenizer.get_tokens_as_string() == "1e4,<EOF>"


def test_float_exponent_upper_signed():
    tokenizer = Tokenizer("2E-3")
    assert tokenizer.get_tokens_as_string() == "2E-3,<EOF>"


def test_float_decimal_exponent():
    tokenizer = Tokenizer("1.23e+4")
    assert tokenizer.get_tokens_as_string() == "1.23e+4,<EOF>"


def test_float_many_variants_1():
    tokenizer = Tokenizer(".5 1. 0e0 5.0E2")
    assert tokenizer.get_tokens_as_string() == ".5,1.,0e0,5.0E2,<EOF>"


def test_string_empty():
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == ",<EOF>"


def test_string_simple_char():
    tokenizer = Tokenizer('"a"')
    assert tokenizer.get_tokens_as_string() == "a,<EOF>"


def test_string_with_space():
    tokenizer = Tokenizer('"hello world"')
    assert tokenizer.get_tokens_as_string() == "hello world,<EOF>"


def test_string_with_escape_tab():
    tokenizer = Tokenizer('"a\\t"')
    assert tokenizer.get_tokens_as_string() == "a\\t,<EOF>"


def test_string_with_escape_newline_literal():
    tokenizer = Tokenizer('"a\\n"')
    assert tokenizer.get_tokens_as_string() == "a\\n,<EOF>"


def test_string_with_escaped_quote():
    tokenizer = Tokenizer('"He said: \\\"hi\\\""')
    assert tokenizer.get_tokens_as_string() == "He said: \\\"hi\\\",<EOF>"


def test_string_with_backslash():
    tokenizer = Tokenizer('"\\\\"')
    assert tokenizer.get_tokens_as_string() == "\\\\,<EOF>"


def test_line_comment_then_code():
    tokenizer = Tokenizer("//c\nauto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_block_comment_then_code():
    tokenizer = Tokenizer("/*c*/auto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_block_comment_multi_line():
    tokenizer = Tokenizer("/*a\n b\n*/auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_comment_mix_1():
    tokenizer = Tokenizer("auto/*c*/x=1;//d")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,1,;,<EOF>"


def test_whitespace_tabs_newlines():
    tokenizer = Tokenizer("auto\t\nx\r\n=\f5;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,;,<EOF>"


def test_error_char_at():
    tokenizer = Tokenizer("@")
    assert tokenizer.get_tokens_as_string() == "Error Token @"


def test_error_char_hash():
    tokenizer = Tokenizer("#")
    assert tokenizer.get_tokens_as_string() == "Error Token #"


def test_error_char_caret():
    tokenizer = Tokenizer("^")
    assert tokenizer.get_tokens_as_string() == "Error Token ^"


def test_illegal_escape_1():
    tokenizer = Tokenizer('"a\\q"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: a\\q"


def test_illegal_escape_2():
    tokenizer = Tokenizer('"\\x"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: \\x"


def test_unclose_string_eof():
    tokenizer = Tokenizer('"abc')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_unclose_string_newline():
    tokenizer = Tokenizer('"abc\n')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_unclose_string_crlf():
    tokenizer = Tokenizer('"abc\r\n')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_mixed_statement_tokens_1():
    tokenizer = Tokenizer("int x=1;float y=2.0;string s=\"hi\";")
    assert tokenizer.get_tokens_as_string() == "int,x,=,1,;,float,y,=,2.0,;,string,s,=,hi,;,<EOF>"


def test_mixed_struct_tokens_1():
    tokenizer = Tokenizer("struct Point{int x;int y;};")
    assert tokenizer.get_tokens_as_string() == "struct,Point,{,int,x,;,int,y,;,},;,<EOF>"


def test_mixed_switch_tokens_1():
    tokenizer = Tokenizer("switch(x){case 1:break;default:break;}")
    assert tokenizer.get_tokens_as_string() == "switch,(,x,),{,case,1,:,break,;,default,:,break,;,},<EOF>"


def test_mixed_for_tokens_1():
    tokenizer = Tokenizer("for(auto i=0;i<10;++i){}")
    assert tokenizer.get_tokens_as_string() == "for,(,auto,i,=,0,;,i,<,10,;,++,i,),{,},<EOF>"


def test_mixed_member_access_tokens_1():
    tokenizer = Tokenizer("p.x=p.y+1;")
    assert tokenizer.get_tokens_as_string() == "p,.,x,=,p,.,y,+,1,;,<EOF>"


def test_mixed_call_tokens_1():
    tokenizer = Tokenizer("printInt(123);")
    assert tokenizer.get_tokens_as_string() == "printInt,(,123,),;,<EOF>"


def test_mixed_nested_call_tokens_1():
    tokenizer = Tokenizer("f(g(1),h(2));")
    assert tokenizer.get_tokens_as_string() == "f,(,g,(,1,),,,h,(,2,),),;,<EOF>"


def test_mixed_parentheses_tokens_1():
    tokenizer = Tokenizer("(1+(2*3));")
    assert tokenizer.get_tokens_as_string() == "(,1,+,(,2,*,3,),),;,<EOF>"


def test_mixed_relational_tokens_1():
    tokenizer = Tokenizer("(a<=b)&&(c!=d)||!e;")
    assert tokenizer.get_tokens_as_string() == "(,a,<=,b,),&&,(,c,!=,d,),||,!,e,;,<EOF>"


def test_mixed_string_in_call():
    tokenizer = Tokenizer('printString("Hello, World!");')
    assert tokenizer.get_tokens_as_string() == "printString,(,Hello, World!,),;,<EOF>"


def test_many_semicolons_separated():
    tokenizer = Tokenizer("a;b;c;d;")
    assert tokenizer.get_tokens_as_string() == "a,;,b,;,c,;,d,;,<EOF>"


def test_many_commas_in_args():
    tokenizer = Tokenizer("f(1,2,3,4);")
    assert tokenizer.get_tokens_as_string() == "f,(,1,,,2,,,3,,,4,),;,<EOF>"


def test_array_brackets_tokens_exist():
    tokenizer = Tokenizer("a[1]=2;")
    assert tokenizer.get_tokens_as_string() == "a,[,1,],=,2,;,<EOF>"


def test_dot_vs_float_1():
    tokenizer = Tokenizer("a.5")
    assert tokenizer.get_tokens_as_string() == "a,.5,<EOF>"


def test_dot_vs_float_2():
    tokenizer = Tokenizer("a..5")
    assert tokenizer.get_tokens_as_string() == "a,.,.5,<EOF>"


def test_float_vs_int_dot():
    tokenizer = Tokenizer("1..2")
    assert tokenizer.get_tokens_as_string() == "1.,.2,<EOF>"


def test_and_or_chain():
    tokenizer = Tokenizer("a&&b||c&&d")
    assert tokenizer.get_tokens_as_string() == "a,&&,b,||,c,&&,d,<EOF>"


def test_not_chain():
    tokenizer = Tokenizer("!!!a")
    assert tokenizer.get_tokens_as_string() == "!,!,!,a,<EOF>"


def test_plus_minus_unary_like():
    tokenizer = Tokenizer("+-+5")
    assert tokenizer.get_tokens_as_string() == "+,-,+,5,<EOF>"


def test_complex_whitespace_and_comments():
    tokenizer = Tokenizer("  auto  x/*c*/=\n5  +\t3;//d\n")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,;,<EOF>"
# ========== Top-up to reach 100 tests (18 more) ==========

def test_error_char_tilde():
    tokenizer = Tokenizer("~")
    assert tokenizer.get_tokens_as_string() == "Error Token ~"


def test_error_char_backtick():
    tokenizer = Tokenizer("`")
    assert tokenizer.get_tokens_as_string() == "Error Token `"


def test_error_char_question_mark():
    tokenizer = Tokenizer("?")
    assert tokenizer.get_tokens_as_string() == "Error Token ?"


def test_error_char_dollar():
    tokenizer = Tokenizer("$")
    assert tokenizer.get_tokens_as_string() == "Error Token $"


def test_error_char_unicode():
    tokenizer = Tokenizer("€")
    assert tokenizer.get_tokens_as_string() == "Error Token €"


def test_illegal_escape_3():
    tokenizer = Tokenizer('"a\\1"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: a\\1"


def test_illegal_escape_4():
    tokenizer = Tokenizer('"\\q"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: \\q"


def test_illegal_escape_5():
    tokenizer = Tokenizer('"abc\\z"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: abc\\z"


def test_unclose_string_empty_eof():
    tokenizer = Tokenizer('"')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: "


def test_unclose_string_with_cr():
    tokenizer = Tokenizer('"abc\r')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_float_exponent_plus():
    tokenizer = Tokenizer("1e+4")
    assert tokenizer.get_tokens_as_string() == "1e+4,<EOF>"


def test_float_decimal_exponent_neg():
    tokenizer = Tokenizer("1.0e-4")
    assert tokenizer.get_tokens_as_string() == "1.0e-4,<EOF>"


def test_float_just_dot_then_int():
    tokenizer = Tokenizer(". 5")
    assert tokenizer.get_tokens_as_string() == ".,5,<EOF>"


def test_relop_chain_spacing():
    tokenizer = Tokenizer("a <  b<=c")
    assert tokenizer.get_tokens_as_string() == "a,<,b,<=,c,<EOF>"


def test_comment_only_block():
    tokenizer = Tokenizer("/* only comment */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_comment_only_line_with_newline():
    tokenizer = Tokenizer("// only comment\n")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_string_with_all_valid_escapes():
    tokenizer = Tokenizer('"\\b\\f\\r\\n\\t\\\\\\\""')
    assert tokenizer.get_tokens_as_string() == "\\b\\f\\r\\n\\t\\\\\\\",<EOF>"


def test_identifier_with_digits_tail():
    tokenizer = Tokenizer("a1b2c3")
    assert tokenizer.get_tokens_as_string() == "a1b2c3,<EOF>"