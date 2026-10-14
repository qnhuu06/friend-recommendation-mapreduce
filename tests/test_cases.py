import json
from pathlib import Path
import random
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run_local import run


class RecommendationTests(unittest.TestCase):
    def execute(self, graph):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.jsonl'
            path.write_text(''.join(json.dumps({'user': u, 'friends': f}) + '\n'
                                    for u, f in graph.items()), encoding='utf-8')
            return {r['user']: [(v['candidate'], v['score']) for v in r['recommendations']]
                    for r in run(path, Path(directory) / 'results')}

    def test_sample(self):
        rows = [json.loads(line) for line in (ROOT / 'data/sample.jsonl').read_text().splitlines()]
        actual = self.execute({r['user']: r['friends'] for r in rows})
        self.assertEqual(actual, {'Alice': [('Dan', 1), ('Eve', 1)],
            'Bob': [('Eve', 2), ('Frank', 1)], 'Carol': [('Dan', 2)],
            'Dan': [('Carol', 2), ('Alice', 1)], 'Eve': [('Bob', 2), ('Alice', 1)],
            'Frank': [('Bob', 1), ('Eve', 1)]})

    def test_isolated(self):
        self.assertEqual(self.execute({'A': []}), {'A': []})

    def test_duplicates_and_self(self):
        self.assertEqual(self.execute({'A': ['B', 'B', 'A'], 'B': ['A', 'C'], 'C': ['B']}),
                         {'A': [('C', 1)], 'B': [], 'C': [('A', 1)]})

    def test_asymmetric(self):
        self.assertEqual(self.execute({'A': ['B'], 'B': ['C']}),
                         {'A': [('C', 1)], 'B': [], 'C': [('A', 1)]})

    def test_complete_graph(self):
        self.assertEqual(self.execute({'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}),
                         {'A': [], 'B': [], 'C': []})

    def test_tie_and_top_two(self):
        result = self.execute({'X': ['C', 'A', 'B', 'D']})
        self.assertEqual(result['D'], [('A', 1), ('B', 1)])

    def test_random_against_independent_reference(self):
        randomizer = random.Random(42)
        for _ in range(12):
            names = list('ABCDEFGH')
            graph = {u: set() for u in names}
            for i, u in enumerate(names):
                for v in names[i + 1:]:
                    if randomizer.random() < .3:
                        graph[u].add(v)
                        graph[v].add(u)
            expected = {}
            for u in names:
                candidates = [(v, len(graph[u] & graph[v])) for v in names
                              if v != u and v not in graph[u] and graph[u] & graph[v]]
                expected[u] = sorted(candidates, key=lambda row: (-row[1], row[0]))[:2]
            self.assertEqual(self.execute({u: sorted(f) for u, f in graph.items()}), expected)

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.jsonl'
            path.write_text('{"user":"A","friends":"B"}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Dòng 1'):
                run(path, Path(directory) / 'results')


if __name__ == '__main__':
    unittest.main()
