import unittest
import sys
import os

from utils.taskwarrior import list_domains, run_task, list_projects

class TestTaskwarriorExports(unittest.TestCase):

    def tearDown(self):
        # taskwarrior won't let me delete all tasks automaticaly...
        run_task('1', 'delete')
        run_task('2', 'delete')
        run_task('3', 'delete')

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

if __name__ == '__main__':
    if os.getenv('TASKRC') is None:
        testdir = os.getenv('TESTDIR')
        os.environ['TASKRC'] = os.path.join(testdir, '.taskrc')

    unittest.main()
