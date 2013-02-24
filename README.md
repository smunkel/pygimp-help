pygimp-help
===========

When using the python console in gimp the `help()` function doesn't provide much helpful information for pdb functions. Rather than using the regular procedure browser to look up the documentation for a procedure, you can use this `help()` replacement. Here is a sample of the output for the `plug-in-tile` procedure:


    plug_in_tile(image, drawable, new_width,
                 new_height, new_image, run_mode=RUN_INTERACTIVE)

    Create an array of copies of the image

    This function creates a new image with a single layer sized to
    the specified 'new_width' and 'new_height' parameters.  The
    specified drawable is tiled into this layer.  The new layer will
    have the same type as the specified drawable and the new image
    will have a corresponding base type.

    Parameters
    ----------
    image : Image
        Input image (unused)
    drawable : Drawable
        Input drawable
    new_width : int
        New (tiled) image width
    new_height : int
        New (tiled) image height
    new_image : int
        Create a new image?
    run_mode : int, optional
        the run mode

    Returns
    -------
    new_image : Image
        Output image (-1 if new-image == FALSE)
    new_layer : Layer
        Output layer (-1 if new-image == FALSE)
        
To use this simply import the custom `help()` function from this module when you start the console:

    from gimphelp import help        

License
-------

Copyright (C) 2013 Sean Munkel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
