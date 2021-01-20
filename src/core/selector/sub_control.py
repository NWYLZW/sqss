#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.core.morpheme import Morpheme
from src.core.scope import Scope


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
