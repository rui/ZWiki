#!/usr/bin/env python

def convert_path_to_hierarchy(path):
    """ Parse path and return hierarchy name and link pairs,
    inspired by [GNOME Nautilus](http://library.gnome.org/users/user-guide/2.32/nautilus-location-bar.html.en)
    and [Trac Wiki](http://trac.edgewall.org/browser/trunk/trac/wiki/web_ui.py) .
    
        >>> path = '/shugelab/users/lee'
        >>> t1 = [('shugelab', '/shugelab'), ('users', '/shugelab/users'), ('lee', '/shugelab/users/lee')]
        >>> convert_path_to_hierarchy(path) == t1
        True
    """
    caches = []

    if "/" == path:
        return [("index", "/~index")]
    elif "/" in path:
        parts = path.split('/')
        start = len(parts) - 2
        stop = -1
        step = -1
        for i in range(start, stop, step):
            name = parts[i + 1]
            links = "/" + "/".join(parts[1 : i + 2])
            if name == '':
                continue
            caches.append((name, links))
            
    caches.reverse()
    
    return caches

def test():
    for i in [
        ("/", [("index", "/~index")]), # name, link pairs
        
        ("/system-management/gentoo/abc",
         [("system-management", "/system-management"),("gentoo", "/system-management/gentoo"),("abc", "/system-management/gentoo/abc"),]),
        
        ("/programming-language",
         [("programming-language", "/programming-language"),]),

        ("/programming-language/",
         [("programming-language", "/programming-language"),]),
        ]:
        req_path = i[0]
        links = i[1]        
        assert convert_path_to_hierarchy(req_path) == links

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    test()
