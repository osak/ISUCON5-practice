#! /usr/bin/env python
import json
import sys

import re


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    if not line:
        raise EOFError()
    f.seek(pos)
    return line


def drop_header(log_file):
    while peek_line(log_file)[0] != '#':
        log_file.readline()


def number_field_parser(name):
    def parser(string):
        match = re.search("{name}:\s+(\d+(.\d+)?)".format(name=name), string)
        return float(match.group(1)) if match is not None else None
    return parser


def user_host_parser(string):
    match = re.search("^# User@Host: (.+?)\s+Id:\s+\d+$", string)
    return match.group(1) if match is not None else None


def parse_headers(headers):
    parsers = {
        "user_host": user_host_parser
    }
    for field in ["Id", "Query_time", "Lock_time", "Rows_sent", "Rows_examined"]:
        parsers[field] = number_field_parser(field)
    fields = dict()
    for line in headers:
        for field_name, parser in parsers.items():
            res = parser(line)
            if res is not None:
                fields[field_name.lower()] = res
    return fields


def read_entries(log_file):
    try:
        while True:
            headers = []
            while peek_line(log_file)[0] == '#':
                headers.append(log_file.readline())
            entry = parse_headers(headers)
            queries = []
            while peek_line(log_file)[0] != '#':
                queries.append(log_file.readline())
            entry["query_full"] = ''.join(queries)
            entry["query"] = queries[-1]
            yield entry
    except EOFError:
        raise StopIteration()


def main(log_file):
    drop_header(log_file)
    entries = read_entries(log_file)
    print json.dumps(list(entries))


if __name__ == '__main__':
    main(sys.stdin)