from pathlib import Path
from runpy import run_path

globals().update({
    key: value
    for key, value in run_path(Path(__file__).with_name('pelicanconf.py')).items()
    if key.isupper()
})

SITEURL = 'https://zhangdamao.com'
RELATIVE_URLS = False

DRAFT_SAVE_AS = ''
DRAFT_LANG_SAVE_AS = ''
DRAFT_PAGE_SAVE_AS = ''
DRAFT_PAGE_LANG_SAVE_AS = ''
WITH_FUTURE_DATES = False
