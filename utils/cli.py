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


def exec_page():
    todo = tw.list_pending('-ACTIVE')
    todo = tc.tasks_to_table(todo)

    inprogress = tw.list_tasks('export', 'active')
    inprogress = tc.tasks_to_table(inprogress)

    finished = tw.list_tasks('end.after:today-1wk', 'export', 'completed')
    finished = tc.tasks_to_table(finished)

    inbox = tw.list_pending('-ACTIVE', '+inbox')
    inbox = tc.tasks_to_table(inbox)

    table = html.Table()
    header = table.make_header()
    header.insert('Inbox')
    header.insert('TODO')
    header.insert('In Progess')
    header.insert('Done')
    row = table.add_row()
    row.insert_node(inbox)
    row.insert_node(todo)
    row.insert_node(inprogress)
    row.insert_node(finished)

    print(table.dump())


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
