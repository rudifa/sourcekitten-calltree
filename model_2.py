#! python3

import json


class NodeVisitor:
    def __init__(self):
        self.stack = []

    def visit(self, node, parent_nodes):
        self.stack.append(node)
        print(node, parent_nodes)
        self.stack.pop()


def walk_json(data, visitor):
    if 'n' in data:
        node = data['n']
        parent_nodes = visitor.stack.copy()
        visitor.visit(node, parent_nodes)
    if 's' in data:
        visitor.stack.append(data['n'])
        if isinstance(data['s'], list):
            for item in data['s']:
                walk_json(item, visitor)
        elif isinstance(data['s'], dict):
            walk_json(data['s'], visitor)
        visitor.stack.pop()


json_data = json.loads(
    '{"n":"A","s":[{"n":"B","s":{"n":"C"}},{"n":"D","s":{"n":"E"}}]}')

print(json.dumps(json_data, indent=2))


visitor = NodeVisitor()
walk_json(json_data, visitor)
