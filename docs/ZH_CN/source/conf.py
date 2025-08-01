# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import logging
import os
import sys
from typing import List

from sphinx.ext import autodoc
import sphinxcontrib.redoc


logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "Lightx2v"
copyright = "2025, Lightx2v Team"
author = "the Lightx2v Team"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "myst_parser",
    "sphinxarg.ext",
    "sphinxcontrib.redoc",
    "sphinxcontrib.openapi",
]

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
]

html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = ["**/*.template.rst"]

# Exclude the prompt "$" when copying code
copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = project
html_theme = "sphinx_book_theme"
# html_theme = 'sphinx_rtd_theme'
html_logo = "../../../assets/img_lightx2v.png"
html_theme_options = {
    "path_to_docs": "docs/ZH_CN/source",
    "repository_url": "https://github.com/ModelTC/lightx2v",
    "use_repository_button": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# Generate additional rst documentation here.
def setup(app):
    # from docs.source.generate_examples import generate_examples
    # generate_examples()
    pass


# Mock out external dependencies here.
autodoc_mock_imports = [
    "cpuinfo",
    "torch",
    "transformers",
    "psutil",
    "prometheus_client",
    "sentencepiece",
    "lightllmnumpy",
    "tqdm",
    "tensorizer",
]

for mock_target in autodoc_mock_imports:
    if mock_target in sys.modules:
        logger.info(
            "Potentially problematic mock target (%s) found; autodoc_mock_imports cannot mock modules that have already been loaded into sys.modules when the sphinx build starts.",
            mock_target,
        )


class MockedClassDocumenter(autodoc.ClassDocumenter):
    """Remove note about base class when a class is derived from object."""

    def add_line(self, line: str, source: str, *lineno: int) -> None:
        if line == "   Bases: :py:class:`object`":
            return
        super().add_line(line, source, *lineno)


autodoc.ClassDocumenter = MockedClassDocumenter

navigation_with_keys = False
