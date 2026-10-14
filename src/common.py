import json
import sys


def configure_io():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')


def emit(key, value):
    print(json.dumps(key, ensure_ascii=False) + '\t' +
          json.dumps(value, ensure_ascii=False))


def records():
    for line in sys.stdin:
        if line.strip():
            key, value = line.rstrip('\n').split('\t', 1)
            yield key, json.loads(value)
