#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

from sqss.core.macro.abs_macro import AbsMacro
from sqss.core.scope import Scope
from sqss.util.string_util import StringUtil


class Mixin(AbsMacro):
    def __init__(
            self
            , scope: Scope
            , name:  str, args:  str
    ):
        super().__init__(scope, name, args)
        def_fun = re.match(r'(\S*)\(([\s|\S]*)\)', args)
        if def_fun is None:
            raise NotImplementedError('Function definition failed.')
        self.fun_name = def_fun.group(1)
        self.arguments = [argument.strip() for argument in def_fun.group(2).split(',')]

    def mixin_fun(self, args):
        offset = -1
        wait_append = []
        for child in self.children:
            line = child
            if offset == -1:
                offset = StringUtil.count_indent(line)
            for i in range(len(self.arguments)):
                argument = self.arguments[i][1:]
                line = re.sub(rf'#{{\${argument}}}', args[i], line)
            wait_append.append(line[offset:])
        return wait_append

    def deal_data(self):
        pass
