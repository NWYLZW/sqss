import unittest

from sqss.core.compiler import Compiler
from sqss.core.scope import OutputMode


class TestCompiler(unittest.TestCase):
    def test_compile_marco(self):
        with open('./sqss/compile_marco.sqss', 'r') as f:
            test_strs0 = f.read()
            print(
                Compiler.deal_str(test_strs0)
            )
            print('----------------------')
            print(
                Compiler.deal_str(test_strs0, OutputMode.COMMON)
            )

    def test_simple_base(self):
        test_str = '''\
        $size: 100px
        .main
          w: $size
          h: $size
          > QLabel:!hover
            color: black
          > QLabel:hover
            color: red
        .message
          $height: 40px
          w: $size
          h: $height
          .icon
            $size: 16px
            w: $size
            h: $size
          .label
            w: $size - 16px
            h: $height
        '''
        print(Compiler.deal_str(test_str))
        print(Compiler.deal_str(test_str, OutputMode.COMMON))


if __name__ == '__main__':
    unittest.main()
