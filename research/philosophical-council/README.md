# Philosophical Council — research planning

**Status: conceptual development; planning artifacts only. Revision r1, 2026-10-28.** No
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
| [Study protocol](study-protocol.md) | r1 | No | No harness and no runs |
| [Epistemic evaluation record](epistemic-evaluation-record.md), `pc-eer/0.2` | Proposed design and [schema](schemas/pc-eer-0.2.schema.json) | No | Checked only by the committed validator, and only on the illustrative example |
| [Six development fixtures](fixtures/) | r1. Answer keys use `pc-expectation/0.2`; case packets are byte-identical to r0. | No. Each answer key records `reproduction_state: not_attempted`. | Not yet an oracle; gate G1 is pending. |
| [Validator](validation/), `pc-validate 0.2` | Committed with 51 negative controls | No | Run by hand. Nothing runs it automatically. |
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
  answer keys (`pc-expectation/0.2`) and records (`pc-eer/0.2`).
- **[`fixtures/`](fixtures/)**: six critic-visible case packets and six scorer-only answer
  keys. They carry a canary, and their hashes are pinned in `SHA256SUMS`.
- **[`examples/`](examples/)**: a toy packet and one hand-written illustrative record. It
  contains no model output and is not a result.
- **[`validation/`](validation/)**: the validator, its negative controls, and a statement
  of what a pass does and does not establish.

## Revision record

Revision r1 answers the operator's review of r0 (commit `ea9ecbd`). Each problem is
recorded in REA's terms, as a discrepancy (REA v0.1 §7.11) and its adjudication (§7.12).
r0 is superseded, not erased: it stays addressable at `ea9ecbd` (REA DD-RE-005). No
checkpoint has been published.

| ID | Discrepancy | Detected | Adjudication in r1 | Effect |
|---|---|---|---|---|
| R1-D1 | `documentation_implementation_drift`, material non-blocking. r0's record design said an overreaching record "would fail schema validation", but the schema leaves free text unconstrained. | Operator review, 2026-10-27 | The r0 statement is withdrawn. The record design, section 2, now states what the schema, the validator and human scoring each cover. SC-13 is added. | Records make no guarantee about prose; overreach in prose is scored (M7). |
| R1-D2 | `missing_evidence`, material non-blocking. r0 reported semantic checks made by scratch scripts that were never committed, so nobody could reproduce them. | Operator review, 2026-10-27 | `validation/validate.py` and 51 negative controls are committed. Every rule must have a control. | r0's "checked" statements remain historical claims (reproduction `not_attempted`). r1's checks can be reproduced from a clean checkout. |
| R1-D3 | `missing_evidence`, material non-blocking. The REA v0.1 contract was unavailable to r0, so its definitions could not be reconciled. | r0 reconciliation | The operator supplied the Stage B contract on 2026-10-27, and the reconciliation is rewritten as r1. | The inspected TC repository and the external REA definition are now kept apart. |
| R1-D4 | `conflicting_claims`, material non-blocking. r0's council definitions of observation, adjudication, confidence and absence conflict with REA Stage B. The r0 protocol also lacked REA's experiment requirements: registration, stopping rules and trial fields. | r1 reconciliation | The council adopts REA's definitions (SC-1, SC-8, SC-12). Formats move to `pc-eer/0.2` and `pc-expectation/0.2`. The protocol adds hypotheses in REA form, registration and stopping rules. | Case packets are unchanged. Answer keys and the example record are migrated. |

**Drafting validator run.**

- Command: `python3 research/philosophical-council/validation/validate.py`
- Environment: Python 3.13.17 and `jsonschema` 4.26.0.
- Input: the tree committed with this revision.
- Result: PASS. 41 rules passed and 1 was not applicable (V13: no study records), and
  51 of 51 negative controls were detected.

This is a historical claim about one run. Repeat the run to reproduce it.

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

The full list is in protocol section 16; D10 (the REA contract) is resolved. The most
immediate:

- **D9.** Name a human second reader to re-derive the answer keys (gate G1). This is the
  main outstanding review.
- **D13.** Keep or change the record's name, given REA's narrower `evaluation`.
- **D1, D7 and D14.** Settle the operators, the pilot structure and the registration
  parameters.
- **D12.** No run is authorized. A feasibility run needs an explicit grant naming its
  scope, model, budget and expiry.

## Relationship to the rest of this repository

- **Vocabulary.** Shared terms follow the canonical
  [trust vocabulary](../../trust-vocabulary.md). Epistemic roles follow REA v0.1 where it
  defines them. Council-specific terms are defined in the record design.
- **Visibility.** The [profile README](../../README.md) does not link to this directory.
  Whether and how to present this work publicly is the operator's decision.
- **Location.** This directory may later move to a dedicated repository. Relative paths in
  `SHA256SUMS` would then need to be regenerated.
