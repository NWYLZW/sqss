#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope

class SubControl(Morpheme):
    def __init__(
            self
            , scope: Scope
    ):
        super().__init__(scope)

    def __str__(self):
        return ''

    def obj(self):
        return {}

    @staticmethod
    def compile(
            scope: Scope, rules: list['Rule'], pseudo_class_name: str
    ):
        from sqss.core.selector import Rule
