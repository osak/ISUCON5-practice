#! /usr/bin/env python
from flask import Flask, render_template, request
import slowquery


app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query():
    log_file = request.files["logfile"]
    query = request.form["where"]
    entries = list(slowquery.filter_entries(slowquery.parse_file(log_file), query))
    context = {
        "entries": entries
    }
    return render_template('index.html', **context)


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5128)