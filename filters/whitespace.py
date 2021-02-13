#!/usr/bin/env python3

"""
Replace regular whitespace before inline math with space symbol to avoid line
breaks before math symbols.

Example:

Consider the string `a vector $u$`. This filter will automatically convert the
whitespace between `vector` and `$u$` to `~` when compiling to Latex and to the
HTML code `&nbsp;` when compiling to html5.
"""

from pandocfilters import toJSONFilter, RawInline


def match_orphan(first, second, third):
    """Matches on potential for orphan."""
    if first['t'] == 'Str' and second['t'] == 'Space' and third['t'] == 'Math':
        if third['c']:
            return third['c'][0]['t'] == 'InlineMath'
    return False


def eat_orphans(tokens, fmt):
    """Match and process potential orphans."""
    if len(tokens) < 3:
        return tokens, []

    if match_orphan(tokens[0], tokens[1], tokens[2]):
        if fmt == 'html5':
            return [tokens[0], RawInline('html', '&nbsp;')], tokens[2:]
        if fmt == 'latex':
            return [tokens[0], RawInline('latex', '~')], tokens[2:]
    return [tokens[0]], tokens[1:]


#pylint: disable=unused-argument
def orphans(key, value, fmt, meta):
    """Search paragraphs for potential orphans."""

    if key == 'Para':
        remaining_tokens = value
        processed_tokens = []
        while remaining_tokens:
            processed, remaining_tokens = eat_orphans(remaining_tokens, fmt)
            processed_tokens += processed
        return {'t' : 'Para', 'c' : processed_tokens}


if __name__ == "__main__":
    toJSONFilter(orphans)
