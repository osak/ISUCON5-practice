import log

class StatusCodeAggregator:
    def __init__(self, status_code):
        self.status_code = status_code

    def aggregate(self, doc):
        freq = {}
        for entry in doc:
            if entry.status not in self.status_code:
                continue
            if entry.status not in freq:
                freq[entry.status] = log.Document()
            freq[entry.status].append(entry)
        return freq


class RequestTimeAggregator:
    def __init__(self, resolution):
        self.resolution = resolution

    def aggregate(self, doc):
        res = {}
        for entry in doc:
            bin = (entry.request_time // self.resolution) * self.resolution
            if bin not in res:
                res[bin] = log.Document()
            res[bin].append(entry)
        return res

class PathAggregator:
    def __init__(self):
        pass

    def aggregate(self, doc):
        res = {}
        for entry in doc:
            path = entry.request_uri
            if path not in res:
                res[path] = log.Document()
            res[path].append(entry)
        return res
