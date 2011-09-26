import os
import re

import web

osp = os.path


def tree(top = '.', filters = None, output_prefix = None, max_level = 4, followlinks = False):
    """
    The Element of filters should be a callable object or is a byte array object of regular expression pattern.
    """
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

def _test():
    top = "pages"

    is_md = lambda x : not x.startswith(".") and x.endswith(".md")
    filters = [is_md]
    r1 = tree(top = top, filters = filters, output_prefix = "''")

    is_md_p = "^([^.]+?)\.md$"
    filters = [is_md_p]
    r2 = tree(top = top, filters = filters, output_prefix = "''")
    assert r1 == r2

if __name__ == "__main__":
#    _test()
    import conf
    is_md_p = "^([^.]+?)\.md$"
    filters = [is_md_p]
    print tree(top = conf.pages_path, filters = filters, output_prefix = "''")
