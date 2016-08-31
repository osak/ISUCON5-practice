import re

class Entry:
    def __coerce(self, val):
        if re.match(r'^\d+$', val):
            return int(val)
        elif re.match(r'^\d+\.\d+$', val):
            return float(val)
        else:
            return str(val)

    def __init__(self, line):
        entries = line.split("\t")
        for entry in entries:
            key, val = entry.split(':', 1)
            val = self.__coerce(val)
            if key == 'request_time':
                val = int(val * 1000)
            setattr(self, key, val)

    def __str__(self):
        result = "<ltsv.Entry\n"
        for key, val in self.__dict__.items():
            result += "\t{0}={1}\n".format(key, val)
        result += '>'
        return result

