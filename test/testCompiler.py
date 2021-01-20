import unittest

from sqss.core.compiler import Compiler
from sqss.core.scope import OutputMode


class TestCompiler(unittest.TestCase):
    def test_something(self):
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
