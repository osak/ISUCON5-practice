#! /usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
import slowquery
import re
from io import StringIO

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import common
config = common.load_config('sqlweb')


app = Flask(__name__)


def int_literal_normalizer(query):
    return re.sub(r"\b\d+\b", "{INT_LIT}", query)


def str_literal_normalizer(query):
    return re.sub("'.*?'", "{STR_LIT}", query)


query_normalizers = {
    "int": int_literal_normalizer,
    "str": str_literal_normalizer
}


@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return redirect(url_for("hello"))

    # FROM clause
    log_file = request.files["logfile"]
    if log_file.filename != '':
        log_file = StringIO(log_file.read().decode())
    else:
        log_file = open(config["default_log_location"])

    # WHERE clause
    query = request.form["where"]
    if not query:
        query = "True"

    # GROUP BY clause
    entries = slowquery.filter_entries(slowquery.parse_file(log_file), query)
    groupbys = request.form.getlist("groupby")
    for groupby in groupbys:
        query_normalizer = query_normalizers[groupby]
        for entry in entries:
            entry["query"] = query_normalizer(entry["query"])

    groups = dict()
    for entry in entries:
        entry["counts"] = 1.
        entry_query = entry["query"]
        if entry_query in groups:
            for agg_items in ["query_time", "lock_time", "rows_sent", "rows_examined", "counts"]:
                groups[entry_query][agg_items] += entry[agg_items]
        else:
            groups[entry_query] = entry
    context = {
        "query": query,
        "entries": groups.values(),
        "groupby": groupbys
    }
    log_file.close()
    return render_template('index.html', **context)


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5128)

