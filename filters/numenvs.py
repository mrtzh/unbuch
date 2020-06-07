#!/usr/bin/env python3

"""
Simple pandoc filter to create flexible environments in markdown. Style of
environments controlled via latex environment definitions or css for html.

Numbered theorem environment example:

  begin-Theorem

  $2+2=4$

  end-Theorem

Unnumered environment:

  begin+Example

  This.

  end+Example

The `begin` and `end` statements must be at the beginning of new paragraph.
"""

from pandocfilters import toJSONFilter, RawBlock


env_counts = {}


def html(x):
  return RawBlock('html', x)


def latex(x):
  return RawBlock('latex', x)


def parse_env_latex(key, value):
  """Parse paragraph opening to extract environment name."""
  if key == 'Para':
    if len(value) >= 1:
      content = value[0]['c']
      if content[:6] == 'begin+' or content[:6] == 'begin-':
        return 'begin', content[6:]
      if content[:4] == 'end-' or content[:4] == 'end+':
        return 'end', content[4:]
  return '', ''


def parse_env_html(key, value):
  """Parse paragraph opening to extract environment name."""
  if key == 'Para':
    if len(value) >= 1:
      content = value[0]['c']
      if content[:6] == 'begin-':
        global env_counts
        name = content[6:]
        if name in env_counts:
          env_counts[name] += 1
        else:
          env_counts[name] = 1
        return 'begin', name, env_counts[name]
      if content[:6] == 'begin+':
        name = content[6:]
        return 'begin', name, None
      if content[:4] == 'end-' or content[:4] == 'end+':
        return 'end', content[4:], None
  return '', '', None


def num_envs_latex(key, value, fmt, meta):
  """Create numbered divs environments."""
  instr, label = parse_env_latex(key, value)
  if instr == 'begin':
    return latex('\\begin{%s}\n' % label)
  if instr == 'end':
    return latex('\\end{%s}\n' % label)


def num_envs_html(key, value, fmt, meta):
  """Create numbered divs environments."""
  instr, label, num = parse_env_html(key, value)
  if instr == 'begin':
    if num:
      title = label + ' ' + str(num)
    else:
      title = label
    return [html('<div class="numenv %s">' % label),
            html('<span class="numenv %s title">%s.</span>' % (label, title))]
  if instr == 'end':
    return html('</div>')


def num_envs(key, value, fmt, meta):
  """Select action based on format."""
  if fmt == 'html5':
    return num_envs_html(key, value, fmt, meta)
  elif fmt == 'latex':
    return num_envs_latex(key, value, fmt, meta)
  else:
    return None


if __name__ == "__main__":
    toJSONFilter(num_envs)
