#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope
from sqss.core.variable.var import Var

class AttrSel(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str
            , val:   Var
    ):
        super().__init__(scope)
        self.name = name  # type: str
        self.val  = val   # type: Var

    def __str__(self):
        return f'[{self.name}={str(self.val)}]'

    def obj(self):
        return {
            'name': self.name,
            'val': str(self.val)
        }

    @staticmethod
    def compile(
            scope: Scope, rules: list['Rule'], attr_sel_str: str
    ):
        attr_sel = re.match(r'\[(.*)=([\s|\S]*)\]', attr_sel_str)
        name  = attr_sel.group(1)
        value = attr_sel.group(2)

        for rule in rules:
            rule.append(
                AttrSel(scope, name, Var.compile(scope, '', value))
            )
