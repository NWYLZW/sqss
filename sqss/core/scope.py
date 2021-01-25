#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re
from enum import Enum
from typing import Callable, Any

from sqss.exception.CompileException import CompileException
from sqss.util.string_util import StringUtil


class OutputMode(Enum):
    DEFAULT = {
        'isDeep': True,
        'indentSize': 2,
        'braceBr': False
    }
    COMMON = {
        'isDeep': False,
        'indentSize': 4,
        'braceBr': True
    }

class Scope:
    outputMode: OutputMode = OutputMode.DEFAULT

    def __init__(
            self, parent: 'Scope', offset: int = 0
    ):
        from sqss.core.macro import Macro
        from sqss.core.property import Property
        from sqss.core.selector import Selector
        from sqss.core.variable.var import Var

        self.status         = 'init'  # type: str
        self.offset         = offset  # type: int
        self.indent         = -1      # type: int
        self.deal_line_num  = 0       # type: int
        self.__buffer       = []      # type: list[str]
        self.parent         = parent  # type: Scope

        self.cur_child      = None    # type: Scope
        self.mount_selector = None    # type: Selector

        self.vars       = []  # type: list[Var]
        self.macros     = []  # type: list[Macro]
        self.selectors  = []  # type: list[Selector]
        self.properties = []  # type: list[Property]
        self.scopes     = []  # type: list[Scope]

    def obj(self):
        return {
            'deep':       self.deep,
            'vars':       [var.obj() for var in self.vars],
            'macros':     [macro.obj() for macro in self.macros],
            'selectors':  [selector.obj() for selector in self.selectors],
            'properties': [_property.obj() for _property in self.properties],
            'scopes':     [scope.obj() for scope in self.scopes]
        }

    def __repr__(self):
        return json.dumps(
            self.obj(), indent=2
        )

    def content_lines(self) -> list:
        lines = []

        mode = Scope.outputMode.value
        indent = (self.deep if mode['isDeep'] else 0) * mode['indentSize'] * ' '

        for index in range(len(self.properties)):
            _property = self.properties[index]
            need_brace = index == len(self.properties) - 1 and not self.is_root
            end = '}' if need_brace and not mode['braceBr'] else ''
            temp_indent = indent
            if not mode['isDeep']:
                temp_indent = mode['indentSize'] * ' '
            lines.append(f"{temp_indent}{_property}{end}")
            if mode['braceBr'] and need_brace:
                lines.append("}")
        for selector in self.selectors:
            affiliated_scope: Scope = selector.affiliated_scope

            need_brace = not affiliated_scope or (
                    affiliated_scope and len(affiliated_scope.properties) == 0
            )
            end = '}' if need_brace else ''
            if not need_brace:
                lines.append(f"{indent}{selector}{end}")

            if affiliated_scope:
                lines.extend(
                    affiliated_scope.content_lines()
                )
        return lines

    def __str__(self):
        return '\n'.join(self.content_lines())

    def deal_line(self, line: str):
        if line.strip() == '': return

        from sqss.core.macro import Macro
        from sqss.core.property import Property
        from sqss.core.selector import Selector
        from sqss.core.variable.var import Var

        macro = Macro.compile(self, line)
        if macro is not None:
            self.macros.append(macro)
            self.status = 'macro-deal'
        else:
            re_property = r'(.*): +(\S[\s|\S]*)'
            _property = re.match(re_property, line)
            if _property is not None:
                name = _property.group(1)
                val = _property.group(2)
                if name[0] == '$':
                    name = name[1:]
                    self.vars.append(
                        Var.compile(self, name, val)
                    )
                else:
                    self.properties.append(
                        Property(self, name, val)
                    )
            else:
                selector = Selector.compile(self, line)
                if selector is not None:
                    self.selectors.append(selector)

    def append_cur_child(self):
        if self.cur_child is not None:
            self.scopes.append(
                self.cur_child.compile()
            )
            self.cur_selector.affiliated_scope = self.cur_child
            self.cur_child = None

    def foreach_buffer(
            self
            , deal_current: Callable[[str, int], Any]
            , deal_child:   Callable[[str, int], Any]
    ):
        from sqss.core.macro import Macro

        buffer_line= ''
        self.indent = -1
        self.deal_line_num = 0
        try:
            while True:
                if self.deal_line_num == len(self.buffer):
                    pre = len(self.buffer)
                    if self.status == 'macro-deal':
                        cur_macro: Macro = self.macros[len(self.macros) - 1]
                        cur_macro.deal_data()
                        self.status = 'common-deal'
                    if pre == len(self.buffer): break

                buffer_line = self.buffer[self.deal_line_num]
                indent = StringUtil.count_indent(buffer_line)

                if indent == len(buffer_line):
                    self.deal_line_num += 1
                    continue
                if self.indent == -1:
                    self.indent = indent

                if indent == self.indent:
                    if self.status == 'macro-deal':
                        cur_macro: Macro = self.macros[len(self.macros) - 1]
                        cur_macro.deal_data()
                        self.status = 'common-deal'
                        buffer_line = self.buffer[self.deal_line_num]
                        indent = StringUtil.count_indent(buffer_line)

                        if indent == len(buffer_line):
                            self.deal_line_num += 1
                            continue

                    deal_current(buffer_line, indent)
                elif indent > self.indent:
                    if self.status != 'macro-deal':
                        deal_child(buffer_line, indent)
                    else:
                        cur_macro: Macro = self.macros[len(self.macros) - 1]
                        cur_macro.append_child(
                            buffer_line[self.indent:]
                        )

                self.deal_line_num += 1

        except Exception as e:
            if not self.is_root:
                raise e
            else:
                raise CompileException(self.deal_line_num, buffer_line, str(e))

    def compile(self) -> 'Scope':
        def deal_child(buffer_line, indent):
            if self.cur_child is None:
                self.cur_child = Scope(self, indent)
            if indent < self.cur_child.offset:
                raise IndentationError('Improper indentation.')

            self.cur_child.buffer.append(
                buffer_line[self.cur_child.offset:]
            )

        def deal_current(buffer_line, indent):
            self.append_cur_child()
            self.deal_line(buffer_line[indent:])

        self.foreach_buffer(deal_current, deal_child)
        self.append_cur_child()
        return self

    def get_var(self, varName):
        for var in self.vars:
            if var.name == varName:
                return var
        if self.parent is not None:
            return self.parent.get_var(varName)

        raise ValueError(f'Variable \'{varName}\' does not exist.')

    @property
    def buffer(self):
        return self.__buffer

    @buffer.setter
    def buffer(self, val):
        self.__buffer = val.split('\n')

    @property
    def cur_macro(self):
        if len(self.macros) == 0:
            return None
        return self.macros[len(self.macros) - 1]

    @property
    def cur_selector(self):
        if len(self.selectors) == 0:
            return None
        return self.selectors[len(self.selectors) - 1]

    @property
    def is_root(self) -> bool:
        return self.parent is None

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
