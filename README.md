# About ZWiki

ZWiki is a lightweight wiki system implement in Python and web framework [web.py](http://webpy.org/).

## FEATURES

- run up without database
- support [Markdown](http://daringfireball.net/projects/markdown/) syntax

## RUNTIME REQUIREMENTS

- python 2.6+

- web.py 0.37+

    If you install it by `easy_install web.py`,
    you have to fix [issue #95](https://github.com/webpy/webpy/issues/95) by manual.

    Strong recommend you install it from latest source:

        git clone https://github.com/webpy/webpy.git
        cd webpy.git
        sudo python setup.py install

- py-markdown 2.0.3+

    On Mac OS X via MacPorts, `sudo port install py-markdown`