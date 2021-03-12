# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 15:13
@Name: tpwd.py
@Author: https://github.com/liangguijing
@Description: 淘口令解密/淘口令解析
"""

from coupon.api.tkl.base import TKL
from coupon.utils import check_login, singleton

ROUTE = "/index/taobao_tkljm"
METHOD = "POST"


@singleton
class TPwdApi(TKL):
    def __init__(self):
        super().__init__()

    @check_login
    def parse(self, tb_pwd):
        url = self.url + ROUTE
        data = {"text": tb_pwd}
        resp = self.session.request(METHOD, url=url, data=data, allow_redirects=False)
        return resp.json() if resp.status_code == 200 else {}
