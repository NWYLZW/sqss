#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from glob import glob

from sqss.core.scope import Scope, OutputMode


class Compiler:
    @classmethod
    def deal_str(
            cls: 'Complier', text_str: str, outPutConfigure: OutputMode = None
    ) -> Scope:
        if outPutConfigure is not None:
            Scope.outputMode = outPutConfigure
        root = Scope(None)
        root.buffer = text_str
        return root.compile()

    @classmethod
    def deal_paths(
            cls: 'Complier'
            , paths: list[str]
            , output_path: str
    ) -> dict[str, str]:
        if len(paths) == 0: return {}

        if os.path.isdir(paths[0]):
            return cls.deal_directory(
                paths[0], output_path
            )
        if output_path is not None:
            if not os.path.isdir(
                os.path.dirname(output_path)
            ): raise FileNotFoundError('The output directory does not exist.')

            if os.path.isfile(output_path) and len(paths) > 1:
                raise GeneratorExit('The output path must not be a file.')
            if not os.path.exists(output_path):
                os.mkdir(output_path)

        compiled_data = {}
        for path in paths:
            with open(path, 'r', encoding='utf-8') as f:
                compiled_data[path] = cls.deal_str(f.read())
        common_path = os.path.commonpath(paths).replace('\\', '/')
        for path, data in compiled_data.items():
            if output_path is None:
                print(path + ':', data, sep='\n')
            else:
                output_file_path = os.path.join(
                    output_path, path.replace(common_path, '.')
                ).replace('.sqss', '.qss')
                output_file_dir_path = os.path.dirname(output_file_path)
                if not os.path.isdir(output_file_dir_path):
                    os.makedirs(output_file_dir_path)
                with open(output_file_path, 'w+', encoding='utf-8') as f:
                    f.write(data)

        return compiled_data

    @classmethod
    def deal_directory(
            cls: 'Complier'
            , directory: str
            , output_path: str
    ) -> dict[str, str]:
        return cls.deal_paths(
            glob(rf'{directory}/**/*.sqss', recursive=True), output_path
        )
