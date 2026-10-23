# Claim/evidence ledger

| ID | Claim permitted | Evidence | Boundary / missing experiment |
|---|---|---|---|
| C1 | Extended move arguments occur in420/1041 records and2476 calls | `data/collection/interface_audit.json` | No causal estimate of interface mismatch |
| C2 | Fixed SFT run had66/450 successes vs49/450 baseline, tray2 vs14 | `data/evaluation/task_counts.*` | One training seed/checkpoint; interface/prompt adaptations; one abort |
| C3 | Whole-sequence G1 counts D32/R38/O37/H39 out of48 | `data/perception/g1.json` | Two tested contrasts Holm p.140625/.1796875; no significant improvement claim |
| C4 | SOR/CC each attain the observed8-method union7/16 in G2 calibration | `data/perception/g2_calibration.json` | Calibration selection,4 identities, no held-out generalization or equivalence proof |
| C5 | Fixed held-detection AND adds0 FP corrections vs aperture and loses11 TP | `data/verification/held_detection.json` | 32 local layouts; only7 negatives; not all fusion, tasks or RSI |
| C6 | A common-prefix collision changes G1 whole-sequence qualification | G1 `common_prefix_unsafe` | Scoring-window correction, not a new controller gain |
| C7 | Particular historical boxes produced false geometric contact | `data/diagnostics/collision_candidate.json` + migration notes | Selected cases; final candidate can also have real contact |
| C8 | Restoration consistency is necessary to interpret a branch | `contracts.py`, historical failure taxonomy | No new controlled comparison of branch-training benefit |

### Not supported

Interface mismatch caused the tray degradation; SFT generally harms manipulation; re-observation is useless; SOR is universally best; a zero difference proves equivalence; the model performs causal physical reasoning; real-robot deployment works; the data are all reviewed/training-ready; the work is a novel manipulation algorithm or accepted CVPR paper.

### What would strengthen a paper

Freeze model/prompt/initial states and run matched executor variants (supported extension / rejection / explicitly documented semantic translation); do not merely drop `motion_mode`. Replicate training seeds before attributing task interference. Evaluate point-cloud baselines on sealed new identities. Publish licensed raw-state/parent closure before claiming externally reproducible physical audits. These experiments are **not completed by this release**.
