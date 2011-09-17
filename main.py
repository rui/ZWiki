#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cgi
import os
import shutil

import web
from markdown import markdown

import utils
import conf


osp = os.path

RECENT_CHANGE_FILENAME = ".recent_change"

urls = (
    '/', 'WikiIndex',
    '/([a-zA-Z0-9_\-/.]+)', 'WikiPage'
)

app = web.application(urls, globals())

#
# template & session
#
if web.config.get('_session') == None:
    session = web.session.Session(app, web.session.DiskStore(conf.sessions_path), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

t_globals = {
    'utils' : web.utils,
    "session" : session,
    "ctx" : web.ctx
    }
t_render = web.template.render(conf.templates_path, globals=t_globals)

def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session
app.add_processor(web.loadhook(session_hook))


def get_recent_change_content():
    recent_change = osp.join(conf.wiki_dir, RECENT_CHANGE_FILENAME)
    f = file(recent_change)
    buf = f.read()
    f.close()

    lis = []
    lines = web.utils.strips(buf, "\n").split("\n")
    lines.reverse()
    content = None

    for i in lines:
        url = osp.join("/", i)
        lis.append('- [%s](%s)' % (i, url))
        content = "\n".join(lis)

    return content

def update_recent_change_list(req_path, mode = "add", check = True):
    recent_change_filepath = osp.join(conf.wiki_dir, RECENT_CHANGE_FILENAME)

    f = file(recent_change_filepath)
    old_pages = f.read().split('\n')
    f.close()

    if check:
        old_pages = [i for i in old_pages if osp.exists(osp.join(conf.wiki_dir, "%s.md" % i))]


    old_pages = utils.remove_item_from_list(old_pages, req_path)

    if mode == "add":
        old_pages.append(req_path)

    new_content = '\n'.join(old_pages)
    web.utils.safewrite(recent_change_filepath, new_content)


def get_page_file_or_dir_fullpath_by_req_path(req_path):
    if not req_path.endswith("/"):
        return "%s.md" % osp.join(conf.wiki_dir, req_path)
    else:
        return osp.join(conf.wiki_dir, req_path)

def get_dot_idx_content_by_fullpath(fullpath):
    dot_idx_fullpath = osp.join(fullpath, ".index.md")
    return utils.cat(dot_idx_fullpath)

def get_page_file_list_by_fullpath(fullpath):
    parent = osp.dirname(fullpath)
    if osp.isdir(parent):
        buf_list = os.listdir(parent)
        return [web.utils.strips(i, ".md")
                for i in buf_list
                if not i.startswith('.')]
    return []

def get_page_file_list_content_by_fullpath(fullpath):
    req_path = fullpath.replace(conf.wiki_dir, "")
    page_file_list = get_page_file_list_by_fullpath(fullpath)
    lis = []
    for i in page_file_list:
        link = osp.join("/", req_path, i)
        title = link
        lis.append('- [%s](%s)' % (title, link))
    page_file_list_content = "\n".join(lis)
    return page_file_list_content

def delete_page_file_by_fullpath(fullpath):
    if osp.isfile(fullpath):
        os.remove(fullpath)
        return True
    elif osp.isdir(fullpath):
        idx_dot_md = osp.join(fullpath, ".index.md")
        os.remove(idx_dot_md)
        return True
    return False


class WikiIndex:
    def GET(self):
        title = "Recnet Changes"
        content = get_recent_change_content()
        return t_render.canvas(title, markdown(content))

    
class WikiPage:
    def GET(self, req_path):
        req_path = cgi.escape(req_path)
        inputs = web.input()
        action = inputs.get("action", "read")

        if action and action not in ("edit", "read", "rename", "delete"):
            raise web.BadRequest()

        fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
        title = req_path

        if action == "read":
            if osp.isfile(fullpath):
                content = utils.cat(fullpath)
            elif osp.isdir(fullpath):
                dot_idx_content = get_dot_idx_content_by_fullpath(fullpath)
                page_file_list_content = get_page_file_list_content_by_fullpath(fullpath)
                content = ""

                if dot_idx_content:
                    content = dot_idx_content
                if page_file_list_content:
                    content = "%s\n\n----\n%s" % (content, page_file_list_content)
            else:
                web.seeother("/%s?action=edit" % req_path)
                return

            return t_render.canvas(title, markdown(content))
        elif action == "edit":
            if osp.isfile(fullpath):
                content = utils.cat(fullpath)
            elif osp.isdir(fullpath):
                content = get_dot_idx_content_by_fullpath(fullpath)
            elif not osp.exists(fullpath):
                content = ""
            else:
                raise Exception("unknow path")

            return t_render.editor(title, content)
        elif action == "rename":
            if not osp.exists(fullpath):
                raise web.NotFound()

            return t_render.rename(req_path)
        elif action == "delete":
            if delete_page_file_by_fullpath(fullpath):
                update_recent_change_list(req_path, mode="delete")
                
            web.seeother("/")
            return
        
        raise web.BadRequest()

    def POST(self, req_path):
        req_path = cgi.escape(req_path)
        inputs = web.input()
        action = inputs.get("action")

        if action and action not in ("edit", "rename"):
            raise web.BadRequest()

        content = inputs.get("content")
        content = web.utils.safestr(content)

        """ NOTICE:
            if req_path == `users/`,
            fullpath will be `/path/to/users/`,
            parent will be `/path/to/users`. """

        fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

        parent = osp.dirname(fullpath)
        if not osp.exists(parent):
            os.makedirs(parent)

        if action == "edit":
            if not osp.isdir(fullpath):
                web.utils.safewrite(fullpath, content)
            else:
                idx_dot_md_fullpath = osp.join(fullpath, ".index.md")
                web.utils.safewrite(idx_dot_md_fullpath, content)

            update_recent_change_list(req_path)
            web.seeother("/%s" % req_path)
        elif action == "rename":
            new_path = inputs.get("new_path")
            if not new_path:
                raise web.BadRequest()

            old_fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
            if osp.isfile(old_fullpath):
                new_fullpath = get_page_file_or_dir_fullpath_by_req_path(new_path)
            elif osp.isdir(old_fullpath):
                new_fullpath = osp.join(conf.wiki_dir, new_path)

            if osp.exists(new_fullpath):
                err_info = "Warning: The page foobar already exists."
                return t_render.rename(req_path, err_info)

            parent = osp.dirname(new_fullpath)
            if not osp.exists(parent):
                os.makedirs(parent)

            shutil.move(old_fullpath, new_fullpath)
            update_recent_change_list(req_path, mode="delete")
            update_recent_change_list(new_path)

            if osp.isfile(new_fullpath):
                web.seeother("/%s" % new_path)
            elif osp.isdir(new_fullpath):
                web.seeother("/%s/" % new_path)

            return

        url = osp.join("/", req_path)
        web.redirect(url)


if __name__ == "__main__":
    # Notice:
    # you should remove datas/user.sqlite and sessions/* if you want a clean environment

    if not osp.exists(conf.sessions_path):
        os.mkdir(conf.sessions_path)

    if not osp.exists(conf.wiki_dir):
        os.mkdir(conf.wiki_dir)

    recent_change_filepath = osp.join(conf.wiki_dir, RECENT_CHANGE_FILENAME)
    if not osp.exists(recent_change_filepath):
        web.utils.safewrite(recent_change_filepath, "")

#	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
