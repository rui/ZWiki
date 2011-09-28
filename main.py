#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cgi
import os
import pdb
import re
import shutil

import web
from markdown import markdown as _markdown

import utils
import conf
import scripts
import tree
import markdown_utils

osp = os.path


urls = (
    '/', 'WikiIndex',
    '/~([a-zA-Z0-9_\-/.]+)', 'SpecialWikiPage',
    ur'/([a-zA-Z0-9_\-/.%s]+)' % scripts.cjk.CJK_RANGE, 'WikiPage',
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



def markdown(text, static_file_prefix = None):
    if static_file_prefix is not None:
        text = fix_static_file_url(text, static_file_prefix)
    return _markdown(text)

def cat(fullpath):
    fullpath = web.utils.safeunicode(fullpath)
    if osp.isfile(fullpath):
        f = file(fullpath)
        buf = f.read()
        f.close()
        return web.utils.safeunicode(buf)

def tree(top = '.', filters = None, output_prefix = None, max_level = 4, followlinks = False):
    # The Element of filters should be a callable object or
    # is a byte array object of regular expression pattern.
    topdown = True
    total_directories = 0
    total_files = 0

    top_fullpath = osp.realpath(top)
    top_par_fullpath_prefix = osp.dirname(top_fullpath)

    lines = top_fullpath

    if filters is None:
        _default_filter = lambda x : not x.startswith(".")
        filters = [_default_filter]

    for root, dirs, files in os.walk(top = top_fullpath, topdown = topdown, followlinks = followlinks):
        assert root != dirs

        if max_level is not None:
            cur_dir = web.utils.strips(root, top_fullpath)
            path_levels = web.utils.strips(cur_dir, "/").count("/")
            if path_levels > max_level:
                continue

        total_directories += len(dirs)
        total_files += len(files)

        for filename in files:
            for _filter in filters:
                if callable(_filter):
                    if not _filter(filename):
                        total_files -= 1
                        continue
                elif not re.search(_filter, filename, re.UNICODE):
                    total_files -= 1
                    continue

                if output_prefix is None:
                    cur_file_fullpath = osp.join(top_par_fullpath_prefix, root, filename)
                else:
                    buf = web.utils.strips(osp.join(root, filename), top_fullpath)
                    if output_prefix != "''":
                        cur_file_fullpath = osp.join(output_prefix, buf.strip('/'))
                    else:
                        cur_file_fullpath = buf

                lines = "%s%s%s" % (lines, os.linesep, cur_file_fullpath)

    lines = lines.lstrip(os.linesep)
    report = "%d directories, %d files" % (total_directories, total_files)
    lines = "%s%s%s" % (lines, os.linesep * 2, report)

    return lines

def remove_item_from_list(a_list, item):
    return [i for i in a_list if i != item]

def safewrite(filename, content, mode = 'w'):
    """ Writes the content to a temp file and then moves the temp file to
    given filename to avoid overwriting the existing file in case of errors.
    """
    f = file(filename + '.tmp', mode)
    f.write(content)
    f.close()
    os.rename(f.name, filename)


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


def get_recent_change_content():
    recent_change = osp.join(conf.pages_path, conf.RECENT_CHANGE_FILENAME)
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
    req_path = web.utils.safestr(req_path)
    recent_change_filepath = osp.join(conf.pages_path, conf.RECENT_CHANGE_FILENAME)

    f = file(recent_change_filepath)
    old_pages = f.read().split('\n')
    f.close()

    if check:
        old_pages = [i for i in old_pages if osp.exists(osp.join(conf.pages_path, "%s.md" % i))]


    old_pages = remove_item_from_list(old_pages, req_path)

    if mode == "add":
        old_pages.append(req_path)

    new_content = web.utils.safestr('\n'.join(old_pages))
    web.utils.safewrite(recent_change_filepath, new_content)


def get_page_file_or_dir_fullpath_by_req_path(req_path):
    if not req_path.endswith("/"):
        return "%s.md" % osp.join(conf.pages_path, req_path)
    else:
        return osp.join(conf.pages_path, req_path)

def get_dot_idx_content_by_fullpath(fullpath):
    dot_idx_fullpath = osp.join(fullpath, ".index.md")
    return cat(dot_idx_fullpath)

def get_page_file_list_by_fullpath(fullpath):
    parent = osp.dirname(fullpath)
    if osp.isdir(parent):
        buf_list = os.listdir(parent)
        return [web.utils.strips(i, ".md")
                for i in buf_list
                    if not i.startswith('.') and i.endswith(".md")]
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


def update_page_file_index():
    max_level = 4
    output_prefix = "''"
    is_md_p = "^([^.]+?)\.md$"
    filters = [is_md_p]
    resp = tree(top = conf.pages_path, filters = filters,
                     max_level = max_level, output_prefix = output_prefix)

    page_file_idx_fullpath = osp.join(conf.pages_path, conf.PAGE_FILE_INDEX_FILENAME)
    print "page_file_idx_fullpath:", page_file_idx_fullpath
    web.utils.safewrite(page_file_idx_fullpath, resp)

def get_page_file_index(update=False):
    if update:
        update_page_file_index()

    page_file_idx_fullpath = osp.join(conf.pages_path, conf.PAGE_FILE_INDEX_FILENAME)
    if not osp.exists(page_file_idx_fullpath):
        update_page_file_index()

    content = cat(page_file_idx_fullpath)

    lines = content.split(os.linesep)

    # strip first line
    lines = lines[1:]
    latest_line = lines[-1]

    p = '(\d+)\s+directories, (\d+)\s+files'
    m_obj = re.match(p, latest_line)

    if m_obj:
#        dires, files = m_obj.groups()
        # strip latest line
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


def search(keywords):
    pass



class Test:
    def GET(self, req_path):
        print req_path
        return ""


class WikiIndex:
    def GET(self):
        title = "Recnet Changes"
        content = get_recent_change_content()
        content = web.utils.safeunicode(content)
        static_file_prefix = "/static/pages"
        return t_render.canvas(title, markdown(content, static_file_prefix), toolbox=False)


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
                content = cat(fullpath)

                static_file_prefix = osp.join("/static/pages", osp.dirname(req_path))
            elif osp.isdir(fullpath):
                dot_idx_content = get_dot_idx_content_by_fullpath(fullpath)
                page_file_list_content = get_page_file_list_content_by_fullpath(fullpath)
                content = ""

                if dot_idx_content:
                    content = dot_idx_content
                if page_file_list_content:
                    content = "%s\n\n----\n%s" % (content, page_file_list_content)

                static_file_prefix = osp.join("/static/pages", req_path)
                print "static_file_prefix:", static_file_prefix
            else:
                web.seeother("/%s?action=edit" % req_path)
                return

            print "static_file_prefix:", static_file_prefix
            return t_render.canvas(title, markdown(content, static_file_prefix))
        elif action == "edit":
            if osp.isfile(fullpath):
                content = cat(fullpath)
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

        # NOTICE: if req_path == `users/`, fullpath will be `/path/to/users/`,
        # parent will be `/path/to/users`.

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


class SpecialWikiPage:
    def GET(self, req_path):
        f = special_path_mapping.get(req_path)
        inputs = web.input()
        action = inputs.get("action")
        
        if callable(f):
            if req_path == "index":
                if action == "update":
                    content = f(True)
                else:
                    content = f()
            else:
                content = f()
            content = web.utils.safeunicode(content)
            return t_render.canvas(title=req_path, content=content, toolbox=False)
        else:
            raise web.NotFound()


def test_tree():
    top = "pages"

    is_md = lambda x : not x.startswith(".") and x.endswith(".md")
    filters = [is_md]
    r1 = tree(top = top, filters = filters, output_prefix = "''")

    is_md_p = "^([^.]+?)\.md$"
    filters = [is_md_p]
    r2 = tree(top = top, filters = filters, output_prefix = "''")
    assert r1 == r2


if __name__ == "__main__":
    # Notice:
    # you should remove datas/user.sqlite and sessions/* if you want a clean environment

    if not osp.exists(conf.sessions_path):
        os.mkdir(conf.sessions_path)

    if not osp.exists(conf.pages_path):
        os.mkdir(conf.pages_path)

    recent_change_filepath = osp.join(conf.pages_path, conf.RECENT_CHANGE_FILENAME)
    if not osp.exists(recent_change_filepath):
        web.utils.safewrite(recent_change_filepath, "")

#	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
