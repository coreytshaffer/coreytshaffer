# Philosophical Council — research planning

**Status: conceptual development; planning artifacts only. Revision r4, 2026-10-28.** No
implementation is authorized. No model has been run and no data collected. No human has
yet reviewed these documents, and the answer keys have not been independently re-derived.
The documents were drafted with AI assistance at the operator's direction.

This directory plans an empirical study. The research question is whether provenance-aware,
philosophically structured, independent critique improves the evaluation of AI-generated
conceptual reasoning beyond ordinary model critique, without creating unjustified
evaluator confidence. The *council* is the critique procedure under study. It is an
evaluation method, not a body with standing.

## What this work is not

- **Not a certifier.** It does not certify the truth of any claim, guarantee safety, or
  establish malicious intent.
- **Not an authority.** It does not authorize any consequential action. Evaluation stays
  separate from authority, execution and institutional decisions.
- **Not a system.** It is not an existing defensive system, a deployed tool or an
  alignment solution. It is a study protocol at the planning stage.
- **Not representation.** Its reviewer diversity is procedural. No critic represents a
  person, community or tradition.
- **No external standing.** No organization endorses it or takes part in it.

These non-claims are constants in every record's structured fields (`non_claims`). Those
constants do not constrain what a critic writes in free text. Overreach in prose is
detected only by human scoring ([record design](epistemic-evaluation-record.md),
section 2).

## Status at a glance

| Artifact | Exists here | Human-reviewed | Implemented, enforced or run |
|---|---|---|---|
| [Study protocol](study-protocol.md) | r4 | No | No harness and no runs |
| [Epistemic evaluation record](epistemic-evaluation-record.md), `pc-eer/0.3` | Proposed design and [schema](schemas/pc-eer-0.3.schema.json) | No | Checked only by the committed validator, and only on the three illustrative examples |
| [Six development fixtures](fixtures/) | r4. Answer keys use `pc-expectation/0.2` and are unchanged from r1; case packets are byte-identical to r0. | No. Each answer key records `reproduction_state: not_attempted`. | Not yet an oracle; gate G1 is pending. |
| [Validator](validation/), `pc-validate 0.4` | Committed with 69 negative controls | No | Run by hand. Nothing runs it automatically. |
| [Semantic-contract reconciliation](semantic-contract-reconciliation.md) | r1, against TC, REA v0.1 Stage B and ACE | No | Documentation only |

## Contents

- **[`study-protocol.md`](study-protocol.md)**:
  - the research question, and hypotheses H1–H4 in REA form with a registration plan;
  - claim boundaries;
  - the 2×2 design (C1–C4) and the operators O1–O6;
  - controls, measures, scoring and adjudication;
  - the feasibility gate, the pilot with stopping rules, and positioning;
  - decisions D1–D14.
- **[`semantic-contract-reconciliation.md`](semantic-contract-reconciliation.md)**:
  - term-by-term comparison of the inspected TriageCore repository, REA v0.1 Stage B
    (an external research definition) and council usage;
  - the six invariants;
  - what is deliberately not imported;
  - the semantic contract SC-1 to SC-13.
- **[`epistemic-evaluation-record.md`](epistemic-evaluation-record.md)**:
  - what the format does and does not guarantee;
  - the mapping to REA roles;
  - vocabularies and per-field absence tags;
  - rules V0–V13;
  - the scoring, discrepancy and adjudication records.
- **[`schemas/`](schemas/)**: JSON Schemas (Draft 2020-12) for case packets (`pc-case/0.1`),
  answer keys (`pc-expectation/0.2`) and records (`pc-eer/0.3`).
- **[`fixtures/`](fixtures/)**: six critic-visible case packets and six scorer-only answer
  keys. They carry a canary, and their hashes are pinned in `SHA256SUMS`.
- **[`examples/`](examples/)**: two toy packets and three hand-written illustrative records.
  The second packet contains a transformation. In the third record each reviewer outcome
  occurs: an assessment, an invalid output and a transport failure. They contain no model
  output, are not results, and are pinned in `SHA256SUMS`.
- **[`validation/`](validation/)**: the validator, its negative controls, and a statement
  of what a pass does and does not establish.

## Revision record

Each revision answers an operator review. Each problem is recorded in REA's terms, as a
discrepancy (REA v0.1 §7.11) and its adjudication (§7.12). Superseded revisions are not
erased: r0 stays addressable at `ea9ecbd`, r1 at `5ad1c3a`, r2 at `69d8739` and r3 at
`14de682` (REA DD-RE-005). No checkpoint has been published.

### r4

Revision r4 answers the review of r3 (commit `14de682`). The reviewer could not locate the
branch or commit from their workspace, so r3's reported results (24 pins, 41 passing
rules, 68 controls) were not independently verified, and remain drafting claims, as do
r2's. These checks establish structural validation only. They say nothing about model
performance, and they authorize no run.

| ID | Item | Source | Resolution in r4 | Effect |
|---|---|---|---|---|
| R4-D1 | `scope_mismatch`, material non-blocking. r3 recorded the ban on sending a call again after a transport failure as part of D16 (R3-D2, protocol section 6.8 and D16). D16 prohibited only retries based on an output's content. | Review of r3, 2026-10-28 | D16 now states only what the operator decided. The transport restriction is separated as D17: proposed, not decided, and recommended by the review. Its basis is a format limitation, since `pc-eer/0.3` has no attempt or output identities and cannot keep both a failed attempt and a later outcome. Future retry support needs those identities and a defined accounting policy. Protocol, sections 6.8 and 16; record design, section 9; the schema's description of `transport_failures`. | No rule changes: V4 already allows one outcome per reviewer, so the limitation holds whatever D17 decides. D17 awaits the operator. |
| R4-D2 | `missing_evidence`, material non-blocking. A valid record with a transport failure was checked only in a scratch run (r3 report). | Review of r3, 2026-10-28 | `examples/pc-eer-illustrative-03.json`, over PC-TOY-01: r1 has an assessment, r2 an invalid output, and r3 a transport failure with `no_output`. It is pinned and checked by the normal command. NC-V4d (`exact`) gives r3 an output-hash value other than `no_output`. | The positive case is reproducible from a clean checkout. |
| R4-D3 | `unknown`, minor: an ambiguity. r3's G2 reported transport failures "with their rate" without naming the denominator. | Review of r3, 2026-10-28 | G2 measures parse success among completed outputs. Transport failures are counted against scheduled calls, with no G2 threshold; the operator may add one under D4. Protocol section 6.8 defines the call accounting, and section 10 reports it. | Transport failures stay visible in reporting instead of dropping out of the parse rate. |

**Drafting validator run (r4).**

- Command: `python3 research/philosophical-council/validation/validate.py`
- Environment: Python 3.13.17 and `jsonschema` 4.26.0.
- Input: the tree committed with this revision.
- Result: PASS. 41 rules passed and 1 was not applicable (V13: no study records), and
  69 of 69 negative controls were detected. The nine `exact` controls fired exactly their
  listed rules.

This is a historical claim about one run. Repeat the run to reproduce it.

### r3

Revision r3 implements the operator's decisions on r2 (commit `69d8739`). The operator made
them from the r2 report and did not independently check `69d8739`, so r2's results remain
drafting claims. Two of the decisions are recorded REA-style in the protocol, section 16,
as D15 and D16.

| ID | Item | Source | Resolution in r3 | Effect |
|---|---|---|---|---|
| R3-D1 | Decision D15. Different disagreement IDs over the same positions stay allowed, because the same positions can conflict over several distinct issues. Each disagreement must state its scope, semantic duplication is left to human review, and repeated IDs stay rejected. | Operator decision on r2, 2026-10-28 | `scope` is required in `pc-eer/0.3`, and V8 is unchanged. NC-V0e removes a scope. Protocol, section 6.6; record design, sections 5 and 9. | A `pc-eer/0.2` record no longer validates. The first example is migrated. |
| R3-D2 | Decision D16. One completed output per reviewer per trial, with no retries based on the output's content. Transport failures are recorded separately, and repeated invalid entries for one reviewer are rejected. Future retries need explicit attempt and output identities. r2 had left repeated entries allowed as an open question. | Operator decision on r2, 2026-10-28 | Protocol, section 6.8, and G2. `pc-eer/0.3` adds `integrity.transport_failures` and the `no_output` hash tag. V4 requires exactly one outcome per reviewer, and V3 resolves transport failures. NC-V4b (an invalid output listed twice; missed by the r1 and r2 rules), NC-V4c and NC-V3c. r3 also sends no call again after a transport failure, because a second call would be a second trial. | A reviewer whose call failed can now be recorded; r2's format could not represent one. |
| R3-D3 | `missing_evidence`, material non-blocking. r2's V11 repeat check had no committed control. Its drafting test was a scratch artifact that nobody could rerun. | r2 report, 2026-10-28 | A second example: packet PC-TOY-02 with transformation X1, and a valid record over it. NC-V11b appends an exact duplicate X1 entry. NC-V11c puts a falsified X1 entry before a correct one. Examples are now pinned (PIN02) and checked by FX04–FX11 (NC-PIN02b, NC-EX01b). A control marked `exact` must fire its listed rules and no others; all eight r3 controls are exact. | V11 is reproducible from a clean checkout. Each V11 control fires only V11 and the pin check on the edited example. |

**Drafting validator run (r3).**

- Command: `python3 research/philosophical-council/validation/validate.py`
- Environment: Python 3.13.17 and `jsonschema` 4.26.0.
- Input: the tree committed as r3 (`14de682`).
- Result: PASS. 41 rules passed and 1 was not applicable (V13: no study records), and
  68 of 68 negative controls were detected. The eight r3 controls fired exactly their
  listed rules. Judged by the r1 rules, NC-V11b, NC-V11c and NC-V4b were missed; judged
  by the r2 rules, NC-V4b was missed.

This is a historical claim about one run. Repeat the run to reproduce it.

### r2

Revision r2 answers the operator's review of r1 (commit `5ad1c3a`). That review reproduced
r1's validation run and found two mutations that passed every check.

| ID | Discrepancy | Detected | Adjudication in r2 | Effect |
|---|---|---|---|---|
| R2-D1 | `documentation_implementation_drift`, material non-blocking. V7 claimed an exact partition but compared sets, so an exact copy of a position passed. V3 claimed that every reference resolves but skipped `integrity.invalid_reviewer_outputs`, so an invalid output from an undeclared reviewer passed. | Operator review of r1, 2026-10-28 | V7 checks position-ID uniqueness, each assessed reviewer's membership count and distinct assessments before it compares sets. V3 resolves the reviewer of each invalid output, and its rule text names the lists it checks. NC-V7b and NC-V3b are the operator's two mutations. | A record that r1 accepted may now fail. The only record, the illustrative example, passes. |
| R2-D2 | `documentation_implementation_drift`, material non-blocking. The same defect in other rules, found by an r2 audit of every set or keyed comparison. Two differing positions that shared one ID passed with their disagreement deleted, because V8 counted distinct IDs. V9, V10 and V11 kept only the last entry per key, so a falsified attention, lineage or transformation entry placed before a correct one was never compared. An assessment split into two positions, and a repeated disagreement, index entry, case transformation or record transformation, also passed. | r2 audit, 2026-10-28 | Repeats are checked before set comparisons in V7–V11, FX03 and FX11, and V8 counts positions. Seven more controls cover these: NC-V7c, NC-V8b, NC-V8c, NC-V9b, NC-V10b, NC-FX03c and NC-FX11b. The V11 check has no committed control; a drafting test exercised it (validation README). | These rules carry invariants 3, 5 and 6 (record design, section 2). Shadowed attention or lineage could have overstated independent support, a shadowed transformation entry could have raised a summary's fidelity check, and a shared ID could have erased a disagreement. Two cases stay allowed and open (record design, section 9). |
| R2-D3 | `unknown`, material non-blocking: an ambiguity in a measure, for which REA lists no closer kind. M6 assigned binary Brier targets with no rule for duplicates or disputed scoring. A substantively correct duplicate scored 0, an unresolved dispute had no target, and the Brier score and the high-confidence error rate used different targets. | Operator review of r1, 2026-10-28 | Protocol section 8.1 defines one target for both parts of M6. A duplicate's claim is scored once, through the scoring record's new `duplicate_of`. Disputed findings are left out of the primary analysis, and reported with their share, each competing coding and bounds. D14 fixes these rules at registration. | M6 is defined before registration. No data exist, so nothing is rescored. |
| R2-D4 | `conflicting_claims`, minor. The r1 drafting report, a session message to the operator that is not stored here, said r1 fixed the PC-F06 packet. The repository says the case packets are byte-identical to r0, and their hashes agree. The fix, which ties the queried interval in segment S1.2 to the maintenance window, was made while drafting r0, before commit `ea9ecbd`. | Operator review of r1, 2026-10-28 | The repository was right and the report was wrong. No file changes. | None on the artifacts. All six packet hashes are unchanged from r0. |

**Drafting validator run (r2).**

- Command: `python3 research/philosophical-council/validation/validate.py`
- Environment: Python 3.13.17 and `jsonschema` 4.26.0.
- Input: the tree committed as r2 (`69d8739`).
- Result: PASS. 41 rules passed and 1 was not applicable (V13: no study records), and
  60 of 60 negative controls were detected. Judged by the r1 rules, all nine new controls
  were missed.

This is a historical claim about one run. Repeat the run to reproduce it.

### r1

Revision r1 answers the operator's review of r0 (commit `ea9ecbd`).

| ID | Discrepancy | Detected | Adjudication in r1 | Effect |
|---|---|---|---|---|
| R1-D1 | `documentation_implementation_drift`, material non-blocking. r0's record design said an overreaching record "would fail schema validation", but the schema leaves free text unconstrained. | Operator review, 2026-10-27 | The r0 statement is withdrawn. The record design, section 2, now states what the schema, the validator and human scoring each cover. SC-13 is added. | Records make no guarantee about prose; overreach in prose is scored (M7). |
| R1-D2 | `missing_evidence`, material non-blocking. r0 reported semantic checks made by scratch scripts that were never committed, so nobody could reproduce them. | Operator review, 2026-10-27 | `validation/validate.py` and 51 negative controls are committed. Every rule must have a control. | r0's "checked" statements remain historical claims (reproduction `not_attempted`). r1's checks can be reproduced from a clean checkout. |
| R1-D3 | `missing_evidence`, material non-blocking. The REA v0.1 contract was unavailable to r0, so its definitions could not be reconciled. | r0 reconciliation | The operator supplied the Stage B contract on 2026-10-27, and the reconciliation is rewritten as r1. | The inspected TC repository and the external REA definition are now kept apart. |
| R1-D4 | `conflicting_claims`, material non-blocking. r0's council definitions of observation, adjudication, confidence and absence conflict with REA Stage B. The r0 protocol also lacked REA's experiment requirements: registration, stopping rules and trial fields. | r1 reconciliation | The council adopts REA's definitions (SC-1, SC-8, SC-12). Formats move to `pc-eer/0.2` and `pc-expectation/0.2`. The protocol adds hypotheses in REA form, registration and stopping rules. | Case packets are unchanged. Answer keys and the example record are migrated. |

**Drafting validator run (r1).**

- Command: `python3 research/philosophical-council/validation/validate.py`
- Environment: Python 3.13.17 and `jsonschema` 4.26.0.
- Input: the tree committed as r1 (`5ad1c3a`).
- Result: PASS. 41 rules passed and 1 was not applicable (V13: no study records), and
  51 of 51 negative controls were detected.
- Rerun by the operator against `5ad1c3a` (review of r1), with the same results: all 20
  pins matched, 41 rules passed, V13 was not applicable, and 51 of 51 controls were
  detected. That run's environment is not recorded here. The rerun concerns the
  validator's checks, not the answer keys (gate G1).

## First planning milestone: acceptance criteria

| Criterion from the handoff | Where addressed | State |
|---|---|---|
| Documented research question | Protocol section 2 | Drafted; hypotheses in REA form |
| Explicit claim boundaries | Protocol section 3; record design section 2; this README | Drafted. The mechanism behind each boundary is now named. |
| Reproducible fixtures | `fixtures/`: pinned bytes (`SHA256SUMS` under a stated canonicalization contract), schemas, canary, and a committed validator | Drafted. Not an oracle until G1. |
| Independently specified evaluation criteria | Answer keys kept apart from packets; scorers assign codes; adjudication preserves predecessors; reconciliation SC-5 | Drafted. Second reader pending. |
| Provenance preservation | Lineage; quotation source verification; inputs pinned by commit and hash; the revision record | Drafted |
| No unauthorized changes to TC or ACE | Reconciliation section 10 | Checked at drafting time: the clones are unmodified. |

The 24-case pilot and multimodal work stay out of scope until the feasibility gate passes
(protocol section 10).

## Inputs and provenance

| Input | Form | Identity |
|---|---|---|
| Planning handoff, *Philosophical Council: Research Planning Handoff* | Operator message, 2026-10-27 | Received as message text, so there is no byte hash. Not stored here |
| Operator review of r0, with the recommended next milestone | Operator message, 2026-10-27 | Not stored here; summarized in the revision record |
| Operator review of r1 | Operator message, 2026-10-28 | Not stored here; summarized in the revision record (R2-D1, R2-D3 and R2-D4) |
| Review of r3, with recommendations | Operator message, 2026-10-28 | Not stored here; summarized in the revision record (R4-D1 to R4-D3) and as proposed decision D17. The reviewer could not locate `14de682` from their workspace |
| Operator decisions on r2 | Operator message, 2026-10-28 | Not stored here; recorded as D15 and D16 (protocol, section 16) and in the revision record (R3-D1 to R3-D3). Made from the r2 report, without an independent check of `69d8739` |
| REA v0.1, Stage B revision | Operator file, 2026-10-27 | SHA-256 `a0ece23a770d603e4220bc0847cdf02fdbb96e640022d46d8794ac4391f733e3`. Not stored here. The Stage A copy was not supplied or used. |
| TriageCore | Repository, read-only clone | Commit `4e9f238512eec4d9fc417542745962783d3e675f` |
| agent-control-evals | Repository, read-only clone | Commit `b876a287fc27701e79f16208640f86845f1edafc` |
| Redwood article excerpt (E1) | Text pasted by the operator, truncated | Not stored; quoted briefly in protocol section 15 |
| Redwood research summary (E2) | File supplied by the operator | SHA-256 `bae79e8a9dcfa992acf8b06480c8643787254a804395e278e5bce05e332270c7`; not stored |
| Web-search summaries (E3) | Unverified leads | Primary pages were unreachable from the drafting environment |

## Verify

```sh
python3 research/philosophical-council/validation/validate.py   # rules and negative controls
cd research/philosophical-council/fixtures && sha256sum -c SHA256SUMS
```

A pass establishes that the files satisfy the validator's rules. It does not establish
that the answer keys are correct or that free text is free of overreach (validation
README).

## Decisions needed before anything runs

The full list is in protocol section 16. D10 (the REA contract), D15 and D16 are
resolved. The most immediate:

- **D9.** Name a human second reader to re-derive the answer keys (gate G1). This is the
  main outstanding review.
- **D13.** Keep or change the record's name, given REA's narrower `evaluation`.
- **D1, D7 and D14.** Settle the operators, the pilot structure and the registration
  parameters. D14 now includes M6's target rules (protocol, section 8.1).
- **D12.** No run is authorized. A feasibility run needs an explicit grant naming its
  scope, model, budget and expiry.
- **D17.** Decide whether to keep sending a call again after a transport failure
  unsupported in `pc-eer/0.3` (recommended; protocol, section 6.8). D16 does not cover it.
  The format cannot record such a re-send faithfully whatever is decided, so supporting
  one would first need attempt and output identities and an accounting policy.

## Relationship to the rest of this repository

- **Vocabulary.** Shared terms follow the canonical
  [trust vocabulary](../../trust-vocabulary.md). Epistemic roles follow REA v0.1 where it
  defines them. Council-specific terms are defined in the record design.
- **Visibility.** The [profile README](../../README.md) does not link to this directory.
  Whether and how to present this work publicly is the operator's decision.
- **Location.** This directory may later move to a dedicated repository. Relative paths in
  `SHA256SUMS` would then need to be regenerated.
