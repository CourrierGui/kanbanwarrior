from setuptools import setup

setup(
    name='kanbanwarrior',
    version='0.0.1',
    author='Guillaume Courrier',
    author_email='courrier.guillaume.123@gmail.com',
    url='https://github.com/CourrierGui/kanbanwarrior',
    description='An HTML/CSS frontend to taskwarrior to view tasks in a kanban board',
    license='GPLv3',
    packages=['kanbanwarrior'],
    scripts=['kanban'],
    requires=['jinja2', 'flask'],
    provides=['kanbanwarrior'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
