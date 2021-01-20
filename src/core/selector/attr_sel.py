#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src.core.morpheme import Morpheme
from src.core.scope import Scope
from src.core.variable.var import Var


class AttrSel(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str
            , val:   Var
    ):
        super().__init__(scope)

    def __str__(self):
        return ''

    def obj(self):
        return {}

    @staticmethod
    def compile(
            scope: Scope, attr_sel_str: str
    ):
        print(attr_sel_str)
