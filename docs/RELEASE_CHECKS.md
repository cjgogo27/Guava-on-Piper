# Release checks v0.1

Publication packaging uses existing local evidence; it launches no model API, physics, data collection or training job.

Checks performed before push:

- Numeric reconstruction from row-level G1/G2/held tables, the450-episode task summary and aggregated interface audit.
- Seven regression tests: published numerical consistency; pose reorientation; unsafe common prefix despite a held target; missing/nonfinite data; unsupported parameter retention; stale image/model branch rejection; exact paired statistics.
- SHA256 release inventory and a scan for API-key/private-key material and private network hosts.
- Eight primary-source bibliography exports; reviewer reading log10 CVPR+10 empirical-analysis papers; two rounds of author-side simulated pre-review.
- Seven-page plain-report PDF compiled locally, text extracted, rendered representative pages inspected, zero overfull-box warnings after table-width fixes. No official conference template/status implied.

These checks do not substitute for public raw-state replay, multiple training-seed replication, controlled executor ablations, a complete upstream runtime installer or real-robot testing. See `REPRODUCIBILITY.md`.

## Related-work correction, 23 October 2026

The draft now explicitly positions this audit against Code-as-Monitor, RAFAIL and CriticHack. Their bibliography entries were retrieved from arXiv's primary BibTeX endpoints; receipts are in `paper/review/related_work_update_receipts.json`. The bibliography now contains eleven references. These works were not reproduced by this release, and their published performance is not compared to our local counts. No new experimental numbers or RSI claims were added.

The seven-page PDF was rebuilt with zero overfull boxes; revised related-work and reference pages were rendered and visually inspected. Numbered references now retain paragraph separation in the generated TeX.
