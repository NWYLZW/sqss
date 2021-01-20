#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, argparse, toml

from sqss.core.compiler import Compiler

root_path = os.path.join(
    __file__, '../../../..'
)
config = toml.load(f"{root_path}\\pyproject.toml")
toolPoetry = config.get('tool')['poetry']

def main():
    parser = argparse.ArgumentParser(
        prog=toolPoetry['name'],
        description=f"{toolPoetry['description']}",
        epilog=f"{toolPoetry['name']} version {toolPoetry['version']}"
    )
    parser.add_argument(
        '-v', '--version'
        , action='version'
        , version=f"{toolPoetry['name']} version {toolPoetry['version']}"
    )
    parser.add_argument(
        'path'
        , help='Set the compiled file\'s path list'
        , nargs='+'
    )
    parser.add_argument(
        '-o', '--output'
        , help='Set the compiled file output directory'
        , nargs='?'
    )

    command_args = parser.parse_args()
    Compiler.deal_paths(
        command_args.path, command_args.output
    )
