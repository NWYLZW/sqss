#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
from typing import Union

from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope
from sqss.core.selector.attr_sel import AttrSel
from sqss.core.selector.pseudo_class import PseudoClass, PseudoClassType
from sqss.core.selector.sub_control import SubControl

# .main::(sub-control1 | sub-control2):(pseudo-class1 | pseudo-class2)
from sqss.exception.ValAssignedSetException import ValAssignedSetException


class Rule(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str = ''
    ):
        super().__init__(scope)
        self.name = name

        self.parse_orders   = []  # type: list[Union[AttrSel, SubControl, PseudoClass]]
        self.attr_sels      = []  # type: list[AttrSel]
        self.sub_controls   = []  # type: list[SubControl]
        self.pseudo_classes = []  # type: list[PseudoClass]

    def append(self, item: Union[AttrSel, SubControl, PseudoClass]):
        if isinstance(item, AttrSel):
            self.attr_sels.append(item)
        elif isinstance(item, SubControl):
            self.sub_controls.append(item)
        elif isinstance(item, PseudoClass):
            self.pseudo_classes.append(item)
        self.parse_orders.append(item)

    def __str__(self):
        name = self.name
        if self.scope.parent is not None:
            parent_rule = self.scope.mount_selector.rules_str()
            if self.name.find('&') == -1:
                name = f'{parent_rule} {name}'
            else:
                name = self.name.replace(
                    '&', parent_rule
                )
        return f"{name}{''.join([str(parse_order) for parse_order in self.parse_orders])}"

    def obj(self):
        return {
            'name': self.name,

            'attr_sels':
                [attr_sel.obj() for attr_sel in self.attr_sels],
            'sub_control':
                [sub_control.obj() for sub_control in self.sub_controls],
            'pseudo_classes':
                [pseudo_class.obj() for pseudo_class in self.pseudo_classes]
        }

    @staticmethod
    def cp_rule(r: 'Rule', num: int = 1) -> list['Rule']:
        temp = []
        for i in range(num):
            cp_r = Rule(r.scope, r.name)
            for parse_order in r.parse_orders:
                cp_r.parse_orders.append(parse_order)
            for attr_sel in r.attr_sels:
                cp_r.attr_sels.append(attr_sel)
            for sub_control in r.sub_controls:
                cp_r.sub_controls.append(sub_control)
            for pseudo_class in r.pseudo_classes:
                cp_r.pseudo_classes.append(pseudo_class)
            temp.append(cp_r)
        return temp

    @staticmethod
    def compile(
            scope: Scope, rule_str: str
    ) -> list['Rule']:
        r = Rule(scope)
        rules = []

        is_name = True
        is_attr = False
        is_sub = False
        is_pseudo = False

        name = ''

        for index in range(len(rule_str)):
            ch = rule_str[index]

            if ch in '[:\n':
                if is_name:
                    is_name = False
                    r.name = name.strip()
                    rules.append(r)
                else:
                    if is_pseudo:
                        PseudoClass.compile(scope, rules, pseudo_class_name)
                    else:
                        if is_attr:
                            AttrSel.compile(scope, rules, attr)

                if ch == ':':
                    pseudo_class_name = ''
                    is_pseudo = True
                    if index == len(rule_str) - 1:
                        raise ValAssignedSetException()
                    if rule_str[index + 1] == ' ':
                        return []
                    if rule_str[index + 1] == ':':
                        is_sub = True
                        is_pseudo = False
                if ch == '[':
                    attr = ''
                    is_attr = True

            if is_name:
                name += ch
            if is_pseudo:
                pseudo_class_name += ch
            if is_attr:
                attr += ch

        return rules
