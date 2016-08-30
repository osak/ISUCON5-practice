import os
import sys
dir_path = os.path.dirname(__file__)
sys.path.append(os.path.join(dir_path, 'lib'))

import log
import argparse
from aggregator import *
from presenter import *

parser = argparse.ArgumentParser()
parser.add_argument('--time-res', type=int, help='クエリ時間の分解能 (ms)', dest='time_res', default=100)
parser.add_argument('filename', help='解析したいファイル名')
args = parser.parse_args()

document = None
with open(args.filename) as f:
    document = log.Document(f)

path_agg = PathAggregator().aggregate(document)

for path, doc in path_agg.items():
    print(path + ':')
    with Indentor.indent() as indentor:
        indentor.print('Status code trends')
        with indentor.indent():
            indentor.print(HistogramPresenter().format(StatusCodeAggregator().aggregate(doc)))

        indentor.print('Response time trends')
        with indentor.indent():
            indentor.print(HistogramPresenter().format(RequestTimeAggregator(args.time_res).aggregate(doc)))
    print()
