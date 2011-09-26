#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
http://www.unicode.org/versions/latest/
click `East Asian Scripts` at left content table

This script is based on The Unicode Standard Version 6.0 – Core Specification.
"""

cjk_unified_ideographs = ur'\u4E00-\u9FFF'
cjk_unified_ideographs_extension_a = ur'\u3400-\u4DFF'
cjk_unified_ideographs_extension_b = ur'\u20000-\u2A6DF'
cjk_unified_ideographs_extension_c = ur'\u2A700-\u2B73F'
cjk_unified_ideographs_extension_d = ur'\u2B740-\u2B81F'
cjk_compatibility_ideographs = ur'\uF900-\uFAFF'
cjk_compatibility_ideographs_supplement = ur"\u2F800-\u2FA1F"

CJK_RANGE = ur"".join([
    cjk_unified_ideographs,
    cjk_unified_ideographs_extension_a,
    cjk_unified_ideographs_extension_b,
    cjk_compatibility_ideographs,
    cjk_compatibility_ideographs_supplement
])


if __name__ == "__main__":
    import re

    p = ur"([%s]+)" % CJK_RANGE

    t = '中文'.decode('utf-8')
    groups = re.search(p, t, re.UNICODE).groups()

    for i in groups:
        print i