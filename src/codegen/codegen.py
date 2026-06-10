"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.structs: dict[str, dict[str, tuple[Any, int]]] = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, MemberAccess):
            obj_type = self._infer_type(node.obj, o)
            if is_struct_type(obj_type):
                return self.structs[obj_type.struct_name][node.member][0]
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return IntType()
        return IntType()

    def _struct_name(self, typ):
        return typ.struct_name if hasattr(typ, "struct_name") else typ.name

    def _emit_value_assignment(self, lhs, rhs_code, rhs_type, o: Access):
        frame = o.frame
        if isinstance(lhs, Identifier):
            sym = self._lookup_symbol(lhs.name, o.sym)
            code = rhs_code + self.emit.emit_dup(frame) + self.emit.emit_write_var(lhs.name, sym.type, sym.value.value, frame)
            return code, rhs_type
        if isinstance(lhs, MemberAccess):
            obj_code, obj_type = self.visit(lhs.obj, o)
            struct_name = self._struct_name(obj_type)
            member_type, _ = self.structs[struct_name][lhs.member]
            code = obj_code + rhs_code + self.emit.emit_dup_x1(frame) + self.emit.emit_put_field(f"{struct_name}/{lhs.member}", member_type, frame)
            return code, rhs_type
        raise RuntimeError("Unsupported assignment target")

    def _emit_lvalue_read(self, lhs, o: Access):
        frame = o.frame
        if isinstance(lhs, Identifier):
            return self.visit_identifier(lhs, o)
        if isinstance(lhs, MemberAccess):
            obj_code, obj_type = self.visit(lhs.obj, o)
            struct_name = self._struct_name(obj_type)
            member_type, _ = self.structs[struct_name][lhs.member]
            return obj_code + self.emit.emit_get_field(f"{struct_name}/{lhs.member}", member_type, frame), member_type
        raise RuntimeError("Unsupported lvalue")

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else VoidType()
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = node.return_type if node.return_type else VoidType()
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        for stmt in node.statements:
            o = self.visit(stmt, o)
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            rhs_code, _ = self.visit(node.init_value, Access(frame, o.sym))
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def _stmt_ends_with_return(self, stmt):
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt) and stmt.statements:
            return self._stmt_ends_with_return(stmt.statements[-1])
        return False


    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        if not self._stmt_ends_with_return(node.then_stmt):
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        end_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator == "+" and (is_string_type(left_type) or is_string_type(right_type)):
            def to_string(code, typ):
                if is_string_type(typ):
                    return code
                if is_int_type(typ):
                    return code + self.emit.jvm.emitINVOKESTATIC("java/lang/String/valueOf", "(I)Ljava/lang/String;")
                if is_float_type(typ):
                    return code + self.emit.jvm.emitINVOKESTATIC("java/lang/String/valueOf", "(F)Ljava/lang/String;")
                return code + self.emit.jvm.emitINVOKESTATIC("java/lang/String/valueOf", "(Ljava/lang/Object;)Ljava/lang/String;")

            code = ""
            code += self.emit.jvm.emitNEW("java/lang/StringBuilder")
            code += self.emit.jvm.emitDUP()
            code += self.emit.jvm.emitINVOKESPECIAL("java/lang/StringBuilder/<init>", "()V")
            code += to_string(left_code, left_type)
            code += self.emit.jvm.emitINVOKEVIRTUAL("java/lang/StringBuilder/append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;")
            code += to_string(right_code, right_type)
            code += self.emit.jvm.emitINVOKEVIRTUAL("java/lang/StringBuilder/append", "(Ljava/lang/String;)Ljava/lang/StringBuilder;")
            code += self.emit.jvm.emitINVOKEVIRTUAL("java/lang/StringBuilder/toString", "()Ljava/lang/String;")
            return code, StringType()

        if node.operator in ["+", "-", "*", "/"] and (is_float_type(left_type) or is_float_type(right_type)):
            def promote(code, typ):
                return code if is_float_type(typ) else code + self.emit.emit_i2f(frame)

            left_code = promote(left_code, left_type)
            right_code = promote(right_code, right_type)

        def promote(code, typ):
            if is_float_type(typ):
                return code
            if is_int_type(typ):
                return code + self.emit.emit_i2f(frame)
            return code

        if node.operator in ["+", "-", "*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(result_type):
                left_code = promote(left_code, left_type)
                right_code = promote(right_code, right_type)
            if node.operator in ["+", "-"]:
                return left_code + right_code + self.emit.emit_add_op(node.operator, result_type, frame), result_type
            return left_code + right_code + self.emit.emit_mul_op(node.operator, result_type, frame), result_type
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            if is_float_type(op_type):
                left_code = promote(left_code, left_type)
                right_code = promote(right_code, right_type)
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        rhs_code, rhs_type = self.visit(node.rhs, o)
        return self._emit_value_assignment(node.lhs, rhs_code, rhs_type, o)

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg in node.args:
            arg_code, _ = self.visit(arg, o)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        self.structs[node.name] = {}
        for idx, member in enumerate(node.members):
            self.structs[node.name][member.name] = (member.member_type, idx)

        # Emit a dedicated JVM class for this struct so struct literals and field
        # access can use GETFIELD/PUTFIELD against a real class.
        struct_filename = f"{node.name}.j"
        struct_emit = Emitter(struct_filename)
        struct_emit.print_out(struct_emit.emit_prolog(node.name))
        for member in node.members:
            struct_emit.print_out(
                f".field public {member.name} {struct_emit.get_jvm_type(member.member_type)}\n"
            )
        struct_emit.print_out(".method public <init>()V\n")
        struct_emit.print_out(".limit stack 1\n.limit locals 1\n")
        struct_emit.print_out("aload_0\n")
        struct_emit.print_out("invokespecial java/lang/Object/<init>()V\n")
        struct_emit.print_out("return\n")
        struct_emit.print_out(".end method\n")
        struct_emit.print_out(struct_emit.emit_epilog())
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return node.member_type

    def visit_param(self, node: Param, o: Any = None):
        return node.param_type

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        frame = o.frame
        frame.enter_loop()
        if node.init is not None:
            self.visit(node.init, o)
        start_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(break_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        if node.update is not None:
            upd_code, upd_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(upd_code)
            if not is_void_type(upd_type):
                self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.exit_loop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        frame = o.frame
        end_label = frame.get_new_label()
        expr_code, expr_type = self.visit(node.expr, Access(frame, o.sym))
        self.emit.print_out(expr_code)
        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label() if node.default_case else end_label
        for case, label in zip(node.cases, case_labels):
            case_code, _ = self.visit(case.expr, Access(frame, o.sym))
            self.emit.print_out(self.emit.emit_dup(frame))
            self.emit.print_out(case_code)
            self.emit.print_out(self.emit.emit_re_op("==", expr_type, frame))
            self.emit.print_out(self.emit.emit_if_true(label, frame))
        self.emit.print_out(self.emit.emit_goto(default_label, frame))
        self.emit.print_out(self.emit.emit_label(default_label, frame))
        if node.default_case:
            self.visit(node.default_case, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        for case, label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(label, frame))
            self.visit(case, o)
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        self.emit.print_out(self.emit.emit_pop(frame))
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)
        return o

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        _ = node
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        _ = node
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        if node.operator == "+":
            return self.visit(node.operand, o)
        if node.operator == "-":
            code, typ = self.visit(node.operand, o)
            return code + self.emit.emit_neg_op(typ, o.frame), typ
        if node.operator in ["++", "--"]:
            frame = o.frame
            one = IntLiteral(1)
            op = "+" if node.operator == "++" else "-"
            if isinstance(node.operand, Identifier):
                rhs_code, rhs_type = self.visit(BinaryOp(node.operand, op, one), o)
                return self._emit_value_assignment(node.operand, rhs_code, rhs_type, o)
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                struct_name = self._struct_name(obj_type)
                member_type, _ = self.structs[struct_name][node.operand.member]
                code = obj_code + self.emit.emit_dup(frame) + self.emit.emit_get_field(
                    f"{struct_name}/{node.operand.member}", member_type, frame
                )
                val_code, val_type = self.visit(BinaryOp(node.operand, op, one), o)
                code += val_code[len(obj_code):] if val_code.startswith(obj_code) else val_code
                code += self.emit.emit_dup_x1(frame) + self.emit.emit_put_field(
                    f"{struct_name}/{node.operand.member}", member_type, frame
                )
                return code, val_type
        return self.visit(node.operand, o)

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        if node.operator in ["++", "--"]:
            old_code, old_type = self._emit_lvalue_read(node.operand, o)
            one = IntLiteral(1)
            op = "+" if node.operator == "++" else "-"
            new_code, new_type = self.visit(BinaryOp(node.operand, op, one), o)
            frame = o.frame
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                assign_code = new_code + self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
            elif isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                struct_name = self._struct_name(obj_type)
                member_type, _ = self.structs[struct_name][node.operand.member]
                assign_code = obj_code + new_code + self.emit.emit_put_field(f"{struct_name}/{node.operand.member}", member_type, frame)
            else:
                raise RuntimeError("Unsupported postfix target")
            return old_code + assign_code, old_type
        return self.visit(node.operand, o)

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        return self._emit_lvalue_read(node, o)

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        if not self.structs:
            raise RuntimeError("StructLiteral used before any struct declarations")
        frame = o.frame

        def emit_default_struct(struct_name: str):
            code = self.emit.emit_new_instance(struct_name, frame)
            ordered = sorted(self.structs[struct_name].items(), key=lambda item: item[1][1])
            for field_name, (field_type, _) in ordered:
                code += self.emit.emit_dup(frame)
                if is_struct_type(field_type):
                    code += emit_default_struct(field_type.struct_name)
                else:
                    code += self.emit.emit_push_iconst(0, frame)
                code += self.emit.emit_put_field(f"{struct_name}/{field_name}", field_type, frame)
            return code

        def literal_matches_type(val, typ):
            if is_struct_type(typ):
                return isinstance(val, StructLiteral) or (isinstance(val, IntLiteral) and val.value == 0)
            if is_int_type(typ):
                return isinstance(val, IntLiteral)
            if is_float_type(typ):
                return isinstance(val, FloatLiteral) or isinstance(val, IntLiteral)
            if is_string_type(typ):
                return isinstance(val, StringLiteral)
            return True

        candidates = []
        for struct_name, fields in self.structs.items():
            if len(fields) != len(node.values):
                continue
            ordered_fields = sorted(fields.items(), key=lambda item: item[1][1])
            if all(literal_matches_type(val, field_type) for val, (_, (field_type, _)) in zip(node.values, ordered_fields)):
                candidates.append((struct_name, ordered_fields))

        if not candidates:
            struct_name = next(iter(self.structs.keys()))
            code = self.emit.emit_new_instance(struct_name, frame)
            return code, StructType(struct_name)

        struct_name, ordered_fields = candidates[-1]
        code = self.emit.emit_new_instance(struct_name, frame)
        for idx, (field_name, (field_type, _)) in enumerate(ordered_fields):
            code += self.emit.emit_dup(frame)
            val = node.values[idx]
            if is_struct_type(field_type) and isinstance(val, IntLiteral) and val.value == 0:
                code += emit_default_struct(field_type.struct_name)
            else:
                val_code, _ = self.visit(val, o)
                code += val_code
            code += self.emit.emit_put_field(f"{struct_name}/{field_name}", field_type, frame)
        return code, StructType(struct_name)

