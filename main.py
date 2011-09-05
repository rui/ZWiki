#!/usr/bin/python
import cgi
import web
from markdown import markdown
import os
import re
import time

osp = os.path
PWD = osp.dirname(osp.realpath(__file__))
wikidir = osp.join(PWD, "pages")

urls = (
    # '/', 'WikiPages',
    # '/page/([a-zA-Z_]+)', 'WikiPage',
    # '/editor/([a-zA-Z_]+)', 'WikiEditor'

    # '/', 'WikiPageIndex',
    '/([a-zA-Z0-9_\-/.]*)', 'WikiPage',
    '/~edit/([a-zA-Z_\-/.]+)', 'WikiEditor'
)

app = web.application(urls, globals())

#
# template & session
#
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

t_globals = {
    'markdown': markdown,
    'utils' : web.utils,
    "session" : session,
    "ctx" : web.ctx
    }
t_render = web.template.render('templates', globals=t_globals)

def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session
app.add_processor(web.loadhook(session_hook))


"""
exists '/.*' ? read '/.*' : redirect '/edit/(?<page_name>)'

list files/directory of a directory
list recent (tree)
custom macro

search

templates
static
"""

class WikiPages:
    def GET(self):
        t = re.compile('^[a-zA-Z_]+$')
        wikipages = os.listdir(wikidir)
        msg = "<html><head><title>wiki pages</title></head><body>"
        msg += "<h1>Wiki Pages:</h1><ul>"
        for wikipage in wikipages:
            if osp.isfile(osp.join(wikidir, wikipage)) and t.match(wikipage):
                msg += "<li><a href=\"%(path)s/page/%(page)s\">%(page)s</a></li>" \
                    % {'path':web.ctx.home+web.ctx.path[1:],'page':wikipage}
        msg += "</ul></body></html>"

        return msg


class WikiPage:
    def GET(self, name):
        print "name:", name
        
        title = cgi.escape(name).rstrip(".md")
#        filepath = "%s.md" % osp.join(wikidir, title)
        filepath = osp.join(wikidir, title)
        filepath_with_suffix = "%s.md" % filepath

        content = None
        if osp.isfile(filepath_with_suffix):
            with open(filepath_with_suffix) as f:
                buf = f.read()
            content = markdown(buf)            
        elif osp.isfile(filepath):
            with open(filepath) as f:
                buf = f.read()
            content = markdown(buf)
        elif osp.isdir(filepath):
            files = os.listdir(filepath)
            content = "\n".join(['- [%s](%s)' % (osp.join(name, i), i) for i in files])

        if content:
            return t_render.canvas(title, content)

        url = '/~edit/%s' % title
        web.redirect(url)


class WikiEditor:
    def GET(self, name):
        title = cgi.escape(name).rstrip(".md")
        filepath = osp.join(wikidir, title)
        filepath_with_suffix = "%s.md" % filepath

        content = ""
        
        if osp.isfile(filepath_with_suffix):
            with open(filepath_with_suffix) as f:
                buf = f.read()
                content = buf
        elif osp.isfile(filepath):
            with open(filepath) as f:
                buf = f.read()
                content = buf

        return t_render.editor(title, content)

    def POST(self, name):
        title = cgi.escape(name).rstrip(".md")
        filepath = osp.join(wikidir, title)
        filepath_with_suffix = "%s.md" % filepath

        inputs = web.input()
        content = inputs.get("content")

        parent = osp.dirname(filepath_with_suffix)
        if not osp.exists(parent):
            os.makedirs(parent)

        with open(filepath_with_suffix, "w") as f:
            f.write(content)

        url = osp.join("/", title)
        web.redirect(url)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
