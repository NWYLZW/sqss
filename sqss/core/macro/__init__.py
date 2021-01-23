#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import ClassVar

from sqss.core.macro.abs_macro import AbsMacro
from sqss.core.scope import Scope

class Macro(AbsMacro):
    def __init__(
            self
            , scope: Scope
            , name:  str, args:  str
    ):
        super().__init__(scope, name, args)

    macros: dict[str, ClassVar] = {}

    @classmethod
    def register(cls, name: str, macro: ClassVar):
        from sqss.core.macro.mixin import Mixin
        Macro.macros[name] = macro

    @classmethod
    def register_all(cls):
        from sqss.core.macro.mixin import Mixin
        cls.register('mixin', Mixin)
        from sqss.core.macro.include import Include
        cls.register('include', Include)

    @classmethod
    def compile(
            cls, scope: Scope, text: str
    ) -> 'Macro':
        cls.register_all()

        if text[0] != '@': return None
        macro = re.match(r'@(\S+) ([\s|\S]+)', text)
        if macro is None: return None
        name = macro.group(1)
        args = macro.group(2)

        macroClass = cls.macros.get(name, None)
        if macroClass is None:
            raise FileNotFoundError('Macro is not defined.')

        return macroClass(
            scope, name, args
        )
