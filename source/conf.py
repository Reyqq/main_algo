import os
import sys
import bokeh
import pandas
import numpy
import typing
sys.path.insert(0, os.path.abspath('../../code'))

project = 'Vlad'
copyright = '2025, Reyqq'
author = 'Reyqq'
release = '1.0'


import pydata_sphinx_theme

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc.typehints',
    'sphinx_copybutton',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
]


autosectionlabel_prefix_document = True
source_encoding = 'utf-8-sig'
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'


html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    "navbar_align": "left",
    "navigation_depth": 4,
    "show_toc_level": 2,
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Reyqq/main_algo",
            "icon": "fab fa-github-square",
        },
    ],
    "use_edit_page_button": True,
    "show_nav_level": 2,
    "collapse_navigation": False,
}



html_context = {
    "github_user": "Reyqq",
    "github_repo": "main_algo",
    "github_version": "master",
    "doc_path": "docs/source/",
}

master_doc = 'index'

html_static_path = ['source/_static']

