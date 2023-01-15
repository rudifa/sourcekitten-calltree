#! python

import unittest
from sourcekitten_calltree import walker, VisitorFuncDecl, VisitorExprCall, VisitorFuncDeclAndCall
from sourcekitten_calltree import print_list, read_json_file


class Testing(unittest.TestCase):

    def test_VisitorFuncDecl(self):
        node = {
            "key.kind": "source.lang.swift.decl.function.method.instance",
            "key.name": "updateSelected()"
        }

        visitor = VisitorFuncDecl()
        visitor.process(node)
        self.assertEqual(visitor.method_names, [
            "updateSelected()"])
        visitor.process(node)
        self.assertEqual(visitor.method_names, [
            "updateSelected()",
            "updateSelected()"])

    def test_walker_decl(self):
        top_node = read_json_file("sample-script.json")
        visitor = VisitorFuncDecl()
        walker(top_node, visitor)
        self.assertEqual(visitor.method_names, ['fibonacci(_:)'])

    def test_walker_call(self):
        top_node = read_json_file("sample-script.json")
        visitor = VisitorExprCall()
        walker(top_node, visitor)
        self.assertEqual(visitor.method_names, [
                         'fibonacci', 'fibonacci', 'CommandLine.arguments', 'Int', 'print', 'fibonacci', 'print', 'print'])

    def test_walker_funcs_and_calls(self):
        top_node = read_json_file("sample-script.json")
        visitor = VisitorFuncDeclAndCall()
        walker(top_node, visitor)
        # print(visitor.funcs_and_calls)
        self.assertEqual(visitor.funcs_and_calls, {'fibonacci': [
                         'fibonacci', 'fibonacci', 'CommandLine.arguments', 'Int', 'print', 'fibonacci', 'print', 'print']})


if __name__ == '__main__':
    unittest.main()
