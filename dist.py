# -*- coding: utf-8 -*-
"""
@Time: 3/19/2021 11:55
@Name: dist.py
@Author: https://github.com/liangguijing
@Description: 
"""

import os
import shutil

DIR = os.getcwd()
DIST = os.path.dirname(os.getcwd()) + r"\dist"


def copy_file(from_path, to_path):
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    items = os.listdir(from_path)
    for item in items:
        if filter_file(item):
            continue
        from_file_path = os.path.join(from_path, item)
        to_file_path = os.path.join(to_path, item)
        if os.path.isdir(from_file_path):
            copy_file(from_file_path, to_file_path)
        else:
            shutil.copy(from_file_path, to_file_path)


def filter_file(fn):
    file_name = {".idea", "__pycache__", "config.ini", "cookie.txt", "settings.py"}
    if fn in file_name:
        return True


if __name__ == "__main__":
    copy_file(DIR, DIST)

