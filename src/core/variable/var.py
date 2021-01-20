#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from src.core.morpheme import Morpheme
from src.core.scope import Scope


class Var(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name: str, val: str
    ):
        super().__init__(scope)
        self.name = name
        self.val = val

    @classmethod
    def compile(
            cls
            , scope: Scope
            , name: str, val: str
    ) -> 'Var':
        from src.core.variable.fun import Fun
        from src.core.variable.num import Num
        from src.core.variable.str import Str

        re_num = r'(-?\d)(.*)'
        re_fun = r'\$(.*)\(.*\)'

        num = re.match(re_num, val)
        if num is not None:
            return Num(scope, name, val)
        fun = re.match(re_fun, val)
        if fun is not None:
            return Fun(scope, name, val)
        return Str(scope, name, val)

    def obj(self):
        return {
            'name': self.name,
            'val': self.val
        }
