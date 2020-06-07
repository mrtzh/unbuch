#!/usr/bin/env python3

"""
Minimalistic filter to enable Tufte style sidenotes.

The filter replaces the pandoc internal Note token by suitable html tags to be
used with tufte.css.
"""

from pandocfilters import toJSONFilter, RawInline


sidenote_count = 0


def html(x):
    return RawInline('html', x)


def sidenote(key, value, fmt, meta):
    """Replace `Note` token with html code and incremnt counter."""

    global sidenote_count
    pre = '<span>'
    pre += ('<label for="sn-%d" class="margin-toggle sidenote-number"></label>'
              % sidenote_count)
    pre += ('<input type="checkbox" id="sn-%d" class="margin-toggle" />'
              % sidenote_count)
    pre += '<span class="sidenote">'
    post = '</span></span>'

    if key == 'Note':
      sidenote_count += 1
      return  [html(pre)] + value[0]['c'] + [html(post)]


if __name__ == "__main__":
    toJSONFilter(sidenote)
