#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from enum import Enum

from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope

class PseudoClassType(Enum):
    ACTIVE = 'active'
    ADJOINS_ITEM = 'adjoins-item'
    ALTERNATE = 'alternate'
    BOTTOM = 'bottom'
    CHECKED = 'checked'
    CLOSABLE = 'closable'
    CLOSED = 'closed'
    DEFAULT = 'default'
    DISABLED = 'disabled'
    EDITABLE = 'editable'
    EDIT_FOCUS = 'edit-focus'
    ENABLED = 'enabled'
    EXCLUSIVE = 'exclusive'
    FIRST = 'first'
    FLAT = 'flat'
    FLOATABLE = 'floatable'
    FOCUS = 'focus'
    HAS_CHILDREN = 'has-children'
    HAS_SIBLINGS = 'has-siblings'
    HORIZONTAL = 'horizontal'
    HOVER = 'hover'
    INDETERMINATE = 'indeterminate'
    LAST = 'last'
    LEFT = 'left'
    MAXIMIZED = 'maximized'
    MIDDLE = 'middle'
    MINIMIZED = 'minimized'
    MOVABLE = 'movable'
    NO_FRAME = 'no-frame'
    NON_EXCLUSIVE = 'non-exclusive'
    OFF = 'off'
    ON = 'on'
    ONLY_ONE = 'only-one'
    OPEN = 'open'
    NEXT_SELECTED = 'next-selected'
    PRESSED = 'pressed'
    PREVIOUS_SELECTED = 'previous-selected'
    READ_ONLY = 'read-only'
    RIGHT = 'right'
    SELECTED = 'selected'
    TOP = 'top'
    UNCHECKED = 'unchecked'
    VERTICAL = 'vertical'
    WINDOW = 'window'

    @staticmethod
    def indexOf(pseudoClassName):
        for item in PseudoClassType:
            if item.value == pseudoClassName:
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

    def __str__(self):
        return f":{('!' if self.is_not else '')}{self.type.value}"

    def obj(self):
        return {
            'type': self.type.value,
            'is_not': self.is_not
        }

    @staticmethod
    def compile(
            scope: Scope, rules: list['Rule'], pseudo_class_name: str
    ):
        from sqss.core.selector import Rule
        pseudo_class_name = pseudo_class_name[1:]
        is_not = False
        pseudo_class_names = re.match(r'\((.*)\)', pseudo_class_name)
        if pseudo_class_names is not None:
            pseudo_class_names = pseudo_class_names.group(1).split('|')
        else:
            pseudo_class_names = [pseudo_class_name]

        new_rules = []
        for rule in rules:
            new_rules = Rule.cp_rule(rule, len(pseudo_class_names) - len(rules))

        for i in range(len(pseudo_class_names)):
            pseudo_class_name = pseudo_class_names[i]

            if pseudo_class_name[0] == '!':
                is_not = True
                pseudo_class_name = pseudo_class_name[1:]

            _type = PseudoClassType.indexOf(pseudo_class_name)
            if _type is None: return []

            if i < len(rules):
                if len(pseudo_class_names) == 1:
                    for rule in rules:
                        rule.append(
                            PseudoClass(scope, _type, is_not)
                        )
                else:
                    rules[i].append(
                        PseudoClass(scope, _type, is_not)
                    )
            else:
                new_rules[i - len(rules)].append(
                    PseudoClass(scope, _type, is_not)
                )
        if new_rules:
            rules.append(*new_rules)
