from ast import Return
from src.core.environment import Environment
from src.lox_objects.lox_callable import LoxCallable


class LoxFunction(LoxCallable): 
    def __init__(self, declaration, closure, is_intitializer=False):
        self.declaration = declaration  # A Function stmt
        self.closure = closure          # An Environment instance
        self.is_initializer = is_intitializer

    def arity(self): # Number of parameters in the function declaration
        return len(self.declaration.params)

    def call(self, interpreter, arguments): # Call the function with the given arguments
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            param_name = self.declaration.params[i].lexeme
            environment.define(param_name, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer:
            return self.closure.get_at(0, "this")

        return None
    
    def bind(self, instance):  
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
