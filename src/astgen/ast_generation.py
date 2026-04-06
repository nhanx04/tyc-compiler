from build.TyCVisitor import TyCVisitor
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    def visitProgram(self, ctx):
        decls = [self.visit(c) for c in ctx.getChildren() if type(c).__name__.endswith(("StructsContext", "FunctionsContext"))]
        return Program(decls)

    def visitStructs(self, ctx):
        return StructDecl(ctx.ID().getText(), [self.visit(x) for x in ctx.struct_var_statement()])

    def visitStruct_var_statement(self, ctx):
        return MemberDecl(self.visit(ctx.all_struct_type()), ctx.ID().getText())

    def visitAll_struct_type(self, ctx):
        t = ctx.getText()
        if t == "int":
            return IntType()
        if t == "float":
            return FloatType()
        if t == "string":
            return StringType()
        return StructType(t)

    def visitFunctions(self, ctx):
        return FuncDecl(self.visit(ctx.all_func_type()) if ctx.all_func_type() else None, ctx.ID().getText(), self.visit(ctx.params()) if ctx.params() else [], self.visit(ctx.block_statement()))

    def visitAll_func_type(self, ctx):
        t = ctx.getText()
        if t == "int":
            return IntType()
        if t == "float":
            return FloatType()
        if t == "string":
            return StringType()
        if t == "void":
            return VoidType()
        return StructType(t)

    def visitParams(self, ctx):
        return self.visit(ctx.list_param()) if ctx.list_param() else []

    def visitList_param(self, ctx):
        tys, ids = ctx.all_param_type(), ctx.ID()
        return [Param(self.visit(ty), ids[i].getText()) for i, ty in enumerate(tys)]

    def visitAll_param_type(self, ctx):
        t = ctx.getText()
        if t == "int":
            return IntType()
        if t == "float":
            return FloatType()
        if t == "string":
            return StringType()
        return StructType(t)

    def visitList_statement(self, ctx):
        return [self.visit(s) for s in ctx.statement()]

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitVar_statement(self, ctx):
        return VarDecl(self.visit(ctx.all_type()), ctx.ID().getText(), self.visit(ctx.expression()) if ctx.expression() else None)

    def visitAll_type(self, ctx):
        t = ctx.getText()
        if t == "int":
            return IntType()
        if t == "float":
            return FloatType()
        if t == "string":
            return StringType()
        if t == "auto":
            return None
        return StructType(t)

    def visitIf_statement(self, ctx):
        return IfStmt(self.visit(ctx.expression()), self.visit(ctx.statement(0)), self.visit(ctx.statement(1)) if len(ctx.statement()) > 1 else None)

    def visitWhile_statement(self, ctx):
        return WhileStmt(self.visit(ctx.expression()), self.visit(ctx.statement()))

    def visitFor_statement(self, ctx):
        return ForStmt(self.visit(ctx.first()) if ctx.first() else None, self.visit(ctx.expression()) if ctx.expression() else None, self.visit(ctx.third()) if ctx.third() else None, self.visit(ctx.statement()))

    def visitFirst(self, ctx):
        return self.visit(ctx.for_var_statement()) if ctx.for_var_statement() else ExprStmt(self.visit(ctx.assign()))

    def visitFor_var_statement(self, ctx):
        var_type = self.visit(ctx.all_type()) if ctx.all_type() else StructType(ctx.ID(0).getText())
        var_name = ctx.ID()[-1].getText() if isinstance(ctx.ID(), list) else ctx.ID().getText()
        return VarDecl(var_type, var_name, self.visit(ctx.expression()) if ctx.expression() else None)

    def visitThird(self, ctx):
        return self.visit(ctx.incre_decre()) if ctx.incre_decre() else self.visit(ctx.assign())

    def visitIncre_decre(self, ctx):
        if ctx.getChild(0).getText() in ["++", "--"]:
            return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.lhs()))
        return PostfixOp(ctx.getChild(1).getText(), self.visit(ctx.lhs()))

    def visitAssign(self, ctx):
        return AssignExpr(self.visit(ctx.lhs()), self.visit(ctx.expression()))

    def visitSwitch_statement(self, ctx):
        return SwitchStmt(self.visit(ctx.expression()), [self.visit(c) for c in ctx.case_statement()], self.visit(ctx.default_statement()) if ctx.default_statement() else None)

    def visitCase_statement(self, ctx):
        return CaseStmt(self.visit(ctx.expression()), self.visit(ctx.list_statement()) if ctx.list_statement() else [])

    def visitDefault_statement(self, ctx):
        return DefaultStmt(self.visit(ctx.list_statement()) if ctx.list_statement() else [])

    def visitBreak_statement(self, _):
        return BreakStmt()

    def visitContinue_statement(self, _):
        return ContinueStmt()

    def visitBlock_statement(self, ctx):
        return BlockStmt(self.visit(ctx.list_statement()) if ctx.list_statement() else [])

    def visitExpression_statement(self, ctx):
        return ExprStmt(self.visit(ctx.expression()))

    def visitReturn_statement(self, ctx):
        return ReturnStmt(self.visit(ctx.expression()) if ctx.expression() else None)

    def visitCall_statement(self, ctx):
        return ExprStmt(self.visit(ctx.function_call()))

    def visitList_expression(self, ctx):
        return [self.visit(e) for e in ctx.expression()]

    def visitExpression(self, ctx):
        if ctx.ASSIGN(): return AssignExpr(self.visit(ctx.lhs()), self.visit(ctx.expression()))
        return self.visit(ctx.expression1()) if ctx.expression1() else self.visit(ctx.all_literal())

    def visitLhs(self, ctx):
        return Identifier(ctx.ID().getText()) if ctx.getChildCount() == 1 else MemberAccess(self.visit(ctx.expression10()), ctx.ID().getText())

    def visitExpression1(self, ctx):
        return self.visit(ctx.expression2()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression1()), ctx.OR().getText(), self.visit(ctx.expression2()))

    def visitExpression2(self, ctx):
        return self.visit(ctx.expression3()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression2()), ctx.AND().getText(), self.visit(ctx.expression3()))

    def visitExpression3(self, ctx):
        return self.visit(ctx.expression4()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression3()), ctx.getChild(1).getText(), self.visit(ctx.expression4()))

    def visitExpression4(self, ctx):
        return self.visit(ctx.expression5()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression4()), ctx.getChild(1).getText(), self.visit(ctx.expression5()))

    def visitExpression5(self, ctx):
        return self.visit(ctx.expression6()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression5()), ctx.getChild(1).getText(), self.visit(ctx.expression6()))

    def visitExpression6(self, ctx):
        return self.visit(ctx.expression7()) if ctx.getChildCount() == 1 else BinaryOp(self.visit(ctx.expression6()), ctx.getChild(1).getText(), self.visit(ctx.expression7()))

    def visitExpression7(self, ctx):
        return self.visit(ctx.expression8()) if ctx.getChildCount() == 1 else PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expression7()))

    def visitExpression8(self, ctx):
        return self.visit(ctx.expression9()) if ctx.getChildCount() == 1 else PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expression8()))

    def visitExpression9(self, ctx):
        return self.visit(ctx.expression10()) if ctx.getChildCount() == 1 else PostfixOp(ctx.getChild(1).getText(), self.visit(ctx.expression9()))

    def visitExpression10(self, ctx):
        return self.visit(ctx.primary()) if ctx.getChildCount() == 1 else MemberAccess(self.visit(ctx.expression10()), ctx.ID().getText())

    def visitPrimary(self, ctx):
        if ctx.expression(): return self.visit(ctx.expression())
        if ctx.all_literal(): return self.visit(ctx.all_literal())
        if ctx.function_call(): return self.visit(ctx.function_call())
        return Identifier(ctx.ID().getText())

    def visitFunction_call(self, ctx):
        return FuncCall(ctx.ID().getText(), [self.visit(e) for e in ctx.expression()])

    def visitAll_literal(self, ctx):
        if ctx.INT_LIT(): return IntLiteral(int(ctx.INT_LIT().getText()))
        if ctx.FLOAT_LIT(): return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        if ctx.STRING_LIT(): return StringLiteral(ctx.STRING_LIT().getText())
        return self.visit(ctx.struct_literal())

    def visitStruct_literal(self, ctx):
        return StructLiteral([self.visit(e) for e in ctx.expression()])