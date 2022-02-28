from flask import Flask
from utils import cli
from utils import taskwarrior as tw
from utils import task_converter as tc
from utils import _html


app = Flask(__name__)


def build_domain_table(domains: list[str]) -> _html.Table:
    table = _html.Table()

    header = table.make_header()
    header.insert('Domains')

    for domain in domains:
        row = table.add_row()
        a = _html.Anchor('/domains/'+domain,
                         _html.Button(_html.Text(domain)))
        row.insert_node(a)

    return table


def build_project_table(projects: list[str]) -> _html.Table:
    table = _html.Table()

    header = table.make_header()
    header.insert('Projects')

    for project in projects:
        row = table.add_row()
        a = _html.Anchor('/projects/' + project,
                         _html.Button(_html.Text(project)))
        row.insert_node(a)

    return table


def build_kanban_board(action: str, value: str) -> _html.Table:
    if action == 'projects':
        query = '+' + value
    elif action == 'domains':
        query = 'project:' + value
    else:
        return None

    todo = cli.table_from_query(query, 'status:pending', '-ACTIVE',
                                '-inbox', 'export')
    inprogress = cli.table_from_query(query, 'export', 'active')
    done = tw.list_tasks(query, 'end.after:today-1wk', 'export',
                         'completed')
    done = tc.tasks_to_table(done, id=False)

    table = _html.Table()
    header = table.make_header()
    row = table.add_row(align_top=True)

    header.insert('TODO')
    row.insert_node(todo)

    header.insert('In Progess')
    row.insert_node(inprogress)

    header.insert('Done')
    row.insert_node(done)

    return table


def build_page(action: str, value: str) -> _html.Table:
    main = _html.Table()
    rows = main.add_row(align_top=True)
    kanban = build_kanban_board(action, value);

    inbox_table = _html.Table()
    inbox_header = inbox_table.add_row()
    inbox_header.insert('<b>Inbox</b>')
    inbox_content = inbox_table.add_row()
    inbox_content.insert_node(cli.table_from_query('status:pending', '-ACTIVE',
                                                   '+inbox', 'export'))

    rows.insert_node(inbox_table)
    rows.insert_node(build_domain_table(tw.list_domains()))
    if action == 'domains':
        rows.insert_node(build_project_table(tw.list_projects(value)))


    if action == 'domains' and kanban:
        rows.insert_node(kanban)
    elif action == 'projects':

        sub = _html.Table()
        project = sub.add_row()
        project.insert('<b>Project:</b> ' + value)
        k = sub.add_row()
        if kanban:
            k.insert_node(kanban)

        rows.insert_node(sub)
    else:
        return None


    page = _html.Page('My Kanban', css='/static/styles/style.css')
    page.insert(main)
    return page


@app.route('/')
def get_backlog():
    table = cli.build_page()
    return table.dump() if table else 'page not found'


@app.route('/<string:action>/<string:name>')
def get_project_backlog(action: str, name: str):
    table = build_page(action, name)
    if not table:
        return 'page not found: /' + action + '/' + name
    else:
        return table.dump()


if __name__ == '__main__':
    app.run()
