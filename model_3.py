#! python3

import json


def walk_json(json_obj, visitor):
    if 'n' in json_obj:
        visitor.visit(json_obj['n'], visitor.stack)
    if 's' in json_obj:
        if isinstance(json_obj['s'], list):
            visitor.stack.append(json_obj['n'])
            for item in json_obj['s']:
                walk_json(item, visitor)
            visitor.stack.pop()
        elif isinstance(json_obj['s'], dict):
            visitor.stack.append(json_obj['n'])
            walk_json(json_obj['s'], visitor)
            visitor.stack.pop()


class Visitor:
    def __init__(self):
        self.stack = []

    def visit(self, n, stack):
        print(f'Visiting node {n} with stack {stack}')


data = json.loads(
    '{"n":"A","s":[{"n":"B","s":{"n":"C"}},{"n":"D","s":{"n":"E"}}]}')

print(json.dumps(data, indent=2))

visitor = Visitor()
walk_json(data, visitor)
