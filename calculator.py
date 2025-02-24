import tkinter as tk
import math
import sympy as sp
import random

# Memory to store last 4 answers
memory = []

# Define a function to toggle between normal mode and scientific mode
def toggle_mode():
    global normal_mode
    normal_mode = not normal_mode
    update_buttons()

# Function to update button layout based on mode
def update_buttons():
    for widget in frame.winfo_children():
        widget.grid_forget()

    if normal_mode:
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('(', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), (')', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3), ('x²', 4, 4),
        ]
    else:
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('(', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), (')', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3), ('x²', 4, 4),
            ('sqrt', 5, 0), ('log10', 5, 1), ('sin', 5, 2), ('cos', 5, 3), ('tan', 5, 4),
            ('x³', 6, 0), ('1/x', 6, 1), ('e^x', 6, 2), ('x!', 6, 3), ('pi', 6, 4),
            ('M+', 7, 0), ('M-', 7, 1), ('MR', 7, 2), ('MC', 7, 3), ('Rand', 7, 4),
            ('EE', 8, 0), ('Rad', 8, 1), ('sinh', 8, 2), ('cosh', 8, 3), ('tanh', 8, 4),
        ]

    # Add buttons to grid based on mode
    for btn in buttons:
        text, row, col = btn[:3]
        rowspan, colspan = (btn[3], btn[4]) if len(btn) == 5 else (1, 1)

        if text == 'C':
            action = clear_entry
        elif text == '=':
            action = evaluate_expression
        elif text == 'Solve x':
            action = solve_quadratic
        elif text in ['x²', 'x³', '1/x', 'e^x', 'log10', 'sin', 'cos', 'tan', 'sqrt', 'sinh', 'cosh', 'tanh', 'pi', 'Rand', 'EE']:
            action = lambda op=text: scientific_operations(op)
        elif text == 'M+':
            action = lambda: update_memory(entry.get())
        elif text == 'M-':
            action = lambda: update_memory(-float(entry.get()))
        elif text == 'MC':
            action = lambda: memory.clear()
        elif text == 'MR':
            action = lambda: recall_memory(len(memory)-1)
        elif text == 'Rand':
            action = lambda: entry.insert(tk.END, random.random())
        elif text == 'Rad':
            action = lambda: entry.insert(tk.END, "math.radians(")
        elif text == 'x!':
            action = lambda: entry.insert(tk.END, f"math.factorial({entry.get()})")
        else:
            action = lambda x=text: insert_value(x)

        tk.Button(frame, text=text, width=5, height=2, font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#45a049", command=action).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew")

# Adjust the size of the grid to be responsive
def on_resize(event):
    for row in range(9):
        frame.grid_rowconfigure(row, weight=1, minsize=70)  # Ensure a minimum size for rows
    for col in range(5):
        frame.grid_columnconfigure(col, weight=1, minsize=100)  # Ensure a minimum size for columns

def evaluate_expression():
    try:
        expression = entry.get()
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        update_memory(result)  # Save the result to memory
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def insert_value(value):
    entry.insert(tk.END, value)

def clear_entry():
    entry.delete(0, tk.END)

def backspace():
    current_text = entry.get()
    entry.delete(len(current_text)-1, tk.END)

def solve_quadratic():
    try:
        eq = entry.get()
        x = sp.Symbol('x')
        solutions = sp.solve(eq, x)
        entry.delete(0, tk.END)
        entry.insert(tk.END, solutions)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def update_memory(result):
    memory.append(result)
    if len(memory) > 4:
        memory.pop(0)

def recall_memory(index):
    if index < len(memory):
        entry.delete(0, tk.END)
        entry.insert(tk.END, memory[index])

def scientific_operations(op):
    try:
        expression = entry.get()
        if op == "x²":
            result = eval(f"({expression})**2")
        elif op == "x³":
            result = eval(f"({expression})**3")
        elif op == "1/x":
            result = 1 / float(expression)
        elif op == "e^x":
            result = math.exp(float(expression))
        elif op == "log10":
            result = math.log10(float(expression))
        elif op == "sin":
            result = math.sin(math.radians(float(expression)))
        elif op == "cos":
            result = math.cos(math.radians(float(expression)))
        elif op == "tan":
            result = math.tan(math.radians(float(expression)))
        elif op == "sinh":
            result = math.sinh(float(expression))
        elif op == "cosh":
            result = math.cosh(float(expression))
        elif op == "tanh":
            result = math.tanh(float(expression))
        elif op == "pi":
            result = math.pi
        elif op == "rand":
            result = random.random()
        elif op == "EE":
            result = float(expression) * 10**6  # Example scientific notation scaling
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        update_memory(result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# GUI Setup
root = tk.Tk()
root.title("Scientific Calculator")

# Make the window resizable and bigger on start
root.geometry("800x800")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

entry = tk.Entry(root, width=40, font=("Arial", 18), relief="sunken", bd=3)
entry.grid(row=0, column=0, columnspan=5, sticky="nsew")

# Frame for the buttons
frame = tk.Frame(root)
frame.grid(row=1, column=0, columnspan=5, sticky="nsew")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Toggle button (set to always visible)
toggle_button = tk.Button(root, text="Toggle Mode", font=("Arial", 14), bg="red", fg="white", activebackground="#e53935", command=toggle_mode)
toggle_button.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)

# Adding backspace button
backspace_button = tk.Button(root, text="←", width=5, height=2, font=("Arial", 14), bg="#f44336", fg="white", activebackground="#e53935", command=backspace)
backspace_button.grid(row=4, column=5, sticky="nsew")

# Initially set to normal mode
normal_mode = True
update_buttons()

# Bind window resize
root.bind("<Configure>", on_resize)

root.mainloop()

