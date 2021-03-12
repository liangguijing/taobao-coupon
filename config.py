# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 09:42
@Name: config.py
@Author: https://github.com/liangguijing
@Description: 读取和修改配置文件
"""

import os
import configparser
from tb_coupon.settings import BASE_DIR


class Config:
    def __init__(self, filename="config.ini"):
        self._path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(self._path):
            raise FileNotFoundError("Missing config file: %s" % self._path)
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding="utf-8")

    def get(self, section, option, strip_blank=True, strip_quote=True):
        s = self._config.get(section, option)
        if strip_blank:
            s = s.strip()
        if strip_quote:
            s = s.strip('"').strip("'")
        return s

    def getboolean(self, section, option):
        return self._config.getboolean(section, option)

    def update(self, section, option, value):
        self._config.set(section, option, str(value))
        with open(self._path, "w", encoding="utf-8") as f:
            self._config.write(f, space_around_delimiters=False)


config = Config()

