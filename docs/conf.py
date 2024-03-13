# Configuration file for the Sphinx documentation builder.

import os
import sys
# import sphinx_copybutton

# -- Project information

project = 'DiSH'
copyright = '2024, Miskov-Zivanov Lab (MeLoDy lab)'
author = 'Khaled Sayed'

release = '2024'
version = 'Latest'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
