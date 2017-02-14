# -*- coding: utf-8 -*-
#
# Python documentation build configuration file
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).

import sys, os, time
sys.path.append(os.path.abspath('tools/extensions'))

# General configuration
# ---------------------

# JP: ../Include ディレクトリが存在しないので、coverage拡張を無効化
# JP: jpsupport 拡張を利用

extensions = ['sphinx.ext.doctest',
              'sphinx.ext.todo',
              'pyspecific', 'c_annotations',
              'jpsupport']

# General substitutions.
project = 'Python'
copyright = u'1990-%s, Python Software Foundation (translated by Python ドキュメント日本語翻訳プロジェクト)' % time.strftime('%Y')

# The default replacements for |version| and |release|.
#
# The short X.Y version.
# version = '2.6'
# The full version, including alpha/beta/rc tags.
# release = '2.6a0'

# We look for the Include/patchlevel.h file in the current Python source tree
# and replace the values accordingly.

# JP: ../Include が無いので patchlevel モジュールを使わない
#import patchlevel
#version, release = patchlevel.get_version_info()
version, release = '2.7', '2.7.x'

language = 'ja'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = u'%Y年 %m月 %d日'

# List of files that shouldn't be included in the build.
exclude_patterns = [
    'maclib/scrap.rst',
    'library/xmllib.rst',
    'library/xml.etree.rst',
    'refs',
    'tools',
]

# Require Sphinx 1.2 for build.
needs_sphinx = '1.3'


# Options for HTML output
# -----------------------

html_theme = 'default'
html_theme_options = {'collapsiblesidebar': True}

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# JP: 英語の日付フォーマットから変更
html_last_updated_fmt = '%Y-%m-%d'

# Path to find HTML templates.
templates_path = ['tools/templates']

# Custom sidebar templates, filenames relative to this file.
html_sidebars = {
    'index': 'indexsidebar.html',
}

# Additional templates that should be rendered to pages.
html_additional_pages = {
    #'download': 'download.html',
    'index': 'indexcontent.html',
}

# Output an OpenSearch description file.
html_use_opensearch = 'https://docs.python.org/'

# Additional static files.
html_static_path = ['tools/static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'python' + release.replace('.', '')

# Split the index
html_split_index = True


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
_stdauthor = r'Guido van Rossum\\and the Python development team'
latex_documents = [
    ('c-api/index', 'c-api.tex',
     'The Python/C API', _stdauthor, 'manual'),
    ('distributing/index', 'distributing.tex',
     'Distributing Python Modules', _stdauthor, 'manual'),
    ('extending/index', 'extending.tex',
     'Extending and Embedding Python', _stdauthor, 'manual'),
    ('installing/index', 'installing.tex',
     'Installing Python Modules', _stdauthor, 'manual'),
    ('library/index', 'library.tex',
     'The Python Library Reference', _stdauthor, 'manual'),
    ('reference/index', 'reference.tex',
     'The Python Language Reference', _stdauthor, 'manual'),
    ('tutorial/index', 'tutorial.tex',
     'Python Tutorial', _stdauthor, 'manual'),
    ('using/index', 'using.tex',
     'Python Setup and Usage', _stdauthor, 'manual'),
    ('faq/index', 'faq.tex',
     'Python Frequently Asked Questions', _stdauthor, 'manual'),
    ('whatsnew/' + version, 'whatsnew.tex',
     'What\'s New in Python', 'A. M. Kuchling', 'howto'),
]
# Collect all HOWTOs individually
latex_documents.extend(('howto/' + fn[:-4], 'howto-' + fn[:-4] + '.tex',
                        '', _stdauthor, 'howto')
                       for fn in os.listdir('howto')
                       if fn.endswith('.rst') and fn != 'index.rst')

# Additional stuff for the LaTeX preamble.
latex_preamble = r'''
\authoraddress{
  \strong{Python Software Foundation}\\
  Email: \email{docs@python.org}
}
\let\Verbatim=\OriginalVerbatim
\let\endVerbatim=\endOriginalVerbatim
'''

# Documents to append as an appendix to all manuals.
latex_appendices = ['glossary', 'about', 'license', 'copyright']

# Get LaTeX to handle Unicode correctly
latex_elements = {'inputenc': r'\usepackage[utf8x]{inputenc}', 'utf8extra': ''}


# Options for Epub output
# -----------------------

epub_author = 'Python Documentation Authors'
epub_publisher = 'Python Software Foundation'


# Options for the coverage checker
# --------------------------------

# The coverage checker will ignore all modules/functions/classes whose names
# match any of the following regexes (using re.match).
coverage_ignore_modules = [
    r'[T|t][k|K]',
    r'Tix',
    r'distutils.*',
]

coverage_ignore_functions = [
    'test($|_)',
]

coverage_ignore_classes = [
]

# Glob patterns for C source files for C API coverage, relative to this directory.
coverage_c_path = [
    '../Include/*.h',
]

# Regexes to find C items in the source files.
coverage_c_regexes = {
    'cfunction': (r'^PyAPI_FUNC\(.*\)\s+([^_][\w_]+)'),
    'data': (r'^PyAPI_DATA\(.*\)\s+([^_][\w_]+)'),
    'macro': (r'^#define ([^_][\w_]+)\(.*\)[\s|\\]'),
}

# The coverage checker will ignore all C items whose names match these regexes
# (using re.match) -- the keys must be the same as in coverage_c_regexes.
coverage_ignore_c_items = {
#    'cfunction': [...]
}


# Options for the link checker
# ----------------------------

# Ignore certain URLs.
linkcheck_ignore = [r'https://bugs.python.org/(issue)?\d+',
                    # Ignore PEPs for now, they all have permanent redirects.
                    r'http://www.python.org/dev/peps/pep-\d+']


# Options for extensions
# ----------------------

# Relative filename of the reference count data file.
refcount_file = 'data/refcounts.dat'

# JP: ePub の設定は元の conf.py にはない
# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'Python ドキュメント 日本語訳'
epub_author = u'Python ドキュメント 翻訳プロジェクト'
epub_publisher = epub_author
epub_copyright = u'2010, Pythonドキュメント翻訳プロジェクト'


# gettext
# ---------------
gettext_compact = False
locale_dirs = ["locale"]
language = 'ja'
