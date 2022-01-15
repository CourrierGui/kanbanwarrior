from .taskwarrior import list_domains
from argparse import ArgumentParser


def exec_domains():
    domains = list_domains()
    for domain in domains:
        print(domain)


def dispatch_action(action: str, parser: ArgumentParser):
    try:
        eval('exec_' + action)()
    except NameError:
        print("Unknown command:", action)
        parser.print_help()
