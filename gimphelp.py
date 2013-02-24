#!/usr/bin/env python
"""
Adds functionality to the builtin help function for use in gimp.

The help function in this module can be used to replace the builtin help function,
in addition to the regular functionality of help, it will automatically generate
documentation for a gimp.PDBFunction. 

To use simply import help from this function in gimp's python console:
    from gimphelp import help
"""
import textwrap
import gimp
from gimpfu import _obj_mapping


__author__ = "Sean Munkel"
__copyright__ = "Copyright 2013, Sean Munkel"
__license__ = "MIT"
__version__ = "0.1"

BASE_DOC_TEMPLATE = "%s\n\n%s\n\n%s"
PARAM_DOC_TEMPLATE = "\n\nParameters\n----------\n%s"
RUNMODE_DOC = "run_mode : int, optional\n    the run mode"
RETURN_DOC_TEMPLAYE = "\n\nReturns\n-------\n%s"


def format_signature(proc):
    if proc.nparams > 0 and proc.params[0][1] == "run-mode":
        format_str = "%s(%s, run_mode=RUN_INTERACTIVE)"
        params = proc.params[1:]
    else:
        format_str = "%s(%s)"
        params = proc.params
        
    line_start = len(proc.proc_name) + 1
    args = ", ".join(param[1].replace("-", "_") for param in params)
    signature = format_str % (proc.proc_name, args)
    joiner = "\n" + " " * line_start

    return joiner.join(textwrap.wrap(signature, 64 - line_start))


def format_params(params, template):
    if len(params) == 0:
        return ""

    param_docs = []
    # pygimp will accept the run_mode as a keyword argument, so there must
    # be a check to see if a procedure has one.
    if params[0][1] == "run-mode":
        has_run_mode = True
        params = params[1:]
    else:
        has_run_mode = False

    for param_type, param_name, param_desc in params:
        param_items = [param_name.replace("-", "_"), "\n"]
        # The type information and description will only be added to the 
        # documentation if they are both valid and useful.
        if param_type in _obj_mapping:
            type_name = " : " + _obj_mapping[param_type].__name__
            param_items.insert(1, type_name)
        if param_desc != "":
            param_desc_lines = textwrap.wrap(param_desc, 60)
            param_items.append("    %s\n" % "\n    ".join(param_desc_lines))
        param_docs.append("".join(param_items))
        
    doc = template % ("".join(param_docs))

    if has_run_mode:
        doc += RUNMODE_DOC
    return doc


def proc_help(proc):
    """ Returns a docstring for a gimp procedure. """
    signature = format_signature(proc)
    proc_help = textwrap.fill(proc.proc_help, 64)
    base_doc = BASE_DOC_TEMPLATE % (signature, proc.proc_blurb, proc_help)
    param_doc = format_params(proc.params, PARAM_DOC_TEMPLATE)
    return_doc = format_params(proc.return_vals, RETURN_DOC_TEMPLAYE)

    return "".join([base_doc, param_doc, return_doc])


def help(*args, **kwargs):
    if isinstance(args[0], type(gimp.pdb.plug_in_blur)):
        print(proc_help(args[0]))
    else:
        __builtins__.help(*args, **kwargs)
