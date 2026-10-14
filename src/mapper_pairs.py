import itertools
import json
import sys
from common import configure_io, emit

configure_io()
for line in sys.stdin:
    if not line.strip():
        continue
    row = json.loads(line)
    user = row['user']
    friends = sorted(set(row['friends']) - {user})
    # Giữ cả người cô lập và người không có ứng viên.
    emit(['USER', user], None)
    for friend in friends:
        emit(['PAIR', *sorted((user, friend))], ['DIRECT'])
    for first, second in itertools.combinations(friends, 2):
        emit(['PAIR', first, second], ['MUTUAL', user])
