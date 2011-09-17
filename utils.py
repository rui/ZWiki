import os
import web

osp = os.path

def safewrite(filename, content, mode = 'w'):
    """Writes the content to a temp file and then moves the temp file to
    given filename to avoid overwriting the existing file in case of errors.
    """
    f = file(filename + '.tmp', mode)
    f.write(content)
    f.close()
    os.rename(f.name, filename)


def remove_item_from_list(a_list, item):
    return [i for i in a_list if i != item]


def cat(fullpath):
    if osp.isfile(fullpath):
        f = file(fullpath)
        buf = f.read()
        f.close()
        return web.utils.safeunicode(buf)