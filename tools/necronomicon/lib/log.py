import ltsv

class Document:
    def __init__(self, file):
        self.log = []
        for line in file:
            self.log.append(ltsv.Entry(line.strip()))

    def __str__(self):
        return "<log.Document size={0}>".format(len(self.log))

    def __iter__(self):
        return self.log.__iter__()
