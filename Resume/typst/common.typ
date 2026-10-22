// Shared layout for resume.typ and biodata.typ (ported from the old LaTeX sources).

#let setup(paper: "us-letter", x: 0.5in, body) = {
  set document(author: "Viraj Sanghavi")
  set page(paper: paper, margin: (top: 0.45in, bottom: 0.45in, x: x))
  set text(font: "Libertinus Serif", size: 10pt)
  set par(justify: false, leading: 0.5em, spacing: 0.5em)
  set list(indent: 0.3em, body-indent: 0.5em, spacing: 0.4em)
  show list: set block(above: 0.4em, below: 0.6em)
  show heading.where(level: 1): it => block(above: 0.9em, below: 0.5em, width: 100%)[
    #set text(size: 12pt, weight: "bold")
    #it.body
    #v(-0.7em)
    #line(length: 100%, stroke: 0.4pt)
  ]
  body
}

// Bold title, right-aligned date, optional italic subtitle line.
#let entry(title, org, date, sub: none) = {
  [*#title*, #org #h(1fr) #date]
  if sub != none { linebreak(); text(size: 9pt, emph(sub)) }
}

#let proj(title, date) = [*#title* #h(1fr) #date]

#let ulink(url, body) = link(url, underline(body))

#let sep = [ | ]
