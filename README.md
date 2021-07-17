# Unbuch

A simple pandoc setup to compile a book from markdown sources into html pages and pdf.

Features:

* Tufte-inspired layout with sidenotes
* Latex formulas via katex plugin
* Custom Environments
* Cross references
* HTML pages, individual PDF chapters, PDF book

## Examples of major projects in Unbuch

* [Patterns, Predictions, and Actions](https://mlstory.org)
* [Fairness and Machine Learning](https://fairmlbook.org)

## Getting started

1. Install [pandoc](https://pandoc.org/) **v2.14** (exact version requirement)
2. Make sure you have python 3.5+ installed. 
3. Clone the repository.
4. Install dependencies with `pip3 install -r requirements.txt`.
5. Customize your book by setting up variables in `Makefile`.
6. Type `make` to build both pdf and html files.
  - To build html only, type `make html`.
  - To build pdf only, type `make pdf`.

Find the compiled results in `publish/` directory.

## Dependencies

- `pandoc` 2.5+
- `pandoc-citeproc` 0.15+
- `python` 3.5 or higher
- For generating PDFs, you'll need `pdflatex`, which usually ships with LaTeX distributions.

Note: Every new release of `pandoc` since version 2.10 has broken the compile process due to changes in the way that pandoc handles citations. Getting things to run with a different version of `pandoc` is certainly possible, but may require changes, primarily to the latex template located at `templates/book.tex`. The issue is typically with the latex environments related to `cslreferences`. Copy and paste from the latex template corresponding to your pandoc version as is necessary.  

## Special files and folders

* `assets` -- Put all files linked to from the sources here
* `css` -- All css files. NO NEED TO EDIT.
* `filters` -- Custom pandoc filters. NO NEED TO EDIT.
* `sources` -- This is where the source markdown files live. Go here to edit.
* `templates` -- Pandoc template files. NO NEED TO EDIT.
* `publish` -- Contains compiled pages and pdfs ready for publishing. DO NOT EDIT.

## Credits

The setup is based on:

* [tufte-pandoc-css](https://github.com/jez/tufte-pandoc-css)
* [tufte-css](https://github.com/edwardtufte/tufte-css)
* [pandoc-sidenote](https://github.com/jez/pandoc-sidenote)

## Current issues

See `Issues` tab for current issues and ways of contributing to the project.

Thank you.

# Usage manual

Scroll through the markdown files in `sources/` to get a sense for how this
works. Below is additional documentation.

## Basic workflow

1. Edit one of the source markdown files in `sources/`
2. Type `make` to produce all output in `publish/`

## Compiling

* `make` to compile all sources into `publish/` directory. This will compile
all chapters as html and pdf, as well as the whole book as pdf.

* `make -j8` to compile in parallel.

* `make publish/pdf/chaptername.pdf` to compile individual pdf chapter

* `make publish/chaptername.html` to compile individual html name


## Side notes and margin notes

Example usage in markdown:

```
This is a first paragraph.[^note1]

[^note1]:
  {-} This is an unnumbered margin note.

This is a second paragraph.[^note2]

[^note2]:
  This is a numbered sidenote.
```

## Custom environments

Numbered theorem environment example:

```
  begin-Theorem

  $2+2=4$

  end-Theorem
```

The environment `Theorem` must be defined in latex macros at `templates/macros.sty`.

Unnumered environment:

```
  begin+Example

  This.

  end+Example
```

The `begin` and `end` statements must be at the beginning of a new paragraph each.

## Cross references

Create a reference by writing `!{kind:name}`, e.g., `!{theorem:main}`,
anywhere outside math or code environments.

Use reference with the same syntax, e.g., `Theorem !{theorem:main}`.
Another reference of the form `!{theorem:second}` will increment `theorem`
counter.

Example:

```
Next we're going to see a deep theorem.

!{thm:deep}

begin+Theorem

$1 + 1 = 2$

end+Theorem

We saw in Theorem !{thm:deep} that $1+1=2$.
```

NOTE: This way of doing references is NOT equivalent to the way pdflatex does it. In particular, references don't automatically match to the correct number of the Theorem environment. Instead every numbered theorem has to be prefixed with an `!{thm:name}` expression for this to work.

## Math formulas

Math macros can be defined in `templates/shared-macros.tex`. When compiling from markdown to html, these will be inserted at the top of the markdown file and interpreted by `pandoc` for use with `katex`. When compiling to pdf, these will be interpreted by `pdflatex`.

## Images

Ideally, create images in both SVG and PDF format. Place two files `image.pdf` and `image.svg` in the `assets/` directory. Include the image by its `.svg` extension. 

```
![An image](assets/image.svg)
```

At compile time, the custom filter `filter/svgimagext.py` will subsitute the pdf extension for the pdf compilation. You don't need to worry about it.

If vector graphics are not available use JPG or PNG. Those are the only other two formats that are supported.
