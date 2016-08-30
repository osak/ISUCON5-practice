class Entry:
    def __init__(self, line):
        entries = line.split("\t")
        for entry in entries:
            key, val = entry.split(':', 1)
            setattr(self, key, val)

    def __str__(self):
        result = "<ltsv.Entry\n"
        for key, val in self.__dict__.items():
            result += "\t{0}={1}\n".format(key, val)
        result += '>'
        return result

