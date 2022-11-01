from flask import Flask

from . import taskwarrior as tw
from .kanban import KanbanPage


app = Flask(__name__, static_folder='../static')


def build_page(action: str, value: str = '') -> KanbanPage:
    page = KanbanPage()

    if action == 'projects':
        query = '+' + value if value is not '' else ''
        page.projects(tw.list_projects())
    elif action == 'domains':
        query = 'pro:' + value if value is not '' else ''
        page.projects(tw.list_projects(value))

    page.domains(tw.list_domains())

    page.inbox(tw.list_tasks('status:pending', '-ACTIVE', '+inbox', 'export'))
    page.todo(tw.list_tasks(query, 'status:pending', '-ACTIVE', '-inbox', 'export'))
    page.inprogress(tw.list_tasks(query, 'export', 'active'))
    page.done(tw.list_tasks(query, 'end.after:today-1wk', 'export'))

    return page


@app.route('/')
def get_backlog():
    return build_page('domains').html()


@app.route('/<string:action>/<string:name>')
def get_project_backlog(action: str, name: str):
    return build_page(action, name).html()


if __name__ == '__main__':
    app.run()
