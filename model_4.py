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


# def walk_json(json_obj, visitor):
#     if 'n' in json_obj:
#         visitor.visit(json_obj['n'])
#     if 's' in json_obj:
#         if isinstance(json_obj['s'], list):
#             for item in json_obj['s']:
#                 walk_json(item, visitor)
#         elif isinstance(json_obj['s'], dict):
#             walk_json(json_obj['s'], visitor)


# def walk_json(json_obj, visitor):
#     if 'n' in json_obj:
#         visitor.visit(json_obj['n'])
#     if 's' in json_obj:
#         if isinstance(json_obj['s'], list):
#             for item in json_obj['s']:
#                 new_visitor = Visitor()
#                 new_visitor.stack = visitor.stack.copy()
#                 walk_json(item, new_visitor)
#         elif isinstance(json_obj['s'], dict):
#             new_visitor = Visitor()
#             new_visitor.stack = visitor.stack.copy()
#             walk_json(json_obj['s'], new_visitor)

def walk_json(json_obj, visitor):
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


data = json.loads(
    '{"n":"A","s":[{"n":"B","s":{"n":"C"}},{"n":"D","s":{"n":"E"}}]}')

print(json.dumps(data, indent=2))

visitor = Visitor()
walk_json(data, visitor)
