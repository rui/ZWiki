# About ZWiki

ZWiki is a lightweight wiki system implement in Python and web framework [web.py](http://webpy.org/).


## GET STARTED

To get the latest development version from git:

    git clone git@github.com:shuge/ZWiki.git
    cd ZWiki.git
    python main.py
    

## FEATURES

- run up without database, CRUD page file
- support [Markdown](http://daringfireball.net/projects/markdown/) syntax
- auto include static image file
- auto generate table of content for long text
- list all page files (implement in GNU findutils)
- list recent changed page files (implement in GNU findutils)
- search by file name and file content (implment in GNU findutils and GNU grep)

## RUNTIME REQUIREMENTS

- python 2.6+

    On Mac OS X via MacPorts, `sudo port install python26`

- web.py 0.37+

    If you install it by `easy_install web.py`,
    you have to fix [issue #95](https://github.com/webpy/webpy/issues/95) by manual.

    Strong recommend you install it from latest source:

        git clone https://github.com/webpy/webpy.git
        cd webpy.git
        sudo python setup.py install

- py-markdown 2.0.3+

    On Mac OS X via MacPorts, `sudo port install py-markdown`

- pygments 1.4+

    On Mac OS X via MacPorts, `sudo port install py-pygments`
