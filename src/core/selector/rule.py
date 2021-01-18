#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

from src.core.morpheme import Morpheme
from src.core.scope import Scope
from src.core.selector.attr_sel import AttrSel
from src.core.selector.pseudo_class import PseudoClass, PseudoClassType
from src.core.selector.sub_control import SubControl

# .main::(sub-control1 | sub-control2):(pseudo-class1 | pseudo-class2)
from src.exception.ValAssignedSetException import ValAssignedSetException


class Rule(Morpheme):
    def __init__(
            self
            , scope: Scope
            , name:  str = ''
    ):
        super().__init__(scope)
        self.name = name

        self.attr_sels      = []  # type: list[AttrSel]
        self.sub_controls   = []  # type: list[SubControl]
        self.pseudo_classes = []  # type: list[PseudoClass]

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
    def compile_rule(
            scope: Scope, rule_str: str
    ) -> list['Rule']:
        rules = [Rule(scope)]
        stack = []

        is_sub = False
        is_pseudo = False
        for index in range(len(rule_str)):
            ch = rule_str[index]

            if ch in ':\n':
                if ch == ':':
                    if index == len(rule_str) - 1:
                        raise ValAssignedSetException()
                    if rule_str[index + 1] == ' ':
                        return []
                    if rule_str[index + 1] == ':':
                        is_sub = True

                if not is_sub:
                    if not is_pseudo:
                        is_pseudo = True
                        rules[0].name = ''.join(stack).strip()
                        stack.clear()
                    else:
                        is_not = False
                        pseudo_class_name = ''.join(stack)[1:]
                        stack.clear()

                        pseudo_class_names = re.match(r'\((.*)\)', pseudo_class_name)
                        if pseudo_class_names is not None:
                            pseudo_class_names = pseudo_class_names.group(1).split('|')
                        else:
                            pseudo_class_names = [pseudo_class_name]

                        for pseudo_class_name in pseudo_class_names:
                            if pseudo_class_name[0] == '!':
                                is_not = True
                                pseudo_class_name = pseudo_class_name[1:]

                            _type = PseudoClassType.indexOf(pseudo_class_name)
                            if _type is None: return []
                            for rule in rules:
                                rule.pseudo_classes.append(
                                    PseudoClass(scope, _type, is_not)
                                )

            stack.append(ch)
        return rules
