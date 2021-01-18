#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum

from src.core.morpheme import Morpheme
from src.core.scope import Scope

class PseudoClassType(Enum):
    ACTIVE = ':active'
    ADJOINS_ITEM = ':adjoins-item'
    ALTERNATE = ':alternate'
    BOTTOM = ':bottom'
    CHECKED = ':checked'
    CLOSABLE = ':closable'
    CLOSED = ':closed'
    DEFAULT = ':default'
    DISABLED = ':disabled'
    EDITABLE = ':editable'
    EDIT_FOCUS = ':edit-focus'
    ENABLED = ':enabled'
    EXCLUSIVE = ':exclusive'
    FIRST = ':first'
    FLAT = ':flat'
    FLOATABLE = ':floatable'
    FOCUS = ':focus'
    HAS_CHILDREN = ':has-children'
    HAS_SIBLINGS = ':has-siblings'
    HORIZONTAL = ':horizontal'
    HOVER = ':hover'
    INDETERMINATE = ':indeterminate'
    LAST = ':last'
    LEFT = ':left'
    MAXIMIZED = ':maximized'
    MIDDLE = ':middle'
    MINIMIZED = ':minimized'
    MOVABLE = ':movable'
    NO_FRAME = ':no-frame'
    NON_EXCLUSIVE = ':non-exclusive'
    OFF = ':off'
    ON = ':on'
    ONLY_ONE = ':only-one'
    OPEN = ':open'
    NEXT_SELECTED = ':next-selected'
    PRESSED = ':pressed'
    PREVIOUS_SELECTED = ':previous-selected'
    READ_ONLY = ':read-only'
    RIGHT = ':right'
    SELECTED = ':selected'
    TOP = ':top'
    UNCHECKED = ':unchecked'
    VERTICAL = ':vertical'
    WINDOW = ':window'

    @staticmethod
    def indexOf(pseudoClassName):
        for item in PseudoClassType:
            if item.value[1:] == pseudoClassName:
                return item
        return None

class PseudoClass(Morpheme):
    def __init__(
            self
            , scope: Scope
            , _type:  PseudoClassType
            , is_not: bool = False
    ):
        super().__init__(scope)
        self.type = _type
        self.is_not = is_not

    def obj(self):
        return {
            'type': self.type.value,
            'is_not': self.is_not
        }
