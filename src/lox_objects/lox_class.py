from typing import Optional
from src.lox_objects.lox_function import LoxFunction
from src.lox_objects.lox_instance import LoxInstance

class LoxClass:
    def __init__(self, name: str, superclass: Optional['LoxClass'], methods: dict[str, LoxFunction]):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.find_method(name)
        return None

    def call(self, interpreter, arguments: list):
        # Create a new instance of this class
        instance = LoxInstance(self)
        initializer = self.find_method("init") # Look for an initializer named "init"
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def __str__(self):
        return f"<class {self.name}>"
