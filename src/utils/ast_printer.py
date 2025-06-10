from src.ast.expr import Binary, Grouping, Literal, Unary, Expr
from src.core.token1 import Token
from src.core.token_type import TokenType


class AstPrinter:
    def print(self, expr: Expr) -> str: # This method initiates the printing process by calling the accept method on the expression
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:  
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str: 
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str: # This method creates a parenthesized string representation of the expression.
        parts = [f"({name}"]
        for expr in exprs:
            parts.append(f" {expr.accept(self)}")
        parts.append(")")
        return "".join(parts)


# Testing the AST printer
if __name__ == "__main__":
    # Example expression: (-123) * (45.67)
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )

    printer = AstPrinter()
    print(printer.print(expression))
