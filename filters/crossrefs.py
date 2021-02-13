#!/usr/bin/env python3

"""
Minimal cross references.

Create a reference by writing `@{kind:name}`, e.g., `@{theorem:main}`,
anywhere outside math or code environments.

Use reference with the same syntax, e.g., `Theorem @{theorem:main}`.
Another reference of the form `@{theorem:second}` will increment `theorem`
counter.

Example:

```
Next we're going to see a deep theorem.

@{thm:deep}

begin+Theorem

1 + 1 = 2

end+Theorem

We saw in Theorem @{thm:deep} that $1+1=2$.
```
"""

import re

from pandocfilters import toJSONFilter, Str, Math


crossrefs = {}


def parse(crossrefs, string):
    """Find and parse cross references in a string."""

    number = 1

    match = re.search("@{(.*)}", string)

    if match:
        crossref = match.group(1)

        try:
            kind, name = crossref.split(':')
        except:
            raise ValueError("Reference must be of the form `@{kind:name}`.")

        if kind in crossrefs:
            if name in crossrefs[kind]:
                number = crossrefs[kind][name]
                return crossref, str(number)
            else:
                number = len(crossrefs[kind]) + 1
                crossrefs[kind][name] = number
                # created reference, return empty string
                return crossref, ''
        else:
            crossrefs[kind] = {name : number}
            # created reference, return empty string
            return crossref, ''

    # no match
    return None, None


#pylint: disable=unused-argument
def cross_refs(key, value, fmt, meta):
    """Lookup reference and return number or create reference/number."""

    global crossrefs

    if key == 'Str':
        crossref, string = parse(crossrefs, value)
        if crossref:
            return Str(string)

    if key == 'Math':
        t, s = value
        crossref, string = parse(crossrefs, s)
        if crossref:
            s = s.replace('@{' + crossref + '}', string)
            return Math(t, s)


if __name__ == "__main__":
    toJSONFilter(cross_refs)
