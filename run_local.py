"""Chạy mô phỏng MapReduce cục bộ, không cần thư viện ngoài."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from preprocess import normalize


def run_script(script, source, target, *arguments):
    environment = dict(os.environ, PYTHONIOENCODING='utf-8')
    with source.open('rb') as incoming, target.open('wb') as outgoing:
        subprocess.run([sys.executable, str(ROOT / 'src' / script), *arguments],
                       stdin=incoming, stdout=outgoing, env=environment, check=True)


def shuffle(source, target):
    # Mô phỏng local: sort trong RAM. Hadoop sẽ shuffle/sort phân tán.
    lines = source.read_text(encoding='utf-8').splitlines()
    lines.sort(key=lambda line: line.split('\t', 1)[0])
    target.write_text(''.join(line + '\n' for line in lines), encoding='utf-8')


def run(input_path, output_dir, top_k=2):
    if top_k < 1:
        raise ValueError('top_k phải lớn hơn 0')
    graph, audit = normalize(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized = output_dir / 'normalized.jsonl'
    normalized.write_text(''.join(json.dumps({'user': user, 'friends': sorted(graph[user])},
                          ensure_ascii=False) + '\n' for user in sorted(graph)), encoding='utf-8')
    (output_dir / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2),
                                          encoding='utf-8')
    source = normalized
    for stage, mapper, reducer in [(1, 'mapper_pairs.py', 'reducer_pairs.py'),
                                   (2, 'mapper_rank.py', 'reducer_rank.py')]:
        mapped = output_dir / f'map_{stage}.txt'
        sorted_file = output_dir / f'shuffle_{stage}.txt'
        reduced = output_dir / ('pair_scores.txt' if stage == 1 else 'recommendations.jsonl')
        run_script(mapper, source, mapped)
        shuffle(mapped, sorted_file)
        run_script(reducer, sorted_file, reduced,
                   *(['--top-k', str(top_k)] if stage == 2 else []))
        source = reduced
    return [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=ROOT / 'data' / 'sample.jsonl')
    parser.add_argument('--output', type=Path, default=ROOT / 'results')
    parser.add_argument('--top-k', type=int, default=2)
    args = parser.parse_args()
    try:
        result = run(args.input, args.output, args.top_k)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Lỗi: {exc}\n')
    for row in result:
        names = ', '.join(f"{r['candidate']} ({r['score']})" for r in row['recommendations'])
        print(f"{row['user']}: {names or '(không có gợi ý)'}")
