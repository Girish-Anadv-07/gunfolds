# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import ast

def extract_function_names(file_path):
    function_names=[]
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
    return function_names

with open("tools.rst", "w") as rst_file:
            s="tools package"
            print(s,file=rst_file)
            print(len(s)*"=",file=rst_file)
            print(".. toctree::\n",file=rst_file)
            l=os.listdir("../tools")
            l.sort()
            for filename in l:
                if filename.endswith(".py") and not filename.endswith("__.py"): 
                    print("   ",filename[:-3],file=rst_file)
                    
for filename in os.listdir("../tools"):
    if filename.endswith(".py") and not filename.endswith("__.py"): 
        module = filename[:-3]       
        with open(module+".rst", "w") as rst_file:
            print(module,file=rst_file)
            print(len(module)*"=",file=rst_file)
            print(".. currentmodule:: gunfolds.tools."+module,file=rst_file)
            print("\n",file=rst_file)
            file_path="../tools"
            function_names = extract_function_names(file_path+"/"+filename)
            function_names.sort()
            for func in function_names:
                funct = ""
                for c in func:
                    if c=="_":
                        funct+="\\"
                        funct+=c
                    else:
                        funct+=c
                print(funct,file=rst_file)
                print(len(funct)*"-",file=rst_file)
                print(".. autofunction:: gunfolds.tools."+module+"."+func,file=rst_file)
                print("\n",file=rst_file)
                
sys.path.insert(0,os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

project = 'gunfolds'
copyright = 'neuroneural.net'
author = 'neuroneural.net'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.ifconfig"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
