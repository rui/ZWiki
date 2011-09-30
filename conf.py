import os
osp = os.path

PWD = osp.dirname(osp.realpath(__file__))
pages_path = osp.join(PWD, "pages")

sessions_path = osp.join(PWD, 'sessions')
templates_path = osp.join(PWD, "templates")
