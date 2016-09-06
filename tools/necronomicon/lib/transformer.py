import collections

RowEntry = collections.namedtuple('RowEntry', ['min_time', 'median_time', 'max_time', 'count', 'status_codes', 'paths', 'methods', 'cumulative_time'])

class BasicTransformer:
    def transform(self, doc, path=None):
        time_list = []
        status_codes = set()
        paths = set()
        methods = set()
        for entry in doc:
            time_list.append(entry.reqtime)
            status_codes.add(entry.status)
            if path is None:
                paths.add(entry.uri)
            methods.add(entry.method)
        time_list.sort()
        if path is not None:
            paths.add(path)
        return RowEntry(
                min_time=time_list[0],
                median_time=time_list[len(time_list)//2],
                max_time=time_list[-1],
                count=len(doc),
                status_codes=list(status_codes),
                paths=list(paths),
                methods=list(methods),
                cumulative_time=sum(time_list)
        )
