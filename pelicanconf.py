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
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
}

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'

THEME = 'themes/pelican-alchemy/alchemy'
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

ARTICLE_PATHS = ['posts']
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feed/all_atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/nervouna'),
          ('GitHub', 'https://github.com/nervouna'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
