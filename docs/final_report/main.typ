#import "template.typ": appendix, config

#show: config

#align(center)[
  #v(25%)
  #text(size: 20pt)[
    *Distributed brute-force 3-SAT solver:\
    Final report*
  ]

  Group 8:
  Jiahao Li, Petteri Huvio and Vilho Raatikka
]

#pagebreak()

#outline()

#pagebreak()

#include "parts/introduction.typ"
#include "parts/background.typ"
#include "parts/architecture/index.typ"
#include "parts/communication/index.typ"
#include "parts/distributing_work.typ"
#include "parts/prototype.typ"
#include "parts/scalability/index.typ"
#include "parts/key_enablers_and_lessons_learned.typ"
#include "parts/conclusions.typ"
#include "parts/participation.typ"

#bibliography("references.bib")

#appendix("Appendix")[
  #include "appendix/index.typ"
]
