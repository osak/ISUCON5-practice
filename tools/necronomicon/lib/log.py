import ltsv

class Document:
    def __init__(self, file=None):
        self.log = []
        if file:
            for line in file:
                self.log.append(ltsv.Entry(line.strip()))

    def append(self, val):
        if not isinstance(val, ltsv.Entry):
            raise TypeError('Illegal val type')
        self.log.append(val)

    def __str__(self):
        return "<log.Document size={0}>".format(len(self.log))

    def __iter__(self):
        return self.log.__iter__()

    def __len__(self):
        return len(self.log)
