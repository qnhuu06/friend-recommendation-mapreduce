"""Chuẩn hóa đồ thị vô hướng; báo cáo các sửa đổi dữ liệu."""
import json


def normalize(path):
    graph = {}
    audit = []
    with open(path, encoding='utf-8-sig') as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                user, friends = row['user'], row['friends']
                if not isinstance(user, str) or not user.strip():
                    raise ValueError('user phải là chuỗi không rỗng')
                if not isinstance(friends, list) or any(
                    not isinstance(f, str) or not f.strip() for f in friends
                ):
                    raise ValueError('friends phải là danh sách tên không rỗng')
                user = user.strip()
                if user in graph:
                    audit.append({'line': number, 'issue': 'duplicate_user', 'user': user})
                target = graph.setdefault(user, set())
                seen = set()
                for name in friends:
                    friend = name.strip()
                    if friend == user:
                        audit.append({'line': number, 'issue': 'self_link', 'user': user})
                    elif friend in seen or friend in target:
                        audit.append({'line': number, 'issue': 'duplicate_friend',
                                      'user': user, 'friend': friend})
                    else:
                        target.add(friend)
                    seen.add(friend)
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f'Dòng {number}: {exc}') from exc
    for user, friends in list(graph.items()):
        for friend in sorted(friends):
            graph.setdefault(friend, set())
    for user in sorted(graph):
        for friend in sorted(graph[user]):
            if user not in graph[friend]:
                graph[friend].add(user)
                audit.append({'issue': 'added_reverse_link', 'user': friend, 'friend': user})
    return graph, audit
