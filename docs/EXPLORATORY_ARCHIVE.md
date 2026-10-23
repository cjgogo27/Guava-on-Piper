# Additional bounded grasp-learning results

These completed local-model studies are retained for future researchers, **not added to the main paper's independent sample count**. They are not case studies of automated research frameworks. No new model calls were made to package them.

## Feedback-use mechanism

`data/exploratory/feedback.json` exports the original summary, including arm-level/paired results. Frozen Qwen3.5-4B received no feedback, binary feedback, or concrete physical feedback. Four physical candidates were executed first and frozen; subsequent model choices were **lookup-scored against those real results**, not new online rollouts. Reset retry was not continuous recovery from the altered failure state.

The test has32 independent layouts /64 target conditions. Three presentation arrangements are correlated repetitions, not three training seeds or192 independent scenes. Average new-layout qualified rates are27.1%,31.3%,33.9%; a support-only fixed-grasp baseline reaches43.8%. Concrete minus binary feedback is+2.60pp with an exploratory parent-cluster bootstrap95% interval[-3.13,+8.33]pp. The interval crosses zero; equivalence is not established. Physical pool:96 planned conditions,80 initial-perception-valid,320 actual candidate actions,119 qualified; the remaining64 candidate slots were not executed. This is not full Guava task SR or a positive weight-learning/RSI result.

## Bounded proposal/update and student pilot

`data/exploratory/bounded_grasp_learning.json` retains three actual training-seed lineages and student summaries. Four predefined grasp candidates and three predefined update operators restrict the problem. Physical pool:72 target conditions over36 layouts;4 conditions initially perception-blocked;272 actual candidates,116 qualified. Test:8 independent layouts /16 target conditions, including2 blocked conditions counted as failure.

Three-seed averages: initial4B37.5%, first update39.6%, uniform update39.6%, ancestor-proposed update39.6%, descendant-proposed update39.6%, support-selected fixed grasp43.8%. Student0.8B direct SFT39.6%, initial-teacher distillation39.6%, updated-teacher distillation37.5%. These are small, lookup-scored candidate-policy studies, not fresh full-task online rollouts. They do not establish recursive improvement or beneficial capability distillation.

## Interpretation

These negative findings prevent a false success claim and identify a useful baseline requirement. They do not show that physical feedback or self-improvement is impossible, and they should not be pooled with G1/G2 or held verification. Raw physical tables, all prompts, models and training checkpoints are not public in this compact release, so only exported summary-level checks are available. Original-summary identity hashes are retained in `data/provenance/source_hashes.json`.
