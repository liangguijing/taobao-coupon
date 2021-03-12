# -*- coding: utf-8 -*-
"""
@Time: 3/11/2021 09:34
@Name: itemid.py
@Author: https://github.com/liangguijing
@Description: 淘口令获取商品ID
{
    "code": "1",
    "msg": "解析成功",
    "time": 1615428922,
    "data": {
        "itemid": "597109007243"
    }
}
"""

from coupon.api.tkl.base import TKL
from coupon.utils import check_login, singleton

ROUTE = "/index/tbtkltoitemid/"
METHOD = "POST"


@singleton
class ItemApi(TKL):
    def __init__(self):
        super().__init__()

    @check_login
    def parse(self, tb_pwd):
        url = self.url + ROUTE
        data = {"tkl": tb_pwd}
        resp = self.session.request(METHOD, url=url, data=data, allow_redirects=False)
        return resp.json() if resp.status_code == 200 else {}
