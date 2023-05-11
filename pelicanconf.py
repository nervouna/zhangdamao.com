AUTHOR = 'ZHANG Damao'
SITENAME = 'Ignore the Blueprint'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

THEME = 'themes/mnmlist'

# Theme settings
HIDE_DATE = True
# COLOR_SCHEME_CSS = 'github_jekyll.css'

ARTICLE_PATHS = ['posts']
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/nervouna'),
          ('GitHub', 'https://github.com/nervouna'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
