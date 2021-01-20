#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqss.core.scope import Scope

class Morpheme(object):
    """
    基本词素
    """
    def __init__(self, scope: Scope):
        self.scope = scope  # type: Scope
