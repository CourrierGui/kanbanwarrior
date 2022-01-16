from . import taskwarrior as tw
from . import task_converter as tc

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
    tasks = tw.list_pending()
    table = tc.tasks_to_table(tasks)

    print(table.dump())


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
