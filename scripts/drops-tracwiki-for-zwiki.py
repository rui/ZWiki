#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This script assists you migrate data from Trac Wiki to ZWiki.

NOTICE: it supports SQLite3 database backend only.


File conf.py *MUST* contains following variables:

- trac_db_path
    fullpath of your trac wiki database file, i.e., "/path/to/trac-wiki-instance/db/trac.db"

- trac_wiki_attachments_path
    fullpath of your trac wiki attachements folder, i.e., "/Users/lee/backups/enjoy-series/attachments/wiki"

- zwiki_pages_path
    fullpath of your zwiki instance' pages folder, i.e., /path/to/zwiki/pages"

- zwiki_host
    i.e., "127.0.0.1:8080"
"""

import httplib
import os
import shutil
import urllib
import web

import tracwiki2markdown
import conf

osp = os.path
PWD = osp.dirname(osp.realpath(__file__))
db = web.database(dbn="sqlite", db=conf.trac_db_path)


def get_page_latest_rev_by_name(name):
    name = web.utils.safeunicode(name)
    sql = 'select name, text, time from wiki where name = $name order by time desc limit 1'
#    sql = 'select name, text from wiki where version = (select max(version) from wiki where name = $name);'

    vars = {"name" : name}
    records = db.query(sql, vars=vars)
    for record in records:
        return record
    
def title_index():
    total = 0
    step = 100
    offset = 0
    sql = 'select DISTINCT name from wiki limit $limit offset $offset'
    vars = {
        'limit' : step,
        'offset' : offset
    }

    records = list(db.query(sql, vars=vars))
    while len(records) and len(records) == 100:

        total += len(records)
        # do here

        vars["offset"] = vars["offset"] + 100
        records = list(db.query(sql, vars=vars))

        if len(records) < 100:
            total += len(records)

            for record in records:
                # do here
                pass

    print "total:", total

def quote_plus_page_name(page_name):
    return "/".join([urllib.quote_plus(i) for i in page_name.split("/")])

def create_page(req_path, content):
    content = web.utils.safestr(content)
    content = tracwiki2markdown.tracwiki2markdown(content)
    req_path = web.utils.safestr(req_path)

    params = urllib.urlencode({'content': content})
    conn = httplib.HTTPConnection(conf.zwiki_host)
    conn.request("POST", "/%s?action=edit" % req_path, params)
    response = conn.getresponse()

    if response.status == httplib.NOT_FOUND:
        print 'response.status: NOT_FOUND'
        exit(-1)

    assert response.status == httplib.MOVED_PERMANENTLY
    assert response.reason == "Moved Permanently"

    data = response.read()

    assert data == 'None'

    conn.close()
    

def create_attachments(page_name):
    page_name = quote_plus_page_name(web.utils.safestr(page_name))
    attaches_fullpath =  osp.join(conf.trac_wiki_attachments_path, page_name)

    print "attaches_fullpath:", attaches_fullpath
    print 

    if not osp.exists(attaches_fullpath):
        print "warning: `%s` not found" % attaches_fullpath
        return


    save_to = osp.join(conf.zwiki_pages_path, urllib.unquote(page_name))
    parent = osp.dirname(save_to)

    if page_name.count("/") > 0:
        if not osp.exists(parent):
            os.makedirs(parent)

    attaches = os.listdir(attaches_fullpath)
    attaches = [i for i in attaches if not i.startswith(".")]
    for i in attaches:
        src = osp.join(attaches_fullpath, i)
        if osp.isfile(src):
            if page_name.count("/") > 0:
                dst = osp.join(parent, i)
            else:
                dst = osp.join(save_to, i)
            print "copy"
            print "\tsrc: ", src
            print "\tdst: ", dst
            print
            shutil.copy(src, dst)

def main():
    page_name = '录音/GNU'
    #page_name2 = 'note/cassandra/zh-cn'
    print "page_name:", page_name

    page = get_page_latest_rev_by_name(page_name)
    create_page(urllib.unquote(page["name"]), page["text"])
    create_attachments(page["name"])


if __name__ == "__main__":
#    main()
    pass