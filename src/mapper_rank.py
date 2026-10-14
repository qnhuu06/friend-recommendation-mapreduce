import json
from common import configure_io, emit, records

configure_io()
for raw_key, value in records():
    key = json.loads(raw_key)
    if key[0] == 'USER':
        emit(key[1], None)
    else:
        first, second = key[1:]
        emit(first, {'candidate': second, **value})
        emit(second, {'candidate': first, **value})
