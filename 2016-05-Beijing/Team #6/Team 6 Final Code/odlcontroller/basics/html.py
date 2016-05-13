# WIP

from __future__ import print_function as _print_function
from basics import render
import sys

_bindings = {}

_escape_table = {
     "&": "&amp;",
     '"': "&quot;",
     "'": "&apos;",
     ">": "&gt;",
     "<": "&lt;",
     "\n": "<BR/>\n",
     "\t": "&nbsp;&nbsp;&nbsp;&nbsp;",
     }

def escape(text):
    text = text.replace("    ", "\t")
    return "".join(_escape_table.get(c, c) for c in text)
 
def print_html(*args, **kwargs):
    first_type = type(next(iter(args)))
    homogeneous = all(isinstance(arg, first_type) for arg in args)
    if homogeneous and first_type in _bindings:
        _bindings[first_type](*args, **kwargs)
    else:
        sep = kwargs.pop("sep", ' ')
        end = kwargs.pop("end", '\n')
        fp = kwargs.pop("file", sys.stdout)
        def write(data):
            fp.write(escape(str(data)))
        for i, arg in enumerate(args):
            if i:
                write(sep)
            if type(arg) in _bindings:
                _bindings[first_type](*args, file=fp, sep=None, end=None)
            else:
                write(arg)
        write(end)

def html_bind(arg_type, print_fn):
    _bindings[arg_type] = print_fn

def enable():
    render.printr = print_html
