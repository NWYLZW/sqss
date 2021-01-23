import json
import unittest

from sqss.core.compiler import Compiler
from sqss.core.scope import OutputMode


class TestCompiler(unittest.TestCase):
    def test_compile_marco0(self):
        test_strs0 = '''\
        @mixin fun($arg1, $arg2)
          #{$arg1}
            color: #{$arg2}
        .main
          @include fun(test1, #fff)
          @include fun(test2, #fff)
        '''
        print(Compiler.deal_str(test_strs0))

    def test_compile_marco1(self):
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
        # print(json.dumps(
        #     Compiler.deal_str(test_str).obj(), indent=4
        # ))
        print(Compiler.deal_str(test_str))
        print(Compiler.deal_str(test_str, OutputMode.COMMON))


if __name__ == '__main__':
    unittest.main()
