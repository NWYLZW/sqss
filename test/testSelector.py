import json
import unittest

from src.core.scope import Scope
from src.core.selector import Selector


class TestSelector(unittest.TestCase):
    def test_compile_selector_pseudo_class(self):
        test_strs = {
            '.mai1_n:hover': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }]
            },
            '> .mai1_n:hover, mai3_n:hover': {
                "rules": [{
                    'name': '> .mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }, {
                    'name': 'mai3_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }]
            },
            '.mai1_n:(hover|!hover)': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }, {
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": True
                    }]
                }]
            },
            '.mai1_n:!hover': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": True
                    }]
                }]
            },
            '.mai1_n:hover:open': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }, {
                        "type": ":open",
                        "is_not": False
                    }]
                }]
            },
            'mai1_n:hover': {
                "rules": [{
                    'name': 'mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }]
            },
            '#mai1_n:hover': {
                "rules": [{
                    'name': '#mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": ":hover",
                        "is_not": False
                    }]
                }]
            }
        }
        for test_str, val in test_strs.items():
            selector = Selector.compile_selector(
                Scope(None), test_str
            )
            if selector is not None:
                print(test_str)
                print(
                    json.dumps(selector.obj(), indent=2)
                )
                self.assertEqual(
                    selector.obj(), val
                )

    def test_compile_selector(self):
        test_strs = '''\
.mai1_n:x[asd='']
.m-ai2n::y
.m-ai2n::y:x[asd='']
.mai3-n::(a | b):x[asd='']
.ma_i4n::(a | b):(c | d)[asd='']

mai1_n:x[asd='']
m-ai2n::y
m-ai2n::y:x[asd='']
mai3-n::(a | b):x[asd='']
ma_i4n::(a | b):(c | d)[asd='']

#mai1_n:x[asd='']
#m-ai2n::y
#m-ai2n::y:x[asd='']
#mai3-n::(a | b):x[asd='']
#ma_i4n::(a | b):(c | d)[asd='']'''
        for test_str in test_strs.split('\n'):
            selector = Selector.compile_selector(
                Scope(None), test_str
            )
            if selector is not None:
                print(selector.obj())

if __name__ == '__main__':
    unittest.main()
