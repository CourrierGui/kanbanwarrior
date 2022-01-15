from . import html

def task_to_row(task: dict):
    row = html.TableRow()
    row.insert(str(task['id']))
    row.insert(task['description'])
    return row
