# Study Overlap Across 501 Cochrane Reviews

How much primary study overlap exists across large collections of Cochrane systematic reviews, and does this non-independence threaten the validity of methodological meta-research? We mapped all primary studies across 501 Cochrane reviews from the Pairwise70 dataset using normalized first-author-year keys to identify shared studies across reviews. The pipeline computed the Corrected Covered Area index, pairwise Jaccard similarity coefficients, and study frequency distributions across all 125,250 review pairs. The prevalence of overlap was minimal: CCA was 0.0001 (95% CI 0.00005-0.00018), with only 444 of 10,006 unique studies (4.4%) appearing in more than one review. Of 604 overlapping pairs, the most overlapping pair shared 43 studies with a Jaccard coefficient of 0.37, while 72% of pairs shared only one study. These results validate the Pairwise70 dataset as a source of largely independent meta-analyses suitable for large-scale methodological benchmarking. A limitation is that first-author-year matching may produce false positives when different studies share identical author surnames and publication years.

**Live dashboard:** <https://mahmood726-cyber.github.io/overlapdetector/>

## Run

Open `index.html` (or `index.html`) in any modern browser. No build step.

For local development:

```bash
python -m http.server 8000
# then open http://localhost:8000/
```

## Test

```bash
python -m pytest -q
```

The suite under `tests/` includes 1 test file(s).

## Repo layout

| Path | Purpose |
|---|---|
| `index.html` | the dashboard (main artifact) |
| `index.html` | landing page |
| `tests/` | pytest tests |
| `e156-submission/` | E156 micro-paper bundle |
| `E156-PROTOCOL.md` | project metadata (E156 entry #127) |

## License

See `LICENSE` (MIT).
