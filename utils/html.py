class Tag:

    def __init__(self, tag: str, content: str = ''):
        self.tag = tag
        self.content = content

    def dump(self) -> str:
        if len(self.content) > 0:
            return ("<" + self.tag + ">"
                    + self.content
                    + "</" + self.tag + ">")
        else:
            return "<" + self.tag + "/>"


class TableRow:

    def __init__(self):
        self.columns = []

    def dump(self) -> str:
        value = '<tr>'

        for columns in self.columns:
            value += columns.dump()

        value += '</tr>'
        return value

    def insert(self, content: str) -> None:
        self.columns.append(Tag('td', content))
