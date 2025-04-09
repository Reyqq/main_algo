import os
import sys
# Добавляем путь к папке с кодом проекта
sys.path.insert(0, os.path.abspath('../../code')) # <-- ИЗМЕНИ ПУТЬ, если нужно
# Или просто к корню проекта, если модули там
# sys.path.insert(0, os.path.abspath('../..'))

project = 'v'
copyright = '2025, r'
author = 'r'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  'sphinx.ext.githubpages',
  'sphinx.ext.autodoc',
  'sphinx.ext.napoleon',
  'sphinx.ext.viewcode',
  'myst_parser',
  'pydata-sphinx-theme'
  ]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}


html_theme = 'pydata-sphinx-theme'
html_static_path = ['_static']
