#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class CompileException(BaseException):
    """ Common base class for all exceptions """
    def __init__(self, line_num: int, content: str, msg: str = ''):
        super(CompileException, self).__init__()
        self.message = f'The line produced a compilation error.\n[{line_num}]:{content}\n{msg}'

    def __str__(self):
        return self.message
