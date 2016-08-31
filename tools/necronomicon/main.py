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
parser.add_argument('--status-code', nargs='+', type=int, help='表示するステータスコード', dest='status_code', default=range(1000))
parser.add_argument('filename', help='解析したいファイル名')
args = parser.parse_args()

with open(args.filename) as f:
    document = log.Document(f)

path_agg = PathAggregator().aggregate(document)

for path, doc in path_agg.items():
    status_agg = StatusCodeAggregator(args.status_code).aggregate(doc)
    request_agg = RequestTimeAggregator(args.time_res).aggregate(doc)
    if len(status_agg) > 0 and len(request_agg) > 0:
        print(path + ':')
        with Indentor.dig():
            Indentor.print('Status code trends')
            with Indentor.dig():
                Indentor.print(HistogramPresenter().format(status_agg))

            Indentor.print('Response time trends')
            with Indentor.dig():
                Indentor.print(HistogramPresenter().format(request_agg))
    print()
