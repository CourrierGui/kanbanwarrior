from flask import Flask
from utils import cli
from utils import taskwarrior as tw
from utils import task_converter as tc
from utils import _html


app = Flask(__name__)


def build_table_from_query(query: str) -> _html.Table:
    inbox = cli.table_from_query(query, 'status:pending', '-ACTIVE',
                                 '+inbox', 'export')
    todo = cli.table_from_query(query, 'status:pending', '-ACTIVE',
                                '-inbox', 'export')
    inprogress = cli.table_from_query(query, 'export', 'active')
    done = tw.list_tasks(query, 'end.after:today-1wk', 'export',
                         'completed')
    done = tc.tasks_to_table(done, id=False)

    table = _html.Table()
    header = table.make_header()
    row = table.add_row(align_top=True)

    header.insert('Inbox')
    row.insert_node(inbox)

    header.insert('TODO')
    row.insert_node(todo)

    header.insert('In Progess')
    row.insert_node(inprogress)

    header.insert('Done')
    row.insert_node(done)

    return table


@app.route('/')
def get_backlog():
    table = cli.build_page()
    return table.dump()


@app.route('/<string:action>/<string:name>')
def get_project_backlog(action: str, name: str):
    if action == 'domain':
        table = build_table_from_query('project:' + name)
    elif action == 'project':
        table = build_table_from_query('+' + name)
    else:
        return 'page not found'

    return table.dump()


if __name__ == '__main__':
    app.run()
