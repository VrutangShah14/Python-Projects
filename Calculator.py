import tkinter as tk

Pale_Gray = "#F5F5F5"
Text_Color = "#000000"
Snow_White = "#FFFFFF"
Light_Silver = "#F6FAFF"
Standard_Font = ("Arial", 20)
Number_Font = ("Arial", 24)
Tiny_Font = ("Arial", 16)
Huge_Font = ("Arial", 40, "bold")
Warning_Font = ("Arial", 20, "bold")


class Calculator:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("375x667")
        self.main_window.resizable(True, True)
        self.main_window.title("Calculator")
        self.main_window.iconbitmap('favicon.ico')
        self.aggregate_expression = ""
        self.active_expression = ""
        self.display_panel = self.setup_display_panel()
        self.aggregate_label, self.active_label = self.setup_labels()
        self.numeric_keys = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            ".": (4, 3),
        }
        self.math_operations = {"/": "÷", "*": "×", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.build_number_buttons()
        self.build_operator_buttons()
        self.build_clear_button()
        self.build_equals_button()
        self.build_sign_change_button()
        self.build_square_button()
        self.build_square_root_button()
        self.active_expression_font = Huge_Font
        self.setup_bindings()

    def setup_bindings(self):
        self.main_window.bind("<Return>", lambda event: self.evaluate())
        self.main_window.bind("<Escape>", lambda event: self.clear())
        for key in self.numeric_keys:
            self.main_window.bind(
                str(key), lambda event, digit=key: self.add_to_expression(digit)
            )
        for key in self.math_operations:
            self.main_window.bind(
                key, lambda event, operator=key: self.append_operator(operator)
            )

    def setup_labels(self):
        total_label = tk.Label(
            self.display_panel,
            text=self.aggregate_expression,
            anchor=tk.E,
            bg=Pale_Gray,
            fg=Text_Color,
            padx=24,
            font=Tiny_Font,
        )
        total_label.pack(expand=True, fill="both")

        label = tk.Label(
            self.display_panel,
            text=self.active_expression,
            anchor=tk.E,
            bg=Pale_Gray,
            fg=Text_Color,
            padx=24,
            font=Huge_Font,
        )
        label.pack(expand=True, fill="both")

        return total_label, label

    def setup_display_panel(self):
        frame = tk.Frame(self.main_window, height=221, bg=Pale_Gray)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        if "Error" in self.active_expression:
            self.active_expression = ""

        if "." in self.active_expression and value == ".":
            return

        self.active_expression += str(value)
        self.update_label()

    def build_number_buttons(self):
        for digit, grid_value in self.numeric_keys.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg=Snow_White,
                fg=Text_Color,
                font=Number_Font,
                borderwidth=0,
                command=lambda x=digit: self.add_to_expression(x),
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if "Error" in self.active_expression:
            self.clear()
        if self.active_expression:
            if self.active_expression.startswith("-"):
                self.aggregate_expression += "(" + self.active_expression + ")"
            else:
                self.aggregate_expression += self.active_expression
            self.aggregate_expression += operator
            self.active_expression = ""
        elif operator != "" and self.aggregate_expression:
            self.aggregate_expression = self.aggregate_expression[:-1] + operator
        self.update_total_label()
        self.update_label()

    def build_operator_buttons(self):
        i = 0
        for operator, symbol in self.math_operations.items():
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=Snow_White,
                fg=Text_Color,
                font=Standard_Font,
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x),
            )
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_buttons_frame(self):
        frame = tk.Frame(self.main_window)
        frame.pack(expand=True, fill="both")
        return frame

    def clear(self):
        self.active_expression = ""
        self.aggregate_expression = ""
        self.update_label()
        self.update_total_label()

    def build_clear_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="c",
            bg=Snow_White,
            fg=Text_Color,
            font=Standard_Font,
            borderwidth=0,
            command=self.clear,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        try:
            self.active_expression = str(eval(f"{self.active_expression}**2"))
        except Exception:
            self.active_expression = "Error"
        finally:
            self.update_label()

    def build_square_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2",
            bg=Snow_White,
            fg=Text_Color,
            font=Standard_Font,
            borderwidth=0,
            command=self.square,
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        try:
            self.active_expression = str(eval(f"{self.active_expression}**0.5"))
        except Exception:
            self.active_expression = "Error"
        finally:
            self.update_label()

    def build_square_root_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax",
            bg=Snow_White,
            fg=Text_Color,
            font=Standard_Font,
            borderwidth=0,
            command=self.sqrt,
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.aggregate_expression += self.active_expression
        self.update_total_label()
        expression = self.aggregate_expression.replace("÷", "/").replace("x", "*")
        try:
            self.active_expression = str(eval(expression))
            self.aggregate_expression = ""
            self.active_expression_font = Huge_Font
        except ZeroDivisionError:
            self.active_expression = "Error: Division by Zero"
            self.active_expression_font = Warning_Font
            self.aggregate_expression = ""
        except Exception as e:
            self.active_expression = "Error"
            self.active_expression_font = Warning_Font
            self.aggregate_expression = ""
        finally:
            self.update_label()
            self.update_total_label()

    def build_equals_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="=",
            bg=Snow_White,
            fg=Text_Color,
            font=Standard_Font,
            borderwidth=0,
            command=self.evaluate,
        )
        button.grid(row=4, column=4, sticky=tk.NSEW)

    def toggle_sign(self):
        if not self.active_expression:
            if self.aggregate_expression and not self.aggregate_expression.endswith(
                ("-", "+", "×", "÷")
            ):
                self.aggregate_expression += "-"
        else:
            if self.active_expression[0] == "-":
                self.active_expression = self.active_expression[1:]
            else:
                self.active_expression = "-" + self.active_expression
        self.update_label()
        self.update_total_label()

    def build_sign_change_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="+/-",
            bg=Snow_White,
            fg=Text_Color,
            font=Standard_Font,
            borderwidth=0,
            command=self.toggle_sign,
        )
        button.grid(row=4, column=1, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.aggregate_expression
        for operator, symbol in self.math_operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.aggregate_label.config(text=expression)

    def update_label(self):
        if len(self.active_expression) > 10:
            self.active_expression_font = Warning_Font
        else:
            self.active_expression_font = Huge_Font

        self.active_label.config(
            text=self.active_expression, font=self.active_expression_font
        )

    def run(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
