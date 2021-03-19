# -*- coding: utf-8 -*-
"""
@Time: 3/11/2021 16:52
@Name: func.py
@Author: https://github.com/liangguijing
@Description: 
"""
import logging
from coupon.api import item_api, TaobaoTbkTPwdCreate, TbkDgMaterialOptional

logger = logging.getLogger("django")


def get_item_url(tpwd):
    """
    taokouling.com接口，通过淘口令解析出item id
    :param tpwd:
    :return: item url
    """
    try:
        res = item_api.parse(tpwd)
        if res.get("code") == "1":  # 成功解析
            return "https://item.taobao.com/item.htm?id=" + res["data"]["itemid"]
    except Exception as e:
        logger.error(e)


def get_item_info(item_url):
    """
    淘宝客API 获取部分商品详情
    :param item_url:
    :return: 包括淘口令的商品详情
    """
    item_info = {}
    material = TbkDgMaterialOptional()
    material.q = item_url
    try:
        resp = material.get_response()
        if resp.get("result_list"):
            item = resp["result_list"][0]
            item_info.update({
                "coupon_info": item["coupon_info"] or "",
                "coupon_start_time": item.get("coupon_start_time") or "",
                "coupon_end_time": item.get("coupon_end_time") or "",
                "item_url": item["item_url"],
                "pict_url": item["pict_url"],
                "title": item["title"],
                "share_url": "https:" + (item.get("coupon_share_url") or item["url"]),
            })
            item_info["tpwd"] = _get_tpwd(item_info)
    except Exception as e:
        logger.error(e)
    finally:
        return item_info


def _get_tpwd(item_info: dict):
    """
    淘宝客API 生成淘口令
    """
    tpwd = TaobaoTbkTPwdCreate()
    tpwd.logo = item_info["pict_url"]
    tpwd.text = item_info["title"]
    tpwd.url = item_info["share_url"]
    try:
        resp = tpwd.get_response()
        if resp.get("data"):
            return resp["data"]["model"]
    except Exception as e:
        logger.error(e)
        return "淘口令生成出错"
