#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class StringUtil:
    @staticmethod
    def count_indent(line_str: str) -> int:
        indent = 0
        for ch in line_str:
            if ch == ' ':
                indent += 1
            else:
                break
        return indent
