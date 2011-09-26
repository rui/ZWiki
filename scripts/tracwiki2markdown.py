#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Trac Wiki to Markdown
- http://trac.edgewall.org/wiki/TracDev/DatabaseApi
- http://trac.edgewall.org/wiki/TracDev/DatabaseSchema
- http://trac.edgewall.org/browser/trunk/trac/wiki/web_ui.py
- from trac.wiki import parser
- https://gist.github.com/619537/94091aa59bdf6d6e5ad2fbb063465b2d160156ad

Trac Wiki Syntax
- http://trac.edgewall.org/wiki/WikiFormatting

Markdown Refs
- http://daringfireball.net/projects/markdown

Regular Expression Refs
- http://luy.li/2010/05/12/python-re/
- http://docs.python.org/howto/regex.html#regex-howto
"""

import re


def tracwiki2markdown(text):
    # TODO: add table filter

#    alias_p = '[a-zA-Z0-9#\-\+ \.]'
#    shebang_p = '(?:\s*#!%s{1,21}\s*?)' % alias_p
#    code_p = "^\{\{\{%s([^\r\f\v]+?)\}\}\}" % shebang_p
#    code_p_obj = re.compile(code_p, re.MULTILINE)
#    text = code_p_obj.sub('`\\1`', text)

    h6_p = "^======\s(.+?)\s======"
#    text = re.sub(h6_p, '###### \\1', text)
    h6_p_obj = re.compile(h6_p, re.MULTILINE)
    text = h6_p_obj.sub('###### \\1', text)

    h5_p = "^=====\s(.+?)\s====="
#    text = re.sub(h5_p, '##### \\1', text)
    h5_p_obj = re.compile(h5_p, re.MULTILINE)
    text = h5_p_obj.sub('##### \\1', text)

    h4_p = "^====\s(.+?)\s===="
#    text = re.sub(h4_p, '#### \\1', text)
    h4_p_obj = re.compile(h4_p, re.MULTILINE)
    text = h4_p_obj.sub('#### \\1', text)

    h3_p = "^===\s(.+?)\s==="
#    text = re.sub(h3_p, '### \\1', text)
    h3_p_obj = re.compile(h3_p, re.MULTILINE)
    text = h3_p_obj.sub('### \\1', text)

    h2_p = "^==\s(.+?)\s=="
#    text = re.sub(h2_p, '## \\1', text)
    h2_p_obj = re.compile(h2_p, re.MULTILINE)
    text = h2_p_obj.sub('## \\1', text)

    h1_p = "^=\s(.+?)\s="
#    text = re.sub("^=\s(.+?)\s=", '# \\1', text)
    h1_p_obj = re.compile(h1_p, re.MULTILINE)
    text = h1_p_obj.sub('# \\1', text)

    link_p = "\[(http[^\s\[\]]+)\s([^\[\]]+)\]"
#    text = re.sub(link_p, '[\\2](\\1)', text)
    link_p_obj = re.compile(link_p, re.MULTILINE)
    text = link_p_obj.sub('[\\2](\\1)', text)

    text = re.sub("\!(([A-Z][a-z0-9]+){2,})", '\\1', text)

    bold_italic_p = "'''''(.+?)'''''"
#    text = re.sub(bold_italic_p, '***\\1***', text)
    bold_italic_p_obj = re.compile(bold_italic_p)
    text = bold_italic_p_obj.sub('***\\1***', text)

    bold_p = "'''(.+?)'''"
#    text = re.sub(bold_p, '**\\1**', text)
    bold_p_obj = re.compile(bold_p)
    text = bold_p_obj.sub('**\\1**', text)

    italic_p = "''(.+?)''"
#    text = re.sub(italic_p, '*\\1*', text)
    italic_p_obj = re.compile(italic_p)
    text = italic_p_obj.sub('*\\1*', text)

    italic_wiki_p = "//(.+?)//"
#    text = re.sub(italic_wiki_p, '*\\1*', text)
    italic_wiki_p_obj = re.compile(italic_wiki_p)
    text = italic_wiki_p_obj.sub('*\\1*', text)

    underline_p = "__(.+?)__"
    underline_p_obj = re.compile(underline_p)
    text = underline_p_obj.sub('<u>\\1</u>', text)

#    strike_p = "~~(.+?)~~"
#    strike_p_obj = re.compile(strike_p)
#    strike_p_obj.sub('~~\\1~~')

    sub_script_p = ",,(.+?),,"
    sub_script_p_obj = re.compile(sub_script_p)
    text = sub_script_p_obj.sub("<sub>\\1</sub>", text)

    super_script_p = "\^(.+?)\^"
    super_script_p_obj = re.compile(super_script_p)
    text = super_script_p_obj.sub("<sub>\\1</sub>", text)


    def img_url_repl(matchobj):
        groups = matchobj.groups(0)
        args = [i.strip() for i in groups[0].split(',')]
        url = args[0]
        if url.startswith("wiki:"):
            img_url = re.match(r"wiki:(?:[^:]+?):(.+)", url).groups()[0]
            return '![alt](%s)' % img_url

        return '![alt](\\1)'

    img_p = r"\[\[Image\((.+?)\)\]\]"
    img_p_obj = re.compile(img_p, re.MULTILINE)
    text = img_p_obj.sub(img_url_repl, text)


#    text = re.sub("^\s\*", '*', text)
#    text = re.sub("^\s\d\.", '1.', text)

    return text


if __name__ == "__main__":
    pass
