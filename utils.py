import os
import platform
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

def which(program, extra_paths=None):
    # http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        paths = os.environ["PATH"].split(os.pathsep)
        macport_bin_path = "/opt/local/bin"
        if platform.system() == "Darwin" and osp.exists(macport_bin_path):
            paths.insert(0, macport_bin_path)

        if extra_paths:
            extra_paths.extend(paths)
            paths = extra_paths

        for path in paths:
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

if __name__ == "__main__":
    if platform.system() == "Darwin":
        assert which("tree") == "/opt/local/bin/tree"