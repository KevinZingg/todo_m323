# How to use

Login with Username "Sivan" and password "password".

Find then come to the next screen where you see all tasks, can add new ones, delete and filter.

## Pure Functions

create_task 
This function returns a new dictionary based on the inputs without modifying any external state.

def create_task(description, category, deadline):
    return {'description': description, 'category': category, 'deadline': deadline}


## Immutable Data:

add_task, remove_task, update_task


def add_task(tasks, task):
    return tasks + [task]

def remove_task(tasks, index):
    return tasks[:index] + tasks[index+1:]

def update_task(tasks, index, task):
    return tasks[:index] + [task] + tasks[index+1:]

## Recursion:

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


## Functional Programming Features:

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



def apply_to_tasks(tasks, operation):
    return [operation(task) for task in tasks]


## Implementation of Pipelines:

task_display_pipeline function is a pipeline that loads tasks, filters them, and then refreshes the display.


def task_display_pipeline(username, app, listbox, category=None, deadline=None):
    tasks = load_tasks(username)
    filtered_tasks = filter_tasks(tasks, category, deadline)
    refresh_listbox(app, listbox, filtered_tasks)
