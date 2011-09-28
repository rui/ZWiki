import os
import re

from markdown import markdown as _markdown

import zhighlight

osp = os.path

__all__ = ["fix_static_file_url"]


def _fix_img_url(text, static_file_prefix = None):
    """
    text = '![blah blah](20100426-400x339.png)'
    static_file_prefix = '/static/files/'
    result = _fix_img_url(text, static_file_prefix)
    >>> assert result == '![blah blah](/static/files/20100426-400x339.png)'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group("img_alt")
        img_url = match_obj.group("img_url")
        if static_file_prefix:
            fixed_img_url = osp.join(static_file_prefix, img_url)
            return '![%s](%s)' % (img_alt, fixed_img_url)
        else:
            return '![%s](%s)' % (img_alt, img_url)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def _fix_img_url_with_option(text, static_file_prefix = None):
    """
    text = '![blah blah](20100426-400x339.png "png title")'
    static_file_prefix = '/static/files/'
    result = _fix_img_url_with_option(text, static_file_prefix)
    >>> assert result == '![blah blah](/static/files/20100426-400x339.png "png title")'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group('img_alt')
        img_url = match_obj.group('img_url')
        img_title = match_obj.group('img_title')
        if static_file_prefix:
            fixed_img_url = osp.join(static_file_prefix, img_url)
            return '![%s](%s "%s")' % (img_alt, fixed_img_url, img_title)
        else:
            return '![%s](%s "%s")' % (img_alt, img_url, img_title)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\s\"(?P<img_title>.+?)\"\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def fix_static_file_url(text, static_file_prefix):
    text = _fix_img_url(text, static_file_prefix)
    text = _fix_img_url_with_option(text, static_file_prefix)
    return text


def markdown(text, static_file_prefix = None):
    text = text.replace("\r\n", "\n")
    if static_file_prefix is not None:
        text = fix_static_file_url(text, static_file_prefix)

    text = zhighlight.highlight_trac_wiki_code(text)
    return _markdown(text)