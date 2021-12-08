# -- Project information

project = "Prototype Python Project"
copyright = "2021, Nuno Costa"  # pylint: disable=redefined-builtin
author = "Nuno Costa"

release = "0.4"
version = "0.4.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

#  -- Theme options
# see https://alabaster.readthedocs.io/en/latest/installation.html

html_theme = "alabaster"

html_theme_options = {
    # logo.png should be under docs/source/_static
    # 'logo': 'logo.png',
    "github_user": "91nunocosta",
    "github_repo": "prototype-python-library",
}
