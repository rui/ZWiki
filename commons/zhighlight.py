#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Available lexers
- http://pygments.org/docs/lexers/

Syntax Coloring of Source Code
- http://trac.edgewall.org/wiki/TracSyntaxColoring

"""

import re

import web
from pygments import highlight as _highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


__all__ = ["highlight", "highlight_trac_wiki_code",
           "HIGHLIGHT_STYLE"]


HIGHLIGHT_STYLE = HtmlFormatter().get_style_defs('.code')
HIGHLIGHT_STYLE = ""


def highlight(code, filename = None, stripall=True, linenos=False, cssclass="code"):
    # TODO: DONT USE PERL_LEXER AS DEFAULT
    if filename:
        try:
            lexer = guess_lexer_for_filename(filename, code, stripall=stripall)
        except ClassNotFound:
            lexer = guess_lexer(code, stripall=stripall)
    else:
        lexer = guess_lexer(code, stripall=stripall)


    formatter = HtmlFormatter(linenos=linenos, cssclass=cssclass)
    highlight_code = _highlight(code, lexer, formatter)
    return highlight_code

def highlight_trac_wiki_code(text):
    text = text.replace("\r\n", "\n")
    alias_p = '[a-zA-Z0-9#\-\+ \.]'
    shebang_p = '(?P<shebang_line>[\s]*#!%s{1,21}[\s]*?)' % alias_p

    code_p = '(?P<code>[^\f\v]+?)'

    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        shebang_line = match_obj.group('shebang_line')
        if shebang_line:
            suffix = web.utils.strips(shebang_line, "#!")
            filename = "foo.%s" % suffix
            return highlight(code=code, filename=filename)
        return highlight(code=code)

    return code_block_p_obj.sub(code_repl, text)


text1 = """{{{
#!cc

main() {
    printf("hello");
}

}}}"""

text2 = """
{{{
#!/usr/bin/env python

def main():
    print 'hello world'

if __name__ == "__main__":
    main()

}}}
"""

text3 = """{{{#!javascript

$(ducoment).ready(
    function() {
        foo();
    }
);
}}}
"""

text4 = """
{{{
main() {
    printf("hello world");
}
}}}
"""

text5 = '{{{\r\n#!cc\r\n\r\nmain() {\r\n    printf("hello");\r\n}\r\n\r\n}}}\r\n'


def main():
    texts = [text1, text2, text3, text4, text5.find("\r\n")]

    for idx in xrange(len(texts)):
        text = texts[idx]
        output = highlight_trac_wiki_code(text)

#        print "output:"
#        print output

        with open('/tmp/%d.html' % idx, 'w') as f:
            c = "<style>%s</style>\n\n%s" % (HIGHLIGHT_STYLE, output)
            f.write(web.utils.safestr(c))

if __name__ == "__main__":
    main()
