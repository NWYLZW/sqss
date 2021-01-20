#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.core.scope import Scope
from src.core.variable.var import Var

class Num(Var):
    def __init__(
            self
            , scope: Scope
            , name: str, val: str
    ):
        super().__init__(scope, name, val)

    def __str__(self):
        return self.val
