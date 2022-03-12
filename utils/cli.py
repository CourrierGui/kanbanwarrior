from argparse import ArgumentParser

from . import taskwarrior as tw


def exec_domains():
    domains = tw.list_domains()
    for domain in domains:
        print(domain)


def exec_projects():
    projects = tw.list_projects()
    for project in projects:
        print(project)


def exec_server():
    from .server import app
    app.run()


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
