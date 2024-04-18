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



## Functional Programming Features:

filter_tasks uses the filter function.


def filter_tasks(tasks, category=None, deadline=None):
    if category:
        tasks = filter(lambda x: x['category'].lower() == category.lower(), tasks)
    if deadline:
        tasks = filter(lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d') <= datetime.strptime(deadline, '%Y-%m-%d'), tasks)
    filtered_tasks = list(tasks)
    return filtered_tasks
Higher-Order Functions
apply_to_tasks is a higher-order function that applies a given operation to each task.


def apply_to_tasks(tasks, operation):
    return [operation(task) for task in tasks]


## Implementation of Pipelines:

task_display_pipeline function is a pipeline that loads tasks, filters them, and then refreshes the display.


def task_display_pipeline(username, app, listbox, category=None, deadline=None):
    tasks = load_tasks(username)
    filtered_tasks = filter_tasks(tasks, category, deadline)
    refresh_listbox(app, listbox, filtered_tasks)
