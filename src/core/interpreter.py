from src.ast.expr import (  
    Assign,
    Expr,
    Literal,
    Unary,
    Binary,
    Grouping,
    Variable,
    Call,
    Get,
    Set,
    This,
    Super,
)

from src.ast.stmt import (
    Stmt,
    ExpressionStmt,
    PrintStmt,
    VarStmt,
    BlockStmt,
    IfStmt,
    WhileStmt, 
    FunctionStmt,
    ReturnStmt,
    ClassStmt, 
)

from src.core.token_type import TokenType
import time

class RuntimeError(Exception):  # Custom exception for runtime errors 
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

class ReturnException(Exception): # Custom exception for return statements
    def __init__(self, value):
        self.value = value

class LoxCallable: # Base class for callable objects
    def arity(self):
        pass 
    def call(self, interpreter, arguments):
        pass 

class Clock(LoxCallable): # Built-in clock function
    def arity(self):
        return 0
    def call(self, interpreter, arguments):
        return time.time()
    def __str__(self):
        return "<native fn>"

class LoxClass(LoxCallable): # Class representation
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass  
        self.methods = methods

    def find_method(self, name): # Find method in class or superclass
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.find_method(name)
        return None

    def call(self, interpreter, arguments): # Create an instance of the class
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self): # Get the number of parameters for the initializer
        initializer = self.find_method("init")
        return initializer.arity() if initializer else 0

    def __str__(self): 
        return self.name

class LoxInstance: # Instance of a class
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name): # Get property from instance
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method:
            return method.bind(self)
        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value): # Set property on instance
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"

class LoxFunction(LoxCallable): # Function representation
    def __init__(self, declaration, closure, is_initializer=False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance):  # Bind instance to function
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.is_initializer)

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):  # Call the function
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_value:
            if self.is_initializer:
                return self.closure.get("this")
            return return_value.value
        if self.is_initializer:
            return self.closure.get("this")
        return None

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

class Environment:  # Environment for variable storage
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):  # Define a variable in the environment
        self.values[name] = value
 
    def get(self, name):  # Get a variable from the environment
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable '{name}'.")

    def assign(self, name, value): # Assign a value to a variable
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, f"Undefined variable '{name}'.")

    def get_at(self, distance, name):   # Get a variable from a specific distance in the environment chain
        return self.ancestor(distance).values[name]

    def assign_at(self, distance, name, value):   # Assign a value to a variable at a specific distance in the environment chain
        self.ancestor(distance).values[name] = value

    def ancestor(self, distance):   # Get the ancestor environment at a specific distance
        env = self
        for _ in range(distance):
            env = env.enclosing
        return env

class Interpreter: # Main interpreter class
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}  
        self.globals.define("clock", Clock())

    def interpret(self, statements):  # Interpret a list of statements
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as error:
            print(f"Runtime error: {error}")

    def resolve(self, expr, depth):   # Resolve a variable expression to its depth in the environment chain
        self.locals[expr] = depth

    def look_up_variable(self, name, expr):  # Look up a variable in the environment
        if expr in self.locals:
            return self.environment.get_at(self.locals[expr], name.lexeme)
        return self.globals.get(name.lexeme)

    def execute(self, stmt):  # Execute a statement
        return stmt.accept(self)

    def evaluate(self, expr): # Evaluate an expression
        return expr.accept(self)

    def execute_block(self, statements, environment): # Execute a block of statements in a new environment
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def visit_expression_stmt(self, stmt: ExpressionStmt):  # Expression statement
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: PrintStmt):  # Print statement
        value = self.evaluate(stmt.expression)
        print(self.to_string(value))

    def visit_var_stmt(self, stmt: VarStmt):  # Variable declaration statement
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt: BlockStmt):  # Block statement
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_if_stmt(self, stmt: IfStmt):  # If statement
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt): # While statement
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_function_stmt(self, stmt: FunctionStmt):  # Function declaration statement
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_return_stmt(self, stmt: ReturnStmt):  # Return statement
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

    def visit_class_stmt(self, stmt: ClassStmt):   # Class declaration 
        superclass = None
        if stmt.superclass:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = LoxFunction(method, self.environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if stmt.superclass:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name.lexeme, klass)

    def visit_variable_expr(self, expr: Variable): # Variable expression
        return self.look_up_variable(expr.name, expr)

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        if expr in self.locals:
            self.environment.assign_at(self.locals[expr], expr.name.lexeme, value)
        else:
            self.globals.assign(expr.name.lexeme, value)
        return value

    def visit_literal_expr(self, expr: Literal):  # Literal expression
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):  # Grouping expression
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):  # Unary expression
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    def visit_binary_expr(self, expr: Binary):  # Binary expression
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type: 
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise RuntimeError(expr.operator, "Division by zero.")
                return left / right
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

        return None

    def visit_call_expr(self, expr: Call):  # Call expression
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        if not isinstance(callee, LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity():
            raise RuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        return callee.call(self, arguments)

    def visit_get_expr(self, expr: Get):   # Get expression
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)
        raise RuntimeError(expr.name, "Only instances have properties.")

    def visit_set_expr(self, expr: Set):   # Set expression
        object = self.evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise RuntimeError(expr.name, "Only instances have fields.")
        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value

    def visit_this_expr(self, expr: This):   # This expression
        return self.look_up_variable(expr.keyword, expr)

    def visit_super_expr(self, expr: Super):   # Super expression
        distance = self.locals[expr]
        superclass = self.environment.get_at(distance, "super")
        object = self.environment.get_at(distance - 1, "this")
        method = superclass.find_method(expr.method.lexeme)
        if not method:
            raise RuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(object)

    def is_truthy(self, obj): # Check if an object is truthy
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a, b): # Check if two objects are equal
        return a == b

    def check_number_operand(self, operator, operand):  # Check if operand is a number(unary)
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right): # Check if operands are numbers(binary)
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def to_string(self, obj):  # Convert an object to string
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
