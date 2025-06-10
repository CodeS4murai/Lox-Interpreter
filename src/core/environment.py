class Environment:
    def __init__(self, enclosing=None):  # Enclosing environment 
        self.enclosing = enclosing  
        self.values = {} 

    def define(self, name, value):  # Define a variable in the current environment
        self.values[name] = value   

    def get(self, name_token):  # Retrieve a variable's value
        name = name_token.lexeme # Get the variable name from the token
        if name in self.values: # Check if the variable is defined in the current environment
            return self.values[name]  
        if self.enclosing is not None: # Check if there is an enclosing environment
            return self.enclosing.get(name_token)  
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")  # Raise an error if the variable is not found
    
    # Assigns a value to a variable
    def assign(self, name_token, value):
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name_token, value)
            return
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")
    
    def assign_at(self, distance, name_token, value):
        current = self
        # Traverse the environment chain up to the specified distance
        for _ in range(distance):
            if current.enclosing is not None:
                current = current.enclosing
            else:
                raise RuntimeError(name_token, f"Too many levels of enclosing environments.")
        current.values[name_token.lexeme] = value
