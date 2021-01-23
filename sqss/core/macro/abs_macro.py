#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope

class AbsMacro(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str, args:  str
    ):
        super().__init__(scope)
        self.name = name    # type: str
        self.args = args    # type: str
        self.children = []  # type: list[str]

    def deal_data(self):
        pass

    def append_child(self, child):
        self.children.append(child)

    def obj(self):
        return {
            'name': self.name,
            'children': self.children
        }
