import tkinter as tk
from tkinter import messagebox, simpledialog, END, ttk
import json
import os
from datetime import datetime
from tkcalendar import Calendar

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
    tasks.append(task)
    print("Debug: Added task", task)
    return tasks

def remove_task(tasks, index):
    print("Debug: Removed task at index", index)
    return tasks[:index] + tasks[index+1:]

def update_task(tasks, index, task):
    print("Debug: Updated task at index", index, "with", task)
    return tasks[:index] + [task] + tasks[index+1:]

def filter_tasks(tasks, filters, index=0):
    if index >= len(filters):
        print("Debug: Filtered tasks", tasks)
        return tasks

    current_filter_key, current_filter_value = filters[index]
    if current_filter_key == 'category':
        filtered_tasks = list(filter(lambda x: x['category'].lower() == current_filter_value.lower(), tasks))
    elif current_filter_key == 'deadline':
        filtered_tasks = list(filter(lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d') <= datetime.strptime(current_filter_value, '%Y-%m-%d'), tasks))

    return filter_tasks(filtered_tasks, filters, index + 1)  # Recursive call with the next filter index

def refresh_listbox(app, listbox, tasks):
    listbox.delete(0, END)
    for task in tasks:
        listbox.insert(END, f"{task['description']} - {task['category']} - {task['deadline']}")
    print("Debug: Refreshed listbox with tasks", tasks)

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

def main_app(username):
    app = tk.Tk()
    app.title(f"{username}'s ToDo List")
    listbox = tk.Listbox(app, width=80, height=20)
    listbox.pack()

    task_display_pipeline(username, app, listbox)

    tk.Button(app, text="Add Task", command=lambda: add_task_ui(app, username, listbox)).pack()
    tk.Button(app, text="Remove Selected Task", command=lambda: remove_task_ui(username, listbox)).pack()
    tk.Button(app, text="Search/Filter Tasks", command=lambda: search_tasks_ui(username, app, listbox)).pack()

    app.mainloop()

def task_display_pipeline(username, app, listbox, filters=None):
    tasks = load_tasks(username)
    if filters is None:
        filters = []
    filtered_tasks = filter_tasks(tasks, filters)
    refresh_listbox(app, listbox, filtered_tasks)

def add_task_ui(app, username, listbox):
    def submit_task():
        description = description_entry.get()
        category = category_var.get()
        deadline = cal.selection_get().strftime('%Y-%m-%d')
        new_task = create_task(description, category, deadline)
        nonlocal tasks
        tasks = add_task(tasks, new_task)
        save_tasks(username, tasks)
        refresh_listbox(app, listbox, tasks)
        add_task_window.destroy()

    tasks = load_tasks(username)
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

def remove_task_ui(username, listbox):
    selected_indices = listbox.curselection()
    tasks = load_tasks(username)
    for i in selected_indices[::-1]:
        tasks = remove_task(tasks, i)
    save_tasks(username, tasks)
    refresh_listbox(None, listbox, tasks)


def search_tasks_ui(username, app, listbox):
    tasks = load_tasks(username)
    category = simpledialog.askstring("Filter Tasks", "Enter category to filter by (leave blank for none):")
    deadline = simpledialog.askstring("Filter Tasks", "Enter deadline to filter by (YYYY-MM-DD, leave blank for none):")

    filters = []
    if category:
        filters.append(('category', category))
    if deadline:
        filters.append(('deadline', deadline))

    filtered_tasks = filter_tasks(tasks, filters)
    refresh_listbox(app, listbox, filtered_tasks)


login()
