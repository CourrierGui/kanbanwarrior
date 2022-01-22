import unittest
import sys
import os

from utils.taskwarrior import (list_domains,
                               run_task,
                               list_projects,
                               list_pending)

from utils import _html as html
from utils import task_converter as tc

class TestTaskwarriorExports(unittest.TestCase):

    def tearDown(self):
        # taskwarrior won't let me delete all tasks automaticaly...
        run_task('1', 'delete')
        run_task('2', 'delete')
        run_task('3', 'delete')
        # Remove completed as old tags will be listed from there
        os.remove(os.path.join(testdir, '.task/completed.data'))

    def test_one_project(self):
        run_task('add', '+one', 'task description')
        self.assertEqual(list_projects(), ['one'])

    def test_projects(self):
        run_task('add', '+one', 'task description')
        run_task('add', '+two', 'task description')
        run_task('add', '+three', 'task description')

        self.assertEqual(sorted(list_projects()),
                         sorted(['one', 'two', 'three']))

    def test_domains(self):
        run_task('add', 'project:one', 'task description')
        run_task('add', 'project:two', 'task description')
        run_task('add', 'project:three', 'task description')

        self.assertEqual(sorted(list_domains()),
                         sorted(['one', 'two', 'three']))

    def test_one_domain(self):
        run_task('add', 'project:one', 'task description')
        self.assertEqual(list_domains(), ['one'])

    def test_empty_session(self):
        """Make sure that we are not modifying the system task list"""
        if list_domains() != []:
            self.fail("The tests are not run on an empty instance, "
                      "check your config at tests/.taskrc")

    def test_run_task(self):
        self.assertEqual(run_task('_projects').returncode, 0)

    def test_list_no_pending(self):
        tasks = list_pending()
        self.assertEqual(tasks, [])

    def test_list_task(self):
        run_task('add', 'test')
        tasks = list_pending()
        self.assertEqual(tasks[0]["description"], "test")

    def test_list_tasks(self):
        run_task('add', "test")
        run_task('add', "test")

        tasks = list_pending()
        self.assertEqual(tasks[0]["description"], "test")
        self.assertEqual(tasks[1]["description"], "test")

    def test_list_pending_by_domain(self):
        run_task('add', 'test 1', 'project:test1')
        run_task('add', 'test 2', 'project:test2')

        domain1 = list_pending('project:test1')
        domain2 = list_pending('project:test2')

        self.assertEqual(len(domain1), 1)
        self.assertEqual(len(domain2), 1)

        self.assertEqual(domain1[0]["description"], "test 1")
        self.assertEqual(domain2[0]["description"], "test 2")

    def test_list_pending_by_project(self):
        run_task('add', '+test1', 'test 1')
        run_task('add', '+test2', 'test 2')

        project1 = list_pending('+test1')
        project2 = list_pending('+test2')

        self.assertEqual(len(project1), 1)
        self.assertEqual(len(project2), 1)

        self.assertEqual(project1[0]["description"], "test 1")
        self.assertEqual(project2[0]["description"], "test 2")

class TestHTMLGeneration(unittest.TestCase):

    def test_empty_text_node(self):
        self.assertEqual(html.Text('').dump(), '')

    def test_text_node(self):
        self.assertEqual(html.Text('test').dump(), 'test')

    def test_empty_html_node(self):
        self.assertEqual(html.Node('td').dump(), '<td/>')

    def test_empty_tr_node(self):
        self.assertEqual(html.Node('tr').dump(), '<tr/>')

    def test_node_with_text(self):
        node = html.Node('tr')
        node.insert(html.Text('test'))
        self.assertEqual(node.dump(), '<tr>test</tr>')

    def test_table_data(self):
        tabledata = html.TableData('test')
        self.assertEqual(tabledata.dump(),
                         '<td>test</td>')

    def test_empty_row_table(self):
        self.assertEqual(html.TableRow().dump(), '<tr/>')

    def test_table_row_with_one_row(self):
        row = html.TableRow()
        row.insert('test')
        self.assertEqual(row.dump(), '<tr><td>test</td></tr>')

    def test_table_row_with_3_entries(self):
        row = html.TableRow()
        row.insert('test')
        row.insert('test')
        row.insert('test')
        self.assertEqual(row.dump(),
                         '<tr><td>test</td><td>test</td><td>test</td></tr>')

    def test_empty_table_header(self):
        header = html.TableHeader()
        self.assertEqual(header.dump(), '<tr/>')

    def test_table_header(self):
        header = html.TableHeader()
        header.insert("test 1")
        header.insert("test 2")
        header.insert("test 3")
        self.assertEqual(header.dump(),
                '<tr><th>test 1</th><th>test 2</th><th>test 3</th></tr>')

    def test_table(self):
        table = html.Table()
        self.assertEqual(table.dump(), '<table/>')

    def test_table_with_empty_header(self):
        table = html.Table()
        table.make_header()
        self.assertEqual(table.dump(), '<table><tr/></table>')

    def test_table_with_header(self):
        table = html.Table()
        header = table.make_header()
        header.insert('test 1')
        header.insert('test 2')
        self.assertEqual(table.dump(),
                '<table><tr><th>test 1</th><th>test 2</th></tr></table>')

    def test_table_with_empty_row(self):
        table = html.Table()
        row = table.add_row()
        self.assertEqual(table.dump(), '<table><tr/></table>')

    def test_table_with_rows(self):
        table = html.Table()
        row = table.add_row()
        row.insert('test 1')
        row = table.add_row()
        row.insert('test 2')
        self.assertEqual(table.dump(),
                '<table><tr><td>test 1</td></tr><tr><td>test 2</td></tr></table>')

    def test_empty_anchor(self):
        a = html.Anchor('projects')
        self.assertEqual(a.dump(), '<a href="projects"/>')

    def test_anchor_with_text(self):
        a = html.Anchor('projects', child=html.Text('test'))
        self.assertEqual(a.dump(), '<a href="projects">test</a>')

    def test_empty_button(self):
        button = html.Button()
        self.assertEqual(button.dump(), '<button/>')

    def test_named_button(self):
        button = html.Button(child=html.Text('test'))
        self.assertEqual(button.dump(), '<button>test</button>')

    def test_button_with_link(self):
        a = html.Anchor('link', child=html.Button(html.Text('click me')))
        self.assertEqual(a.dump(),
                '<a href="link"><button>click me</button></a>')

    def test_comment(self):
        comment = html.Comment('comment')
        self.assertEqual(comment.dump(), "<!comment>")

    def test_main_empty_page(self):
        page = html.Page('Title')
        self.assertEqual(page.dump(),
                '<!DOCTYPE html><html><head><meta charset="utf-8"/><title>Title</title></head><body/></html>')

    def test_main_page(self):
        page = html.Page('Title')
        page.insert(html.Text('test'))

        self.assertEqual(page.dump(),
                '<!DOCTYPE html><html><head><meta charset="utf-8"/><title>Title</title></head><body>test</body></html>')


class TestTaskToHTMLConversions(unittest.TestCase):

    def tearDown(self):
        # taskwarrior won't let me delete all tasks automaticaly...
        run_task('1', 'delete')
        run_task('2', 'delete')
        run_task('3', 'delete')
        # Remove completed as old tags will be listed from there
        completed = os.path.join(testdir, '.task/completed.data') 
        if os.path.exists(completed):
            os.remove(completed)

    def test_tasks_to_table(self):
        run_task('add', 'test 1')
        run_task('add', 'test 2')
        tasks = list_pending()
        self.assertEqual(len(tasks), 2)
        table = tc.tasks_to_table(tasks)
        self.assertEqual(table.dump(),
                '<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>test 1</td></tr><tr><td>2</td><td>test 2</td></tr></table>')

    def test_tasks_to_table_without_id(self):
        run_task('add', 'test')
        task = list_pending()
        self.assertEqual(len(task), 1)
        table = tc.tasks_to_table(task, id=False)
        self.assertEqual(table.dump(),
                '<table><tr><th>description</th></tr><tr><td>test</td></tr></table>')

    def test_vertical_alignment_on_empty_row(self):
        row = html.TableRow(valign="top")
        self.assertEqual(row.dump(), '<tr valign="top"/>')

    def test_vertical_alignment_on_row(self):
        row = html.TableRow(valign="top")
        row.insert('test')
        self.assertEqual(row.dump(), '<tr valign="top"><td>test</td></tr>')

    def test_insertion_of_top_align_row(self):
        table = html.Table()
        row = table.add_row(align_top=True)
        row.insert('test')
        self.assertEqual(table.dump(),
                '<table><tr valign="top"><td>test</td></tr></table>')


if __name__ == '__main__':
    testdir = 'tests'

    if os.getenv('TASKRC') is None:
        testdir = os.getenv('TESTDIR')
        os.environ['TASKRC'] = os.path.join(testdir, '.taskrc')

    unittest.main()
