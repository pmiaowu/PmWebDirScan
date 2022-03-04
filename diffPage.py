#!/usr/bin/python
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher
from functools import reduce

import re

def get_filtered_page_content(page, only_text=True, split=" "):
    """
    返回经过过滤的页面内容，不包含脚本、样式和/或注释
    或所有HTML标签
    >>> get_filtered_page_content(u'<html><title>foobar</title><body>test</body></html>')
    u'foobar test'
    """
    ret_val = page
    ret_val = re.sub(r"(?si)<script.+?</script>|<!--.+?-->|<style.+?</style>%s" % (r"|<[^>]+>|\t|\n|\r" if only_text else ""),split, page)
    while ret_val.find(2 * split) != -1:
        ret_val = ret_val.replace(2 * split, split)
    ret_val = htmlunescape(ret_val.strip().strip(split))

    return ret_val

def htmlunescape(value):
    """
    返回(基本转换)HTML未转义值
    >>> htmlunescape('a&lt;b')
    'a<b'
    """
    ret_val = value
    codes = (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&nbsp;', ' '), ('&amp;', '&'))
    ret_val = reduce(lambda x, y: x.replace(y[0], y[1]), codes, ret_val)
    try:
        ret_val = re.sub(r"&#x([^ ;]+);", lambda match: unichr(int(match.group(1), 16)), ret_val)
    except ValueError:
        pass
    return ret_val

def get_ratio(first_page, second_page):
    """
    打印出现在两个不同响应页面中的单词
    对比文本相似度, 会去掉html标签
    """
    first_page = get_filtered_page_content(first_page)
    second_page = get_filtered_page_content(second_page)

    match = SequenceMatcher(None, first_page, second_page).ratio()
    return match

def split_by_sep(seq):
    chunks = []
    chunk = ''

    for c in seq:
        if c in '\n\t\r"\'<':
            chunks.append(chunk)
            chunk = ''
        else:
            chunk += c

    chunks.append(chunk)

    return chunks

def relative_distance_boolean(a_str, b_str, threshold=0.6):
    if threshold == 0:
        return True
    elif threshold == 1.0:
        return a_str == b_str

    if len(b_str) < len(a_str):
        a_str, b_str = b_str, a_str

    alen = len(a_str)
    blen = len(b_str)

    if blen == 0 or alen == 0:
        return alen == blen

    if blen == alen and a_str == b_str and threshold <= 1.0:
        return True

    if threshold > upper_bound_similarity(a_str, b_str):
        return False
    else:
        simalar = SequenceMatcher(None, split_by_sep(a_str), split_by_sep(b_str)).quick_ratio()
        return threshold <= simalar

def upper_bound_similarity(a, b):
    return (2.0 * len(a)) / (len(a) + len(b))