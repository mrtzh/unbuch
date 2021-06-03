---
chapter-number: 1
title: A short manual
link-citations: true
reference-section-title: References
---

Below are several features available with the Unbuch setup. Unbuch uses the `pandoc` markdown syntax. Please see the pandoc documentation for details on that.

# Numbered and unnumbered margin notes

To create a side note, use this syntax:[^sidenote1]

[^sidenote1]:
  Aenean id risus at nibh fermentum suscipit vel
  risus. Fusce ornare, ante eget placerat congue.

```
To create a side note, use this syntax:[^sidenote1]

[^sidenote1]: 
  Aenean id risus at nibh fermentum suscipit vel
  risus. Fusce ornare, ante eget placerat congue.
```

To create an unnumbered margin notes, 
prefix the text with `{-}`.[^unnumbered-marginnote]

[^unnumbered-marginnote]:
  {-} Aenean id risus at nibh fermentum suscipit vel
  risus. Fusce ornare, ante eget placerat congue.
  
```
To create an unnumbered margin notes, 
prefix the text with `{-}`.[^unnumbered-marginnote]

[^unnumbered-marginnote]:
  {-} Aenean id risus at nibh fermentum suscipit vel
  risus. Fusce ornare, ante eget placerat congue.
```

# Math formulas

You can use inline and display math environments. These are handled by `pdflatex` when compiling to pdf, and they're handled by `katex` when when displaying html. Use a single `$` for inline math, and a double `$$` for display.

$$ 
  \langle x, y \rangle \le \|x\|\cdot\|y\| 
$$

You can define macros using standard latex syntax in
`templates/shared-macros.tex`. This will rener in both pdf and html. Here is the
use of some such macros:

$$
  \E[X] = \sum_x x\cdot \Pr[X=x]
$$


# Custom environments

Unbuch supports custom numbered and unnumbered environments.

begin-Definition

We call a thing a thing.

end-Definition

Here is an unnumbered environment.

begin+Example

Something else.

end+Example

For this to work property, the environment `Definition` must be defined as a latex macro. For html these are automatically converted to div classes that can be styled via css. 

# Citations

Citations go in the margin where they are cited and also appear at the end of the document.[@hegel]

The syntax for citations is `[@hegel]`. We can also cite multiple papers at once.[@hegel; @nietzsche]. Simply separate multiple citations with a semicolon: `[@hegel; @nietzsche]`. You see that repeated citations are abbreviated to save space.


# Figures and images



Ideally, create images in both SVG and PDF format. Include them by their `.svg` extension. The compiler will figure out to subsitute the pdf version for the pdf compilation. If vector graphics are not available use JPG or PNG. Those are the only other two formats that are supported.

![Fancy plot](assets/perceptron.svg)

This image was included as:

```
![Fancy plot](assets/perceptron.svg)
```

Figures and images can go in the margin.[^logit] 

[^logit]: 
  Here's an image in the margin.
  ![Plot of the logistic loss](assets/logistic_loss.svg)

You can specify the width of a figure by appending something like `{width="50%"}`.

![Half width plot](assets/logistic_loss.svg){width="50%"}

This image was included as:

```
![Half width plot](assets/logistic_loss.svg){width="50%"}
```

# Tables

Tables work just as they would in pandoc markdown. Nothing is different here.

   A   B   C 
  --- --- ---
   1   0   1
   1   0   0
   0   0   1
   1   0   1

  : A table of something

# Cross references

Unbuch offers a minimalistic syntax for cross references. These aren't full-fledged latex cross references and don't work the same way. You can introduce a cross reference at any point by writing `!{counter:name}`. This will assign a number. You can retrieve this number by writing `!{counter:name}` again later on. You can increment the counter by using the same counter multiple times, e.g., by writing `!{theorem:abc}` and `!{theorem:planar}`. Here's an example:s

This markdown snippet will turn out as follows:

!{thm:something}

begin-Theorem

Curabitur at vestibulum velit. Ut ac turpis purus. 

end-Theorem

!{thm:deep}

begin+Theorem

$1 + 1 = 2$

end+Theorem

We saw in Theorem !{thm:deep} that $1+1=2$.


This also works with equations.

!{eq:blah}

$$
1 + 1 = 2\qquad(!{eq:blah})
$$
