# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 09:42
@Name: base.py
@Author: https://github.com/liangguijing
@Description: 登录淘口令
"""

import logging
import requests
import os

from config import config
from tb_coupon.settings import BASE_DIR

logger = logging.getLogger("django")
USER = config.get("account", "username")
PWD = config.get("account", "password")
USER_AGENT = config.get("config", "user_agent")
HOST = "www.taokouling.com"
HEADERS = {
    "Host": HOST,
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}


class TKL:
    def __init__(self):
        self.url = f"https://{HOST}:443"
        self.session = requests.Session()
        self.session.headers = HEADERS
        self._is_logged = False

    @property
    def is_logged(self):
        return self._is_logged

    def login(self):
        try:
            if self._login_by_cookie() or self._login_by_pwd():
                self._is_logged = True
        except Exception as e:
            logger.error(f"登录失败 {e}")

    def _login_by_cookie(self):
        try:
            with open(os.path.join(BASE_DIR, "cookie.txt"), "r", encoding="utf-8") as f:
                cookies = f.read()
                cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split(";")}
                self.session.cookies.update(cookies)
            if self._validate_cookie():
                logger.error("cookie登录成功")
                return True
        except Exception as e:
            logger.error(f"cookie登录失败 {e}")

    def _validate_cookie(self):
        url = self.url + "/index/taobao_tkljm"
        resp = self.session.post(url=url, data={"text": "1"})
        if resp.json()["msg"][0:2] != "防止":
            return True

    def _login_by_pwd(self):
        url = self.url + "/user/login/"
        data = {
            "username": USER,
            "password": PWD,
            "remember": True,
        }
        resp = self.session.post(url=url, data=data)
        if resp.json().get("status") == 1:
            logger.info("密码登录成功")
            self._save_cookie()

    def _save_cookie(self):
        cookies = ";".join(k + "=" + v for k, v in self.session.cookies.items())
        with open(os.path.join(BASE_DIR, "cookie.txt"), "w", encoding="utf-8") as f:
            f.write(cookies)
            logger.info("cookie保存成功")
