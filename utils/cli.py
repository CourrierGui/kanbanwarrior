from . import taskwarrior as tw
from . import task_converter as tc
from . import html

from argparse import ArgumentParser


def exec_domains():
    domains = tw.list_domains()
    for domain in domains:
        print(domain)


def exec_projects():
    projects = tw.list_projects()
    for project in projects:
        print(project)


def table_from_query(*args: str) -> html.Table:
    tasks = tw.list_tasks(*args)
    return tc.tasks_to_table(tasks)


def exec_page():
    inbox = table_from_query('status:pending', '-ACTIVE', '+inbox', 'export')
    todo = table_from_query('status:pending', '-ACTIVE', '-inbox', 'export')
    inprogress = table_from_query('export', 'active')
    done = table_from_query('end.after:today-1wk', 'export', 'completed')

    table = html.Table()
    header = table.make_header()
    row = table.add_row()

    header.insert('Inbox')
    row.insert_node(inbox)

    header.insert('TODO')
    row.insert_node(todo)

    header.insert('In Progess')
    row.insert_node(inprogress)

    header.insert('Done')
    row.insert_node(done)

    print(table.dump())


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
