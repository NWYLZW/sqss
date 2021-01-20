#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope
from sqss.core.variable.str import Str


class Property(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name: str, val: str
    ):
        super().__init__(scope)
        self.name = name
        re_fun = r'^\$(\S*)$'
        if re.match(re_fun, val) is not None:
            self.var = scope.get_var(val[1:])
        else:
            self.var = Str(scope, '', val)

    def __str__(self):
        return f'{self.name}: {str(self.var)};'

    def obj(self):
        return {
            'name': self.name,
            'var':  self.var.obj()
        }
