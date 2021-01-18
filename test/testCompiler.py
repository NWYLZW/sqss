import unittest

from src.core.compiler import Compiler


class TestCompiler(unittest.TestCase):
    def test_something(self):
        print(Compiler.deal_str('''\
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
        '''))



if __name__ == '__main__':
    unittest.main()
