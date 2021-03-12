# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 17:00
@Name: uland.py
@Author: https://github.com/liangguijing
@Description: 二合一解析/优惠券提取 https://uland.taobao.com/coupon/edetail?e=...
"""

from coupon.api.tkl.base import TKL
from coupon.utils import check_login, singleton

ROUTE = "/index/taobao_ehylj/"
METHOD = "POST"


@singleton
class ULandApi(TKL):
    def __init__(self):
        super().__init__()

    @check_login
    def parse(self, uland_url):
        url = self.url + ROUTE
        data = {"url": uland_url}
        resp = self.session.request(METHOD, url=url, data=data, allow_redirects=False)
        return resp.json() if resp.status_code == 200 else {}

