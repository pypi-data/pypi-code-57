
from lark import Lark

def on_error(token, e):
    breakpoint()

p = Lark("""
    start: expr
    expr: "(" expr ")"
        | "1"
""", on_error=on_error, parser='lalr')

p.parse("((((1)))")