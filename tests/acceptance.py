import unittest
import sys
import os

from utils.taskwarrior import test

class TestTaskwarriorExports(unittest.TestCase):

    def test_list_projects(self):
        self.assertEqual(test().upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
