# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 17:20
@Name: __init__.py
@Author: https://github.com/liangguijing
@Description: 初始化
"""

from coupon.api.tkl.sclick import SClickApi
from coupon.api.tkl.tpwd import TPwdApi
from coupon.api.tkl.uland import ULandApi
from coupon.api.tkl.itemid import ItemApi
from coupon.api.top.tbk_dg_material_optional import TbkDgMaterialOptional
from coupon.api.top.taobao_tbk_tpwd_create import TaobaoTbkTPwdCreate

sclick_api = SClickApi()
tbpwd_api = TPwdApi()
uland_api = ULandApi()
item_api = ItemApi()
