# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 16:50
@Name: sclick.py
@Author: https://github.com/liangguijing
@Description: click链接解密 / s.click链接转商品id  https://s.click.taobao.com/...
"""

from coupon.api.tkl.base import TKL
from coupon.utils import check_login, singleton

ROUTE = "/index/tbclickljjx/"
METHOD = "POST"


@singleton
class SClickApi(TKL):
    def __init__(self):
        super().__init__()

    @check_login
    def parse(self, click_url):
        url = self.url + ROUTE
        data = {"url": click_url}
        resp = self.session.request(METHOD, url=url, data=data, allow_redirects=False)
        return resp.json() if resp.status_code == 200 else {}
