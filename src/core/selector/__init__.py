#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.core.morpheme import Morpheme
from src.core.scope import Scope
from src.core.selector.rule import Rule

class Selector(Morpheme):
    def __init__(
            self
            , scope: Scope
    ):
        super().__init__(scope)
        self.rules = []     # type: list[Rule]

    def __str__(self):
        return ', '.join([str(rule) for rule in self.rules])

    def obj(self):
        return {
            'rules': [rule.obj() for rule in self.rules]
        }

    @staticmethod
    def compile_selector(
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
