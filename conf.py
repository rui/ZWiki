import os
osp = os.path

PWD = osp.dirname(osp.realpath(__file__))
wiki_dir = osp.join(PWD, "pages")

sessions_path = osp.join(PWD, 'sessions')
templates_path = osp.join(PWD, "templates")

