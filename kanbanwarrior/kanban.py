from flask import render_template


class KanbanPage:

    def __init__(self):
        self._domains = dict()

    def domains(self, values: list[str]) -> None:
        for domain in values:
            subdomains = domain.split('.')
            if subdomains[0] not in self._domains:
                self._domains[subdomains[0]] = []

            # FIXME add support for nested domains?
            if len(subdomains) == 2:
                self._domains[subdomains[0]].append(subdomains[1])
            elif len(subdomains) > 2:
                self._domains[subdomains[0]].append('.'.join(subdomains[1:]))

    def projects(self, values: list[str]) -> None:
        self._projects = values

    def inbox(self, values: list[str]) -> None:
        self._inbox = values

    def todo(self, values: list[str]) -> None:
        self._todo = values

    def inprogress(self, values: list[str]) -> None:
        self._inprogress = values

    def done(self, values: list[str]) -> None:
        self._done = values

    def html(self) -> str:
        return render_template('template.html',
                               title='My Kanban',
                               inbox=self._inbox,
                               todo=self._todo,
                               inprogress=self._inprogress,
                               done=self._done,
                               projects=self._projects,
                               domains=self._domains)
