from . import html

def tasks_to_table(tasks: list[dict]):
    table = html.Table()
    header = table.make_header()
    header.insert('id')
    header.insert('description')

    for task in tasks:
        row = table.add_row()
        row.insert(str(task['id']))
        row.insert(task['description'])

    return table
