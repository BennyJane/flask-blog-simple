# -*- coding: utf-8 -*-
# @Time : 2020/10/2
# @Author : Benny Jane
# @Email : 暂无
# @File : Helper.py
# @Project : flask-blog-v1
import math


def iPagination(params):
    ret = {
        "is_prev": 1,
        "is_next": 1,
        "from": 0,
        "end": 0,
        "current": 0,
        "total_pages": 0,
        "page_size": 0,
        "total": 0,
        "url": params['url']
    }

    total = params['total']
    page_size = params['page_size']
    page = params['page']
    half_page_display = int(params['half_page_display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    if page - half_page_display > 0:
        ret['from'] = page - half_page_display
    else:
        ret['from'] = 1

    if page + half_page_display <= total_pages:
        ret['to'] = page + half_page_display
    else:
        ret['to'] = total_pages
    ret['current'] = page  # 其实就是 page的值
    ret['total'] = total
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['range'] = range(ret['from'], ret['to'] + 1)
    return ret


def getTitleIndex(title):
    index = 100
    title = title.replace(',', '.').replace('，', '.')
    if '.' in title:
        try:
            index = int(title.split('.')[0])
        except Exception as _:
            # todo 设置全局异常捕获，弹窗提示
            pass
    return index
