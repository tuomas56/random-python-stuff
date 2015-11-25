class File:
    def __init__(self, name, length, offset, contents):
        self.name = name
        self.length = length
        self.offset = offset
        self.contents = contents

    def from_dict(d):
        self.name = d['name']
        self.length = d['length']
        self.offset = d['offset']
        self.contents = d['contents']

    def to_dict(d):
        return { 'name': self.name,
                 'length': self.length,
                 'offset': self.offset,
                 'contents': self.contents }