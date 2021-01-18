#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from src.core.morpheme import Morpheme
from src.core.scope import Scope


class AttrSel(Morpheme):
    def __init__(
            self
            , scope: Scope
    ):
        super().__init__(scope)

    def obj(self):
        return {}
