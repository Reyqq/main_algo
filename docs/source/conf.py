# -*- coding: utf-8 -*-
import os
import sys
import pydata_sphinx_theme # Убедись, что он установлен

# -- Path setup --------------------------------------------------------------
# Добавляем путь к папке с кодом (src), которая на два уровня выше source/
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
project = 'ez_prof'
copyright = '2025, Reyqq' # Исправлено имя пользователя
author = 'Reyqq'
release = '0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Импорт документации из docstrings
    'sphinx.ext.viewcode',     # Ссылки на исходный код
    'sphinx.ext.napoleon',     # Поддержка Google/NumPy style docstrings
    'sphinx.ext.githubpages',  # Помощь для GitHub Pages
    #'sphinx.ext.autosectionlabel', # Раскомментируй, если нужно
    'sphinx.ext.autosummary',  # Генерация сводок (может требовать настройки)
    #'sphinx_autodoc_typehints', # Используй sphinx.ext.autodoc.typehints вместо этого? (Добавлено ниже)
    'sphinx.ext.autodoc.typehints', # Обработка аннотаций типов
    'sphinx_copybutton',       # Кнопка копирования для блоков кода
]

# Napoleon settings (если используешь Google/NumPy стиль docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Autodoc settings
autodoc_member_order = 'bysource' # Порядок членов как в исходном коде
autodoc_typehints = "description" # Показывать типы в описании, не в сигнатуре
#autodoc_typehints_format = "short" # Показывать короткие имена типов

templates_path = ['_templates']
exclude_patterns = []
language = 'ru'
source_encoding = 'utf-8-sig' # Кодировка исходных .rst файлов

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static'] # Папка для статических файлов (CSS, JS) внутри source/

# Theme options specific to pydata-sphinx-theme
html_theme_options = {
    "navbar_align": "left",
    "navigation_depth": 4,
    "show_toc_level": 2,
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version", "theme-version"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Reyqq/main_algo", # URL твоего репозитория
            "icon": "fab fa-github-square", # Иконка FontAwesome
        },
    ],
    "use_edit_page_button": True, # Кнопка "Редактировать на GitHub"
    "show_nav_level": 2,
    "collapse_navigation": False,
}

# Context for "Edit on GitHub" button
html_context = {
    "github_user": "Reyqq",
    "github_repo": "main_algo",
    "github_version": "main", # Имя основной ветки
    "doc_path": "docs/source", # Путь к папке source/ относительно корня репо
}

# -- Options for autosectionlabel ------------------------------------------
# Раскомментируй, если используешь 'sphinx.ext.autosectionlabel'
# autosectionlabel_prefix_document = True
