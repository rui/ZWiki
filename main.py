#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cgi
import os
import re
import shlex
import shutil
import subprocess

import web
from markdown import markdown

import utils
import conf


osp = os.path

RECENT_CHANGE_FILENAME = ".recent_change"
PAGE_FILE_INDEX_FILENAME = ".page_file_index"

urls = (
    '/', 'WikiIndex',
    '/([a-zA-Z0-9_\-/.]+)', 'WikiPage',
    '/~([a-zA-Z0-9_\-/.]+)', 'SpecialWikiPage',
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
    recent_change = osp.join(conf.pages_path, RECENT_CHANGE_FILENAME)
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
    recent_change_filepath = osp.join(conf.pages_path, RECENT_CHANGE_FILENAME)

    f = file(recent_change_filepath)
    old_pages = f.read().split('\n')
    f.close()

    if check:
        old_pages = [i for i in old_pages if osp.exists(osp.join(conf.pages_path, "%s.md" % i))]


    old_pages = utils.remove_item_from_list(old_pages, req_path)

    if mode == "add":
        old_pages.append(req_path)

    new_content = '\n'.join(old_pages)
    web.utils.safewrite(recent_change_filepath, new_content)


def get_page_file_or_dir_fullpath_by_req_path(req_path):
    if not req_path.endswith("/"):
        return "%s.md" % osp.join(conf.pages_path, req_path)
    else:
        return osp.join(conf.pages_path, req_path)

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
    req_path = fullpath.replace(conf.pages_path, "")
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
        return t_render.canvas(title, markdown(content), toolbox=False)

    
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
                new_fullpath = osp.join(conf.pages_path, new_path)
            else:
                raise Exception('unknow path')

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


def update_page_file_index():
    """ ztree options:
    -i : not print the indentation lines
    -f : prints the full path prefix for each file
    -P : List  only  those files that match the wild-card pattern
    -t : Sort the output by last modification time instead of alphabetically
    -L : Max display depth of the directory tree
    -n : Turn colorization off always, over-ridden by the -C option
    """
    max_level = 4
    obj_prefix = "''"
    tree_fullpath = utils.which("tree", extra_paths=[osp.join(conf.PWD, 'bin')])
    cmd = "%s -i -E %s -P '*.md' -t  -L %d -n %s" % \
          (tree_fullpath, obj_prefix, max_level, conf.pages_path)
    p_obj = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    p_obj.wait()
    resp = p_obj.stdout.read().strip()

    page_file_idx_fullpath = osp.join(conf.pages_path, PAGE_FILE_INDEX_FILENAME)
    web.utils.safewrite(page_file_idx_fullpath, resp)

def get_page_file_index(update=False):
    if update:
        update_page_file_index()

    page_file_idx_fullpath = osp.join(conf.pages_path, PAGE_FILE_INDEX_FILENAME)
    if not osp.exists(page_file_idx_fullpath):
        update_page_file_index()

    content = utils.cat(page_file_idx_fullpath)

    lines = content.split(os.linesep)

    # strip first line
    # TODO: strip first line in ztree
    lines = lines[1:]
    latest_line = lines[-1]

    p = '(\d+)\s+directories, (\d+)\s+files'
    m_obj = re.match(p, latest_line)

    if m_obj:
        dires, files = m_obj.groups()
        print "dires, files:", dires, files
        lines = lines[:-2]

    lis = []
    for i in lines:
        i = web.utils.strips(i, ".md")
        url = osp.join("/", i)
        lis.append('- [%s](%s)' % (i, url))
        content = "\n".join(lis)

    return markdown(content)

special_path_mapping = {
    'index' : get_page_file_index,
}
class SpecialWikiPage:
    def GET(self, req_path):
        f = special_path_mapping.get(req_path, None)
        if callable(f):
            content = f(True)
            return t_render.canvas(title=req_path, content=content, toolbox=False)
        else:
            raise web.NotFound()


if __name__ == "__main__":
    # Notice:
    # you should remove datas/user.sqlite and sessions/* if you want a clean environment

    if not osp.exists(conf.sessions_path):
        os.mkdir(conf.sessions_path)

    if not osp.exists(conf.pages_path):
        os.mkdir(conf.pages_path)

    recent_change_filepath = osp.join(conf.pages_path, RECENT_CHANGE_FILENAME)
    if not osp.exists(recent_change_filepath):
        web.utils.safewrite(recent_change_filepath, "")

#	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
