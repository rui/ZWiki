#!/usr/bin/env python
import os
import re
import web.utils

osp = os.path


__all__ = ["cat"]


def cat(*args):
    buf = ""
    for i in args:
        fullpath = web.utils.safeunicode(i)
        if osp.isfile(fullpath):
            f = file(fullpath)
            buf = "%s%s" % (buf, f.read())
            f.close()
            
    return web.utils.safeunicode(buf)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
