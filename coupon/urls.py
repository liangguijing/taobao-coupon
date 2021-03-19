# -*- coding: utf-8 -*-
"""
@Time: 3/18/2021 08:41
@Name: urls.py
@Author: https://github.com/liangguijing
@Description: 
"""

from django.urls import path
from coupon.views import index, optimus, search, search_page

urlpatterns = [
    path('', index),
    path('search_page', search_page, name="search_page"),
    path('search', search, name="search"),
    path('optimus', optimus, name="optimus"),
]
