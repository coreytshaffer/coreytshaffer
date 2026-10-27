# Semantic-Contract Reconciliation — Philosophical Council, TriageCore and agent-control-evals (r0)

**Status: proposed planning artifact, revision r0 (2026-10-27).** This is a read-only
reconciliation and it changes nothing in TriageCore (TC) or agent-control-evals (ACE). It
is not reviewed and not accepted, and it grants no authority. Section 10 records the
no-change check.

## 1. Scope, inputs and method

**Question.** Which TC and ACE research semantics can the council reuse, narrow or leave
behind, and where must it define terms of its own? A second constraint governs the whole
answer: none of TC's action-governance responsibilities may come with them.

**Pinned inputs.** Citations below are `path:line` at these commits. Appendix A gives the
SHA-256 of every cited file.

| Repository | Commit | Commit date |
|---|---|---|
| `coreytshaffer/TriageCore` | `4e9f238512eec4d9fc417542745962783d3e675f` | 2026-10-26 |
| `coreytshaffer/agent-control-evals` | `b876a287fc27701e79f16208640f86845f1edafc` | 2026-10-17 |
| `coreytshaffer/triagecore-signed-intent` | `85c44709cbaf64fa06d7e81c8c1ed52ffbedabcf` (searched for the REA contract only) | 2026-10-25 |
| this repository, base | `78371f0e3ae026aa59ce5b4deef07e582db880b6` | 2026-10-24 |

**Method.** Shallow clones were made, and nothing was written to them. Terms were located
with `grep` and then read in context.

**Search for the REA contract.** The operator's research summary names a *Research
Evidence Architecture & Schema Contract v0.1* (Stage B). The search for it covered:

- TC `main`;
- two TC branches, `ccr-a93d18f0-7tyn4t` and `feature/specialized-council-handoffs`;
- the titles and bodies of TC and ACE pull requests;
- `triagecore-signed-intent`.

**Not inspected:**

- TC's other branches (there are 142 heads in all);
- artifacts kept outside any repository.

The contract was found in none of the searched places. That is not evidence that it is
absent elsewhere. TC's backlog already treats one operator plan as "an off-repository
planning artifact" (`docs/current_backlog.md:310`), and this contract may be the same kind
of thing.

## 2. Findings in brief

1. **Most handoff terms already have TC semantics, but scattered.** They appear across
   contracts and operations records, not in one vocabulary.
   - *Formal definitions exist* for artifact identity, the claim taxonomy for model
     reviews, the evaluation boundary, source verification for compressed context, and
     contradiction (in the MCI contract).
   - *Consistent practice exists, but no record type*, for hypothesis, interpretation,
     reproduction and corroboration.
2. **Adjudication has no definition** in the inspected TC or ACE sources. Its only
   occurrence is "UNADJUDICATED BOUNDARY OBSERVATIONS"
   (`docs/operations/privacy-propagation-2026-08-29.md:232`). The council defines it
   locally (row 11).
3. **The REA v0.1 Stage B contract was not available.** By the operator summary's account,
   it is where the full separation lives: artifacts, observations, claims, hypotheses,
   evaluations, interpretations, adjudications and decisions. Every row of section 3
   therefore keeps an open REA column. Where the contract defines a term, it should take
   precedence for TC-compatible meaning (SC-1).
4. **Four homonyms need disambiguation.**
   - *Claim*: an assertion, or a capability claim.
   - *Council*: TC's `worker_council` runner, or this evaluation procedure.
   - *Reproduction*: restatement, or independent re-derivation.
   - *Observation*: an MCI runtime-effect record, or a quotation from a packet.

   Section 3 resolves each.
5. **TC already declines knowledge-specific primitives.** It refuses to add
   `KnowledgeClaim`, `TrustLevel`, `EpistemicAuthority`, `MemoryCapability` or
   `KnowledgeSource` on the strength of an external candidate
   (`docs/research/candidates/governed-knowledge-substrate.md:163`). The council's
   epistemic vocabulary (standing, independence class, support assessment) therefore stays
   outside TC (SC-7).
6. **ACE's oracle-independence practices transfer, but co-locating the oracle does not.**
   ACE stores the scored oracle inside the scenario file
   (`schemas/scenario_fixture.schema.json:5`). That suits deterministic producers, but
   model critics would read it. The council keeps answer keys in separate files (section
   6).

## 3. Term-by-term reconciliation

*Status* describes the inspected sources only:

- **defined**: a contract or protocol states the meaning;
- **practiced**: the meaning is used consistently, with no record type;
- **absent**.

| # | Term | TC / ACE expression | Status | Council treatment | REA v0.1 Stage B |
|---|---|---|---|---|---|
| 1 | Artifact identity | A mutable tag "must not stand in for an immutable artifact identity" (`docs/research/candidates/nemotron-3.5-lightning-governed-execution-specialist.md:39`). Aliases without artifact identity are not identity (`docs/security/runtime_integrity_model_provenance_policy.md:157`). Hashes "establish byte identity only" (`docs/operations/local-heavy-diagnostic-2026-08-07.md:248`). Commitments "are not signatures or evidence of independent computation" (`docs/research/monitoring-coverage-contract-v0.1.md:684`). | defined | **Reuse.** Packets, prompts and outputs are identified by the SHA-256 of their exact bytes. A model is identified by its exact version; aliases are labels only (`model.alias_labels`). A hash establishes byte identity, nothing more. | open |
| 2 | Observation | MCI `kind=observation` is a witness record of a runtime effect boundary (`monitoring-coverage-contract-v0.1.md:149`). Operations records keep what TC received apart from what a backend did (`local-heavy-diagnostic-2026-08-07.md:181`), and keep source-confirmed apart from runtime-observed (`:215`). | defined (MCI), practiced | **Narrow.** A council observation is an exact quotation from a packet segment, checkable against bytes (record V5). MCI observation records are not imported. | open |
| 3 | Claim | *Assertion sense:* the review-protocol taxonomy `context-supported`, `uncertain-inference`, `unsupported`, `authorized-next-action` (`docs/evals/evidence_bound_review_protocol.md:33-36`); "Cite or downgrade" (`:40`); "Confidence is not evidence" (`:43`). *Capability sense:* `claim` appears in TC's existing-vocabulary list (`governed-knowledge-substrate.md:142`) and is a lifecycle state, "issued -> claimed -> completed" (`triage_core/capability_claims.py:19`). | defined (both senses) | **Reuse the assertion sense only.** Proposed correspondence, not adopted: `context-supported` ≈ a finding with a verified quotation; `uncertain-inference` ≈ an interpretation held at lower confidence; `unsupported` ≈ adjudicated `unsupported`. Adopt "cite or downgrade" and "confidence is not evidence" as adjudication rules. **Do not import** `authorized-next-action` or the capability sense; both are action governance. | open |
| 4 | Hypothesis | A statement "is a hypothesis to be tested, not an observation" (`governed-knowledge-substrate.md:45`). "A hypothesis that proved wrong, recorded rather than dropped" (`docs/operations/classifier-terminal-fallback-2026-08-29.md:216`). | practiced | **Reuse.** A hypothesis is a proposition put forward for testing. It is never recorded as an observation, and it is kept when refuted. `pc-eer/0.1` has no hypothesis field: critics' hypotheses stay in interpretation text (open question, section 9). | open |
| 5 | Interpretation | "Scoring and score interpretation happen outside TriageCore" (`docs/research/eval_taxonomy.md:109`). Quality gates "qualify cost interpretations but never rewrite or rank them" (`docs/operations/control-plane-invariant-checklist.md:43`). Downstream synthesis must not collapse distinctions (`local-heavy-diagnostic-2026-08-07.md:215`). | practiced | **Define locally.** An interpretation is a reviewer's reading that rests on cited observations. It is stored only in `interpretation` and can never be recorded as an observation. | open |
| 6 | Evaluation | TC "must treat evaluator findings as external artifacts" (`docs/evals/evaluation_handoff_contract.md:75`). "Evaluator output remains untrusted and externally interpreted" (`docs/evals/external_evaluator_adapter_contract.md:152`). `block` is reserved for cases that cannot be scored safely (`eval_taxonomy.md:51`). Evaluator independence is part of the governance kernel (`docs/architecture/triagecore_identity.md:45`). ACE: "Evaluator Scores Are Not Approvals" (`docs/evaluator_signal_model.md:48`). | defined (as a boundary) | **Reuse the boundary.** Council output is evaluation evidence for human judgment: it is external to TC and never an approval. Adopt the strictness of `block`: a run that cannot be scored deterministically fails closed and is not scored as a failure. | open |
| 7 | Provenance | Canonical definition in this repository's `trust-vocabulary.md`. TC: provenance must not be "treated as a trust anchor without evidence" (`docs/research/triagecore_research_question.md:18`). | defined (canonical) | **Reuse the canonical definition.** Extend it with declared lineage and transformation records. Declared lineage is an assertion, not verified dependence. | open |
| 8 | Source verification | Compressed summaries "do not replace source verification" (`docs/change/requests/CR-005-local-preflight-context-compression.md:19`; reminder at `triage_core/compression.py:118`). "A summary is not a substitute for original messages" (`monitoring-coverage-contract-v0.1.md:716`). A matching digest without access to the bytes does not satisfy review (`:714`). | defined (compressed context) | **Reuse and generalize.** A transformed view never replaces checking its source. Transformations carry `fidelity_check`, and fidelity reported by the transformation's own producer is not verification. | open |
| 9 | Reproduction | The reproducibility standard (`triagecore_research_question.md:108`). A second reader derives expectations "without using a future reconciler's output as the oracle" (`monitoring-coverage-contract-v0.1.md:731`). "A reviewer can reproduce them rather than trust this record" (`docs/change/requests/CR-134-public-export-admission-contract.md:215`). A reproduction record (`docs/operations/monitoring-coverage-baseline-2026-10-22.md:119`). | practiced | **Define locally, with two senses (SC-8).** *Restatement* (copying or repeating) adds no standing. *Reproduction* is independent re-derivation by a distinct method, witness and traceable record. Only a reproduction can add standing, and only as a separate evidence item. | open |
| 10 | Contradiction | Conflicts in source sequences or record IDs "are integrity failures, not competing opinions" (`monitoring-coverage-contract-v0.1.md:237`). "Do not choose a favorable branch" (`:408`). Contradictory evidence "remains visible and does not become optimistic permission" (`triagecore_identity.md:78`). | defined (MCI), principle | **Reuse the distinction.** Records that are inconsistent with each other are an `integrity_conflict`, an integrity finding rather than an opinion. Competing assessments are retained positions. Neither is resolved by picking a favorable branch. | open |
| 11 | Adjudication | No definition. The only occurrence is "UNADJUDICATED BOUNDARY OBSERVATIONS" (`privacy-propagation-2026-08-29.md:232`), with open lanes "MARKED not decided" (`:262`). Related practice: decide the cause before accepting a lesson (`docs/verification_guide.md:128`). ACE: mismatches are aligned explicitly, and neither side is patched to appease the other (`docs/oracle_alignment_findings.md:20-22`). | **absent** | **Define locally.** Adjudication is a recorded human decision about how a study output is scored against independently specified expectations. It is a separate record that confers no authority, and contested items stay contested (record design, section 7). No TC change is proposed. | open; likely defined there |
| 12 | Corroboration | Distinguish the basis for a conclusion from corroborating evidence (`docs/operations/privacy-declaration-evidence-join-2026-08-29.md:45`). "Agreement between two producers is insufficient" (`monitoring-coverage-contract-v0.1.md:711`). "Only an exact retransmission of the original producer record is idempotent" (`:202`): a repeat adds nothing. | practiced | **Reuse.** Corroboration requires a dependence analysis. Agreement among reviewers is recorded as attention, never as corroboration (record constant). | open |
| 13 | Decision and authority | `Approved` status alone does not authorize (`docs/change/requests/CR-130-approved-status-authority-semantics.md:43`). "Proposed != Authorized != Implemented" (`AGENTS.md:23`). Agent verdicts are not authority (`AGENTS.md:51`). Observation, recommendation, authorization, execution and evaluation "do not silently confer authority on one another" (`triagecore_identity.md:75`). | defined | **Do not import** decision semantics. Council records contain no decisions. The council does adopt the *negative* constraint: its outputs confer no authority (SC-3). | open (REA lists decisions) |
| 14 | "Council" | TC's `worker_council` is an execution runner (`triage_core/orchestration.py:82`, `triage_core/context_budget.py:27`) with a role taxonomy `2026-06-worker-council-v2` (`triage_core/task_ledger.py:21`). | defined (different meaning) | **Keep distinct (SC-6).** Use the `pc-` prefix for every identifier. Never use a bare `council` as a runner, role or event name. Never register the council as a TC runner. | n/a |

## 4. The six invariants

| Invariant | TC / ACE precedent | Council rule | Where enforced (proposed) | Development fixture |
|---|---|---|---|---|
| Evidence is not authority | Separation of functions (`triagecore_identity.md:75`); no verdict "is action permission" (`monitoring-coverage-contract-v0.1.md:223`); ACE: "The world can provide evidence. It cannot grant authority." (`docs/trust_boundary_eval_family.md:9`) | No decision vocabulary. `authority: none`. Authorization by an evaluator is an overreach marker. | record schema; adjudication | PC-F01 (subject infers that a review can stop) |
| Interpretation is not observation | Source-confirmed and runtime-observed kept apart (`local-heavy-diagnostic-2026-08-07.md:215`); hypothesis not observation (`governed-knowledge-substrate.md:45`) | Observations are verified quotations; interpretation is a separate field. | record V5, V6 | all; PC-F02 (an interpretation in a briefing) |
| Repetition is not independent corroboration | `monitoring-coverage-contract-v0.1.md:202`, `:711`; basis versus corroboration (`privacy-declaration-evidence-join-2026-08-29.md:45`) | Declared lineage projected to roots. `agreement_is_not_corroboration`. Error correlation measured. | record V9, V10; protocol M10 | PC-F02 |
| Missing evidence is not negative evidence | "Absence in a corpus that predates the feature ... carries no information" (`privacy-declaration-evidence-join-2026-08-29.md:145`); an ambiguous timeout "is not proven nonexecution" (`monitoring-coverage-contract-v0.1.md:36`); an absent usage record shows what TC received (`local-heavy-diagnostic-2026-08-07.md:181`) | The support scale separates "not supported" from "undermined". An inference from absence must check whether the source could have recorded the event. | record vocabulary; operator O3 | PC-F03, and PC-F06 as its control |
| Disagreement is not erased by synthesis | "Retain both verdicts, and flag behavioral disagreement for human assessment" (`monitoring-coverage-contract-v0.1.md:235-236`); "Recorded as open rather than resolved by inference" (`privacy-declaration-evidence-join-2026-08-29.md:173`); "deliberately not conflated" (`privacy-propagation-2026-08-29.md:240`) | Positions partition assessments. Dropped positions are listed with a justification. Unresolved disagreements are recorded. | record V7, V8; protocol M9 | PC-F04 |
| A transformation cannot silently raise standing | `CR-005-local-preflight-context-compression.md:19`; byte identity "not semantic equivalence of a summary" (`monitoring-coverage-contract-v0.1.md:180`); "Child context is not a review of discarded parent context" (`docs/research/monitoring-coverage-fixture-spec-v0.1.md:170`); an exemption "cannot launder" a missed deadline (`monitoring-coverage-contract-v0.1.md:281-282`); ACE `memory_laundering_001`, `provenance_confusion_001` | Each transformation carries its ceiling sources and fidelity check. Effects are tied to findings. Self-reported fidelity is not verification. | record V11; operator O3 | PC-F05 |

## 5. Not imported: action-governance semantics

The council takes none of the following. It holds no TC grant, and nothing in this
directory is a TC change request.

- **Control-plane decision vocabularies.** TC's `allow`, `deny` and
  `require_human_approval` (`eval_taxonomy.md:41-43`), and ACE's `allow`, `block` and
  `observe`.
- **The `authorized-next-action` category** (`evidence_bound_review_protocol.md:36`).
- **TC's runtime authority machinery:**
  - capability claiming and its lifecycle (`capability_claims.py`);
  - human authorization receipts;
  - admission evidence;
  - route decisions;
  - mediated execution;
  - MCI exemptions;
  - signed ledger events.
- **The `worker_council` runner and its role taxonomy.**
- **CR lifecycle grants.** Council documents may *describe* their own status using the
  distinction "proposed, not authorized, not implemented". That is a status description,
  not a grant.

## 6. Divergences from ACE, and what is adopted

**Diverges.**

1. **Oracle location.** ACE's scored `expected_outcome` sits in the scenario file
   (`schemas/scenario_fixture.schema.json:5`). Council answer keys sit in separate,
   adjudicator-only files, because the critics are models and would read them.
2. **Who assigns codes.** ACE expects the system under test to export stable reason codes
   (`docs/reason_taxonomy.md:5`). Council critics write free text and adjudicators assign
   codes. This keeps the defect taxonomy out of every prompt.
3. **Trust model.** ACE trusts the producer to report honestly (`README.md:13`). The
   council verifies critics' quotations mechanically, and treats their claims as
   unverified until adjudicated.
4. **Decisions.** ACE scores decisions. The council has none to score.

**Adopted.**

- An independent oracle: expectations are never derived from the system's internals
  (`docs/reuse_manifest.md:10`).
- Allow-side controls, "so an always-block system cannot score well" (`README.md:28`).
  PC-F06 and the traps play this role.
- Self-tests are not evidence: a mock mode "carries no information about any evaluated
  system" (`README.md:53`). A council pipeline dry run with echoed outputs would likewise
  be no evidence.
- Evaluating the evaluator: "If any adversarial actual ever scores `match: true`, the
  evaluator itself has regressed" (`docs/adversarial_actuals.md:5`). Drafting used negative
  tests of the scratch checkers in the same spirit.
- Oracle-alignment findings are recorded rather than patched away
  (`oracle_alignment_findings.md:20-22`).
- Stable codes are kept apart from diagnostic detail (`reason_taxonomy.md:5`).

## 7. Semantic contract

These are proposed normative statements for council artifacts. "Must" states proposed
conformance for council work. It asserts nothing about TC or ACE.

- **SC-1, vocabulary precedence.**
  - Shared terms use the canonical [trust vocabulary](../../trust-vocabulary.md).
  - Where TC defines a term in section 3, the council uses that meaning or a stated
    narrowing of it.
  - Council-local definitions apply only where the inspected sources define nothing.
  - When the REA v0.1 Stage B contract is supplied, its definitions take precedence for
    TC-compatible meaning, and this document is revised.
- **SC-2, no action governance.** Council artifacts must not emit or imply control-plane
  decisions, approvals, exemptions, capability claims, admission evidence, routing or
  signatures. This includes the `authorized-next-action` category.
- **SC-3, evaluation is not authority.** No council output confers authority on anyone or
  anything. Consumers treat outputs as evidence for human judgment. Every record carries
  `non_claims.authority: none`.
- **SC-4, external-artifact boundary.**
  - Council records are external to TC.
  - TC could ingest them only through a separately approved TC change request, as static
    files across TC's file-based evaluation handoff boundary
    (`evaluation_handoff_contract.md:75`).
  - No runtime coupling and no code imports exist in either direction.
- **SC-5, independent oracle.**
  - Expectations are derived from case packets alone. They are never derived from council
    outputs or from TC or ACE internals (`docs/reuse_manifest.md:10`;
    `monitoring-coverage-fixture-spec-v0.1.md:17`).
  - They are stored apart from critic-visible material.
  - They become an oracle only after a human second reader re-derives them (protocol G1).
- **SC-6, naming.**
  - Council identifiers use the `pc-` prefix.
  - A bare `council` is never a runner, role or event identifier.
  - The council is not a TC runner.
- **SC-7, no TC primitives.**
  - Council epistemic terms (standing, independence class, support assessment, adjudication
    codes) stay outside TC.
  - The council proposes neither the primitives TC has declined
    (`governed-knowledge-substrate.md:163`) nor equivalents.
  - Any later proposal must first pass TC's existing-vocabulary test (`:131`) and rest on a
    demonstrated semantic insufficiency (`:179`).
- **SC-8, two senses of reproduction.**
  - Restating or transforming a claim must not silently raise its standing.
  - Additional verification needs a distinct method, witness and traceable record. This
    wording follows the operator's research summary, section 9.
- **SC-9, integrity is not opinion.**
  - Inconsistent records are integrity findings (`monitoring-coverage-contract-v0.1.md:237`).
  - Competing assessments are retained positions.
  - Neither is settled by picking a favorable branch (`:408`).
- **SC-10, status discipline.**
  - Every council artifact states its status.
  - No status value confers authority (`CR-130-approved-status-authority-semantics.md:43`).
  - A council artifact may be proposed, accepted and implemented only through separate,
    recorded operator decisions.
- **SC-11, read-only toward TC and ACE.** Council work reads TC and ACE only as copies
  pinned at a commit, and never writes to either.

## 8. Layering

Adapted from the operator's research summary, section 9.

| Layer | Responsibility | Not a substitute for |
|---|---|---|
| Epistemic records (`pc-eer`, consistent with TC semantics) | What was observed, asserted, interpreted, contested and evaluated, with provenance | Truth |
| Council critics | Bounded argument analysis and provisional assessments | Human or institutional decision authority |
| Human adjudication | Scoring against independently specified expectations | Settling contested questions |
| Technical validators (none in v0.1) | Reproducible checks against specified contracts and observables | Conceptual or ethical judgment |
| TC action governance, only if ever separately authorized | Governing consequential operations on a named execution path | Isolation or safety assurance; council evaluation |

## 9. Open questions

1. **Reconciling with REA v0.1 Stage B** (protocol D10). If the contract defines record
   types for hypothesis, interpretation and adjudication, `pc-eer` should probably carry
   them by reference rather than restate them.
2. **The review-protocol mapping.** Should TC's evidence-bound review categories be mapped
   formally to council findings? A correspondence is sketched in row 3; it is not adopted.
3. **The trust vocabulary.** Should any council term join the canonical trust vocabulary?
   Candidates are *corroboration*, *standing* and *adjudication*. None is proposed now:
   the vocabulary's own rule keeps domain-specific terms local.
4. **Where fixtures live.** Should ACE ever host council fixtures? Recommended no: ACE
   scores control-plane decision contracts, a different domain.
5. **Branch coverage.** Only two of TC's 142 branches were inspected, so terms defined only
   on unmerged branches may be missing here.

## 10. No-change verification

At the end of drafting, `git status --short` in the TC, ACE and `triagecore-signed-intent`
clones printed nothing. The only operation performed against TC beyond the clone was a
read-only `git fetch` of the two branches named in section 1, into the local clone. No
branch, commit, push, issue or pull-request comment was made in any of the three
repositories. The only repository changed is this one, on its development branch.

To reproduce the citations:

```sh
git clone https://github.com/coreytshaffer/TriageCore triagecore
git -C triagecore checkout 4e9f238512eec4d9fc417542745962783d3e675f
git clone https://github.com/coreytshaffer/agent-control-evals ace
git -C ace checkout b876a287fc27701e79f16208640f86845f1edafc
# then compare the files below with `sha256sum` and read the cited lines
```

## Appendix A. Pinned file hashes (SHA-256)

**TriageCore at `4e9f238`.**

| File | SHA-256 |
|---|---|
| `AGENTS.md` | `58d83280245b053718b04cab0fe84c8d9640c09780018761bcf880add088a77e` |
| `docs/architecture/triagecore_identity.md` | `409bcc85440f6db92e120b34db3cee3b27d6a1082ab9c949bea90a4d8dd2e6b5` |
| `docs/research/triagecore_research_question.md` | `942e344c82ad0b4133601970fe126239aaeb03a949a4791103c1d9ea49fad515` |
| `docs/research/candidates/governed-knowledge-substrate.md` | `9d4de98591a97c5e4bf6167880abc560f156c6fdf80848e6dca5e241c19be533` |
| `docs/research/candidates/nemotron-3.5-lightning-governed-execution-specialist.md` | `7c4122a79401c2461dfc116152412618b18280188c9fff7121b9b4d7127a82c7` |
| `docs/research/monitoring-coverage-contract-v0.1.md` | `f8ece79edc562a30c413f7b3946151b6a87213ad4d5c6e67a4ebfc9b83e3d643` |
| `docs/research/monitoring-coverage-fixture-spec-v0.1.md` | `9039f4ea979823c7a713ec28842c6a73b1880c80f275f9e8ca18b839974ab024` |
| `docs/research/eval_taxonomy.md` | `550e262e981eef0b5d3c5dce56a0986e001d79bbc065437572b0ce98aed92d7f` |
| `docs/evals/evidence_bound_review_protocol.md` | `29a77ac5659d415b02c64d7ae43c29555025719c99300f0a34032224ae99720d` |
| `docs/evals/evaluation_handoff_contract.md` | `4391d4e073039a22a39e8017c76eea595bb48514c3420869742cee677704977a` |
| `docs/evals/external_evaluator_adapter_contract.md` | `5f4819e8beea85a0188456ea30ef11c15ea0880c2827fd915c55927438f32572` |
| `docs/change/requests/CR-005-local-preflight-context-compression.md` | `7bfff08456c471ea0811903d3088345abbb04b6e43cec6316fc2fc299e92608a` |
| `docs/change/requests/CR-130-approved-status-authority-semantics.md` | `56443bbf0c5c391ff61c8bf9597a347030324a9edcb4f3ab6ead6d8957fb7f16` |
| `docs/change/requests/CR-134-public-export-admission-contract.md` | `2fa5b469b40c81ee1ff56edda3800bfea2dca0daf86f17c811f0874ee8866263` |
| `docs/operations/local-heavy-diagnostic-2026-08-07.md` | `faa73f54d4eddbfa982a8292a5b372832482b0a176972b7b279edb352a5b1de2` |
| `docs/operations/privacy-declaration-evidence-join-2026-08-29.md` | `3d7552f4ba936d126d7d883622fefe21067fbb2dc80e93990858b94cf485aeba` |
| `docs/operations/privacy-propagation-2026-08-29.md` | `f368df4495cadee3b1de5d1d3ac47adf1c6d50596f471b8adc1c040ffaafca03` |
| `docs/operations/classifier-terminal-fallback-2026-08-29.md` | `7ef412afc5c39020c5e3d5bf49207bffb1be6a6c53ac3f4ba80fa0f4c1d5490f` |
| `docs/operations/control-plane-invariant-checklist.md` | `dc51be9e257e45c47da79f3e6ebebd9d1f3e579bdc0b4598fdd8f816fb171815` |
| `docs/operations/monitoring-coverage-baseline-2026-10-22.md` | `66a5bd01a47e4418209be3030fe4763fd297027b2a2eace82b701fc3e91c5b5a` |
| `docs/verification_guide.md` | `6a32c4ac1d211378b474b4cdcdc75ee8973cded4ee45bc07875572c904877bb6` |
| `docs/security/runtime_integrity_model_provenance_policy.md` | `0d310931915ac1517c82a73d8608b298333fd90ee89b4fd99848ae18eb1b48e8` |
| `docs/current_backlog.md` | `73f8dd26c6b609f881f9b2dd60dc474b2baa07d8efdc8a81bf2343c667ae413c` |
| `triage_core/capability_claims.py` | `5667e30c1718048cb11c49500c92070f89e305ade92703d989b08b7b1846603f` |
| `triage_core/compression.py` | `50f62b8f7709349b883a74938d4c819dfa51f89a5bcd8bc2539baf3cdf711e81` |
| `triage_core/task_ledger.py` | `ab9be73a38e3e7f2cb4b1dec1a0436f5338380239ac19e2bd105126affa39f61` |
| `triage_core/orchestration.py` | `ab23cf09378ea450a7c574c370ce94bea4eece0f375e839faa02f1502498e875` |
| `triage_core/context_budget.py` | `bb816282d46eba8a49dbd29f45fa1929368d288634423d40b90a2829ae3d399d` |

**agent-control-evals at `b876a28`.**

| File | SHA-256 |
|---|---|
| `README.md` | `ae7ee30ea41a087752775e67c096fa9ec3a7ca5b5e1a8c49662220731e9002b2` |
| `docs/evaluator_signal_model.md` | `3d600484f894c63635597f4c443be2102319a53ff5395278c4946bdf98ff3936` |
| `docs/oracle_alignment_findings.md` | `1f5fc5eecfeb0f0bf377fe25cf8f19c1ff07e52cc7ee372f06e3c6d5fda89835` |
| `docs/trust_boundary_eval_family.md` | `8634fde500f009763d6f0bf82702a5297ad6680462ac1339becffc4f1f49ea22` |
| `docs/reuse_manifest.md` | `b3843549caba7c9434658b6acabd7c9b4e7c9eaf7f699ab5394c5daa9cc44c04` |
| `docs/adversarial_actuals.md` | `a979b7d5c48fdd546e252e0ec795105832f616ab978e57ccedce852ce4ea9ead` |
| `docs/reason_taxonomy.md` | `7f87caf80b6ca5e4d0af29b976b138cfa0ef635502212e7ce12254229d664689` |
| `schemas/scenario_fixture.schema.json` | `f0a79c29beb782d8cde8309756b01b8d3d9d561609f912c1c6199f45b16eab41` |
| `fixtures/scenarios/provenance_confusion_001.json` | `ce102c092cb3bbcc338fc62d8c26744831c51dfcf2fa0e0442c45b39e52197dc` |
| `fixtures/scenarios/memory_laundering_001.json` | `f5c7c9bcdde328a736c35cc92af82bac156253a0f6e4e9018c7cee3e3f8d6044` |

**This repository at `78371f0`.**

| File | SHA-256 |
|---|---|
| `trust-vocabulary.md` | `c082ae38b3ddbb963108eae749967239c25039f6c5688de9613c33d8e243f018` |
