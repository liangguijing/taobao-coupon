# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 09:42
@Name: base.py
@Author: https://github.com/liangguijing
@Description:
"""

import logging
from functools import wraps
from threading import RLock

logger = logging.getLogger("django")


def check_login(func):
    """
    检查当前实例是否已经登录
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_logged:
            try:
                self.login()
                return func(self, *args, **kwargs)
            except Exception as e:
                logger.error(e)
                self.login()
        return func(self, *args, **kwargs)
    return wrapper


def singleton(cls, *args, **kwargs):
    """
    单例模式装饰器
    """
    lock = RLock()
    instance = {}

    @wraps(cls)
    def wrapper():
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper
