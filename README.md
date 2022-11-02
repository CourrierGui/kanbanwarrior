# Kanban Warrior

A front-end to taskwarrior based on the kanban method with some inspirations
from the PARA and GTD methods.

## Features

This front end display tasks in a classic kanban: `TODO`, `In Progress` and `Done`.
- `TODO`: contains every task not starting in `taskwarrior`
- `In Progress`: contains every started ones
- `Done`: contains every tasks done

When a task is created (`task add ...`), it goes in the `TODO` column, `task
<n> start` puts it in the `In Progress` column and finally `task <n> done` puts
it in `Done`.

`Inbox`: this column contains unprocessed tasks. The goal is to put tasks first
in this column by giving them the tag `+inbox`. They can then be processed
later to assign projects and domains to them.

`Domains` map to projects in `taskwarrior`. They represent a theme or area that
create a constant flow of projects and tasks to maintain and don't have an end.

`Subdomains` map to subprojects in `taskwarrior`. They enable a finer
definition of areas of responsibilities.

`Projects` map to tags in `taskwarrior`. They have a beginning and an end.
They are the smallest way of aggregating tasks. A `domain` may contain
several projects.

## Installation

```
git clone https://github.com/CourrierGui/kanbanwarrior
cd kanbanwarrior
pip install .
```

### Dependencies

This project depends on `jinja2`, `flask` and `taskwarrior`.

## How to use

Start a local server to query different kanban boards:
```
kanban server
```

Then, access the boards with:
- `http://localhost:5000/`: all the tasks in one board
- `http://localhost:5000/projects/<name>`: access to the board of project `<name>`
- `http://localhost:5000/domains/<domain>.<subdomain>`:
    - access to the board of `<domain>.<subdmain>`
    - the subdomain is optional

## TODO

- add link between tasks
- display annotations
- display the project of a task
- add more control over queries
