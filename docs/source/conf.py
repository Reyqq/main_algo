import os
import sys
import pydata_sphinx_theme
sys.path.insert(0, os.path.abspath('../../code'))

project = 'ez_prof'
copyright = '2025, Reyqqq'
author = 'Reyqq'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

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

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

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
    "github_version": "main",
    "doc_path": "docs/source/",
}