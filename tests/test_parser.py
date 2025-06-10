"""from scanner import Scanner   
from parser import Parser      
from token1 import Token
from token_type import TokenType

def test_parser(source_code):
    # Tokenize the source code using Scanner
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    # Parse the tokens using Parser
    parser = Parser(tokens)
    expression = parser.parse()

    # Print the resulting AST (Abstract Syntax Tree)
    if expression:
        print(f"AST for '{source_code}': {expression}")
    else:
        print(f"Parse failed for '{source_code}'.")

# Test the parser with a sample expression
if __name__ == "__main__":
    source_code = "(-123) * (45.67)"
    test_parser(source_code)"""


from src.core.scanner import Scanner
from src.core.parser import Parser
from src.ast.expr import Expr
from src.ast.stmt import Stmt
from src.utils.ast_printer import AstPrinter

# Sample Lox source code to test parsing
source = """
class Foo {
  sayHi() {
    print "Hi!";
  }
}

fun greet(name) {
  print "Hello, " + name;
}

var x = 10;
if (x > 5) {
  print "Greater";
} else {
  print "Smaller";
}

while (x < 20) {
  x = x + 1;
}
"""

# Step 1: Scan tokens
from src.core.scanner import Scanner
scanner = Scanner(source)
tokens = scanner.scan_tokens()

# Step 2: Parse into AST
from src.core.parser import Parser
parser = Parser(tokens)
statements = parser.parse()

# Step 3: Print the parsed statements (AST summary)
for stmt in statements:
    print(stmt)
