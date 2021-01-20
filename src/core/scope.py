#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re

class Scope(object):
    def __init__(
            self, parent: 'Scope'
    ):
        from src.core.macro import Macro
        from src.core.property import Property
        from src.core.selector import Selector
        from src.core.variable.var import Var

        self.parent = parent  # type: Scope

        self.vars       = []  # type: list[Var]
        self.macros     = []  # type: list[Macro]
        self.selectors  = []  # type: list[Selector]
        self.properties = []  # type: list[Property]
        self.scopes     = []  # type: list[Scope]

    def deal_line(self, line, line_num):
        from src.core.macro import Macro
        from src.core.property import Property
        from src.core.selector import Selector
        from src.core.variable.var import Var

        selector = Selector.compile(self, line)
        if selector is not None:
            self.selectors.append(selector)

        re_property = r'(.*):\s*(\S[\s|\S]*)'
        _property = re.match(re_property, line)
        if _property is not None:
            name = _property.group(1)
            val = _property.group(2)
            if name[0] == '$':
                name = name[1:]
                self.vars.append(
                    Var.compile_var(self, name, val)
                )
            else:
                self.properties.append(
                    Property(self, name, val)
                )

    def divideScope(
            self
            , buffer: str
    ):
        buffer_lines = buffer.split('\n')
        scope_indent = -1

        child_scope = None
        child_scope_buffer = ''
        child_scope_indent = -1

        for line_num in range(len(buffer_lines)):
            buffer_line = buffer_lines[
                line_num
            ]
            indent = 0
            for ch in buffer_line:
                if ch == ' ':
                    indent += 1
                else:
                    break
            if indent == len(buffer_line): continue

            if scope_indent == -1:
                scope_indent = indent

            if indent > scope_indent:
                if child_scope is None:
                    child_scope = Scope(self)
                    child_scope_indent = indent
                else:
                    if scope_indent < indent < child_scope_indent:
                        raise IndentationError(
                            'Improper indentation.\n' + f'{line_num}: {buffer_line}'
                        )
                child_scope_buffer += buffer_line[child_scope_indent:] + '\n'
            elif indent == scope_indent:
                if child_scope is not None:
                    child_scope.deal_buffer(
                        child_scope_buffer
                    )
                    self.scopes.append(child_scope)
                    child_scope = None
                    child_scope_indent = -1
                    child_scope_buffer = ''
                self.deal_line(
                    buffer_line[indent:], line_num
                )

        if child_scope is not None:
            child_scope.deal_buffer(
                child_scope_buffer
            )
            self.scopes.append(child_scope)

    def deal_buffer(self, buffer: str):
        self.divideScope(buffer)

    def getVar(self, varName):
        for var in self.vars:
            if var.name == varName:
                return var
        if self.parent is not None:
            return self.parent.getVar(varName)

        raise ValueError(f'Variable \'{varName}\' does not exist.')

    @property
    def root(self):
        if self.parent is not None:
            return self
        return self.parent.root

    @property
    def deep(self):
        if self.parent is None:
            return 0
        return self.parent.deep + 1

    def obj(self):
        return {
            'deep':       self.deep,
            'vars':       [var.obj() for var in self.vars],
            'macros':     self.macros,
            'selectors':  [selector.obj() for selector in self.selectors],
            'properties': [_property.obj() for _property in self.properties],
            'scopes':     [scope.obj() for scope in self.scopes]
        }

    def __repr__(self):
        return json.dumps(
            self.obj(), indent=2
        )

    def __str__(self):
        return ''
