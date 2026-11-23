import os
from pathlib import Path
from runpy import run_path

globals().update({
    key: value
    for key, value in run_path(Path(__file__).with_name('pelicanconf.py')).items()
    if key.isupper()
})

SITEURL = 'https://zhangdamao.com'
RELATIVE_URLS = False

# Cloudflare Pages previews are served from their own hosts. With the
# production SITEURL they would load the stylesheet and fonts from the live
# site and show the old theme, so previews use root-relative URLs instead.
if os.environ.get('CF_PAGES_BRANCH', 'main') != 'main':
    SITEURL = ''

DRAFT_SAVE_AS = ''
DRAFT_LANG_SAVE_AS = ''
DRAFT_PAGE_SAVE_AS = ''
DRAFT_PAGE_LANG_SAVE_AS = ''
WITH_FUTURE_DATES = False
