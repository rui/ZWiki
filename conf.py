import os
osp = os.path

PWD = osp.dirname(osp.realpath(__file__))
pages_path = osp.join(PWD, "pages")

sessions_path = osp.join(PWD, 'sessions')
templates_path = osp.join(PWD, "templates")


RECENT_CHANGE_FILENAME = ".recent_change"
PAGE_FILE_INDEX_FILENAME = ".page_file_index"
