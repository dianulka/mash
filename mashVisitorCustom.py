from antlr4 import *
import sys
from gen.mashParser import mashParser
from gen.mashVisitor import mashVisitor

class mashVisitorCustom(mashVisitor):
    def __init__(self):
        self.variables = {}

    def visitProgram(self, ctx: mashParser.ProgramContext):
        result = []
        for statement in ctx.statement():
            result.append(self.visit(statement))
        return result

    def visitStatement(self, ctx: mashParser.StatementContext):
        return self.visitChildren(ctx)

    def visitEcho_function(self, ctx: mashParser.Echo_functionContext):
        if ctx.expression():
            result = self.visit(ctx.expression())
        else:
            var_name = ctx.IDENTIFIER().getText()
            if var_name not in self.variables:
                raise Exception(f"Variable '{var_name}' is not declared.")
            result = self.variables[var_name]["value"]

        if isinstance(result, str):
            print(result.strip('"'))
        elif isinstance(result, int):
            print(result)
        elif isinstance(result, bool):
            print("true" if result else "false")
        return result

    def visitExpression(self, ctx: mashParser.ExpressionContext):
        if ctx.arithmetic_expression():
            return self.visit(ctx.arithmetic_expression())
        elif ctx.string_expression():
            return self.visit(ctx.string_expression())
        elif ctx.logical_expression():
            return self.visit(ctx.logical_expression())
        elif ctx.int_expression():
            return int(ctx.int_expression().getText())
        elif ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            if var_name not in self.variables:
                raise Exception(f"Variable '{var_name}' is not declared.")
            return self.variables[var_name]["value"]
        return None

    def visitArithmetic_expression(self, ctx: mashParser.Arithmetic_expressionContext):
        return self.visit(ctx.additive_expression())

    def visitAdditive_expression(self, ctx: mashParser.Additive_expressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.visit(ctx.getChild(2))

        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right

    def visitMultiplicative_expression(self, ctx: mashParser.Multiplicative_expressionContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        left = self.visit(ctx.getChild(0))
        operator = ctx.getChild(1).getText()
        right = self.visit(ctx.getChild(2))

        if operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ValueError("Division by zero!")
            return int(left / right)

    def visitPrimary_expression(self, ctx: mashParser.Primary_expressionContext):
        if ctx.INTEGER():
            return int(ctx.INTEGER().getText())
        elif ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            if var_name not in self.variables:
                raise Exception(f"Variable '{var_name}' is not declared.")
            return self.variables[var_name]["value"]
        elif ctx.getChildCount() == 3:
            return self.visit(ctx.getChild(1))
        return None

    def visitString_expression(self, ctx: mashParser.String_expressionContext):
        return ctx.STRING().getText()

    def visitLogical_expression(self, ctx: mashParser.Logical_expressionContext):
        if ctx.getText() == "true":
            return True
        elif ctx.getText() == "false":
            return False

        if ctx.getChildCount() == 3:
            left = self.visit(ctx.getChild(0))
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.getChild(2))
            if operator == 'and':
                return left and right
            elif operator == 'or':
                return left or right

        if ctx.getChildCount() == 2 and ctx.getChild(0).getText() == 'not':
            expr = self.visit(ctx.getChild(1))
            return not expr

        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.getChild(1))

        if ctx.comparison_expression():
            return self.visit(ctx.comparison_expression())

        return None

    def visitComparison_expression(self, ctx: mashParser.Comparison_expressionContext):
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        operator = ctx.getChild(1).getText()

        if isinstance(left, str):
            left = left.strip('"')
        if isinstance(right, str):
            right = right.strip('"')

        if operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right

    def visitVar_declar(self, ctx: mashParser.Var_declarContext):
        var_type = ctx.type_().getText()
        var_name = ctx.IDENTIFIER(0).getText()
        if var_name in self.variables:
            print(f"Error: Variable '{var_name}' is already declared.", file=sys.stderr)
            return None
        self.variables[var_name] = {"type": var_type, "value": None}

        if ctx.expression():
            value = self.visit(ctx.expression())
            if var_type == "int_var" and not isinstance(value, int):
                print(f"Error: Variable '{var_name}' must be assigned an integer.", file=sys.stderr)
                return None
            elif var_type == "string_var" and not isinstance(value, str):
                print(f"Error: Variable '{var_name}' must be assigned a string.", file=sys.stderr)
                return None
            self.variables[var_name]["value"] = value
        elif ctx.IDENTIFIER(1):
            assigned_var_name = ctx.IDENTIFIER(1).getText()
            if assigned_var_name not in self.variables:
                print(f"Error: Variable '{assigned_var_name}' is not declared.", file=sys.stderr)
                return None
            value = self.variables[assigned_var_name]["value"]
            if var_type == "int_var" and not isinstance(value, int):
                print(f"Error: Variable '{var_name}' must be assigned an integer.", sys.stderr)
                return None
            elif var_type == "string_var" and not isinstance(value, str):
                print(f"Error: Variable '{var_name}' must be assigned a string.", sys.stderr)
                return None
            self.variables[var_name]["value"] = value

        return None

    def visitAssignment(self, ctx: mashParser.AssignmentContext):
        var_name = ctx.IDENTIFIER(0).getText()
        if var_name not in self.variables:
            print(f"Error: Variable '{var_name}' is not declared.", file=sys.stderr)
            return None
        var_type = self.variables[var_name]["type"]

        if ctx.IDENTIFIER(1):
            assigned_var_name = ctx.IDENTIFIER(1).getText()
            if assigned_var_name not in self.variables:
                print(f"Error: Variable '{assigned_var_name}' is not declared.", sys.stderr)
                return None
            value = self.variables[assigned_var_name]["value"]
        else:
            value = self.visit(ctx.expression())

        if var_type == "int_var" and not isinstance(value, int):
            print(f"Error: Variable '{var_name}' must be assigned an integer.", sys.stderr)
            return None
        elif var_type == "string_var" and not isinstance(value, str):
            print(f"Error: Variable '{var_name}' must be assigned a string.", sys.stderr)
            return None
        self.variables[var_name]["value"] = value
        return value

    def visitWhile_statement(self, ctx: mashParser.While_statementContext):
        while self.visit(ctx.logical_expression()):
            for statement in ctx.statement():
                self.visit(statement)
        return None

    def visitFor_statement(self, ctx: mashParser.For_statementContext):
        self.visit(ctx.assignment(0))

        while self.visit(ctx.logical_expression()):
            for statement in ctx.statement():
                self.visit(statement)

            self.visit(ctx.assignment(1))

        return None
        

    def visitIf_statement(self, ctx: mashParser.If_statementContext):
        if self.visit(ctx.logical_expression()):
            for statement in ctx.statement():
                self.visit(statement)
        else:
            for elifCtx in ctx.elif_block():
                if self.visit(elifCtx.logical_expression()):
                    for statement in elifCtx.statement():
                        self.visit(statement)
                    return None
            if ctx.else_block():
                for statement in ctx.else_block().statement():
                    self.visit(statement)
        return None


    # def visitIf_statement(self, ctx: mashParser.If_statementContext):
    #     conditions = []
    #     statements = []
    #     else_statement = None
    #
    #     for i in range(len(ctx.logical_expression())):
    #         conditions.append(ctx.logical_expression(i))
    #         statements.append(ctx.statement(i))
    #
    #     # Check if there is an else statement by checking if the number of statements is greater than the number of conditions
    #     if len(ctx.statement()) > len(ctx.logical_expression()):
    #         else_statement = ctx.statement(len(ctx.statement()) - 1)
    #
    #     for i in range(len(conditions)):
    #         if self.visit(conditions[i]):
    #             for statement in statements[i].statement():
    #                 self.visit(statement)
    #             return
    #
    #     if else_statement:
    #         for statement in else_statement.if_statement():
    #             self.visit(statement)
