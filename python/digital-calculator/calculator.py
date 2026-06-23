"""A desktop calculator application built with Python and Tkinter."""

import ast
import math
import operator
import tkinter as tk

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expression):
    """Safely evaluate an arithmetic expression."""

    def evaluate_node(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
            left = evaluate_node(node.left)
            right = evaluate_node(node.right)
            return BINARY_OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
            return UNARY_OPERATORS[type(node.op)](evaluate_node(node.operand))

        raise ValueError("Unsupported expression")

    parsed_expression = ast.parse(expression, mode="eval")
    return evaluate_node(parsed_expression.body)

class Calculator:
    """Create and manage the calculator interface."""

    DISPLAY_SYMBOLS = {
        "/": "\u00f7",
        "*": "\u00d7",
        "-": "-",
        "+": "+",
    }

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Digital Calculator")
        self.window.geometry("380x600")
        self.window.resizable(False, False)
        self.window.configure(bg="#f3f4f6")

        self.expression = "0"
        self.history = ""
        self.just_evaluated = False

        self.history_text = tk.StringVar()
        self.display_text = tk.StringVar()

        self.create_display()
        self.create_buttons()
        self.bind_keys()
        self.update_display()

    def create_display(self):
        display_frame = tk.Frame(
            self.window,
            height=150,
            bg="#f3f4f6",
            padx=24,
            pady=20,
        )
        display_frame.pack(fill="both")
        display_frame.pack_propagate(False)

        history_label = tk.Label(
            display_frame,
            textvariable=self.history_text,
            anchor="e",
            bg="#f3f4f6",
            fg="#6b7280",
            font=("Calibri", 16),
        )
        history_label.pack(fill="both", expand=True)

        display_label = tk.Label(
            display_frame,
            textvariable=self.display_text,
            anchor="e",
            bg="#f3f4f6",
            fg="#111827",
            font=("Calibri", 38, "bold"),
        )
        display_label.pack(fill="both", expand=True)

    def create_buttons(self):
        button_frame = tk.Frame(self.window, bg="#d1d5db")
        button_frame.pack(fill="both", expand=True, padx=1, pady=1)

        for row in range(6):
            button_frame.rowconfigure(row, weight=1)

        for column in range(4):
            button_frame.columnconfigure(column, weight=1)

        buttons = [
            ("C", 0, 0, 1, self.clear, "#e5e7eb"),
            ("\u232b", 0, 1, 1, self.backspace, "#e5e7eb"),
            ("x\u00b2", 0, 2, 1, self.square, "#fdba74"),
            ("\u221ax", 0, 3, 1, self.square_root, "#fdba74"),
            ("7", 1, 0, 1, lambda: self.add_digit("7"), "#ffffff"),
            ("8", 1, 1, 1, lambda: self.add_digit("8"), "#ffffff"),
            ("9", 1, 2, 1, lambda: self.add_digit("9"), "#ffffff"),
            ("\u00f7", 1, 3, 1, lambda: self.add_operator("/"), "#fdba74"),
            ("4", 2, 0, 1, lambda: self.add_digit("4"), "#ffffff"),
            ("5", 2, 1, 1, lambda: self.add_digit("5"), "#ffffff"),
            ("6", 2, 2, 1, lambda: self.add_digit("6"), "#ffffff"),
            ("\u00d7", 2, 3, 1, lambda: self.add_operator("*"), "#fdba74"),
            ("1", 3, 0, 1, lambda: self.add_digit("1"), "#ffffff"),
            ("2", 3, 1, 1, lambda: self.add_digit("2"), "#ffffff"),
            ("3", 3, 2, 1, lambda: self.add_digit("3"), "#ffffff"),
            ("-", 3, 3, 1, lambda: self.add_operator("-"), "#fdba74"),
            ("0", 4, 0, 2, lambda: self.add_digit("0"), "#ffffff"),
            (".", 4, 2, 1, self.add_decimal, "#ffffff"),
            ("+", 4, 3, 1, lambda: self.add_operator("+"), "#fdba74"),
            ("=", 5, 0, 4, self.calculate, "#93c5fd"),
        ]

        for text, row, column, span, command, color in buttons:
            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                borderwidth=1,
                relief="flat",
                bg=color,
                activebackground="#e5e7eb",
                font=("Calibri", 20, "bold"),
                cursor="hand2",
            )
            button.grid(
                row=row,
                column=column,
                columnspan=span,
                sticky="nsew",
                padx=1,
                pady=1,
            )

    def bind_keys(self):
        self.window.bind("<Key>", self.handle_key)

    def handle_key(self, event):
        if event.char.isdigit():
            self.add_digit(event.char)
        elif event.char == ".":
            self.add_decimal()
        elif event.char in self.DISPLAY_SYMBOLS:
            self.add_operator(event.char)
        elif event.keysym in ("Return", "KP_Enter"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()

        return "break"

    def add_digit(self, digit):
        if self.expression == "Error" or self.just_evaluated:
            self.expression = digit
            self.history = ""
            self.just_evaluated = False
        elif self.expression == "0":
            self.expression = digit
        elif len(self.expression) < 24:
            self.expression += digit

        self.update_display()

    def add_decimal(self):
        if self.expression == "Error" or self.just_evaluated:
            self.expression = "0."
            self.history = ""
            self.just_evaluated = False
        else:
            current_number = self.expression

            for symbol in self.DISPLAY_SYMBOLS:
                current_number = current_number.rsplit(symbol, 1)[-1]

            if "." not in current_number:
                self.expression += "." if current_number else "0."

        self.update_display()

    def add_operator(self, selected_operator):
        if self.expression == "Error":
            return

        if self.expression[-1] in self.DISPLAY_SYMBOLS:
            self.expression = self.expression[:-1] + selected_operator
        else:
            self.expression += selected_operator

        self.just_evaluated = False
        self.update_display()

    def calculate(self):
        if self.expression == "Error":
            return

        expression = self.expression.rstrip("+-*/")

        try:
            result = evaluate_expression(expression)

            if not math.isfinite(result):
                raise ValueError("Result is not finite")

            self.history = f"{self.format_expression(expression)} ="
            self.expression = self.format_number(result)
            self.just_evaluated = True
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
            self.show_error()

        self.update_display()

    def square(self):
        try:
            value = evaluate_expression(self.expression.rstrip("+-*/"))
            result = value**2

            if not math.isfinite(result):
                raise ValueError("Result is not finite")

            self.history = f"({self.format_number(value)})\u00b2"
            self.expression = self.format_number(result)
            self.just_evaluated = True
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
            self.show_error()

        self.update_display()

    def square_root(self):
        try:
            value = evaluate_expression(self.expression.rstrip("+-*/"))

            if value < 0:
                raise ValueError("Negative square root")

            self.history = f"\u221a({self.format_number(value)})"
            self.expression = self.format_number(math.sqrt(value))
            self.just_evaluated = True
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
            self.show_error()

        self.update_display()

    def backspace(self):
        if self.expression == "Error" or self.just_evaluated:
            self.clear()
            return

        self.expression = self.expression[:-1] or "0"
        self.update_display()

    def clear(self):
        self.expression = "0"
        self.history = ""
        self.just_evaluated = False
        self.update_display()

    def show_error(self):
        self.expression = "Error"
        self.history = ""
        self.just_evaluated = True

    def format_expression(self, expression):
        for operator_symbol, display_symbol in self.DISPLAY_SYMBOLS.items():
            expression = expression.replace(
                operator_symbol,
                f" {display_symbol} ",
            )

        return expression

    @staticmethod
    def format_number(number):
        if abs(number) < 1e-12:
            return "0"

        if float(number).is_integer() and abs(number) < 1e12:
            return str(int(number))

        return f"{number:.12g}"

    def update_display(self):
        self.history_text.set(self.history)
        self.display_text.set(self.format_expression(self.expression))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()