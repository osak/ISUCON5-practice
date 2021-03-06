#! /usr/bin/env python
import argparse
import sys

import re


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    if not line:
        raise EOFError()
    f.seek(pos)
    return line


def peek_char(f):
    pos = f.tell()
    char = f.read(1)
    if not char:
        raise EOFError()
    f.seek(pos)
    return char


def drop_header(log_file):
    while peek_char(log_file) != '#':
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
        for field_name, parser in list(parsers.items()):
            res = parser(line)
            if res is not None:
                fields[field_name.lower()] = res
    return fields


def read_entries(log_file):
    try:
        while True:
            headers = []
            while peek_char(log_file) == '#':
                headers.append(log_file.readline())
            entry = parse_headers(headers)
            queries = []
            while peek_char(log_file) != '#':
                queries.append(log_file.readline())
            entry["query_full"] = ''.join(queries)
            entry["query"] = queries[-1]
            yield entry
    except EOFError:
        raise StopIteration()


def parse_file(log_file):
    drop_header(log_file)
    return read_entries(log_file)


def filter_entries(entries, query):
    return [entry for entry in entries if eval(query, None, entry)]


def report_sum_and_average(entries, name):
    total = sum([entry[name] for entry in entries])
    average = total / float(len(entries))
    print("average {name} = {average} (total: {total})".format(**vars()))


def main(log_file, query, n_queries):
    filtered_entries = list(filter_entries(parse_file(log_file), query))
    print("query:", query)
    print("SUMMARY")
    print("found {} entries".format(len(filtered_entries)))
    report_sum_and_average(filtered_entries, "query_time")
    report_sum_and_average(filtered_entries, "lock_time")
    report_sum_and_average(filtered_entries, "rows_sent")
    report_sum_and_average(filtered_entries, "rows_examined")
    print()
    print("{} SLOWEST queries".format(n_queries))
    for entry in sorted(filtered_entries, key=lambda entry: entry["query_time"], reverse=True)[:n_queries]:
        print("{}, {}".format(entry["query_time"], entry["query"].strip()))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("query", default="True", help="entry selector in Python expression which returns truthy value. An entries' field can be referenced by its name. e.g.: rows_examined==1000")
    argparser.add_argument("--file", type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument("--n", type=int, default=5)
    args = argparser.parse_args()
    main(args.file, args.query, args.n)