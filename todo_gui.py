import tkinter as tk
from tkinter import messagebox, colorchooser

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        self.bg_color = "white"
        self.root.configure(bg=self.bg_color)

        self.tasks = []

        self.heading = tk.Label(root, text="To-Do List", font=("Georgia", 20, "bold"), bg=self.bg_color)
        self.heading.pack(pady=10)

        self.task_entry = tk.Entry(root, font=("Georgia", 14), width=30)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", font=("Georgia", 12), command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=45, height=10, font=("Georgia", 12), selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", font=("Georgia", 12), command=self.delete_task)
        self.delete_button.grid(row=0, column=0, padx=5)

        self.mark_done_button = tk.Button(self.button_frame, text="Mark as Done", font=("Georgia", 12), command=self.mark_done)
        self.mark_done_button.grid(row=0, column=1, padx=5)

        self.color_button = tk.Button(root, text="🎨 Change Background Color", font=("Georgia", 12), command=self.change_color)
        self.color_button.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_done(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.tasks[selected_index[0]]
            if not task.endswith(" ✔"):
                self.tasks[selected_index[0]] += " ✔"
                self.update_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def change_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color = color
            self.root.configure(bg=color)
            self.heading.configure(bg=color)
            self.button_frame.configure(bg=color)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
