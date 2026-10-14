import itertools
import json
from common import configure_io, emit, records

configure_io()
for raw_key, group in itertools.groupby(records(), key=lambda item: item[0]):
    key = json.loads(raw_key)
    direct = False
    mutual = set()
    for _, value in group:
        if key[0] == 'PAIR':
            if value[0] == 'DIRECT':
                direct = True
            elif value[0] == 'MUTUAL':
                mutual.add(value[1])
    if key[0] == 'USER':
        emit(key, None)
    elif not direct and mutual:
        emit(key, {'score': len(mutual), 'mutual_friends': sorted(mutual)})
