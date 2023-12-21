# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# Verifica se está rodando no Read the Docs
on_read_the_docs = os.environ.get('READTHEDOCS') == 'True'

if on_read_the_docs:
    # Define o diretório de saída para o Read the Docs
    html_build_dir = os.path.join(os.environ.get('READTHEDOCS_OUTPUT', ''), 'html')


project = 'Ilha Proibida'
copyright = '2023, Grupo Terra'
author = 'Grupo Terra'
release = '0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt_BR'

# Verificar se estamos rodando no Read the Docs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

html_theme = 'sphinx_rtd_theme'
if on_rtd:
    html_theme = 'default'

html_static_path = ['_static']