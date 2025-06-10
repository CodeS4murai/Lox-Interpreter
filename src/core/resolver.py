from enum import Enum, auto
from src.ast.expr import *
from src.ast.stmt import *
from src.core.token1 import Token  
from src.core.lox import Lox  
from src.core.interpreter import Interpreter  

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()
    
class ClassType(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()

class Resolver:
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []  
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, statements: list[Stmt]):
        for stmt in statements:
            self._resolve(stmt)

    def _resolve(self, node):
        node.accept(self)

    def visit_block_stmt(self, stmt: BlockStmt):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    def visit_var_stmt(self, stmt: VarStmt):
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve(stmt.initializer)
        self._define(stmt.name)

    def visit_variable_expr(self, expr: Variable):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            Lox.error(expr.name, "Can't read local variable in its own initializer.")
        self._resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr: Assign):
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_function_stmt(self, stmt: FunctionStmt):
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        self._resolve(stmt.expression)

    def visit_if_stmt(self, stmt: IfStmt):
        self._resolve(stmt.condition)
        self._resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: PrintStmt):
        self._resolve(stmt.expression)

    def visit_return_stmt(self, stmt: ReturnStmt):
        if self.current_function == FunctionType.NONE:
            Lox.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                Lox.error(stmt.keyword, "Can't return a value from an initializer.")
            self._resolve(stmt.value)

    def visit_while_stmt(self, stmt: WhileStmt):
        self._resolve(stmt.condition)
        self._resolve(stmt.body)

    def visit_binary_expr(self, expr: Binary):
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_call_expr(self, expr: Call):
        self._resolve(expr.callee)
        for argument in expr.arguments:
            self._resolve(argument)

    def visit_grouping_expr(self, expr: Grouping):
        self._resolve(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return None  

    def visit_logical_expr(self, expr: Logical):
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_unary_expr(self, expr: Unary):
        self._resolve(expr.right)
        
    def visit_class_stmt(self, stmt: ClassStmt):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        
        self._declare(stmt.name)
        self._define(stmt.name)
        
        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                Lox.error(stmt.superclass.name, "A class can't inherit from itself.")
            self.current_class = ClassType.SUBCLASS
            self._resolve(stmt.superclass)
            
            self._begin_scope()
            self.scopes[-1]["super"] = True
        
        self._begin_scope()
        self.scopes[-1]["this"] = True  
        
        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self._resolve_function(method, declaration)
        
        self._end_scope()
        
        if stmt.superclass is not None:
            self._end_scope()
        
        self.current_class = enclosing_class

    def visit_get_expr(self, expr):
        self._resolve(expr.object)
        return None

    def visit_set_expr(self, expr):
        self._resolve(expr.value)
        self._resolve(expr.object)
        return None

    def visit_this_expr(self, expr: This):
        if self.current_class == ClassType.NONE:
            Lox.error(expr.keyword, "Can't use 'this' outside of a class.")
            return
        self._resolve_local(expr, expr.keyword)

    def visit_super_expr(self, expr: Super):
        if self.current_class == ClassType.NONE:
            Lox.error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.current_class != ClassType.SUBCLASS:
            Lox.error(expr.keyword, "Can't use 'super' in a class with no superclass.")
        self._resolve_local(expr, expr.keyword)

    def _resolve_function(self, function: FunctionStmt, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()
        self.current_function = enclosing_function

    def _resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            Lox.error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False  

    def _define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True  
