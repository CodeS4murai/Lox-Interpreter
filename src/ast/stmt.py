from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class ExpressionStmt(Stmt): # Expression statement
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class PrintStmt(Stmt): # Print statement
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

class VarStmt(Stmt): # Variable declaration
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

class BlockStmt(Stmt): # Block statement
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

class IfStmt(Stmt): # If statement
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)

class WhileStmt(Stmt): # While statement
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

class FunctionStmt(Stmt):
    def __init__(self, name, params, body):
        self.name = name          # Token
        self.params = params      # List[Token]
        self.body = body          # List[Stmt]

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)

class ReturnStmt(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword    # Token
        self.value = value        # Expr or None

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)
    
class ClassStmt(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)