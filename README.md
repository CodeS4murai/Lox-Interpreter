# Lox Interpreter in Python

A Python implementation of the Lox language, based on Robert Nystrom's [Crafting Interpreters](https://craftinginterpreters.com/). This project follows the book's tree-walk interpreter structure from the original Java implementation and adapts it to idiomatic Python.


## About the Project

This project is a personal reimplementation of the Lox interpreter in Python. It serves as a learning tool for understanding programming language design and interpreter construction. It closely mirrors the architecture and structure described in the book while embracing Pythonic practices.

- Based on Crafting Interpreters by Robert Nystrom
- Written entirely in Python 3
- Implements the full tree-walk interpreter for Lox
- Includes lexical analysis, parsing, AST generation, semantic analysis, and interpretation


## Components

- *Scanner*: Converts source code into tokens
- *Parser*: Parses tokens into an Abstract Syntax Tree (AST)
- *Resolver*: Performs semantic checks like variable resolution
- *Interpreter*: Evaluates the AST and executes code
- *Error Handling*: Reports both compile-time and runtime errors


## Usage

The Lox interpreter supports two modes of operation: executing a Lox script file or interacting via a Read-Eval-Print Loop (REPL).

### 1. Running a Lox Script File

To execute a Lox source file, provide its path as a command-line argument:

```bash
python lox.py <path/to/your_script.lox>
```

**Example:**

Given `examples/simple.lox`:
```lox
// examples/simple.lox
var greeting = "Hello, Lox!";
print greeting;

fun multiply(a, b) {
  return a * b;
}
print multiply(5, 3);
```

Execute it:
```bash
python lox.py examples/simple.lox
```

**Output:**
```
Hello, Lox!
15
```

### 2. Interactive Mode (REPL)

For direct interaction and experimentation, launch the interpreter without arguments:

```bash
python lox.py
```

This initiates an interactive prompt (`>`). Type Lox expressions or statements, and the interpreter will evaluate them immediately.

```
> print "Welcome to the Lox REPL!";
Welcome to the Lox REPL!
> var x = 10;
> print x / 2;
5
> fun fib(n) {
.   if (n <= 1) return n;
.   return fib(n - 2) + fib(n - 1);
. }
> print fib(8);
21
> // Press Ctrl+C or type 'exit' (if supported) to quit.
```
## License
This source code is licensed under MIT License.





