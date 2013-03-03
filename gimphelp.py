#!/usr/bin/env python
"""
Adds functionality to the builtin help function for use in gimp.

The help function in this module can be used to replace the builtin help
function, in addition to the regular functionality of help, it will
automatically generate documentation for a gimp.PDBFunction.

To use simply import help from this function in gimp's python console:
    from gimphelp import help
"""
import textwrap
import gimp
from gimpfu import _obj_mapping


__author__ = "Sean Munkel"
__copyright__ = "Copyright 2013, Sean Munkel"
__license__ = "MIT"
__version__ = "0.2"
__all__ = ["proc_help", "help"]

BASE_DOC_TEMPLATE = "%s\n\n%s\n\n%s"
PARAM_DOC_TEMPLATE = "\n\nParameters\n----------\n%s"
RUNMODE_DOC = "run_mode : int, optional\n    the run mode"
RETURN_DOC_TEMPLATE = "\n\nReturns\n-------\n%s"

#Used to make sure that each line isn't too wide, break_on_hyphens is disabled
#because it can split constants within the parameters description
textwrapper = textwrap.TextWrapper(64, break_on_hyphens=False)


def _format_signature(proc):
    if proc.nparams > 0 and proc.params[0][1] == "run-mode":
        format_str = "%s(%s, run_mode=RUN_INTERACTIVE)"
        params = proc.params[1:]
    else:
        format_str = "%s(%s)"
        params = proc.params

    line_start = len(proc.proc_name) + 1
    args = ", ".join(param[1].replace("-", "_") for param in params)
    signature = format_str % (proc.proc_name, args)
    #Set the subsequent indent to have the function parameters line up correctly
    textwrapper.subsequent_indent = " " * line_start
    wrapped = textwrapper.fill(signature)
    textwrapper.subsequent_indent = ""
    return wrapped


def _format_params(params, template):
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

    # Setup indentation for the parameter descriptions
    textwrapper.initial_indent = "    "
    textwrapper.subsequent_indent = "    "

    for param_type, param_name, param_desc in params:
        param_items = [param_name.replace("-", "_"), "\n"]
        # The type information and description will only be added to the
        # documentation if they are both valid and useful.
        if param_type in _obj_mapping:
            type_name = " : " + _obj_mapping[param_type].__name__
            if type_name == "int" and param_desc.endswith("{ TRUE, FALSE }"):
                type_name = "bool"
                #Remove the { TRUE, FALSE } part of the description
                param_desc = param_desc[:-16]
            param_items.insert(1, type_name)
        if param_desc != "":
            param_desc = textwrapper.fill(param_desc) + "\n"
            param_items.append(param_desc)
        param_docs.append("".join(param_items))

    doc = template % ("".join(param_docs))

    # Restore the indentation just to be safe, even if it isn't used again.
    textwrapper.initial_indent = ""
    textwrapper.subsequent_indent = ""

    if has_run_mode:
        doc += RUNMODE_DOC
    return doc


def proc_help(proc):
    """ Returns a docstring for a gimp procedure. """
    signature = _format_signature(proc)
    proc_help = textwrapper.fill(proc.proc_help)
    proc_blurb = textwrapper.fill(proc.proc_blurb)
    base_doc = BASE_DOC_TEMPLATE % (signature, proc_blurb, proc_help)
    param_doc = _format_params(proc.params, PARAM_DOC_TEMPLATE)
    return_doc = _format_params(proc.return_vals, RETURN_DOC_TEMPLATE)

    print(base_doc + param_doc + return_doc)


def help(item):
    if isinstance(item, type(gimp.pdb.plug_in_blur)):
        proc_help(item)
    else:
        __builtins__.help(item)
