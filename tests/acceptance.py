import unittest
import sys
import os

from utils.taskwarrior import (list_domains,
                               run_task,
                               list_projects,
                               list_pending)

from utils import html

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

    def test_empty_td_generation(self):
        self.assertEqual(html.Tag('td').dump(), '<td/>')

    def test_empty_tr_generation(self):
        self.assertEqual(html.Tag('tr').dump(), '<tr/>')

    def test_td_with_content(self):
        self.assertEqual(html.Tag('td', 'test').dump(), '<td>test</td>')

    def test_empty_row_table(self):
        self.assertEqual(html.TableRow().dump(), '<tr></tr>')

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

if __name__ == '__main__':
    testdir = 'tests'

    if os.getenv('TASKRC') is None:
        testdir = os.getenv('TESTDIR')
        os.environ['TASKRC'] = os.path.join(testdir, '.taskrc')

    unittest.main()
