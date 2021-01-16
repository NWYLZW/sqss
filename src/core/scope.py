#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.core.variable.var import Var

class Scope(object):
    def __init__(self):
        self.vars:   list[Var]   = []
        self.scopes: list[Scope] = []
