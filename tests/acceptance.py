import unittest
import sys
import os

from utils.taskwarrior import list_domains, run_task

class TestTaskwarriorExports(unittest.TestCase):

    def test_run_task(self):
        self.assertEqual(run_task('_projects').returncode, 0)

    def test_empty_session(self):
        """Make sure that we are not modifying the system task list"""
        if list_domains() != []:
            self.fail("The tests are not run on an empty instance, "
                    "check your config at tests/.taskrc")

    def test_one_domain(self):
        pass

if __name__ == '__main__':
    root = os.getenv('PYTHONPATH')
    os.environ['TASKRC'] = os.path.join(root, 'tests', '.taskrc')
    unittest.main()
