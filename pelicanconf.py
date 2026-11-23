import hashlib
from pathlib import Path

AUTHOR = 'ZHANG Damao'
SITENAME = 'Ignore the Blueprint'
SITESUBTITLE = 'A blog about programming, life and everything.'
SITEURL = 'https://zhangdamao.com'
DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True

STATIC_PATHS = [
    'images',
    'extra',
]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/favicon.svg': {'path': 'favicon.svg'},
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
}

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'

THEME = 'themes/ignore-the-blueprint'
# Appended to the stylesheet URL so a deploy never pairs new pages with a
# cached copy of the old stylesheet.
THEME_VERSION = hashlib.sha1(
    Path(THEME, 'static/css/style.css').read_bytes()
).hexdigest()[:8]

PLUGIN_PATHS = ['plugins']
PLUGINS = ['plates', 'og_cards', 'title_font']
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

ARTICLE_PATHS = ['posts']
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feed/all_atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Used for the twitter:site card tag
TWITTER_USERNAME = 'nervouna'

# Extra links in the site navigation
# \uFE0E asks for the text form of the arrow; without it iOS draws an emoji.
MENUITEMS = (('Projects ↗\uFE0E', 'https://damao.io'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/nervouna'),
          ('GitHub', 'https://github.com/nervouna'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
