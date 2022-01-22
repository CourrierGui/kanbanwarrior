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

    def add_row(self, align_top=False) -> Node:
        node = TableRow(valign="top") if align_top else TableRow()
        self.node.insert(node)

        return node


class Anchor:

    def __init__(self, link: str, child: Node = None):
        self.child = child
        self.link = link

    def dump(self) -> str:
        node = Node('a', tags='href="' + self.link + '"')
        if self.child:
            node.insert(self.child)

        return node.dump()


class Button:

    def __init__(self, child: Node = None):
        self.child = child

    def dump(self) -> str:
        node = Node('button')
        if self.child:
            node.insert(self.child)
        return node.dump()


class Comment:

    def __init__(self, comment: str):
        self.comment = comment

    def dump(self) -> str:
        return '<!' + self.comment + '>'


class Page:

    def __init__(self, title: str, css: str=''):
        self.title = title
        self.body = Node('body')
        self.css = css

    def insert(self, child: Node) -> None:
        self.body.insert(child)

    def dump(self) -> str:
        comment = Comment('DOCTYPE html')

        page = Node('html')
        head = Node('head')
        title = Node('title')

        page.insert(head)
        page.insert(self.body)
        title.insert(Text(self.title))
        head.insert(Node('meta', tags='charset="utf-8"'))
        if self.css:
            head.insert(Link(rel='stylesheet', type='text/css', href=self.css))

        head.insert(title)

        return comment.dump() + page.dump()


class Link:

    def __init__(self, rel: str='', type: str='', href: str=''):
        self.rel = rel
        self.href = href
        self.type = type

    def dump(self) -> str:
        value = 'rel="' + self.rel + '" ' if self.rel else ''
        value += 'type="' + self.type + '" ' if self.type else ''
        value += 'href="' + self.href + '"' if self.href else ''

        return Node('link', tags=value).dump()

