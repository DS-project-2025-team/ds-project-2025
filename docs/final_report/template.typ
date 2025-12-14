#let config(lang: "en", body) = {
  set page(paper: "a4", numbering: "1")

  set text(
    font: "New Computer Modern",
    size: 12pt,
    lang: lang,
    ligatures: false,
  )
  set par(justify: true)
  set enum(numbering: "(1)(a)(i)")
  set figure(placement: auto)
  set heading(numbering: "1.1.1")

  set math.mat(delim: "[")
  set math.vec(delim: "[")
  show math.equation: set block(breakable: true)
  show sym.nothing: set text(font: "Fira Sans")
  show math.equation: x => {
    show sym.colon: $class("fence", colon)$
    x
  }

  show ref: x => {
    let element = x.element

    if element != none and element.func() == math.equation {
      link(element.location())[#element.supplement~#numbering(
          element.numbering,
          ..counter(math.equation).at(element.location()),
        )]
    } else {
      x
    }
  }

  body
}

#let appendix(title, body) = {
  set heading(numbering: "A.1", supplement: title)
  counter(heading).update(0)

  heading(title)

  body
}
