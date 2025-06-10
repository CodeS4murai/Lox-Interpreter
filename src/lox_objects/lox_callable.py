from abc import ABC, abstractmethod

class LoxCallable(ABC): # Represents a callable object in the Lox language
    @abstractmethod
    def arity(self) -> int:
        # Returns the number of arguments this callable expects
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        #Calls the function with the given arguments
        pass
