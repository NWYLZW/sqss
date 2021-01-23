import json
import unittest

from sqss.core.compiler import Compiler
from sqss.core.scope import Scope, OutputMode
from sqss.core.selector import Selector


class TestSelector(unittest.TestCase):
    def test_selector_attr_sel_and_pseudo_class(self):
        test_strs = {
            '.btn[type=\'primary\']:hover:!hover': {
                "rules": [{
                    'name': '.btn',
                    "attr_sels": [{
                        'name': 'type', 'val': '\'primary\''
                    }],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": False
                    }, {
                        "type": "hover",
                        "is_not": True
                    }]
                }]
            },
            '.btn[plain=true][type=\'primary\']:(hover|!hover)': {
                "rules": [{
                    'name': '.btn',
                    "attr_sels": [{
                        'name': 'plain', 'val': 'true'
                    }, {
                        'name': 'type', 'val': '\'primary\''
                    }],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": False
                    }]
                }, {
                    'name': '.btn',
                    "attr_sels": [{
                        'name': 'plain', 'val': 'true'
                    }, {
                        'name': 'type', 'val': '\'primary\''
                    }],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": True
                    }]
                }]
            }
        }
        for test_str, val in test_strs.items():
            selector = Selector.compile(
                Scope(None), test_str
            )
            print(f"'{test_str}'", ' -> ', f"'{selector}'")
            if selector is not None:
                # print(
                #     json.dumps(selector.obj(), indent=2)
                # )
                self.assertEqual(
                    selector.obj(), val
                )

    def test_selector_attr_sel(self):
        test_strs = {
            '.btn[type=\'primary\']': {
                "rules": [{
                    'name': '.btn',
                    "attr_sels": [{
                        'name': 'type', 'val': '\'primary\''
                    }],
                    "sub_control": [],
                    "pseudo_classes": []
                }]
            },
            '.btn[plain=true][type=\'primary\']': {
                "rules": [{
                    'name': '.btn',
                    "attr_sels": [{
                        'name': 'plain', 'val': 'true'
                    }, {
                        'name': 'type', 'val': '\'primary\''
                    }],
                    "sub_control": [],
                    "pseudo_classes": []
                }]
            }
        }
        for test_str, val in test_strs.items():
            selector = Selector.compile(
                Scope(None), test_str
            )
            print(f"'{test_str}'", ' -> ', f"'{selector}'")
            if selector is not None:
                # print(
                #     json.dumps(selector.obj(), indent=2)
                # )
                self.assertEqual(
                    selector.obj(), val
                )

    def test_selector_pseudo_class(self):
        test_strs = {
            '.mai1_n:hover': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": False
                    }]
                }]
            },
            '> .mai1_n:hover': {
                "rules": [{
                    'name': '> .mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
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
                        "type": "hover",
                        "is_not": False
                    }]
                }, {
                    'name': 'mai3_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": False
                    }]
                }]
            },
            '.mai1_n:(hover|!hover):open': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": False
                    }, {
                        "type": "open",
                        "is_not": False
                    }]
                }, {
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
                        "is_not": True
                    }, {
                        "type": "open",
                        "is_not": False
                    }]
                }]
            },
            '.mai1_n:!hover': {
                "rules": [{
                    'name': '.mai1_n',
                    "attr_sels": [],
                    "sub_control": [],
                    "pseudo_classes": [{
                        "type": "hover",
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
                        "type": "hover",
                        "is_not": False
                    }, {
                        "type": "open",
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
                        "type": "hover",
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
                        "type": "hover",
                        "is_not": False
                    }]
                }]
            }
        }
        for test_str, val in test_strs.items():
            selector = Selector.compile(
                Scope(None), test_str
            )
            print(f"'{test_str}'", ' -> ', f"'{selector}'")
            if selector is not None:
                # print(
                #     json.dumps(selector.obj(), indent=2)
                # )
                self.assertEqual(
                    selector.obj(), val
                )

    def test_selector(self):
        test_strs0 = '''\
        .ElePyButton
          margin: 0
          padding: 10px 15px
          border-radius: 4px
          outline: none
          background-color: #fff
          border: 1px solid #dcdfe6

          &[type='primary']
            background-color: #409eff
            border: 1px solid #409eff
            QLabel
              color: #fff

            &[plain=true]
              background-color: #ecf5ff
              QLabel
                color: #409eff

            &[hover=true][disabled=false]
              background-color: #66b1ff
              border: 1px solid #66b1ff
              QLabel
                color: #fff

              &[plain=true]
                background-color: #409eff

          &[type='success']
            background-color: #67c23a
            border: 1px solid #67c23a
            QLabel
              color: #fff

            &[plain=true]
              background-color: #f0f9eb
              QLabel
                color: #67c23a

            &[hover=true][disabled=false]
              background-color: #85ce61
              border: 1px solid #85ce61
              QLabel
                color: #fff

              &[plain=true]
                background-color: #67c23a
        '''
        print(
            Compiler.deal_str(test_strs0)
        )
        print('----------------------')
        print(
            Compiler.deal_str(test_strs0, OutputMode.COMMON)
        )

if __name__ == '__main__':
    unittest.main()
