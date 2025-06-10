import os 

def main():  # Generate the AST classes
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True) # Create the output directory if it doesn't exist
    define_ast(output_dir, "Expr", [       # List of AST node types
        "Binary   : left, operator, right",
        "Grouping : expression",
        "Literal  : value",
        "Unary    : operator, right",
        "Variable : name",
        "Assign   : name, value",
        "Logical  : left, operator, right",
        "Call     : callee, paren, arguments",  
        "Get      : object, name",
        "Set      : object, name, value",
        "This     : keyword",
        "Super    : keyword, method"
    ])
    
    define_ast(output_dir, "Stmt", [
        "Expression : expression", 
        "Print      : expression",
        "Var        : name, initializer",
        "Block      : statements",
        "If         : condition, then_branch, else_branch",
        "While      : condition, body"
        "Function   : name, params, body",
        "Return     : keyword, value"
        "Class      : name, superclass, methods",
    ])

def define_ast(output_dir, base_name, types):   
    path = os.path.join(output_dir, f"{base_name.lower()}.py")   # Path to the generated file
    with open(path, "w") as f:   # Open the file for writing
        f.write("from abc import ABC, abstractmethod\n\n")   # Import ABC and abstractmethod for defining abstract classes
        f.write(f"class {base_name}(ABC):\n")   # Base class for all AST nodes
        f.write("    @abstractmethod\n")  # Abstract method to be implemented by subclasses
        f.write("    def accept(self, visitor):\n")  # Accept method for the visitor pattern
        f.write("        pass\n\n")

        for type_def in types:         # Iterate over the types to define
            class_name, fields = map(str.strip, type_def.split(":"))     # Split the type definition into class name and fields
            define_type(f, base_name, class_name, fields)    

        # Visitor interface
        f.write("\nclass Visitor(ABC):\n")
        for type_def in types:
            type_name = type_def.split(":")[0].strip()
            f.write(f"    @abstractmethod\n")
            f.write(f"    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}):\n")
            f.write(f"        pass\n")

def define_type(f, base_name, class_name, field_list):
    fields = [field.strip() for field in field_list.split(",")]

    f.write(f"class {class_name}({base_name}):\n")

    # Constructor
    f.write("    def __init__(self, " + ", ".join(fields) + "):\n")
    for field in fields:
        f.write(f"        self.{field} = {field}\n")
    f.write("\n")

    # Accept method
    f.write("    def accept(self, visitor):\n")
    f.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n")

if __name__ == "__main__":
    main()
    print("AST classes generated successfully.")