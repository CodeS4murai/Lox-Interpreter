import sys

from src.core.interpreter import Interpreter
from src.utils.runtime_error import RuntimeError

class Lox:
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()
    
    @staticmethod
    def run_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
        Lox.run(source)

        if Lox.had_error:
            sys.exit(65)
        if Lox.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        print("Welcome to PyLox")
        try:
            while True:
                line = input("> ")
                if line.strip() == "":
                    continue
                Lox.run(line.strip())  
                Lox.had_error = False  # reset error after each line
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye")

    @staticmethod
    def run(source, Interpreter=None):
        from src.core.scanner import Scanner  
        from src.core.parser import Parser 
        from src.core.resolver import Resolver  
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()
        
        if Lox.had_error:
            return
        
        resolver = Resolver(Lox.interpreter)
        resolver.resolve(statements)
        
        if Lox.had_error:
            return
        
        try:
            Lox.interpreter.interpret(statements)
        except RuntimeError as e:
            Lox.runtime_error(e)

    @staticmethod
    def error(token_or_line, message):
        if isinstance(token_or_line, int):  # called with a line number
            Lox.report(token_or_line, "", message)
        else:
            token = token_or_line
            if token.type.name == "EOF":
                Lox.report(token.line, " at end", message)
            else:
                Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.had_error = True
        
    @staticmethod
    def runtime_error(error):
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        Lox.had_runtime_error = True

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: python lox.py [script]")
        sys.exit(64)
    elif len(args) == 1:
        Lox.run_file(args[0])
    else:
        Lox.run_prompt()
