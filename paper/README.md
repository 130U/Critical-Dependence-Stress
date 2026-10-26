# Paper

[Read the public edition](paper.pdf) · [LaTeX source](source/paper.tex)

**Critical Dependence Stress for Diversification Gains under Fixed Marginals**  
Letao Ouyang · Author manuscript · 2026

The public edition uses a conventional article layout with a linked contents page and PDF bookmarks. Its abstract, mathematical body, proofs, numbered equations, figures, references and declarations are retained from the author's manuscript. The paper contains 114 numbered equations, 15 theorem-class statements and four figures.

## Build

Install [Tectonic](https://tectonic-typesetting.github.io/), then run from the repository root:

```bash
python paper/source/build.py
```

The rebuilt file is written to `paper/source/build/paper.pdf`. Tectonic downloads its TeX dependencies on the first build. The Latin Modern text fonts are included with their GUST license; no system fonts are required for the text. A Tectonic/XeTeX build was checked on Windows.

## Cite

```bibtex
@unpublished{ouyang2026critical,
  author = {Ouyang, Letao},
  title = {Critical Dependence Stress for Diversification Gains under Fixed Marginals},
  year = {2026},
  note = {Author manuscript}
}
```
