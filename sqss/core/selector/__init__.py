#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqss.core.morpheme import Morpheme
from sqss.core.scope import Scope
from sqss.core.selector.rule import Rule

class Selector(Morpheme):
    def __init__(
            self
            , scope: Scope
    ):
        super().__init__(scope)
        self.rules: list[Rule] = []
        self._affiliated_scope: Scope = None

    def rules_str(self):
        return ', '.join([str(rule) for rule in self.rules])

    def __str__(self):
        return f'{self.rules_str()} {{'

    def obj(self):
        return {
            'rules': [rule.obj() for rule in self.rules]
        }

    @property
    def affiliated_scope(self) -> Scope:
        return self._affiliated_scope

    @affiliated_scope.setter
    def affiliated_scope(self, val: Scope):
        val.mount_selector = self
        self._affiliated_scope = val

    @staticmethod
    def compile(
            scope: Scope, line: str
    ) -> 'Selector':
        selector = Selector(scope)
        wait_deal_rules = line.split(',')
        for wait_deal_rule in wait_deal_rules:
            rules = Rule.compile(
                scope, wait_deal_rule + '\n'
            )
            for rule in rules:
                selector.rules.append(rule)

        if len(selector.rules) > 0:
            return selector
        return None
