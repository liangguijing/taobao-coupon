# -*- coding: utf-8 -*-
"""
@Time: 3/11/2021 15:36
@Name: taobao_tbk_tpwd_create.py
@Author: https://github.com/liangguijing
@Description: 
"""

from coupon.api.top.base import RestApi


class TaobaoTbkTPwdCreate(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.user_id = None  # 生成口令的淘宝用户ID
        self.logo = None  # 口令弹框logoURL
        self.text = None  # 必填 口令弹框内容
        self.url = None  # 必填 口令跳转目标页

    def get_api_name(self):
        return 'taobao.tbk.tpwd.create'
