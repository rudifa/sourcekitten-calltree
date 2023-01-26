#! python

import unittest
from sourcekitten_calltree import walker, VisitorFuncDeclAndCall
from sourcekitten_calltree import print_list, read_json_file


class Testing(unittest.TestCase):

    def test_walker_funcs_and_calls(self):
        top_node = read_json_file("sample_script_0.json")
        visitor = VisitorFuncDeclAndCall()
        walker(top_node, visitor)
        # print(visitor.funcs_and_calls)
        self.assertEqual(visitor.funcs_and_calls,  {'fibonacci': {
                         'fibonacci'}, 'test_fibonacci': {'fibonacci', 'print'}})

    def test_walker_funcs_and_calls_exclude(self):
        top_node = read_json_file("sample_script_0.json")
        exclude_list = ["print"]
        visitor = VisitorFuncDeclAndCall(exclude_list)
        walker(top_node, visitor)
        # print(visitor.funcs_and_calls)
        self.assertEqual(visitor.funcs_and_calls, {'fibonacci': {
                         'fibonacci'}, 'test_fibonacci': {'fibonacci'}})

    def test_walker_funcs_and_calls_1(self):
        top_node = read_json_file("sample_script_1.json")
        # exclude_list = ["print"]
        visitor = VisitorFuncDeclAndCall()
        walker(top_node, visitor)
        # print(visitor.funcs_and_calls)
        self.assertEqual(visitor.funcs_and_calls,  {'aaa': {'ccc', 'bbb', 'print'}, 'bbb': {
                         'print'}, 'ccc': {'print', 'ddd'}, 'ddd': {'print'}})


if __name__ == '__main__':
    unittest.main()
