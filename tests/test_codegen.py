"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))
            ])
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(42)]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(6), "*", IntLiteral(7))
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                    ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("no")]))
                )
            ])
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        ))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add", [IntLiteral(20), IntLiteral(22)])
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(20)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011_string_concat_and_print():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [BinaryOp(StringLiteral("Hello "), "+", StringLiteral("TyC"))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "Hello TyC"


def test_012_float_arithmetic():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(1.5), "+", FloatLiteral(2.25))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "3.75"


def test_013_relational_and_if_else():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(3), ">", IntLiteral(2)),
                   ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("F")])) )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "T"


def test_014_nested_if():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                   IfStmt(BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                          ExprStmt(FuncCall("printString", [StringLiteral("nested")])),
                          ExprStmt(FuncCall("printString", [StringLiteral("no")]))),
                   ExprStmt(FuncCall("printString", [StringLiteral("no")])) )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "nested"


def test_015_while_loop_sum():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            VarDecl(IntType(), "sum", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(4)), BlockStmt([
                ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i")))),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ])),
            ExprStmt(FuncCall("printInt", [Identifier("sum")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "6"


def test_016_for_loop():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "sum", IntLiteral(0)),
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                BlockStmt([ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))))])
            ),
            ExprStmt(FuncCall("printInt", [Identifier("sum")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "6"


def test_017_break_and_continue():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(6)), BlockStmt([
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), ContinueStmt(), BlockStmt([])),
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(5)), BreakStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "134"


def test_018_function_call_and_return():
    ast = Program([
        FuncDecl(IntType(), "add", [Param(IntType(), "a"), Param(IntType(), "b")],
                 BlockStmt([ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("add", [IntLiteral(10), IntLiteral(32)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_019_prefix_and_postfix_ops():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            ExprStmt(FuncCall("printInt", [PrefixOp("++", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [PostfixOp("++", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "223"


def test_020_assignment_expression():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(5)),
            ExprStmt(FuncCall("printInt", [AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "*", IntLiteral(3)))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "1515"



def test_021_function_with_multiple_returns():
    ast = Program([
        FuncDecl(IntType(), "abs_val", [Param(IntType(), "x")], BlockStmt([
            IfStmt(BinaryOp(Identifier("x"), "<", IntLiteral(0)),
                   ReturnStmt(BinaryOp(IntLiteral(0), "-", Identifier("x"))),
                   ReturnStmt(Identifier("x")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("abs_val", [IntLiteral(-7)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_022_nested_while_and_if():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(3)), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(1)),
                       ExprStmt(FuncCall("printString", [StringLiteral("B")])),
                       ExprStmt(FuncCall("printString", [StringLiteral("A")]))),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ABA"


def test_023_for_loop_with_continue():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                BlockStmt([
                    IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), ContinueStmt(), BlockStmt([])),
                    ExprStmt(FuncCall("printInt", [Identifier("i")]))
                ])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "0134"


def test_024_for_loop_with_break():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                BlockStmt([
                    IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)), BreakStmt(), BlockStmt([])),
                    ExprStmt(FuncCall("printInt", [Identifier("i")]))
                ])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_025_function_calls_chain():
    ast = Program([
        FuncDecl(IntType(), "inc", [Param(IntType(), "x")], BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(1)))])),
        FuncDecl(IntType(), "twice", [Param(IntType(), "y")], BlockStmt([ReturnStmt(BinaryOp(Identifier("y"), "*", IntLiteral(2)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("twice", [FuncCall("inc", [IntLiteral(20)])])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_026_expression_statements_discard_values():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(IntLiteral(1), "+", IntLiteral(2))),
            ExprStmt(FuncCall("printString", [StringLiteral("done")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "done"


def test_027_mixed_arithmetic_precedence():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [BinaryOp(BinaryOp(IntLiteral(2), "+", IntLiteral(3)), "*", IntLiteral(4))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "20"


def test_028_equality_and_inequality():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(5), "==", IntLiteral(5)),
                   ExprStmt(FuncCall("printString", [StringLiteral("eq")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("ne")]))),
            IfStmt(BinaryOp(IntLiteral(5), "!=", IntLiteral(4)),
                   ExprStmt(FuncCall("printString", [StringLiteral("ok")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("bad")])) )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "eqok"


def test_029_nested_function_scopes():
    ast = Program([
        FuncDecl(IntType(), "add3", [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c")],
                 BlockStmt([ReturnStmt(BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "+", Identifier("c")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("add3", [IntLiteral(10), IntLiteral(20), IntLiteral(12)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_030_float_and_int_mixed_arithmetic():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printFloat", [BinaryOp(IntLiteral(2), "+", FloatLiteral(0.5))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "2.5"



def test_031_struct_member_assignment_and_access():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(1), IntLiteral(2)])),
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "x"), IntLiteral(5))),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "52"


def test_032_nested_struct_access():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        StructDecl("Box", [MemberDecl(StructType("Point"), "p")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Box"), "b", StructLiteral([IntLiteral(0)])),
            ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("b"), "p"), "x"), IntLiteral(9))),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("b"), "p"), "x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "9"


def test_033_switch_case_default():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(2)),
            SwitchStmt(
                Identifier("x"),
                [
                    CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("one")]))]),
                    CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("two")]))]),
                ],
                DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("other")]))])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "two"


def test_034_switch_default_fallback():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                IntLiteral(9),
                [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("one")]))])],
                DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("other")]))])
            )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "other"


def test_035_struct_literal_with_assignment_and_prints():
    ast = Program([
        StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Pair"), "p", StructLiteral([IntLiteral(3), IntLiteral(4)])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "a")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "b")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "34"



def test_036_nested_function_and_struct_usage():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        FuncDecl(IntType(), "sum_point", [Param(StructType("Point"), "p")],
                 BlockStmt([ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "x"), "+", MemberAccess(Identifier("p"), "y")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(10), IntLiteral(32)])),
            ExprStmt(FuncCall("printInt", [FuncCall("sum_point", [Identifier("p")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_037_loop_with_postfix_increment():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(3)), BlockStmt([
                ExprStmt(FuncCall("printInt", [PostfixOp("++", Identifier("i"))]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_038_prefix_decrement_and_assignment():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(5)),
            ExprStmt(FuncCall("printInt", [PrefixOp("--", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")])),
            ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(10)))),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "445"


def test_039_deeply_nested_control_flow():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(4)), BlockStmt([
                IfStmt(BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                       ExprStmt(FuncCall("printString", [StringLiteral("E")])),
                       ExprStmt(FuncCall("printString", [StringLiteral("O")]))),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "EOEO"


def test_040_mixed_prints_and_returns():
    ast = Program([
        FuncDecl(IntType(), "id", [Param(IntType(), "x")], BlockStmt([ReturnStmt(Identifier("x"))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [StringLiteral("start")])),
            ExprStmt(FuncCall("printInt", [FuncCall("id", [IntLiteral(40)])])),
            ExprStmt(FuncCall("printString", [StringLiteral("end")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "start40end"



def test_041_if_without_else():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                   ExprStmt(FuncCall("printString", [StringLiteral("hit")]))),
            ExprStmt(FuncCall("printString", [StringLiteral("done")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "hitdone"


def test_042_multi_argument_function_and_local_vars():
    ast = Program([
        FuncDecl(IntType(), "mix", [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c")],
                 BlockStmt([
                     VarDecl(IntType(), "t", BinaryOp(Identifier("a"), "+", Identifier("b"))),
                     ReturnStmt(BinaryOp(Identifier("t"), "+", Identifier("c")))
                 ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("mix", [IntLiteral(10), IntLiteral(20), IntLiteral(12)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_043_nested_break_inside_while():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(10)), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)), BreakStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")])),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "012"


def test_044_structs_and_functions_together():
    ast = Program([
        StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
        FuncDecl(IntType(), "sum_pair", [Param(StructType("Pair"), "p")],
                 BlockStmt([ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "a"), "+", MemberAccess(Identifier("p"), "b")))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Pair"), "p", StructLiteral([IntLiteral(19), IntLiteral(23)])),
            ExprStmt(FuncCall("printInt", [FuncCall("sum_pair", [Identifier("p")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_045_switch_without_default():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                IntLiteral(1),
                [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("one")]))])],
                None
            ),
            ExprStmt(FuncCall("printString", [StringLiteral("done")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "onedone"



def test_046_postfix_decrement_returns_old_value():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(3)),
            ExprStmt(FuncCall("printInt", [PostfixOp("--", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "32"


def test_047_nested_struct_field_update():
    ast = Program([
        StructDecl("Inner", [MemberDecl(IntType(), "n")]),
        StructDecl("Outer", [MemberDecl(StructType("Inner"), "inner")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(1)])])),
            ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("o"), "inner"), "n"), IntLiteral(7))),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("o"), "inner"), "n")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "7"


def test_048_float_branch_and_prints():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(FloatLiteral(1.5), "<", FloatLiteral(2.0)),
                   ExprStmt(FuncCall("printString", [StringLiteral("lt")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("ge")]))),
            ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(1.25), "+", FloatLiteral(0.75))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "lt2.0"


def test_049_empty_loop_body_with_continue():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(4)), BlockStmt([
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), ContinueStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "134"


def test_050_chained_calls_and_returned_value():
    ast = Program([
        FuncDecl(IntType(), "inc", [Param(IntType(), "x")], BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(1)))])),
        FuncDecl(IntType(), "twice", [Param(IntType(), "x")], BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "*", IntLiteral(2)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("twice", [FuncCall("inc", [IntLiteral(20)])])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"



def test_051_struct_member_assignment_via_function():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        FuncDecl(VoidType(), "shift", [Param(StructType("Point"), "p")], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "x"), BinaryOp(MemberAccess(Identifier("p"), "x"), "+", IntLiteral(5)))),
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "y"), BinaryOp(MemberAccess(Identifier("p"), "y"), "+", IntLiteral(7))))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(1), IntLiteral(2)])),
            ExprStmt(FuncCall("shift", [Identifier("p")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "612"


def test_052_nested_switch_and_loop():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(3)), BlockStmt([
                SwitchStmt(
                    Identifier("i"),
                    [
                        CaseStmt(IntLiteral(0), [ExprStmt(FuncCall("printString", [StringLiteral("a")]))]),
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("b")]))]),
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("c")]))])
                ),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "abc"


def test_053_multiple_returns_and_if_else():
    ast = Program([
        FuncDecl(IntType(), "abs_like", [Param(IntType(), "x")], BlockStmt([
            IfStmt(BinaryOp(Identifier("x"), "<", IntLiteral(0)), ReturnStmt(BinaryOp(IntLiteral(0), "-", Identifier("x"))), BlockStmt([])),
            ReturnStmt(Identifier("x"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("abs_like", [IntLiteral(-42)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_054_nested_function_calls_with_strings():
    ast = Program([
        FuncDecl(StringType(), "wrap", [Param(StringType(), "s")], BlockStmt([ReturnStmt(BinaryOp(StringLiteral("<"), "+", BinaryOp(Identifier("s"), "+", StringLiteral(">"))))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [FuncCall("wrap", [StringLiteral("x")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "<x>"


def test_055_prefix_increment_on_member_access():
    ast = Program([
        StructDecl("Counter", [MemberDecl(IntType(), "n")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Counter"), "c", StructLiteral([IntLiteral(9)])),
            ExprStmt(FuncCall("printInt", [PrefixOp("++", MemberAccess(Identifier("c"), "n"))])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("c"), "n")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "1010"



def test_056_boolean_like_relational_chain():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(3), ">", IntLiteral(2)),
                   ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("F")]))),
            IfStmt(BinaryOp(IntLiteral(2), "<", IntLiteral(1)),
                   ExprStmt(FuncCall("printString", [StringLiteral("X")])),
                   ExprStmt(FuncCall("printString", [StringLiteral("Y")]))),
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "TY"


def test_057_nested_while_and_continue():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(3)), BlockStmt([
                VarDecl(IntType(), "j", IntLiteral(0)),
                WhileStmt(BinaryOp(Identifier("j"), "<", IntLiteral(3)), BlockStmt([
                    ExprStmt(AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1)))),
                    IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(2)), ContinueStmt(), BlockStmt([])),
                    ExprStmt(FuncCall("printInt", [Identifier("j")]))
                ])),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "111111"


def test_058_float_arithmetic_output():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(3.5), "-", FloatLiteral(1.0))])),
            ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(2.0), "*", FloatLiteral(2.5))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "2.54.0"


def test_059_function_returning_struct_field_sum():
    ast = Program([
        StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
        FuncDecl(IntType(), "sum", [Param(StructType("Pair"), "p")], BlockStmt([
            ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "a"), "+", MemberAccess(Identifier("p"), "b")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Pair"), "p", StructLiteral([IntLiteral(20), IntLiteral(22)])),
            ExprStmt(FuncCall("printInt", [FuncCall("sum", [Identifier("p")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_060_switch_case_two_matches_first_wins():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(IntLiteral(2), [
                CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("A")]))]),
                CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("B")]))]),
            ], None)
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "A"


def test_061_prefix_increment_returns_new_value():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            ExprStmt(FuncCall("printInt", [PrefixOp("++", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "22"


def test_062_postfix_increment_returns_old_value():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            ExprStmt(FuncCall("printInt", [PostfixOp("++", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "12"


def test_063_member_access_in_expression():
    ast = Program([
        StructDecl("Box", [MemberDecl(IntType(), "v")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Box"), "b", StructLiteral([IntLiteral(40)])),
            ExprStmt(FuncCall("printInt", [BinaryOp(MemberAccess(Identifier("b"), "v"), "+", IntLiteral(2))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_064_string_concat_and_return():
    ast = Program([
        FuncDecl(StringType(), "greet", [Param(StringType(), "name")], BlockStmt([
            ReturnStmt(BinaryOp(StringLiteral("hi "), "+", Identifier("name")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [FuncCall("greet", [StringLiteral("tyc")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "hi tyc"


def test_065_empty_function_side_effects():
    ast = Program([
        FuncDecl(VoidType(), "say", [], BlockStmt([
            ExprStmt(FuncCall("printString", [StringLiteral("ok")]))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("say", [])),
            ExprStmt(FuncCall("printString", [StringLiteral("done")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "okdone"


def test_066_assignment_expression_in_print():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(0)),
            ExprStmt(FuncCall("printInt", [AssignExpr(Identifier("x"), IntLiteral(7))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "77"


def test_067_nested_if_else_output():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(1)),
                   IfStmt(BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                          ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                          ExprStmt(FuncCall("printString", [StringLiteral("no")]))),
                   ExprStmt(FuncCall("printString", [StringLiteral("bad")])) )
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "yes"


def test_068_for_loop_sum_print():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "s", IntLiteral(0)),
            ForStmt(VarDecl(IntType(), "i", IntLiteral(1)), BinaryOp(Identifier("i"), "<", IntLiteral(5)), AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))), BlockStmt([
                ExprStmt(AssignExpr(Identifier("s"), BinaryOp(Identifier("s"), "+", Identifier("i"))))
            ])),
            ExprStmt(FuncCall("printInt", [Identifier("s")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "10"


def test_069_break_in_for_loop():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(5)), AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), BreakStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "01"


def test_070_continue_in_for_loop():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(4)), AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(1)), ContinueStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "023"



def test_071_struct_literal_then_field_read():
    ast = Program([
        StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Pair"), "p", StructLiteral([IntLiteral(4), IntLiteral(2)])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "a")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "b")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_072_nested_struct_literal_and_access():
    ast = Program([
        StructDecl("Inner", [MemberDecl(IntType(), "n")]),
        StructDecl("Outer", [MemberDecl(StructType("Inner"), "inner")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(5)])])),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("o"), "inner"), "n")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "5"


def test_073_function_parameter_passing_by_value():
    ast = Program([
        FuncDecl(VoidType(), "inc", [Param(IntType(), "x")], BlockStmt([
            ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1))))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            ExprStmt(FuncCall("inc", [Identifier("x")])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "1"


def test_074_function_call_as_statement_and_expression():
    ast = Program([
        FuncDecl(IntType(), "f", [], BlockStmt([ReturnStmt(IntLiteral(21))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("f", [])),
            ExprStmt(FuncCall("printInt", [BinaryOp(FuncCall("f", []), "+", FuncCall("f", []))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_075_string_print_twice():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [StringLiteral("a")])),
            ExprStmt(FuncCall("printString", [StringLiteral("b")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ab"


def test_076_float_then_int_print():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printFloat", [FloatLiteral(1.5)])),
            ExprStmt(FuncCall("printInt", [IntLiteral(2)]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "1.52"


def test_077_deep_if_while_mix():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(2)), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(0)),
                       ExprStmt(FuncCall("printString", [StringLiteral("x")])),
                       ExprStmt(FuncCall("printString", [StringLiteral("y")] ))),
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "xy"


def test_078_break_skips_remaining_statements():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(1)), BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("a")])),
                BreakStmt(),
                ExprStmt(FuncCall("printString", [StringLiteral("b")]))
            ])),
            ExprStmt(FuncCall("printString", [StringLiteral("c")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ac"


def test_079_continue_skips_remaining_statements():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "i", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntLiteral(2)), BlockStmt([
                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                ContinueStmt(),
                ExprStmt(FuncCall("printString", [StringLiteral("bad")]))
            ])),
            ExprStmt(FuncCall("printString", [StringLiteral("ok")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ok"


def test_080_nested_return_in_if():
    ast = Program([
        FuncDecl(IntType(), "f", [Param(IntType(), "x")], BlockStmt([
            IfStmt(BinaryOp(Identifier("x"), ">", IntLiteral(0)), ReturnStmt(Identifier("x")), BlockStmt([])),
            ReturnStmt(BinaryOp(IntLiteral(0), "-", Identifier("x")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("f", [IntLiteral(42)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"



def test_081_struct_member_update_then_sum():
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(1), IntLiteral(2)])),
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "x"), IntLiteral(20))),
            ExprStmt(AssignExpr(MemberAccess(Identifier("p"), "y"), IntLiteral(22))),
            ExprStmt(FuncCall("printInt", [BinaryOp(MemberAccess(Identifier("p"), "x"), "+", MemberAccess(Identifier("p"), "y"))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_082_function_with_many_parameters():
    ast = Program([
        FuncDecl(IntType(), "sum4", [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c"), Param(IntType(), "d")],
                 BlockStmt([ReturnStmt(BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "+", BinaryOp(Identifier("c"), "+", Identifier("d"))))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("sum4", [IntLiteral(10), IntLiteral(11), IntLiteral(12), IntLiteral(9)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_083_switch_default_only():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(IntLiteral(99), [], DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("d")]))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "d"


def test_084_nested_function_calls_three_deep():
    ast = Program([
        FuncDecl(IntType(), "f", [Param(IntType(), "x")], BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(1)))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("f", [FuncCall("f", [FuncCall("f", [IntLiteral(39)])])])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_085_for_loop_with_empty_body():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(3)), AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))), BlockStmt([])),
            ExprStmt(FuncCall("printString", [StringLiteral("ok")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ok"


def test_086_while_loop_never_enters():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(BinaryOp(IntLiteral(0), "==", IntLiteral(1)), BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("bad")]))
            ])),
            ExprStmt(FuncCall("printString", [StringLiteral("ok")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "ok"


def test_087_if_else_chain():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(1), "==", IntLiteral(0)),
                   ExprStmt(FuncCall("printString", [StringLiteral("a")])),
                   IfStmt(BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                          ExprStmt(FuncCall("printString", [StringLiteral("b")])),
                          ExprStmt(FuncCall("printString", [StringLiteral("c")]))))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "b"


def test_088_prefix_minus_on_literal():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [PrefixOp("-", IntLiteral(42))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "-42"


def test_089_string_and_int_combination_output():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [StringLiteral("x")])),
            ExprStmt(FuncCall("printInt", [IntLiteral(4)])),
            ExprStmt(FuncCall("printString", [StringLiteral("y")])),
            ExprStmt(FuncCall("printInt", [IntLiteral(2)]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "x4y2"


def test_090_nested_struct_functions_and_assignment():
    ast = Program([
        StructDecl("Inner", [MemberDecl(IntType(), "n")]),
        StructDecl("Outer", [MemberDecl(StructType("Inner"), "inner")]),
        FuncDecl(IntType(), "get", [Param(StructType("Outer"), "o")], BlockStmt([
            ReturnStmt(MemberAccess(MemberAccess(Identifier("o"), "inner"), "n"))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(41)])])),
            ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("o"), "inner"), "n"), IntLiteral(42))),
            ExprStmt(FuncCall("printInt", [FuncCall("get", [Identifier("o")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"



def test_091_struct_field_chain_assignment():
    ast = Program([
        StructDecl("A", [MemberDecl(IntType(), "v")]),
        StructDecl("B", [MemberDecl(StructType("A"), "a")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("B"), "b", StructLiteral([StructLiteral([IntLiteral(1)])])),
            ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("b"), "a"), "v"), IntLiteral(42))),
            ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("b"), "a"), "v")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_092_function_returning_string_concat():
    ast = Program([
        FuncDecl(StringType(), "join", [Param(StringType(), "a"), Param(StringType(), "b")], BlockStmt([
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printString", [FuncCall("join", [StringLiteral("4"), StringLiteral("2")])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_093_for_loop_nested_break_continue():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(4)), AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))), BlockStmt([
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(1)), ContinueStmt(), BlockStmt([])),
                IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)), BreakStmt(), BlockStmt([])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "02"


def test_094_multi_case_switch_then_print():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(IntLiteral(3), [
                CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("a")]))]),
                CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("b")]))]),
                CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printString", [StringLiteral("c")]))]),
            ], DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("d")]))])),
            ExprStmt(FuncCall("printString", [StringLiteral("z")]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "cz"


def test_095_prefix_increment_in_arithmetic_expression():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("++", Identifier("x")), "+", IntLiteral(40))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_096_postfix_increment_in_arithmetic_expression():
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(2)),
            ExprStmt(FuncCall("printInt", [BinaryOp(PostfixOp("++", Identifier("x")), "+", IntLiteral(40))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_097_nested_function_calls_with_struct_argument():
    ast = Program([
        StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
        FuncDecl(IntType(), "sum", [Param(StructType("Pair"), "p")], BlockStmt([
            ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "a"), "+", MemberAccess(Identifier("p"), "b")))
        ])),
        FuncDecl(IntType(), "twice", [Param(IntType(), "x")], BlockStmt([
            ReturnStmt(BinaryOp(Identifier("x"), "*", IntLiteral(2)))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Pair"), "p", StructLiteral([IntLiteral(20), IntLiteral(1)])),
            ExprStmt(FuncCall("printInt", [FuncCall("twice", [FuncCall("sum", [Identifier("p")])])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_098_void_function_with_local_assignment():
    ast = Program([
        FuncDecl(VoidType(), "set_and_print", [Param(IntType(), "x")], BlockStmt([
            VarDecl(IntType(), "y", BinaryOp(Identifier("x"), "+", IntLiteral(1))),
            ExprStmt(FuncCall("printInt", [Identifier("y")]))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("set_and_print", [IntLiteral(41)]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"


def test_099_struct_literal_and_switch_mix():
    ast = Program([
        StructDecl("S", [MemberDecl(IntType(), "v")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("S"), "s", StructLiteral([IntLiteral(2)])),
            SwitchStmt(MemberAccess(Identifier("s"), "v"), [
                CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("a")]))]),
                CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("b")]))]),
            ], DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("c")]))]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "b"


def test_100_final_coverage_case():
    ast = Program([
        FuncDecl(IntType(), "f", [Param(IntType(), "x")], BlockStmt([
            IfStmt(BinaryOp(Identifier("x"), "<", IntLiteral(40)), ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(2))), BlockStmt([])),
            ReturnStmt(IntLiteral(0))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("f", [IntLiteral(40)])]))
        ]))
    ])
    assert CodeGenerator().generate_and_run(ast) == "42"

