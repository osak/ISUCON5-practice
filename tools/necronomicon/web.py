import os.path
import sys
ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_DIR, 'lib'))

import log
from aggregator import *
from transformer import *
from flask import Flask
from flask_mako import MakoTemplates, render_template
from plim import preprocessor
import yaml

with open(os.path.join(ROOT_DIR, 'config.yml')) as f:
    config = yaml.load(f.read())

app = Flask(__name__)
mako = MakoTemplates(app)
app.config['MAKO_PREPROCESSOR'] = preprocessor


def load_log():
    log_path = config['log_path']
    with open(log_path) as f:
        document = log.Document(f)
    return document


@app.route('/')
def index():
    document = load_log()
    rows = []
    for doc1 in PathAggregator().aggregate(document).values():
        for doc2 in StatusCodeAggregator().aggregate(doc1).values():
            rows.append(BasicTransformer().transform(doc2))
    return render_template('index.plim', rows=rows)

if __name__ == '__main__':
    app.run()
