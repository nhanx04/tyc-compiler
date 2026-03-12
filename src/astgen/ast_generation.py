"""AST Generation for TyC parse tree -> AST nodes."""

from build.TyCVisitor import TyCVisitor
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    def visitProgram(self, ctx):
        return Program(self.visit(ctx.topDeclList()))

    def visitTopDeclList(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.topDecl())] + self.visit(ctx.topDeclList())

    def visitTopDecl(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitStructDecl(self, ctx):
        return StructDecl(ctx.ID().getText(), self.visit(ctx.structMemberDeclList()))

    def visitStructMemberDeclList(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.structMemberDecl())] + self.visit(ctx.structMemberDeclList())

    def visitStructMemberDecl(self, ctx):
        return MemberDecl(self.visit(ctx.typeSpec()), ctx.ID().getText())

    def visitFuncDecl(self, ctx):
        return FuncDecl(
            self.visit(ctx.returnTypeOpt()),
            ctx.ID().getText(),
            self.visit(ctx.paramListOpt()),
            self.visit(ctx.blockStmt()),
        )

    def visitReturnTypeOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.returnType())

    def visitReturnType(self, ctx):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.typeSpec())

    def visitParamListOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.paramList())

    def visitParamList(self, ctx):
        return [self.visit(ctx.param())] + self.visit(ctx.paramListTail())

    def visitParamListTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.param())] + self.visit(ctx.paramListTail())

    def visitParam(self, ctx):
        return Param(self.visit(ctx.typeSpec()), ctx.ID().getText())

    def visitTypeSpec(self, ctx):
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.STRING():
            return StringType()
        return StructType(ctx.ID().getText())

    def visitStmt(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitBlockStmt(self, ctx):
        return BlockStmt(self.visit(ctx.stmtList()))

    def visitStmtList(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.stmt())] + self.visit(ctx.stmtList())

    def visitVarDeclStmt(self, ctx):
        name = ctx.ID().getText()
        if ctx.AUTO():
            init = self.visit(ctx.varDeclAutoInitOpt())
            return VarDecl(None, name, init)
        var_type = self.visit(ctx.typeSpec())
        init = self.visit(ctx.varDeclTypedInitOpt())
        return VarDecl(var_type, name, init)

    def visitVarDeclAutoInitOpt(self, ctx):
        return self.visit(ctx.expr()) if ctx.getChildCount() else None

    def visitVarDeclTypedInitOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        if ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.structInit())

    def visitStructInit(self, ctx):
        return StructLiteral(self.visit(ctx.structInitListOpt()))

    def visitStructInitListOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.structInitElem())] + self.visit(ctx.structInitListTail())

    def visitStructInitListTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.structInitElem())] + self.visit(ctx.structInitListTail())

    def visitStructInitElem(self, ctx):
        if ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.structInit())

    def visitIfStmt(self, ctx):
        return IfStmt(
            self.visit(ctx.expr()),
            self.visit(ctx.stmt()),
            self.visit(ctx.elseOpt()),
        )

    def visitElseOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.stmt())


    def visitWhileStmt(self, ctx):
        return WhileStmt(self.visit(ctx.expr()), self.visit(ctx.stmt()))

    def visitForStmt(self, ctx):
        init = self.visit(ctx.forInitOpt())
        cond = self.visit(ctx.exprOpt())
        update = self.visit(ctx.forUpdateOpt())
        return ForStmt(init, cond, update, self.visit(ctx.stmt()))

    def visitForInitOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.forInit())

    def visitForInit(self, ctx):
        if ctx.varDeclFor():
            return self.visit(ctx.varDeclFor())
        return ExprStmt(self.visit(ctx.assignExpr()))

    def visitExprOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    def visitVarDeclFor(self, ctx):
        name = ctx.ID().getText()
        if ctx.AUTO():
            init = self.visit(ctx.varDeclAutoInitOpt())
            return VarDecl(None, name, init)
        var_type = self.visit(ctx.typeSpec())
        init = self.visit(ctx.varDeclTypedInitOpt())
        return VarDecl(var_type, name, init)

    def visitForUpdateOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.forUpdate())

    def visitForUpdate(self, ctx):
        if ctx.assignExpr():
            return self.visit(ctx.assignExpr())
        return self.visit(ctx.postfixExpr())

    def visitSwitchStmt(self, ctx):
        sections = self.visit(ctx.switchSectionList())
        cases = []
        default_case = None
        for sec in sections:
            labels, stmts = sec
            for lb in labels:
                if lb is None:
                    if default_case is None:
                        default_case = DefaultStmt(stmts)
                else:
                    cases.append(CaseStmt(lb, stmts))
        return SwitchStmt(self.visit(ctx.expr()), cases, default_case)

    def visitSwitchSectionList(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.switchSection())] + self.visit(ctx.switchSectionList())

    def visitSwitchSection(self, ctx):
        labels = self.visit(ctx.caseLabelPlus()) if ctx.caseLabelPlus() else [None]
        stmts = self.visit(ctx.stmtList())
        return labels, stmts

    def visitCaseLabelPlus(self, ctx):
        return [self.visit(ctx.caseLabel())] + self.visit(ctx.caseLabelStar())

    def visitCaseLabelStar(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.caseLabel())] + self.visit(ctx.caseLabelStar())

    def visitCaseLabel(self, ctx):
        return self.visit(ctx.expr())

    def visitDefaultLabel(self, ctx):
        return None

    def visitBreakStmt(self, ctx):
        return BreakStmt()

    def visitContinueStmt(self, ctx):
        return ContinueStmt()

    def visitReturnStmt(self, ctx):
        return ReturnStmt(self.visit(ctx.returnExprOpt()))

    def visitReturnExprOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    def visitExprStmt(self, ctx):
        return ExprStmt(self.visit(ctx.expr()))

    def visitExpr(self, ctx):
        return self.visit(ctx.assignExpr())

    def visitAssignExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.orExpr())
        return AssignExpr(self.visit(ctx.lhs()), self.visit(ctx.assignExpr()))

    def visitLhs(self, ctx):
        if ctx.getChildCount() == 1:
            return Identifier(ctx.ID().getText())
        return MemberAccess(self.visit(ctx.postfixExpr()), ctx.ID().getText())

    def visitOrExpr(self, ctx):
        left = self.visit(ctx.andExpr())
        for op, right_ctx in self.visit(ctx.orExprTail()):
            left = BinaryOp(left, op, right_ctx)
        return left

    def visitOrExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(ctx.OR().getText(), self.visit(ctx.andExpr()))] + self.visit(ctx.orExprTail())

    def visitAndExpr(self, ctx):
        left = self.visit(ctx.eqExpr())
        for op, right in self.visit(ctx.andExprTail()):
            left = BinaryOp(left, op, right)
        return left

    def visitAndExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(ctx.AND().getText(), self.visit(ctx.eqExpr()))] + self.visit(ctx.andExprTail())

    def visitEqExpr(self, ctx):
        left = self.visit(ctx.relExpr())
        for op, right in self.visit(ctx.eqExprTail()):
            left = BinaryOp(left, op, right)
        return left

    def visitEqExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(self.visit(ctx.eqOp()), self.visit(ctx.relExpr()))] + self.visit(ctx.eqExprTail())

    def visitEqOp(self, ctx):
        return ctx.getChild(0).getText()

    def visitRelExpr(self, ctx):
        left = self.visit(ctx.addExpr())
        for op, right in self.visit(ctx.relExprTail()):
            left = BinaryOp(left, op, right)
        return left

    def visitRelExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(self.visit(ctx.relOp()), self.visit(ctx.addExpr()))] + self.visit(ctx.relExprTail())

    def visitRelOp(self, ctx):
        return ctx.getChild(0).getText()

    def visitAddExpr(self, ctx):
        left = self.visit(ctx.mulExpr())
        for op, right in self.visit(ctx.addExprTail()):
            left = BinaryOp(left, op, right)
        return left

    def visitAddExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(self.visit(ctx.addOp()), self.visit(ctx.mulExpr()))] + self.visit(ctx.addExprTail())

    def visitAddOp(self, ctx):
        return ctx.getChild(0).getText()

    def visitMulExpr(self, ctx):
        left = self.visit(ctx.unaryExpr())
        for op, right in self.visit(ctx.mulExprTail()):
            left = BinaryOp(left, op, right)
        return left

    def visitMulExprTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [(self.visit(ctx.mulOp()), self.visit(ctx.unaryExpr()))] + self.visit(ctx.mulExprTail())

    def visitMulOp(self, ctx):
        return ctx.getChild(0).getText()

    def visitUnaryExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.postfixExpr())
        return PrefixOp(self.visit(ctx.unaryOp()), self.visit(ctx.unaryExpr()))

    def visitUnaryOp(self, ctx):
        return ctx.getChild(0).getText()

    def visitPostfixExpr(self, ctx):
        base = self.visit(ctx.primaryExpr())
        for tail in self.visit(ctx.postfixTailList()):
            kind = tail[0]
            if kind == "member":
                base = MemberAccess(base, tail[1])
            elif kind == "call":
                if isinstance(base, Identifier):
                    base = FuncCall(base.name, tail[1])
                else:
                    base = FuncCall(str(base), tail[1])
            elif kind == "postfix":
                base = PostfixOp(tail[1], base)
        return base

    def visitPostfixTailList(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.postfixTail())] + self.visit(ctx.postfixTailList())

    def visitPostfixTail(self, ctx):
        if ctx.DOT():
            return ("member", ctx.ID().getText())
        if ctx.LPAREN():
            return ("call", self.visit(ctx.argListOpt()))
        return ("postfix", ctx.getChild(0).getText())

    def visitArgListOpt(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.argList())

    def visitArgList(self, ctx):
        return [self.visit(ctx.expr())] + self.visit(ctx.argListTail())

    def visitArgListTail(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.argListTail())

    def visitPrimaryExpr(self, ctx):
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.expr():
            return self.visit(ctx.expr())
        return None

    def visitLiteral(self, ctx):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        return None
