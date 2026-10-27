# Philosophical Council — research planning

**Status: conceptual development; planning artifacts only. Revision r0, 2026-10-27.** No
implementation is authorized. No model has been run and no data collected, and no human
has yet reviewed these documents. They were drafted with AI assistance at the operator's
direction.

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

These non-claims are also constants in every evaluation record (`non_claims`), and the
protocol states them in full (section 3).

## Status at a glance

| Artifact | Exists here | Human-reviewed | Implemented or enforced |
|---|---|---|---|
| [Study protocol](study-protocol.md) | r0 draft | No | No harness and no runs |
| [Epistemic evaluation record](epistemic-evaluation-record.md), `pc-eer/0.1` | Proposed design and [schema](schemas/pc-eer-0.1.schema.json) | No | No validator in the repository |
| [Six development fixtures](fixtures/) | Draft | No; the second-reader gate G1 is pending | Not yet an oracle |
| [Semantic-contract reconciliation](semantic-contract-reconciliation.md) | r0 | No | Documentation only |

## Contents

- **[`study-protocol.md`](study-protocol.md)**:
  - the research question, hypotheses and claim boundaries;
  - the 2×2 design (C1–C4) and the operators O1–O6;
  - controls, measures, adjudication and the feasibility gate;
  - the 24-case pilot options and external positioning;
  - the decisions requested from the operator.
- **[`semantic-contract-reconciliation.md`](semantic-contract-reconciliation.md)**:
  - term-by-term reuse of TriageCore (TC) and agent-control-evals (ACE) semantics, with
    `path:line` citations at pinned commits;
  - what is deliberately not imported;
  - the semantic contract SC-1 to SC-11.
- **[`epistemic-evaluation-record.md`](epistemic-evaluation-record.md)**:
  - the six invariants made structural;
  - the record's anatomy and vocabularies;
  - semantic rules V1–V13;
  - the separate adjudication record.
- **[`schemas/`](schemas/)**: proposed JSON Schemas (Draft 2020-12) for case packets,
  expectations and records.
- **[`fixtures/`](fixtures/)**: six case packets, which critics may see, and six
  expectation files, which only adjudicators see. They carry a canary, and their hashes
  are pinned in `SHA256SUMS`.
- **[`examples/`](examples/)**: a toy packet and one hand-written illustrative record. It
  contains no model output and is not a result.

## First planning milestone: acceptance criteria

| Criterion from the handoff | Where addressed | State |
|---|---|---|
| Documented research question | Protocol section 2 | Drafted |
| Explicit claim boundaries | Protocol section 3; record `non_claims`; this README | Drafted |
| Reproducible fixtures | `fixtures/`: pinned bytes (`SHA256SUMS`, `.gitattributes`), schemas, canary, authoring rules | Drafted. Not an oracle until G1 |
| Independently specified evaluation criteria | Answer keys kept apart from critic-visible packets; adjudicators assign codes; protocol section 9; reconciliation SC-5 | Drafted. Second reader pending |
| Provenance preservation | Record lineage and verified quotations; inputs pinned by commit and hash; reconciliation appendix A | Drafted |
| No unauthorized changes to TC or ACE | Reconciliation section 10 | Checked at drafting time: TC and ACE clones unmodified |

The 24-case pilot and multimodal work are out of scope until the feasibility gate passes
(protocol section 10).

## Inputs and provenance

| Input | Form | Identity |
|---|---|---|
| Planning handoff, *Philosophical Council: Research Planning Handoff* | Operator message in the drafting session, 2026-10-27 | Received as message text, so there is no byte hash. Not stored here |
| TriageCore | Repository, read-only clone | Commit `4e9f238512eec4d9fc417542745962783d3e675f` |
| agent-control-evals | Repository, read-only clone | Commit `b876a287fc27701e79f16208640f86845f1edafc` |
| Redwood article excerpt (E1) | Text pasted by the operator, truncated | Not stored; quoted briefly in protocol section 15 |
| Redwood research summary (E2) | File supplied by the operator | SHA-256 `bae79e8a9dcfa992acf8b06480c8643787254a804395e278e5bce05e332270c7`; not stored |
| Web-search summaries (E3) | Unverified leads | Primary pages were unreachable from the drafting environment |

## Verify

```sh
cd research/philosophical-council/fixtures
sha256sum -c SHA256SUMS
```

The fixtures README describes what was checked during drafting and how.

## Decisions needed before anything runs

The full list is in protocol section 16. The most immediate:

- **D10.** Supply the *Research Evidence Architecture & Schema Contract v0.1* (Stage B).
  It was not available to this session, and the reconciliation and the record format
  defer to it.
- **D9.** Name a human second reader for the fixtures (gate G1).
- **D1 and D7.** Settle the operators and the pilot structure.
- **D12.** No run is authorized. A feasibility run needs an explicit grant naming its
  scope, model and budget.

## Relationship to the rest of this repository

- **Vocabulary.** Shared terms follow the canonical
  [trust vocabulary](../../trust-vocabulary.md). Council-specific terms are defined
  locally, in the record design.
- **Visibility.** The [profile README](../../README.md) does not link to this directory.
  Whether and how to present this work publicly is the operator's decision. If presented,
  it should be framed as an empirical investigation of philosophical critique and
  conceptual reasoning assessment.
- **Location.** This directory may later move to a dedicated repository. Relative paths in
  `SHA256SUMS` would then need to be regenerated.
