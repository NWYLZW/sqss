#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

from sqss.core.macro.abs_macro import AbsMacro
from sqss.core.macro.mixin import Mixin
from sqss.core.scope import Scope

class Include(AbsMacro):
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

    def get_fun_by_name(self, scope, name) -> Mixin:
        for macro in scope.macros:
            if macro.name == 'mixin':
                mixin: Mixin = macro
                if mixin.fun_name == name:
                    return mixin
        if scope.is_root: return None
        return self.get_fun_by_name(scope.parent, name)

    def deal_data(self):
        mixin = self.get_fun_by_name(self.scope, self.fun_name)
        if mixin is None:
            raise FileNotFoundError('Function is not defined.')
        append_items = mixin.mixin_fun(self.arguments)
        for index in range(len(append_items)):
            append_item = append_items[index]
            self.scope.buffer.insert(
                self.scope.deal_line_num + index, ' '*self.scope.indent + append_item
            )
