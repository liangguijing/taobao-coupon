# -*- coding: utf-8 -*-
"""
@Time: 3/9/2021 09:42
@Name: base.py
@Author: https://github.com/liangguijing
@Description:
"""

import re
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from coupon.func import get_item_url, get_item_info
from coupon.api import TbkDgOptimusMaterial, TbkDgMaterialOptional


# ULAND_PATTERN = re.compile(r"^https://uland\w+")
# SCLICK_PATTERN = re.compile(r"^https://s\.click\w+")
TPWD_PATTERN = re.compile(r"\W\w{11}\W")


def index(request):
    return render(request, "index.html")


def search(request: HttpRequest):
    """
    输入淘口令或者商品名称，解析淘口令或者直接搜索
    :param request:
    :return: item信息和推广链接
    """
    query = request.GET.get("query")
    page_no = request.GET.get("page")
    if not query:
        return JsonResponse({"err_msg": "请输入内容"})
    tpwd = TPWD_PATTERN.search(query)
    if tpwd:
        query = get_item_url(tpwd)
    tb = TbkDgMaterialOptional()
    tb.page_size = "12"
    tb.q = query
    tb.page_no = page_no
    resp = tb.get_response()
    return JsonResponse(resp)


def search_page(request: HttpRequest):
    query = request.GET.get("query") or ""
    return render(request, "search_page.html", {"query": query})


def tpwd2coupon(request: HttpRequest):
    """
    输入淘口令，首先解析出item链接，然后在阿里妈妈查询是否有优惠券，最后生成推广淘口令
    :param request:
    :return: item信息和推广链接
    """
    result = {"err_msg": ""}
    tpwd = request.GET.get("tpwd")
    if not tpwd:
        return JsonResponse({"err_msg": "请输入淘口令"})
    item_url = get_item_url(tpwd)
    if item_url:
        item_info = get_item_info(item_url)
        if item_info:
            result.update(item_info)
        else:
            result["err_msg"] = "获取商品信息出错!"
    else:
        result["err_msg"] = "您输入的淘口令有误或不存在!"
    return JsonResponse(result)


def optimus(request: HttpRequest):
    tb = TbkDgOptimusMaterial()
    tb.material_id = request.GET.get("material_id")
    if tb.material_id != "32366":
        tb.page_no = request.GET.get("page_no")
    else:
        tb.page_no = "1"
    tb.page_size = "12"
    resp = tb.get_response()
    return JsonResponse(resp)
