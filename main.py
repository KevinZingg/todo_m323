import tkinter as tk
from tkinter import messagebox, simpledialog, END, ttk
import json
import os
from datetime import datetime
from tkcalendar import Calendar

# Utility functions to handle task persistence and functional programming principles
def load_tasks(username):
    filename = f"{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []
    print("Debug: Loaded tasks for user", username)
    return tasks

def save_tasks(username, tasks):
    with open(f"{username}.json", "w") as file:
        json.dump(tasks, file)
    print("Debug: Saved tasks for user", username)

def create_task(description, category, deadline):
    return {'description': description, 'category': category, 'deadline': deadline}

def add_task(tasks, task):
    print("Debug: Added task", task)
    return tasks + [task]

def remove_task(tasks, index):
    print("Debug: Removed task at index", index)
    return tasks[:index] + tasks[index+1:]

def update_task(tasks, index, task):
    print("Debug: Updated task at index", index, "with", task)
    return tasks[:index] + [task] + tasks[index+1:]

def filter_tasks(tasks, category=None, deadline=None):
    if category:
        tasks = filter(lambda x: x['category'].lower() == category.lower(), tasks)
    if deadline:
        tasks = filter(lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d') <= datetime.strptime(deadline, '%Y-%m-%d'), tasks)
    filtered_tasks = list(tasks)
    print("Debug: Filtered tasks", filtered_tasks)
    return filtered_tasks

# Login window
def login():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        print("Debug: Attempting login for", username)
        if password == "password":  # Replace with proper validation
            login_window.destroy()
            main_app(username)
        else:
            messagebox.showerror("Login failed", "Incorrect username or password")

    login_window = tk.Tk()
    login_window.title("Login")
    tk.Label(login_window, text="Username:").grid(row=0, column=0)
    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    username_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
    tk.Button(login_window, text="Login", command=attempt_login).grid(row=2, column=1)
    login_window.mainloop()

# Main application window
def main_app(username):
    app = tk.Tk()
    app.title(f"{username}'s ToDo List")

    tasks = load_tasks(username)

    def refresh_listbox(updated_tasks):
        listbox.delete(0, END)
        for task in updated_tasks:
            listbox.insert(END, f"{task['description']} - {task['category']} - {task['deadline']}")
        print("Debug: Refreshed listbox with tasks", updated_tasks)

    def add_task_ui():
        def submit_task():
            description = description_entry.get()
            category = category_var.get()
            deadline = cal.selection_get().strftime('%Y-%m-%d')
            new_task = create_task(description, category, deadline)
            nonlocal tasks
            tasks = add_task(tasks, new_task)
            save_tasks(username, tasks)
            refresh_listbox(tasks)
            add_task_window.destroy()

        add_task_window = tk.Toplevel(app)
        tk.Label(add_task_window, text="Task Description:").pack()
        description_entry = tk.Entry(add_task_window)
        description_entry.pack()

        tk.Label(add_task_window, text="Category:").pack()
        categories = ['Work', 'Home', 'Personal', 'Health']
        category_var = tk.StringVar(value=categories[0])
        category_dropdown = ttk.Combobox(add_task_window, textvariable=category_var, values=categories)
        category_dropdown.pack()

        tk.Label(add_task_window, text="Deadline:").pack()
        cal = Calendar(add_task_window, selectmode='day')
        cal.pack()

        tk.Button(add_task_window, text="Add Task", command=submit_task).pack()

    def remove_task_ui():
        selected_indices = listbox.curselection()
        nonlocal tasks
        for i in selected_indices[::-1]:
            tasks = remove_task(tasks, i)
        save_tasks(username, tasks)
        refresh_listbox(tasks)

    def search_tasks_ui():
        category = simpledialog.askstring("Filter Tasks", "Enter category to filter by (leave blank for none):")
        deadline = simpledialog.askstring("Filter Tasks", "Enter deadline to filter by (YYYY-MM-DD, leave blank for none):")
        filtered_tasks = filter_tasks(tasks, category, deadline)
        refresh_listbox(filtered_tasks)

    tk.Button(app, text="Add Task", command=add_task_ui).pack()
    tk.Button(app, text="Remove Selected Task", command=remove_task_ui).pack()
    tk.Button(app, text="Search/Filter Tasks", command=search_tasks_ui).pack()
    listbox = tk.Listbox(app, width=80, height=20)
    refresh_listbox(tasks)
    listbox.pack()
    app.mainloop()

# Start the login process
login()
