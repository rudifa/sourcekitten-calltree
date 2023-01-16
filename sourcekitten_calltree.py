#! python3

#

import json
import sys
import os
import re
import argparse
import textwrap
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
                # print("KeyError:", node)
                pass

    def json_compatible_result(self):
        """Converts the set of callees to a list for JSON serialization."""
        return {k: list(v) for k, v in self.funcs_and_calls.items()}


# walker


def walker(node, visitor):
    # print("walker:", node)
    if isinstance(node, dict):
        visitor.process(node)
        for key, value in node.items():
            walker(value, visitor)
    elif isinstance(node, list):
        for item in node:
            walker(item, visitor)
    return node

# plotter


def plotter(funcs_and_calls, basename):
    dot = Digraph(comment='')
    dot.attr("graph", ratio="0.2")
    dot.attr(size='20,12')

    for func_name, called_funcs in funcs_and_calls.items():
        dot.node(func_name, func_name, rank='source')
        for called_func in called_funcs:
            dot.edge(func_name, called_func)
    dot.render(f'graphviz-output/{basename}.calltree.gv', view=True)

# runners


def run_visitor_func_decl(top_node):
    visitor_decl = VisitorFuncDecl()
    walker(top_node, visitor_decl)
    print("visitor_decl:", visitor_decl.method_names)


def run_visitor_expr_call(top_node):
    visitor_call = VisitorExprCall()
    walker(top_node, visitor_call)
    print("visitor_call:", visitor_call.method_names)


def run_visitor_func_decl_and_call(top_node, exclude_list, basename):
    visitor = VisitorFuncDeclAndCall(exclude_list)
    walker(top_node, visitor)
    # print("visitor:", visitor.funcs_and_calls)
    json_str = json.dumps(visitor.json_compatible_result(), indent=4)
    print(json_str)
    plotter(visitor.funcs_and_calls, basename)


def main(args):

    try:
        top_node = read_json_file(args.file)
    except FileNotFoundError:
        print(f"File not found: {args.file}")
        return

    try:
        exclude_list = args.exclude.split(",")
        assert (isinstance(exclude_list, list))
    except AssertionError:
        print(f"Exclude list is malformed: {args.exclude}")
        return

    basename = os.path.basename(args.file)

    run_visitor_func_decl_and_call(top_node, exclude_list, basename)


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Process a file.')
    # parser.add_argument('file', type=str, help='the file to be processed')

    description = 'Process a json file generated by sourcekitten --structure and generate a calltree.'
    epilog = textwrap.dedent('''  
    How to generate a calltree for a Swift file:
    1. Install sourcekitten:
       brew install sourcekitten
    2. Generate a json file with the call tree:
       sourcekitten structure --file <file> > <file>.json
    3. Run this script:
       ./sourcekitten_calltree.py <file>.json
    4. The calltree is generated in graphviz-output/<file>.calltree.gv and opened in Preview.
    5. You can exclude uninteresting functions from the calltree by passing them as a comma-separated list, e.g.:
       ./sourcekitten_calltree.py <file>.json -x print,String,Int
    ''')

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('file', type=str, help='the file to process')
    parser.add_argument('-x', '--exclude', type=str, default='',
                        help='exclude identifiers from the call tree')

    args = parser.parse_args()

    print(f'Processing file: {args.file} {args.exclude}')

    main(args)
