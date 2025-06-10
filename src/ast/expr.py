from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Binary(Expr): # Represents a binary expressions
    def __init__(self, left, operator, right):  
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor): # Accepts a visitor for the visitor pattern
        return visitor.visit_binary_expr(self)

    def __str__(self): 
        return f"({self.left} {self.operator.lexeme} {self.right})"

class Grouping(Expr): # Represents a grouping expression
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

    def __str__(self):
        return f"(group {self.expression})"

class Literal(Expr): # Represents a literal expression
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

    def __str__(self):
        return str(self.value) if self.value is not None else "nil"

class Unary(Expr): # Represents a unary expression
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

    def __str__(self): 
        return f"({self.operator.lexeme} {self.right})" 
    
class Variable(Expr): # Represents a variable expression
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

    def __str__(self):
        return str(self.name)
    
class Assign(Expr): # Represents an assignment expression
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

    def __str__(self):
        return f"({self.name} = {self.value})"
    
class Call(Expr): # Represents a function call expression
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)

    def __str__(self):
        return f"({self.callee}({', '.join(map(str, self.arguments))}))" 
    
class Logical(Expr): # Represents a logical expression
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

    def __str__(self):
        return f"({self.left} {self.operator.lexeme} {self.right})"
    
class Get(Expr):
    def __init__(self, object, name):
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self) 
    
    def __str__(self):  
        return f"({self.object}.{self.name.lexeme})"

class Set(Expr):
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_expr(self) 
    
    def __str__(self):  
        return f"({self.object}.{self.name.lexeme} = {self.value})"

class This(Expr):
    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_this_expr(self) 
    
    def __str__(self):  
        return "this"

class Super(Expr):
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_super_expr(self) 
    
    def __str__(self):  
        return f"super.{self.method.lexeme}"