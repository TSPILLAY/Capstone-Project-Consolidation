# Configuration file for the Sphinx documentation builder.
import os
import sys
import django

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'news_project'
copyright = '2026, TPILLAY'
author = 'TPILLAY'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'
django.setup()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
