# Reproduction levels

| Level | Available in this release? | Meaning |
|---|---|---|
| A: numerical table reconstruction | **Yes** | Recompute counts, exact paired tests, intervals and denominator/accounting checks from released rows |
| B: original raw-state forward audit | **No public raw package** | Restore saved integration states to compiled MuJoCo model, `mj_forward`, recompute contact/poses; historical project audit passed, not dynamics re-integration |
| C: fresh physics policy replay | **Not packaged** | Requires original runtime/assets, environment, deterministic controller state, perception and model access |
| D: independent training replication | **No** | Requires training corpus/checkpoint pipeline and multiple training seeds |

Do not describe Level A as reproducing all robot experiments. Historical successful Level B audits are reported evidence, not something this small public package lets an outsider independently repeat.

## Level A

```bash
python -m pip install -e .
python -m guava_piper_audit.reproduce --root . --output generated/reproduced.json
python -m unittest discover -s tests -v
python scripts/verify_release.py
```

`reproduce` asserts450 planned counts,449 paired complete cases, all48 G1 row-level labels, Holm-corrected paired tests,16 G2 calibration layouts including rejects,32 held-detection confusion matrices and1041-record schema totals. A corrupt count or omitted failed row fails assertions.

## Test your own native trajectories, without changing them

Create a JSON mapping of tool names to allowed argument names. Supply all tool names used by the target execution contract:

```json
{"move":["target_position"],"grasp":["target_name"]}
```

```bash
python -m guava_piper_audit.interface your_records.jsonl your_schema.json
```

This illustrative two-tool mapping is not the complete upstream nine-tool schema. The audit returns unsupported fields but never deletes or rewrites parameters. Use an explicit parser for any unrecognized native format; JSON parsing errors fail loudly.

## Known non-reproducibility

The official-task comparison has one checkpoint, one training run and30 episode seeds/task; it is not a controlled interface ablation. G2 used calibration identities, not a sealed new-object test. Raw states/meshes/weights are unavailable here. Wall-clock costs depend on shared CPU/GPU load and are not pure inference latency. Rendering/SAM estimates can change with dependencies; exact pixels and cache/controller state are required for parent restoration comparisons.
