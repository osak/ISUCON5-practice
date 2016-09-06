import os.path
import sys
ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_DIR, 'lib'))
sys.path.append(os.path.join(ROOT_DIR, '..'))

import log
import common
from aggregator import *
from transformer import *
from flask import Flask
from flask_mako import MakoTemplates, render_template
from plim import preprocessor
import os

config = common.load_config('necronomicon')

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
    for doc1 in PathAggregator(patterns=[r'/diary/comment/\d+', r'/diary/entry/.+', r'/friends/.+']).aggregate(document).values():
        for doc2 in StatusCodeAggregator().aggregate(doc1).values():
            rows.append(BasicTransformer().transform(doc2))
    return render_template('index.plim', rows=rows)

if __name__ == '__main__':
    app.run()
