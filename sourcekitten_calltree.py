#! python3

#

import json
import sys
import re
import argparse
from graphviz import Digraph

# helpers


def print_list(list):
    for item in list:
        print(item)


def read_file_to_string(file_path):
    with open(file_path, "r") as file:
        return file.read()


def read_json_file(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)


def drop_suffix_regex(string, pattern):
    return re.sub(pattern + "$", "", string)


def drop_suffix_parens(string):
    return re.sub("\(.*\)$", "", string)

# def walker(node, visitor):
#     if isinstance(node, dict):
#         for key, value in node.items():
#             walker(value, visitor)
#     elif isinstance(node, list):
#         for item in node:
#             walker(item, visitor)
#     return node


# visitors

# function or property call
# "key.kind" : "source.lang.swift.expr.call",

# function declaration
# "key.kind": "source.lang.swift.decl.function.method.instance",

class VisitorFuncDecl:
    """ Recognizes function method declarations in visited nodes.
        Collects their names in a list."""

    def __init__(self):
        self.method_names = []

    def process(self, node):
        if isinstance(node, dict):
            try:
                if node["key.kind"] == "source.lang.swift.decl.function.method.instance" or node["key.kind"] == "source.lang.swift.decl.function.free":
                    self.method_names.append(node["key.name"])
            except KeyError:
                pass


class VisitorExprCall:
    """ Recognizes function call in visited nodes.
        Collects their names in a list."""

    def __init__(self):
        self.method_names = []

    def process(self, node):
        if isinstance(node, dict):
            try:
                if node["key.kind"] == "source.lang.swift.expr.call":
                    self.method_names.append(node["key.name"])
            except KeyError:
                pass


class VisitorFuncDeclAndCall:
    """ Recognizes function method declarations in visited nodes.
        Collects their names in a list.
        Recognizes function method calls in visited nodes."""

    def __init__(self, exclusion_list=[]):
        self.funcs_and_calls = {}  # dict where key: method name, value: set of callee names
        self.latest_func_name = ""
        self.exclusion_list = exclusion_list

    def process(self, node):
        if isinstance(node, dict):
            try:
                if node["key.kind"] in ["source.lang.swift.decl.function.method.instance", "source.lang.swift.decl.function.free"]:
                    func_name = drop_suffix_parens(node["key.name"])
                    self.latest_func_name = func_name
                    self.funcs_and_calls.update({func_name: set()})
                elif node["key.kind"] == "source.lang.swift.expr.call":
                    if "key.name" in node:
                        called_func_name = node["key.name"]
                        if called_func_name not in self.exclusion_list:
                            self.funcs_and_calls[self.latest_func_name].add(
                                called_func_name)
            except KeyError:
                #print("KeyError:", node)
                pass

    def json_compatible_result(self):
        """Converts the set of callees to a list for JSON serialization."""
        return {k: list(v) for k, v in self.funcs_and_calls.items()}


# walker


def walker(node, visitor):
    #print("walker:", node)
    if isinstance(node, dict):
        visitor.process(node)
        for key, value in node.items():
            walker(value, visitor)
    elif isinstance(node, list):
        for item in node:
            walker(item, visitor)
    return node

# plotter


def plotter(funcs_and_calls):
    dot = Digraph(comment='')
    dot.attr("graph", ratio="0.2")
    dot.attr(size='20,12')

    for func_name, called_funcs in funcs_and_calls.items():
        dot.node(func_name, func_name, rank='source')
        for called_func in called_funcs:
            dot.edge(func_name, called_func)
    dot.render('graphviz-output/calltree.gv', view=True)

# runners


def run_visitor_func_decl(top_node):
    visitor_decl = VisitorFuncDecl()
    walker(top_node, visitor_decl)
    print("visitor_decl:", visitor_decl.method_names)


def run_visitor_expr_call(top_node):
    visitor_call = VisitorExprCall()
    walker(top_node, visitor_call)
    print("visitor_call:", visitor_call.method_names)


def run_visitor_func_decl_and_call(top_node):
    exclusion_list = ["printClassAndFunc",
                      "self.printClassAndFunc", "print", "String"]
    visitor = VisitorFuncDeclAndCall(exclusion_list)
    walker(top_node, visitor)
    # print("visitor:", visitor.funcs_and_calls)
    json_str = json.dumps(visitor.json_compatible_result(), indent=4)
    print(json_str)
    plotter(visitor.funcs_and_calls)


def main(top_node):
    # try:
    #     top_node = json.loads(sys.stdin.read())
    # except json.JSONDecodeError as e:
    #     print(f'Error parsing JSON: {e}')
    #     return

    # Parse the JSON output of the sourcekitten structure command like
    # sourcekitten structure --file shAre/Controller/PrincipalViewController.swift  >  docs/PrincipalViewController.json

    # usage:
    # cat PrincipalViewController.json | sourcekitten-calltree2.py

    # run_visitor_func_decl(top_node)

    # run_visitor_expr_call(top_node)

    run_visitor_func_decl_and_call(top_node)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('file', type=str, help='the file to be processed')

    args = parser.parse_args()

    print(f'Processing file: {args.file}')

    top_node = read_json_file(args.file)

    main(top_node)
