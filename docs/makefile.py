#!/usr/bin/env python
import os
import markdown
import web


osp = os.path
PWD = osp.dirname(osp.realpath(__file__))


def cat(path):
    f = file(path)
    c = f.read()
    f.close()
    return c

def compile():
    files = os.listdir(PWD)
    mds = [i for i in files if i.endswith(".md")]

    for i in mds:
        c = markdown.markdown(cat(osp.join(PWD, i)))
        md_filename = osp.basename(i)
        output_filename = md_filename.replace(".md", ".html")
        web.utils.safewrite(osp.join(PWD, output_filename), c)

if __name__ == "__main__":
    compile()