# Guava on Piper: adaptation notes and an evidence audit

**Guava迁移到Piper机械臂的适配经验、可复核数值证据与实证分析初稿。**

This is a research artifact, not the official Guava repository, a new manipulation algorithm, a validated real-robot controller, or a reproduction of the official Panda performance. No paid API calls are needed to inspect or reproduce the released tables.

## What is here

| Component | Entry point | Scope |
|---|---|---|
| Paper working draft | [PDF](paper/DRAFT.pdf) · [English source](paper/DRAFT.md) · [中文概述](paper/OVERVIEW_ZH.md) | Evidence-bounded analysis, not an accepted/submitted paper |
| Reproducible analysis | [Offline reproduction](docs/REPRODUCIBILITY.md) | Recomputes published numerical tables; no new physics |
| Adaptation primitives | [src/guava_piper_audit](src/guava_piper_audit) | Pose-consistent contact points, effect qualification, branch provenance and schema audit |
| Failure atlas | [Failure taxonomy](docs/FAILURE_ATLAS.md) | Observations, evidence strength, unresolved questions |
| Data | [Data card](data/README.md) | Small curated numerical records and four diagnostic image examples |
| Migration guide | [Piper adaptation](docs/PIPER_ADAPTATION.md) | Controller, schema, collision, payload and restore requirements |
| Historical implementation | [Four original adapter modules](examples/historical_adapters) | Source-preserved examples; matching upstream runtime required |
| Other completed pilots | [Exploratory grasp-learning archive](docs/EXPLORATORY_ARCHIVE.md) | Bounded feedback/update negative results, separate from main-study samples |
| Claim limits | [Evidence ledger](docs/CLAIM_EVIDENCE.md) | What can and cannot be inferred |

## Main findings

These are **different experiments with different units**, not one pooled success rate.

| Study | Independent units | Result | Interpretation |
|---|---:|---|---|
| Fixed baseline vs SFT evaluation | 450 scheduled episodes per model, 15 tasks | 49→66 task successes; tray 14/30→2/30 | Descriptive single-checkpoint result; not causal evidence about interface mismatch |
| Training schema audit | 1,041 records | 420 records, 2,476 calls contain `move.motion_mode` | Dataset/evaluation contract differs; occurrence alone does not establish runtime effect |
| G1 perception diagnostic | 48 planned layouts, including 7 common initial rejects | Original32, quantile38, reobserve37, simple rule39 qualified | Stronger point-cloud baselines matter; quantile/reobserve contrasts are not significant after Holm correction |
| G2 calibration | 16 planned layouts, 4 identities, 5 initial rejects | Standard SOR and CC each7; all-eight-method observed union7 | No added observed headroom for the proposed routing in this calibration set; no new-object generalization claim |
| Held-object verification | 32 layouts +4 diagnostic repeats | Aperture TP25/FP3; visual+aperture TP14/FP3 | Fixed AND fusion adds no false-positive correction and loses11 held positives |

“Qualified” in local diagnostics requires sampled hold plus a whole-sequence contact proxy. It is **not full-task success** or a real-robot safety certificate. The 2mm contact limit is an engineering threshold. G2 is calibration; its best method is not a held-out discovery.

## Run locally, without a model/API

Python3.10+; numerical reproduction has no third-party dependencies:

```bash
git clone https://github.com/cjgogo27/Guava-on-Piper.git
cd Guava-on-Piper
python -m pip install -e .
python -m guava_piper_audit.reproduce --root . --output generated/reproduced.json
python -m unittest discover -s tests -v
```

Or set `PYTHONPATH=src` to run without installing. This checks released row-level tables, paired contrasts and accounting, **not fresh robot rollouts or the privately retained raw-state audit**. See [exact reproduction levels](docs/REPRODUCIBILITY.md).

## Upstream and licensing

Built around [Guava](https://github.com/hdacnw/guava-release), pinned for these studies at `8eeed908bef4fb63c8bfc7c4e2fa2f5684eb067f`, with the author's robosuite fork. Obtain upstream source, Piper CAD, simulation assets and model weights from their owners. They are **not vendored or relicensed here**. This release does not contain the complete original runtime, training dataset or model checkpoint; it is a portable analysis toolkit and documented migration record.

Original release utilities are MIT; curated numeric tables are CC BY4.0. See [LICENSE](LICENSE), [NOTICE](NOTICE.md), [data card](data/README.md), and per-file provenance. The manuscript is a working draft with authorship/affiliation still to be finalized by the project owner.

Automatic-research-framework case studies and spending logs are intentionally outside this repository's scope. Historical experiment records were generated before this publication packaging; packaging and table verification introduce no new model/API calls or training.

## Writing and review

[Reading log](paper/review/READING_LOG.md): 10 CVPR +10 empirical-analysis papers, with honest abstract/partial-text reading levels. [Two-round internal review](paper/review/REVIEW_ROUND2.md) checked the actual draft. This is an author-authorized simulated pre-review, not an assigned CVPR reviewer or official acceptance. Eight manuscript references have source-fetched BibTeX in `paper/references.bib`.

To rebuild figures, install matplotlib and run `python scripts/make_figures.py`. To regenerate the plain technical-report TeX, run `python scripts/build_paper_tex.py`, then compile `paper/latex/main.tex` from its directory with pdfLaTeX. The default offline numeric reproduction needs neither matplotlib nor TeX. It makes no API requests.
