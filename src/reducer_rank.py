import argparse
import itertools
import json
from common import configure_io, records

configure_io()
parser = argparse.ArgumentParser()
parser.add_argument('--top-k', type=int, default=2)
args = parser.parse_args()
if args.top_k < 1:
    parser.error('--top-k phải lớn hơn 0')
for raw_key, group in itertools.groupby(records(), key=lambda item: item[0]):
    # Chỉ giữ K kết quả tốt nhất, không lưu toàn bộ danh sách ứng viên.
    best = []
    for _, value in group:
        if value is not None:
            best.append(value)
            best.sort(key=lambda row: (-row['score'], row['candidate']))
            del best[args.top_k:]
    print(json.dumps({'user': json.loads(raw_key), 'recommendations': best},
                     ensure_ascii=False))
