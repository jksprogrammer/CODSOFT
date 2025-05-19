import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x550")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        # History frame with Listbox and Scrollbar
        history_frame = tk.Frame(self.root)
        history_frame.pack(side=tk.TOP, fill='both', padx=5, pady=(5, 0))

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(history_frame, height=6, font=('Arial', 12), yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

        scrollbar.config(command=self.history_listbox.yview)

        # Input frame
        input_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        input_frame.pack(side=tk.TOP, fill='x', padx=5, pady=5)

        input_field = tk.Entry(input_frame, font=('Arial', 24), textvariable=self.input_text,
                               bd=0, bg="#eee", justify=tk.RIGHT)
        input_field.pack(fill='x', ipady=10)

        # Buttons frame
        btns_frame = tk.Frame(self.root)
        btns_frame.pack(fill='both', expand=True, padx=5, pady=5)

        for i in range(5):
            btns_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btns_frame.columnconfigure(j, weight=1)

        clear = tk.Button(btns_frame, text="C", fg="black", bd=0,
                          bg="#eee", cursor="hand2", font=('Arial', 16), command=self.btn_clear)
        clear.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=1, pady=1)

        divide = tk.Button(btns_frame, text="/", fg="black", bd=0,
                           bg="#ffa500", cursor="hand2", font=('Arial', 16), command=lambda: self.btn_click("/"))
        divide.grid(row=0, column=3, sticky="nsew", padx=1, pady=1)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2),
        ]

        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(btns_frame, text=text, fg="black", bd=0,
                                bg="#00bfff", cursor="hand2", font=('Arial', 16), command=self.btn_equal)
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=1, pady=1)
            elif text == '0':
                btn = tk.Button(btns_frame, text=text, fg="black", bd=0,
                                bg="#fff", cursor="hand2", font=('Arial', 16), command=lambda t=text: self.btn_click(t))
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            else:
                bg_color = "#fff" if text.isdigit() or text == '.' else "#ffa500"
                btn = tk.Button(btns_frame, text=text, fg="black", bd=0,
                                bg=bg_color, cursor="hand2", font=('Arial', 16), command=lambda t=text: self.btn_click(t))
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    def btn_click(self, item):
        self.expression += str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            result = str(eval(self.expression))
            history_entry = f"{self.expression} = {result}"
            self.append_history(history_entry)
            self.input_text.set(result)
            self.expression = result
        except Exception:
            self.input_text.set("Error")
            self.expression = ""

    def append_history(self, text):
        self.history_listbox.insert(tk.END, text)
        self.history_listbox.see(tk.END)

    def on_history_select(self, event):
        if not self.history_listbox.curselection():
            return
        index = self.history_listbox.curselection()[0]
        selected_text = self.history_listbox.get(index)
        # Extract the expression before '='
        expression = selected_text.split('=')[0].strip()
        self.expression = expression
        self.input_text.set(expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
