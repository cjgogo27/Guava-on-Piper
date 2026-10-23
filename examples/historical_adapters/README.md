# Original historical Piper adapters

These four files are **original project adapters**, exported without changing their historical scientific behavior. SHA256 identities are in `provenance.json`. They reference upstream APIs but do not vendor their implementations or CAD.

| File | What it illustrates | Important limitation |
|---|---|---|
| `contact_path_v33.py` | Recompute fingertip→TCP conversion for each chosen radial tilt | Robot-specific historical offset constants; preserve original arrival gate; not a universal IK solver |
| `robot_self_filter_v2.py` | Filter RGB-D using time-matched robot-only CAD/FK keyed by RGB hash | Only selected task adapters; box approximations can reject valid points; no generic identity solution |
| `visible_approach_v38.py` | Check observed non-target points against candidate gripper hulls and IK | Visible surfaces only; 3mm engineering margin is not hardware certification or proof about hidden obstacles |
| `branch_eligibility.py` | Reject unresolved/ambiguous targets and non-free-joint free-object perturbations | Articulated drawer recovery needs a separate, explicit perturbation contract |

Dependencies: the matching historical Guava/Piper adapter interfaces, NumPy and SciPy. Place these files on an isolated candidate's Python path before using their functions. They are not installed/imported by `guava_piper_audit`, and importing them does not automatically patch the runtime; `install()` is explicit where supplied. Do not stack installs or apply them to a running production job.

The portable, tested equivalents for basic pose/provenance contracts are in `src/guava_piper_audit`. Historical small-case successes do not certify that these adapters preserve every high-success task. No simulation or real-robot end-to-end replay was newly run during publication packaging.
