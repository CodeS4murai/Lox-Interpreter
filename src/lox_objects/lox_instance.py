from src.utils.runtime_error import RuntimeError as LoxRuntimeError

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass  # LoxClass instance
        self.fields = {}    # Dictionary to store instance fields

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method:
            return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"
