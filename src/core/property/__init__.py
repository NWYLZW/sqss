#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from src.core.morpheme import Morpheme
from src.core.scope import Scope
from src.core.variable.str import Str


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
            self.var = scope.getVar(val[1:])
        else:
            self.var = Str(scope, '', val)

    def obj(self):
        return {
            'name': self.name,
            'var':  self.var.obj()
        }
