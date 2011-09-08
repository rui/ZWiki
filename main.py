#!/usr/bin/python
import cgi
import web
from markdown import markdown
import os
import re
import time
import istr

osp = os.path
PWD = osp.dirname(osp.realpath(__file__))
wiki_dir = osp.join(PWD, "pages")
recent_change_page_name = ".recent_change"

urls = (
    '/', 'WikiIndex',
    '/~edit/([a-zA-Z_\-/.]+)', 'WikiEditor',
    '/~([a-zA-Z0-9_\-/.]*)', 'SpecialWikiPage',
    '/([a-zA-Z0-9_\-/.]*)', 'WikiPage',
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

class WikiIndex:
    def GET(self):
        recent_change = osp.join(wiki_dir, recent_change_page_name)
        f = file(recent_change)
        buf = f.read()
        f.close()

        lis = []
        lines = buf.strip("\n").split("\n")
        for i in lines:
            url = osp.join("/", i)
            lis.append('- [%s](%s)' % (i, url))
            content = "\n".join(lis)

        title = "Index"
        return t_render.canvas(title, content)
    

class WikiPage:
    def GET(self, name):
        name = cgi.escape(name)
        title = istr.strip2(name, start_token=".md")
        title = title.rstrip("/")

        filepath = osp.join(wiki_dir, title)
        filepath_with_suffix = "%s.md" % filepath

        content = None
        if osp.isfile(filepath_with_suffix):
            f = file(filepath_with_suffix)
            buf = f.read()
            f.close()
            content = markdown(web.utils.safeunicode(buf))
        elif osp.isfile(filepath):
            f = file(filepath)
            buf = f.read()
            f.close()
            content = markdown(web.utils.safeunicode(buf))
        elif osp.isdir(filepath):
            files = os.listdir(filepath)
            lis = []
            for i in files:
                if not i.startswith('.'):
                    i = istr.strip2(i, '.md')
                    url = osp.join("/", title, i)
                    lis.append('- [%s](%s)' % (i, url))
            content = "\n".join(lis)

        if content:
            return t_render.canvas(title, content)

        url = '/~edit/%s' % title
        web.redirect(url)


class SpecialWikiPage:
    def GET(self, name):
        title = cgi.escape(name)
        title = istr.strip2(title, ".md")
        title = istr.strip2(title, "~")
        special_prefix = '.'
        filepath = osp.join(wiki_dir, "%s%s" % (special_prefix, title))
        filepath_with_suffix = "%s.md" % filepath

        content = None
        if osp.isfile(filepath_with_suffix):
            f = file(filepath_with_suffix)
            buf = f.read()
            f.close()
            content = markdown(web.utils.safeunicode(buf))
        elif osp.isfile(filepath):
            f = file(filepath)
            buf = f.read()
            f.close()
            content = markdown(web.utils.safeunicode(buf))

        if content:
            return t_render.canvas(title, content)

        raise web.NotFound()


class WikiEditor:
    def GET(self, name):
        title = cgi.escape(name)
        title = istr.strip2(title, ".md")
        filepath = osp.join(wiki_dir, title)
        filepath_with_suffix = "%s.md" % filepath

        content = ""
        
        if osp.isfile(filepath_with_suffix):
            f = file(filepath_with_suffix)
            content = f.read()
            f.close()
        elif osp.isfile(filepath):
            f = file(filepath)
            content = f.read()
            f.close()

        return t_render.editor(title, content)

    def POST(self, name):
        title = cgi.escape(name)
        title = istr.strip2(title, ".md")
        filepath = osp.join(wiki_dir, title)
        filepath_with_suffix = "%s.md" % filepath

        inputs = web.input()
        content = inputs.get("content")
        content = web.utils.safestr(content)

        parent = osp.dirname(filepath_with_suffix)
        if not osp.exists(parent):
            os.makedirs(parent)

        web.utils.safewrite(filepath_with_suffix, content)

        recent_change_filepath = osp.join(wiki_dir, recent_change_page_name)
        f = file(recent_change_filepath, "a")
        f.write(title + '\n')
        f.close()

        url = osp.join("/", title)
        web.redirect(url)


if __name__ == "__main__":
    if not osp.exists(wiki_dir):
        os.mkdir(wiki_dir)
        
    recent_change_filepath = osp.join(wiki_dir, recent_change_page_name)
    if not osp.exists(recent_change_filepath):
        web.utils.safewrite(recent_change_filepath, "")
    
    app = web.application(urls, globals())
    app.run()
