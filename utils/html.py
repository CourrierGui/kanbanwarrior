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
