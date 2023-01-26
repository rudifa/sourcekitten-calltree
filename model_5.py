#! python3

import json


class Visitor:
    def __init__(self):
        self.stack = []

    def visit(self, n):
        # self.stack.append(n)
        print(
            f'Visiting node {n["n"]} with self.stack {self.stack}')
        # self.stack.pop()


def walk_json_0(json_obj, visitor):
    if 'n' in json_obj:
        visitor.stack.append(json_obj['n'])
        visitor.visit(json_obj)
    if 's' in json_obj:
        if isinstance(json_obj['s'], list):
            for item in json_obj['s']:
                walk_json(item, visitor)
        elif isinstance(json_obj['s'], dict):
            walk_json(json_obj['s'], visitor)
    if 'n' in json_obj:
        visitor.stack.pop()


def walker(node, visitor, depth=0):
    # print("walker:", node)
    if isinstance(node, dict):
        visitor.process(node, depth)
        for key, value in node.items():
            walker(value, visitor, depth + 1)
    elif isinstance(node, list):
        for item in node:
            walker(item, visitor, depth + 1)
    return node


def walk_json(node, visitor):
    if isinstance(node, dict):
        visitor.stack.append(node['n'])
        visitor.visit(node)
        for key, item in node.items():
            walk_json(item, visitor)
        visitor.stack.pop()
    elif isinstance(node, list):
        for item in node:
            walk_json(item, visitor)


data = json.loads(
    '{"n":"A","s":[{"n":"B","s":{"n":"C"}},{"n":"D","s":{"n":"E"}}]}')

print(json.dumps(data, indent=2))

visitor = Visitor()
walk_json(data, visitor)
