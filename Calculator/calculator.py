# calculator.py - Simple GUI calculator using Tkinter
# Run with:  python3 calculator.py

import tkinter as tk
import math


class Calculator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator - Samarth")
        self.root.resizable(False, False)
        self.root.geometry("320x430")
        self.root.configure(bg="#121212")

        self.expression = ""

        self._create_display()
        self._create_buttons()

    def _create_display(self):
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Segoe UI", 22),
            bg="#1e1e1e",
            fg="#00ff7f",
            bd=0,
            justify="right",
            insertbackground="#00ff7f"
        )
        self.display.pack(fill="x", padx=12, pady=12, ipady=15)

    def _create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#121212")
        btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

        layout = [
            ["C", "DEL", "√", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "%"],
        ]

        for row_values in layout:
            row = tk.Frame(btn_frame, bg="#121212")
            row.pack(fill="both", expand=True)
            for text in row_values:
                btn = tk.Button(
                    row,
                    text=text,
                    font=("Segoe UI", 14),
                    bd=0,
                    relief="flat",
                    command=lambda t=text: self._on_button_click(t)
                )

                if text in {"+", "-", "*", "/", "%"}:
                    btn.configure(bg="#ff9800", fg="white")
                elif text in {"C", "DEL"}:
                    btn.configure(bg="#f44336", fg="white")
                elif text == "=":
                    btn.configure(bg="#4caf50", fg="white")
                else:
                    btn.configure(bg="#2b2b2b", fg="white")

                btn.pack(side="left", fill="both", expand=True, padx=3, pady=3)

    def _on_button_click(self, char: str):
        if char == "C":
            self.expression = ""
        elif char == "DEL":
            self.expression = self.expression[:-1]
        elif char == "=":
            self._evaluate()
        elif char == "√":
            self._sqrt()
        else:
            self.expression += char

        self.display_var.set(self.expression)

    def _evaluate(self):
        try:
            result = eval(self.expression)
            self.expression = str(result)
        except Exception:
            self.expression = "Error"

    def _sqrt(self):
        try:
            value = float(self.expression or "0")
            result = math.sqrt(value)
            self.expression = str(result)
        except Exception:
            self.expression = "Error"


def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

