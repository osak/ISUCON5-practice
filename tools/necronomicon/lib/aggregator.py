import log
import re

class StatusCodeAggregator:
    def __init__(self):
        pass

    def aggregate(self, doc):
        freq = {}
        for entry in doc:
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
            bin = (entry.reqtime // self.resolution) * self.resolution
            if bin not in res:
                res[bin] = log.Document()
            res[bin].append(entry)
        return res


class PathAggregator:
    def __init__(self, patterns=None):
        self.patterns = patterns

    def aggregate(self, doc):
        res = {}
        for entry in doc:
            path = entry.uri
            pattern = self.determine_pattern(path)
            if pattern not in res:
                res[pattern] = log.Document()
            res[pattern].append(entry)
        return res

    def determine_pattern(self, path):
        if self.patterns:
            for pattern in self.patterns:
                if re.match(pattern, path):
                    return pattern
        else:
            return path
        return None
