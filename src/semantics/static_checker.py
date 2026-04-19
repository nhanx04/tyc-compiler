"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


class StaticChecker(ASTVisitor):
    AUTO = object()

    def __init__(self):
        self.structs, self.funcs = {}, {}
        self.scopes, self.param_names = [], set()
        self.current_ret, self.current_func = None, None
        self.loop_depth, self.switch_depth = 0, 0
        self.func_order = []

    def check_program(self, ast: Program):
        self.visit(ast)

    def _same(self, a, b):
        return type(a) == type(b) and (not isinstance(a, StructType) or a.struct_name == b.struct_name)

    def _num(self, t): return isinstance(t, (IntType, FloatType))
    def _is_lvalue(self, e): return isinstance(e, (Identifier, MemberAccess))
    def _declare(self, n, t): self.scopes[-1][n] = t
    def _lookup(self, n):
        for s in reversed(self.scopes):
            if n in s: return s, s[n]
        raise UndeclaredIdentifier(n)

    def _bind_expr(self, e, t):
        if isinstance(e, Identifier): s, _ = self._lookup(e.name); s[e.name] = t
        elif isinstance(e, MemberAccess): pass

    def _must(self, t, e):
        if t is self.AUTO: raise TypeCannotBeInferred(e)
        return t

    def visit_program(self, node: Program, o=None):
        self.funcs = {
            "readInt": (IntType(), []), "readFloat": (FloatType(), []), "readString": (StringType(), []),
            "printInt": (VoidType(), [IntType()]), "printFloat": (VoidType(), [FloatType()]), "printString": (VoidType(), [StringType()])
        }
        for d in node.decls: self.visit(d)
        if "main" not in self.funcs: raise UndeclaredFunction("main")
        rt, ps = self.funcs["main"]
        if not isinstance(rt, VoidType) or len(ps) != 0: raise TypeMismatchInStatement(FuncCall("main", []))

    def visit_struct_decl(self, node: StructDecl, o=None):
        if node.name in self.structs: raise Redeclared("Struct", node.name)
        mem, names = {}, set()
        for m in node.members:
            if m.name in names: raise Redeclared("Member", m.name)
            names.add(m.name)
            if isinstance(m.member_type, StructType) and m.member_type.struct_name not in self.structs: raise UndeclaredStruct(m.member_type.struct_name)
            if isinstance(m.member_type, StructType) and m.member_type.struct_name == node.name: raise UndeclaredStruct(node.name)
            mem[m.name] = m.member_type
        self.structs[node.name] = mem

    def visit_func_decl(self, node: FuncDecl, o=None):
        if node.name in self.funcs:
            raise Redeclared("Function", node.name)
        if isinstance(node.return_type, StructType) and node.return_type.struct_name not in self.structs:
            raise UndeclaredStruct(node.return_type.struct_name)
        ps, seen = [], set()
        for p in node.params:
            if p.name in seen:
                raise Redeclared("Parameter", p.name)
            if isinstance(p.param_type, StructType) and p.param_type.struct_name not in self.structs:
                raise UndeclaredStruct(p.param_type.struct_name)
            seen.add(p.name)
            ps.append(p.param_type)
        self.funcs[node.name] = (node.return_type if node.return_type else self.AUTO, ps)
        self.current_func, self.current_ret = node.name, self.funcs[node.name][0]
        self.scopes.append({}); self.param_names = set(seen)
        for p in node.params: self._declare(p.name, p.param_type)
        self.visit(node.body)
        if self.current_ret is self.AUTO:
            self.current_ret = VoidType()
        self.funcs[node.name] = (self.current_ret, ps)
        self.scopes.pop(); self.param_names = set(); self.current_func = None

    def visit_block_stmt(self, node: BlockStmt, o=None):
        self.scopes.append({})
        for s in node.statements: self.visit(s)
        if any(t is self.AUTO for t in self.scopes[-1].values()): raise TypeCannotBeInferred(node)
        self.scopes.pop()

    def visit_var_decl(self, node: VarDecl, o=None):
        if node.name in self.scopes[-1] or node.name in self.param_names:
            raise Redeclared("Variable", node.name)
        t = node.var_type if node.var_type else self.AUTO
        if isinstance(t, StructType) and t.struct_name not in self.structs:
            raise UndeclaredStruct(t.struct_name)
        if node.init_value is None:
            self._declare(node.name, t)
            return

        rhs = self.visit(node.init_value, t if t is not self.AUTO else None)
        if t is self.AUTO and rhs is self.AUTO:
            raise TypeCannotBeInferred(node.init_value)
        if t is self.AUTO:
            t = rhs
        elif rhs is self.AUTO:
            self._bind_expr(node.init_value, t)
        elif not self._same(t, rhs):
            raise TypeMismatchInStatement(node)
        self._declare(node.name, t)

    def visit_if_stmt(self, node: IfStmt, o=None):
        if not isinstance(self.visit(node.condition, IntType()), IntType): raise TypeMismatchInStatement(node)
        self.visit(node.then_stmt)
        if node.else_stmt: self.visit(node.else_stmt)

    def visit_while_stmt(self, node: WhileStmt, o=None):
        if not isinstance(self.visit(node.condition, IntType()), IntType): raise TypeMismatchInStatement(node)
        self.loop_depth += 1; self.visit(node.body); self.loop_depth -= 1

    def visit_for_stmt(self, node: ForStmt, o=None):
        # Per spec: declarations in for-init are in the enclosing local scope,
        # and remain visible after the loop.
        if node.init:
            self.visit(node.init)
        if node.condition and not isinstance(self.visit(node.condition, IntType()), IntType):
            raise TypeMismatchInStatement(node)
        if node.update:
            self.visit(node.update)

        # The loop body is checked in an inner scope nested under enclosing scope.
        self.loop_depth += 1
        self.scopes.append({})
        self.visit(node.body)
        if any(t is self.AUTO for t in self.scopes[-1].values()):
            raise TypeCannotBeInferred(node.body)
        self.scopes.pop()
        self.loop_depth -= 1

    def visit_switch_stmt(self, node: SwitchStmt, o=None):
        if not isinstance(self.visit(node.expr, IntType()), IntType): raise TypeMismatchInStatement(node)
        self.switch_depth += 1
        for c in node.cases: self.visit(c)
        if node.default_case: self.visit(node.default_case)
        self.switch_depth -= 1

    def visit_case_stmt(self, node: CaseStmt, o=None):
        if not isinstance(self.visit(node.expr, IntType()), IntType): raise TypeMismatchInStatement(node)
        for s in node.statements: self.visit(s)

    def visit_default_stmt(self, node: DefaultStmt, o=None):
        for s in node.statements: self.visit(s)

    def visit_break_stmt(self, node: BreakStmt, o=None):
        if self.loop_depth == 0 and self.switch_depth == 0: raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o=None):
        if self.loop_depth == 0: raise MustInLoop(node)

    def visit_return_stmt(self, node: ReturnStmt, o=None):
        if node.expr is None:
            if isinstance(self.current_ret, VoidType): return
            if self.current_ret is self.AUTO: self.current_ret = VoidType(); return
            raise TypeMismatchInStatement(node)
        t = self.visit(node.expr, None if self.current_ret is self.AUTO else self.current_ret)
        if self.current_ret is self.AUTO: self.current_ret = self._must(t, node)
        elif t is self.AUTO: self._bind_expr(node.expr, self.current_ret)
        elif not self._same(self.current_ret, t): raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: ExprStmt, o=None):
        try:
            self.visit(node.expr)
        except TypeMismatchInExpression:
            if isinstance(node.expr, AssignExpr):
                raise TypeMismatchInStatement(node)
            raise

    def visit_binary_op(self, node: BinaryOp, o=None):
        l, r, op = self.visit(node.left), self.visit(node.right), node.operator
        if l is self.AUTO and r is self.AUTO: raise TypeCannotBeInferred(node)
        if op in ["+","-","*","/"]:
            if l is self.AUTO and isinstance(r, (IntType, FloatType)): self._bind_expr(node.left, r); l = r
            if r is self.AUTO and isinstance(l, (IntType, FloatType)): self._bind_expr(node.right, l); r = l
            if l is self.AUTO or r is self.AUTO: raise TypeCannotBeInferred(node)
            if not (self._num(l) and self._num(r)): raise TypeMismatchInExpression(node)
            return FloatType() if isinstance(l, FloatType) or isinstance(r, FloatType) else IntType()
        if op == "%":
            if l is self.AUTO: self._bind_expr(node.left, IntType()); l = IntType()
            if r is self.AUTO: self._bind_expr(node.right, IntType()); r = IntType()
            if not (isinstance(l, IntType) and isinstance(r, IntType)): raise TypeMismatchInExpression(node)
            return IntType()
        if op in ["<","<=",">",">=","==","!="]:
            if l is self.AUTO and isinstance(r, (IntType, FloatType)): self._bind_expr(node.left, r); l = r
            if r is self.AUTO and isinstance(l, (IntType, FloatType)): self._bind_expr(node.right, l); r = l
            if l is self.AUTO or r is self.AUTO: raise TypeCannotBeInferred(node)
            if not (self._num(l) and self._num(r)): raise TypeMismatchInExpression(node)
            return IntType()
        if op in ["&&","||"]:
            if l is self.AUTO: self._bind_expr(node.left, IntType()); l = IntType()
            if r is self.AUTO: self._bind_expr(node.right, IntType()); r = IntType()
            if not (isinstance(l, IntType) and isinstance(r, IntType)): raise TypeMismatchInExpression(node)
            return IntType()
        raise TypeMismatchInExpression(node)

    def visit_prefix_op(self, node: PrefixOp, o=None):
        t = self.visit(node.operand)
        if node.operator in ["++","--"]:
            if not self._is_lvalue(node.operand): raise TypeMismatchInExpression(node)
            if t is self.AUTO: self._bind_expr(node.operand, IntType()); t = IntType()
            if not isinstance(t, IntType): raise TypeMismatchInExpression(node)
            return IntType()
        if node.operator == "!":
            if t is self.AUTO: self._bind_expr(node.operand, IntType()); t = IntType()
            if not isinstance(t, IntType): raise TypeMismatchInExpression(node)
            return IntType()
        if node.operator in ["+","-"]:
            if t is self.AUTO: raise TypeCannotBeInferred(node)
            if not self._num(t): raise TypeMismatchInExpression(node)
            return t
        raise TypeMismatchInExpression(node)

    def visit_postfix_op(self, node: PostfixOp, o=None): return self.visit_prefix_op(PrefixOp(node.operator, node.operand))
    def visit_assign_expr(self, node: AssignExpr, o=None):
        if not self._is_lvalue(node.lhs):
            raise TypeMismatchInExpression(node)
        lt = self.visit(node.lhs)
        rt = self.visit(node.rhs, lt if lt is not self.AUTO else None)
        if lt is self.AUTO and rt is self.AUTO:
            raise TypeCannotBeInferred(node)
        if lt is self.AUTO:
            self._bind_expr(node.lhs, rt)
            lt = rt
        elif rt is self.AUTO:
            self._bind_expr(node.rhs, lt)
            rt = lt
        elif not self._same(lt, rt):
            raise TypeMismatchInExpression(node)
        return lt

    def visit_member_access(self, node: MemberAccess, o=None):
        ot = self.visit(node.obj)
        if not isinstance(ot, StructType):
            raise TypeMismatchInExpression(node)
        if ot.struct_name not in self.structs:
            raise UndeclaredStruct(ot.struct_name)
        members = self.structs[ot.struct_name]
        if node.member not in members:
            raise TypeMismatchInExpression(node)
        return members[node.member]

    def visit_func_call(self, node: FuncCall, o=None):
        if node.name not in self.funcs:
            raise UndeclaredFunction(node.name)
        rt, params = self.funcs[node.name]
        if len(params) != len(node.args):
            raise TypeMismatchInExpression(node)
        for i, arg in enumerate(node.args):
            at = self.visit(arg, params[i])
            if at is self.AUTO:
                self._bind_expr(arg, params[i])
            elif not self._same(at, params[i]):
                raise TypeMismatchInExpression(node)
        return rt

    def visit_identifier(self, node: Identifier, o=None):
        _, t = self._lookup(node.name)
        if o is not None and t is self.AUTO:
            self._bind_expr(node, o)
            return o
        return t

    def visit_struct_literal(self, node: StructLiteral, o=None):
        if not isinstance(o, StructType):
            return self.AUTO
        if o.struct_name not in self.structs:
            raise UndeclaredStruct(o.struct_name)
        members = list(self.structs[o.struct_name].values())
        if len(members) != len(node.values):
            raise TypeMismatchInExpression(node)
        for i, ev in enumerate(node.values):
            vt = self.visit(ev, members[i])
            if vt is self.AUTO:
                self._bind_expr(ev, members[i])
            elif not self._same(vt, members[i]):
                raise TypeMismatchInExpression(node)
        return o

    def visit_int_literal(self, node: IntLiteral, o=None):
        return IntType()

    def visit_float_literal(self, node: FloatLiteral, o=None):
        return FloatType()

    def visit_string_literal(self, node: StringLiteral, o=None):
        return StringType()

    def visit_member_decl(self, node: MemberDecl, o=None):
        return node.member_type

    def visit_param(self, node: Param, o=None):
        return node.param_type

    def visit_int_type(self, node: IntType, o=None):
        return node

    def visit_float_type(self, node: FloatType, o=None):
        return node

    def visit_string_type(self, node: StringType, o=None):
        return node

    def visit_void_type(self, node: VoidType, o=None):
        return node

    def visit_struct_type(self, node: StructType, o=None):
        if node.struct_name not in self.structs:
            raise UndeclaredStruct(node.struct_name)
        return node

