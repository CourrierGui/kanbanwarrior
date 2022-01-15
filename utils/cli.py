from .taskwarrior import list_domains, list_projects
from argparse import ArgumentParser


def exec_domains():
    domains = list_domains()
    for domain in domains:
        print(domain)


def exec_projects():
    projects = list_projects()
    for project in projects:
        print(project)


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
