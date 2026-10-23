# Failure atlas: observations, not eighteen established contributions

| Failure observed | Smallest defensible diagnosis | Reusable artifact | Status / avoid claiming |
|---|---|---|---|
| Top approach hits neighbor; side approach unreachable | Object pose alone does not specify a feasible gripper approach | Pose/contact-point contract; historical approach-envelope diagnostics | Limited development scenes, no general selection-policy gain |
| Robot/potato/can segmented as semantic target | Target identity/visibility can fail independently of controller arrival | Four posthoc verification images | Examples, not prevalence or a solved detector |
| Cup identities reorder after motion | Left/middle/right is not persistent identity | Migration notes, archived search diagnostics | Position-memory examples not a proven general tracker |
| Large finger collision box | Contact on a conservative proxy may not match CAD surface | Collision transformation provenance | Convex hull still fills cavities; not every contact is false |
| Juice slips while tool arrives | Payload/holding outcome differs from TCP arrival | Effect qualification, payload caveat |70–140g is an assumption, not hardware identification |
| Old wrist rotation used for tip offset | Pose conversion becomes inconsistent after orientation reselection | `geometry.py`, negative regression test | Coordinate repair, not a novel IK method |
| Random edge/neighbor layout infeasible | Initial feasibility and current policy capability are different | Explicit initialization rejects in G1/G2 | Rejects remain in planned denominators |
| Successful tool response but wrong physical effect | Command acceptance/arrival is not object/task success | Held32-row dataset; `contracts.qualification` | Local operational held label only |
| Obscured terminal image | Absence of visual confirmation is not necessarily failure | Separate physical/visual quality concepts | Do not automatically label ambiguous images success |
| Coarse skill retries vs fine primitive overhead | Recovery granularity has a budget tradeoff | Official task-budget record | No controlled granularity gain established |
| Restore loses registry/caches or wrong model | Parent state/history/interface provenance broken | `validate_branch`, image/model/pair checks | Do not silently substitute new models for old parents |
| Nominal perturbation has no effect | A saved checkpoint is not automatically valid recovery data | Fault invalidation/displacement tests | Invalid branches cannot count as recoveries |
| Failed trajectory has useful steps | Episode labels are coarse supervision | Native/loss-preservation requirements | No tool-credit training benefit established |
| Train/eval schema mismatch | Contract divergence is measurable | `interface.py`,1041-record audit | No causal performance attribution |
| Aggregate SFT gain hides tray decline | Report task strata and fixed denominator |15-task table | No demonstrated catastrophic forgetting mechanism |
| Physical-feedback selector underperforms fixed action | Feedback/representation/candidates may be bottlenecks | Archived negative pilot | Does not disprove all conditional-grasp learning |
| More sensing loses to cheaper processing | Include strong simple point-cloud baselines | G1/G2 paired data | Calibration-only result; not universal inferiority |
| Simulated sensor/model differs from hardware | CAD/camera provenance alone is not deployment validation | Explicit no-real-robot scope | No real-robot closed-loop result |

Research-automation framework operation/costs are excluded at the owner's request. Related-work reading and paper-review materials are in `paper/review`; this taxonomy is an empirical organization, not a claim that these problems were previously unknown.
