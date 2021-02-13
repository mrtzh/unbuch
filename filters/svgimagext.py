#!/usr/bin/env python3

"""
Remove '.svg' image extension. This can be useful when markdown sources feed
into both latex and html compilation. This filter will remove the .svg extension
from an image source file name before feeding a file into pdflatex. This allows
pdflatex's smart extension mechanism to look for alternatives to svg, such as,
.png, .pdf.
"""

from pandocfilters import toJSONFilter, Image


#pylint: disable=unused-argument
def svgimagext(key, value, fmt, meta):
    """Lookup reference and return number or create reference/number."""

    if key == 'Image' and fmt == 'latex':

        head, caption, [dest, typedef] = value

        if dest[-4:] == '.svg':
            return Image(head, caption, [dest[:-4], typedef])

        return Image(head, caption, [dest, typedef])


if __name__ == "__main__":
    toJSONFilter(svgimagext)
