import os
import sys
dir_path = os.path.dirname(__file__)
sys.path.append(os.path.join(dir_path, 'lib'))

import log
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='解析したいファイル名')
args = parser.parse_args()

document = None
with open(args.filename) as f:
    document = log.Document(f)

freq = {}
for entry in document:
    if entry.status not in freq:
        freq[entry.status] = 0
    freq[entry.status] += 1

print(freq)
