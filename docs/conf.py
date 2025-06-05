# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../dh-platform'))  # Путь к вашему пакету

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Для поддержки Google-style
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx_copybutton'
]

# Настройки для autodoc
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
}

html_theme = 'sphinx_rtd_theme'  # Тема ReadTheDocs

project = 'DH|Platform'
copyright = '2025, JohnSoi'
author = 'JohnSoi'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
