#!/usr/bin/env python3

"""
Minimalistic filter to enable Tufte style sidenotes.

The filter replaces the pandoc internal Note token by suitable html tags to be
used with tufte.css.

Example usage in markdown:

This is a first paragraph.[^note1]

[^note1]:
  {-} This is an unnumbered margin note.

This is a second paragraph.[^note2]

[^note2]:
  This is a numbered sidenote.
"""

from pandocfilters import toJSONFilter, RawInline


sidenote_count = 0


def html(string):
    """Return inline html element."""
    return RawInline('html', string)


def latex(string):
    """Return inline latex element."""
    return RawInline('latex', string)


def sidenote_html(key, value):
    """Replace `Note` token with html code and incremnt counter."""

    if key == 'Note':
        contents = value[0]['c']
        pre = '<span>'
        post = '</span></span>'

        if contents[0]['c'] == '{-}':
            pre += '<span class="marginnote">'
            return [html(pre)] + contents[1:][1:] + [html(post)]

        global sidenote_count
        pre += ('<label for="sn-%d" class="margin-toggle sidenote-number"></label>'
                % sidenote_count)
        pre += ('<input type="checkbox" id="sn-%d" class="margin-toggle" />'
                % sidenote_count)
        pre += '<span class="sidenote">'
        sidenote_count += 1
        return  [html(pre)] + contents + [html(post)]


def sidenote_latex(key, value):
    """Replace `Note` token with latex code if note is unnumbered.

    Labeled sidenotes become footnotes and are automatically handled by the
    Tufte latex package."""

    if key == 'Note':
        contents = value[0]['c']
        if contents[0]['c'] == '{-}':
            return [latex('\\marginnote{')] + contents[1:][1:] + [latex('}')]


#pylint: disable=unused-argument
def sidenote(key, value, fmt, meta):
    """Select action based on format."""

    if fmt == 'html5':
        return sidenote_html(key, value)

    if fmt == 'latex':
        return sidenote_latex(key, value)


if __name__ == "__main__":
    toJSONFilter(sidenote)
