from abc import ABC, abstractmethod

class Text:

    def __init__(self, value: str):
        self.value = value

    def dump(self) -> str:
        return self.value


class Node:

    def __init__(self, tag: str, tags: str=''):
        self.tags = tags
        self.tag = tag
        self.nodes = []

    def _dump_children(self) -> str:
        value = ""
        for node in self.nodes:
            value += node.dump()
        return value

    def insert(self, node) -> None:
        self.nodes.append(node)

    def dump(self) -> str:
        first_tag = self.tag
        if self.tags:
            first_tag += ' ' + self.tags

        if len(self.nodes) > 0:
            return ('<' + first_tag + '>'
                    + self._dump_children()
                    + '</' + self.tag + '>')
        else:
            return '<' + first_tag + '/>'


class TableData:

    def __init__(self, content: str):
        self.content = content

    def dump(self) -> str:
        return '<td>' + self.content + '</td>'


class TableRow:

    def __init__(self, valign=''):
        if valign:
            value = 'valign="' + valign + '"'
            self.row = Node('tr', tags=value)
        else:
            self.row = Node('tr')

    def dump(self) -> str:
        return self.row.dump()

    def insert(self, content: str) -> None:
        self.row.insert(TableData(content))

    def insert_node(self, node: Node) -> None:
        td = Node('td')
        td.nodes.append(node)
        self.row.insert(td)


class TableHeader:

    def __init__(self):
        self.node = Node('tr')

    def dump(self) -> str:
        return self.node.dump()

    def insert(self, content: str) -> None:
        node = Node('th')
        node.insert(Text(content))
        self.node.insert(node)


class Table:

    def __init__(self):
        self.node = Node('table')

    def dump(self) -> str:
        return self.node.dump()

    def make_header(self) -> Node:
        node = TableHeader()
        self.node.insert(node)

        return node

    def add_row(self) -> Node:
        node = TableRow()
        self.node.insert(node)

        return node
