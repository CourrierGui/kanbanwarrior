from . import html

def tasks_to_table(tasks: list[dict], id: bool = True):
    table = html.Table()
    header = table.make_header()
    if id:
        header.insert('id')
    header.insert('description')

    for task in tasks:
        row = table.add_row()
        if id:
            row.insert(str(task['id']))
        row.insert(task['description'])

    return table
