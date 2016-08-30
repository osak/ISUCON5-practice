class Indentor:
    @classmethod
    def dig(cls):
        if hasattr(cls, 'instance'):
            return cls.instance
        cls.instance = Indentor()
        return cls.instance

    @classmethod
    def print(cls, str):
        cls.instance._print(str)

    def __init__(self):
        self.depth = 0

    def __enter__(self):
        self.depth += 1
        return self

    def __exit__(self, exc_type, exc_val, trace):
        self.depth -= 1

    def _print(self, str):
        lines = str.split('\n')
        if str[-1] == '\n':
            lines.pop()
        indent = '    ' * self.depth
        joiner = '\n' + indent
        print(indent + joiner.join(lines))

class HistogramPresenter:
    def format(self, data):
        res = ''
        for key in sorted(data.keys()):
            str = '*' * (len(data[key]) // 10)
            res += "{key}: {str} {val}\n".format(key=key, str=str, val=len(data[key]))
        return res

