from setuptools import setup, find_packages

setup(
    name='kanbanwarrior',
    version='0.0.1',
    author='Guillaume Courrier',
    author_email='courrier.guillaume.123@gmail.com',
    url='https://github.com/CourrierGui/kanbanwarrior',
    description='An HTML/CSS frontend to taskwarrior to view tasks in a kanban board',
    license='GPLv3',
    packages=['utils'],
    package_dir={'utils': 'utils'},
    scripts=['kanban'],
)
