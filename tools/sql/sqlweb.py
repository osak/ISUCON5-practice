#! /usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
import slowquery


DEFAULT_LOG_LOCATION = "../../sample_logs/mysql-slow.log"


app = Flask(__name__)


@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return redirect(url_for("hello"))
    log_file = request.files["logfile"]
    if log_file.filename == '':
        log_file = open(DEFAULT_LOG_LOCATION)
    query = request.form["where"]
    if not query:
        query = "True"
    entries = list(slowquery.filter_entries(slowquery.parse_file(log_file), query))
    context = {
        "query": query,
        "entries": entries
    }
    log_file.close()
    return render_template('index.html', **context)


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5128)

