# -*- coding: utf-8 -*-
#
# Documentation build configuration file, created by
# sphinx-quickstart on Wed Jun  1 22:56:43 2011.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
#extensions = ['sphinx.ext.autodoc', 'sphinx.ext.pngmath']
extensions = ['sphinx.ext.autodoc', 'mathjax', 'sphinxcontrib.bibtex', 'sphinx.ext.todo']
numfig = True

# mathjax_path is based on http://www.mathjax.org/docs/2.0/start.html
mathjax_path = "http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# Show todo notes (default is false)
# Set to false before handing in the report!
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'IEA EBC Annex 60'
copyright = u'(c) All rights reserved'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'sphinxdoc'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "IEA EBC Annex 60"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = 'img/LBNL.gif'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Documentation'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '10pt' # 10 points per the EBC style guide

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index',
   'final_report.tex',
   u'IEA EBC Annex 60',
   u'Final Report', 'manual'),
]


##latex_elements = {'fontpkg': '\\usepackage[scaled]{helvet}',
##                  'fontpkg': '\\renewcommand*\\familydefault{\\sfdefault}'}
latex_elements = {'babel': '\\usepackage[english]{babel}', \
                  'releasename': 'Final Report', \
				  'geometry': '\\usepackage[margin=0.75in, paperwidth=6in, paperheight=9in, includehead, includefoot, centering]{geometry}'}


# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '_static/ebc-logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_use_parts = False


# Additional stuff for the LaTeX preamble.
latex_elements['preamble'] = r'''
% Format of chapter fonts
\makeatletter
\ChNameVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\ChNumVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\ChTitleVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\makeatother


\usepackage[scaled]{helvet}
\usepackage[T1]{fontenc}
\titleformat*{\section}{\Large\sffamily}
\titleformat*{\subsection}{\large\sffamily}
\titleformat*{\subsubsection}{\sffamily}
\titleformat*{\paragraph}
  {\rmfamily\slshape}
  {}{}{}
  \titlespacing{\paragraph}
  {0pc}{1.5ex minus .1 ex}{0pc}

\renewcommand\familydefault{\sfdefault} 
\renewcommand{\baselinestretch}{1.1}


% Reduce the list spacing
\usepackage{enumitem}
\setlist{nosep} % or \setlist{noitemsep} to leave space around whole list

% This allows adding :cite: in the label of figures.
% It is a work-around for https://github.com/mcmtroffaes/sphinxcontrib-bibtex/issues/92
\usepackage{etoolbox}
\AtBeginEnvironment{figure}{\renewcommand{\phantomsection}{}}


% Set format to 6x9 inches for report to be printed as a book.
% see sphinx elements['geometry'] new in sphinx 1.5


\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}


\setcounter{secnumdepth}{3}
\usepackage{amssymb,amsmath}

% Figure and table caption in italic fonts
\makeatletter
\renewcommand{\fnum@figure}[1]{\small \textit{\figurename~\thefigure}: \it }
\renewcommand{\fnum@table}[1]{\small \textit{\tablename~\thetable}: \it }
\makeatother

% The next two lines patch the References title
\usepackage{etoolbox}
\patchcmd{\thebibliography}{\chapter*}{\phantom}{}{}

\definecolor{TitleColor}{rgb}{0 ,0 ,0} % black rathern than blue titles

\renewcommand{\Re}{{\mathbb R}}
\newcommand{\Na}{{\mathbb N}}
\newcommand{\Z}{{\mathbb Z}}

\usepackage{listings}
% see: http://mirror.aarnet.edu.au/pub/CTAN/macros/latex/contrib/listings/listings-1.3.pdf
\lstset{%
  basicstyle=\small, % print whole listing small
  keywordstyle=\color{red},
  identifierstyle=, % nothing happens
  commentstyle=\color{blue}, % white comments
  stringstyle=\color{OliveGreen}\it, % typewriter type for strings
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny,
  numbersep=5pt} % no special string space

\lstset{
    frame=single,
    breaklines=true,
    postbreak=\raisebox{0ex}[0ex][0ex]{\ensuremath{\color{red}\hookrightarrow\space}}
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\lstdefinelanguage{Modelica}{%
  morekeywords={Thermal,HeatTransfer,Interfaces, flow, %
    SI,Temperature,HeatFlowRate,HeatPort},
  morecomment=[l]{//},
  morecomment=[s]{/*}{*/},
  morestring=[b]",
  emph={equation, partial, connector, model, public, end, %
    extends, parameter}, emphstyle=\color{blue},
}


\usepackage{xcolor}
\usepackage{sectsty}
\definecolor{ebc}{rgb}{0.917, 0.463, 0.220}
\chapterfont{\color{ebc}}  % sets colour of chapters

'''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True
