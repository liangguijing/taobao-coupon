# -*- coding: utf-8 -*-
"""
updated by liang
http://open.taobao.com/api.htm?docId=33947&docType=2

taobao.tbk.dg.optimus.material( 淘宝客物料下行-导购 )
￥免费不需用户授权
通用物料推荐，传入官方公布的物料id，可获取指定物料
"""

from coupon.api.top.base import RestApi
from config import config


AD_ZONE_ID = config.get("account", "pid").split("_")[-1]


class TbkDgOptimusMaterial(RestApi):
    def __init__(self, domain="gw.api.taobao.com", port=80):
        RestApi.__init__(self, domain, port)
        self.adzone_id = AD_ZONE_ID  # 必填 mm_xxx_xxx_xxx的第三位

        self.content_id = None  # 内容专用-内容详情ID
        self.content_source = None

        self.device_encrypt = None  # 智能匹配-设备号加密类型：MD5
        self.device_type = None  # 智能匹配-设备号类型：IMEI，或者IDFA，或者UTDID（UTDID不支持MD5加密）
        self.device_value = None  # 智能匹配-设备号加密后的值（MD5加密需32位小写）
        self.material_id = None  # 必填 官方的物料Id(详细物料id见：https://tbk.bbs.taobao.com/detail.html?appId=45301&postId=8576096
        self.item_id = None  # 商品ID，用于相似商品推荐
        self.page_no = None  # 第几页，默认：1
        self.page_size = None  # 页大小，默认20，1~100

    def get_api_name(self):
        return "taobao.tbk.dg.optimus.material"


