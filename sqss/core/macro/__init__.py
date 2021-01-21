#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope

class Macro(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str, args:  str
    ):
        super().__init__(scope)
        self.name = name

    @staticmethod
    def compile(
            scope: Scope, text: str
    ) -> 'Macro':
        if text[0] != '@': return None
        macro = re.match(r'@(.+)\ ([\s|\S]+)', text)
        if macro is None: return None
        name = macro.group(1)
        args = macro.group(2)
        return Macro(
            scope, name, args
        )
