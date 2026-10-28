# Semantic-Contract Reconciliation — Philosophical Council, TriageCore, REA v0.1 and agent-control-evals (r1)

**Status: proposed planning artifact, revision r1 (2026-10-28).** This is a read-only
reconciliation and it changes nothing in TriageCore (TC) or agent-control-evals (ACE). It
is not reviewed and not accepted, and it grants no authority. It supersedes r0 (commit
`ea9ecbd`), which remains addressable in history. Section 10 records the no-change check.

## 1. Scope, inputs and method

**Question.** Which existing research semantics can the council reuse, narrow or leave
behind, and where must it define terms of its own? The constraint is unchanged from r0:
none of TC's action-governance responsibilities may come with them.

**Three sources of meaning,** kept apart throughout:

- **TC repository (inspected).** What TriageCore's documents and code say at the pinned
  commit. This is the "inspected TriageCore implementation". Most of the relevant meaning
  is documentary; where it lives in code, the code is cited.
- **REA v0.1 Stage B (external research definition).** The operator supplied *Research
  Evidence Architecture & Schema Contract v0.1*, Stage B revision, on 2026-10-27.
  - It describes itself as "a user-facing design artifact outside the TriageCore
    repository".
  - Its status line records that storage-neutral semantic closure passed.
  - It also records that carrier-specific encoding is not validated, design freeze is
    "no", and there is no implementation or integration authority.

  It therefore *defines* record semantics. It does not describe anything TriageCore
  implements.
- **Council usage.** What this directory means by a term, as revised in r1.

**Pinned inputs.** Citations are `path:line` at these commits, or REA section numbers.
Appendix A gives file hashes.

| Input | Identity | Notes |
|---|---|---|
| `coreytshaffer/TriageCore` | `4e9f238512eec4d9fc417542745962783d3e675f` (2026-10-26) | Inspected |
| `coreytshaffer/agent-control-evals` | `b876a287fc27701e79f16208640f86845f1edafc` (2026-10-17) | Inspected |
| `coreytshaffer/triagecore-signed-intent` | `85c44709cbaf64fa06d7e81c8c1ed52ffbedabcf` (2026-10-25) | Searched for the REA contract in r0; not found |
| REA v0.1, Stage B | Operator file received as `research-evidence-architecture-schema-contract-v0.11.md`; SHA-256 `a0ece23a770d603e4220bc0847cdf02fdbb96e640022d46d8794ac4391f733e3`; 1,401 lines; drafted 2026-08-14 | See the provenance notes below |
| this repository, r0 | `ea9ecbd9ccf00dd8712cc029d29e5d97d7a06d63` | Superseded by this revision |

**REA provenance notes.**

- **Which copy.** The operator identifies this file as the "(1)" copy, the Stage B
  revision. The Stage A copy was not supplied to this session and is not used.
- **Its TC pin.** REA's own evidence pin into TC is
  `codex/agents-governance-separation@8cff76d370b88dfbed8180844112c08ef6260a40`. On
  2026-10-27 no remote branch or ref pointed at that commit. REA section 25 records a local
  checkout, so the pin was not inspected.
- **Not stored here.** The file is not stored in this repository.

**Method.**

- TC and ACE were read from shallow clones, with nothing written to them, as in r0.
- REA was read in full.
- For each handoff term, the TC repository's usage and REA's definition were compared
  separately, then reconciled with council usage.

## 2. Findings in brief

1. **REA defines what TC only practices.** REA supplies formal definitions for every
   handoff term. The TC repository practices most of them but defines few (r0's finding
   stands).
   - The council now aligns with REA's definitions.
   - It claims **alignment, not conformance**. REA has no carrier encoding, no design
     freeze and no implementation, so there is nothing to conform to mechanically.
2. **Adjudication.**
   - *REA:* "an explicit finding resolving or narrowing a discrepancy without deleting
     predecessors" (REA §5.3), with an `AdjudicationPayload` (§7.12).
   - *TC repository:* still no definition.
   - *r0:* defined adjudication as a human scoring decision. That merged two REA roles,
     scoring and adjudication, and borrowed decision language that REA keeps separate
     (§7.13).
   - *r1:* scoring is a separate activity. Adjudication resolves or narrows a recorded
     discrepancy and preserves its predecessors.
3. **Observation.**
   - *REA:* "a bounded result directly observed through a stated method" (§5.3, §7.4).
   - *r0:* narrowed "observation" to a critic's quotation.
   - *r1:* a quotation is a citation, that is, a claim about what the packet says. The
     validator's byte-exact check of it is the observation, and its result is recorded
     with REA's source-verification values (§5.4).
4. **Evaluation.**
   - *REA:* reserves `evaluation` for assessing a hypothesis or theory under a declared
     scheme (§5.3, §7.9).
   - *Council:* the "epistemic evaluation record" takes its name from the handoff and uses
     "evaluation" in the ordinary sense of critique. In REA terms its contents are
     interpretations, observations, discrepancies and a derived analysis.
   - The REA sense applies to the study's own hypotheses H1–H4, in the pilot, after
     registration. Whether to rename the record is decision D13.
5. **Confidence.**
   - *REA:* confidence is `high`, `medium`, `low` or `unknown`, with a rationale. "A model's
     self-reported confidence MUST NOT promote source verification, reproduction state, or
     evidence strength" (§6).
   - *r1:* the critics' 0–100 number is renamed `reported_confidence_pct`. It is a measured
     self-report, never REA confidence, and it promotes nothing.
6. **Absence.**
   - *REA:* has no universal null. `Missing`, `Unknown`, `Redacted` and `NotApplicable` are
     distinct, and optional absence is omission (§4, §9.2, decision DD-RE-006,
     counterexample 24).
   - *r0:* used `null` for several different absences.
   - *r1:* removes `null` from every council schema.
7. **Homonyms.** Six now, against r0's four.
   - From r0: *claim*, *council*, *reproduction*, *observation*.
   - New in r1: *evaluation* (finding 4) and *adjudication* (finding 2).
8. **Two layers stay separate.**
   - TC declines knowledge-specific primitives
     (`governed-knowledge-substrate.md:163`).
   - REA keeps the research substrate apart from TC's operational evidence schema:
     "This contract does not silently replace it" (§19).

   Council records are research records. They are neither TC operational records nor TC
   primitives.
9. **ACE.** The divergences stand (section 6).

## 3. Term-by-term reconciliation

| # | Term | TC repository (inspected) | REA v0.1 Stage B | Council treatment (r1) |
|---|---|---|---|---|
| 1 | Artifact identity | A mutable tag must not stand in for artifact identity (`docs/research/candidates/nemotron-3.5-lightning-governed-execution-specialist.md:39`; `docs/security/runtime_integrity_model_provenance_policy.md:157`). "Hashes establish byte identity only" (`docs/operations/local-heavy-diagnostic-2026-08-07.md:248`). | `Artifact` (§7.1): a content hash "identifies the preserved bytes, not their meaning or authenticity". A changed copy is a new artifact linked to its parent. "A digest never grants retrieval or disclosure permission" (decision DD-RE-004). | **Align.** Packets, critic outputs and prompts are artifacts identified by SHA-256 of their exact bytes. A model is identified by its exact version; aliases are labels only. |
| 2 | Activity, trial, experiment | Study and run labels separate exploratory runs from studies (`docs/evidence_schema.md:26-27`). | `Activity` (§7.2). A trial is "an execution attempt under an identified configuration and task snapshot". An experiment adds registered hypotheses, protocol, controls and stopping rules (§14). | **Align.** A critic call is a trial. The feasibility study is an investigation made of trials, not an experiment. The pilot is an experiment: it needs registrations and stopping rules (protocol sections 10–11). |
| 3 | Observation | MCI `kind=observation` records runtime effects (`monitoring-coverage-contract-v0.1.md:149`). Operations records keep what TC received apart from what a backend did (`local-heavy-diagnostic-2026-08-07.md:181`). | "A bounded result directly observed through a stated method" (§5.3), with a typed value (§7.4). | **Corrected from r0.** A critic's quotation is a citation, and the validator's byte-exact substring check is the observation. MCI records are not imported. |
| 4 | Claim | *Assertion sense:* the review-protocol taxonomy (`docs/evals/evidence_bound_review_protocol.md:33-36`). *Capability sense:* "issued -> claimed -> completed" (`triage_core/capability_claims.py:19`). | An atomic asserted proposition with supporting and opposing records (§7.5). | **Align, assertion sense only.** The subject's conclusions, a critic's quotations, and an answer key's planted items are claims. The capability sense is action governance and is not imported. |
| 5 | Hypothesis and registration | "A hypothesis to be tested, not an observation" (`governed-knowledge-substrate.md:45`). Wrong hypotheses are "recorded rather than dropped" (`docs/operations/classifier-terminal-fallback-2026-08-29.md:216`). | `HypothesisPayload` requires a scope, predicted pattern, primary outcome, falsification criterion and evaluation method (§7.6). `HypothesisRegistration` is separate and records outcome-access state (§7.7). | **Align.** H1–H4 are restated in this form, with provisional criteria (protocol section 2), and are registered before the pilot. Feasibility creates no evaluation of them. |
| 6 | Theory | No definition. | A scoped explanatory structure; a failed prediction does not automatically falsify it (§7.8, §5.7). | **Not used.** The study proposes no theory. |
| 7 | Evaluation | Scoring and interpretation happen outside TC (`docs/research/eval_taxonomy.md:109`). Evaluator output is untrusted and externally interpreted (`docs/evals/external_evaluator_adapter_contract.md:152`). | "A bounded assessment of an identified hypothesis or theory under a declared evaluation scheme" (§5.3, §7.9). With no qualifying evaluation there is no record; an `untested` record is not created (§5.7). | **Homonym (D13).** The record's name keeps the ordinary sense. In the REA sense, only H1–H4 are evaluated, in the pilot. TC's boundary still applies: council output is external evidence and never an approval. |
| 8 | Interpretation | Practiced, not defined (`eval_taxonomy.md:109`; `docs/operations/control-plane-invariant-checklist.md:43`). | "A reasoned reading derived from observations or claims" (§5.3). It "MUST NOT be stored as an observation merely because it is strongly supported" (§7.10). | **Align.** Findings and overall support assessments are interpretations derived from cited segments. |
| 9 | Discrepancy | MCI integrity findings (`monitoring-coverage-contract-v0.1.md:237`). Lanes "MARKED not decided" (`docs/operations/privacy-propagation-2026-08-29.md:262`). | A first-class "conflict, missing link, ambiguity, or verification failure", with kind, classification and status. Competing records stay accessible (§7.11). | **Align.** Disagreements between critics are open discrepancies inside a record. Conflicts between scorers, between a critic and the answer key, or between an author and a second reader are separate discrepancy records (record design, section 7). |
| 10 | Adjudication | **Absent.** One occurrence: "UNADJUDICATED BOUNDARY OBSERVATIONS" (`privacy-propagation-2026-08-29.md:232`). | "An explicit finding resolving or narrowing a discrepancy without deleting predecessors" (§5.3). It must not mutate or delete what it evaluates, and may designate records usable "for a named analysis" (§7.12). | **Adopt REA; corrects r0.** Scoring is not adjudication. Adjudication acts only on recorded discrepancies, and its scope is a named analysis (section 9, question 2). |
| 11 | Decision and authority | `Approved` status alone does not authorize (`docs/change/requests/CR-130-approved-status-authority-semantics.md:43`). "Proposed != Authorized != Implemented" (`AGENTS.md:23`). TC's operational schema records `review_decision` and `supervisor_decision` (`docs/evidence_schema.md`). | A human or governed choice with rationale, scope, conditions and expiration. "Recording a decision does not prove the decision maker had authority" (§7.13). "LedgerRecorded != Authorized" (§4). | **Do not import decision semantics into records.** The operator's decisions D1–D14 are REA-style decisions, recorded outside council records with scope, conditions and expiration. |
| 12 | Provenance | Must not be "treated as a trust anchor without evidence" (`docs/research/triagecore_research_question.md:18`). | Artifact provenance "MUST NOT determine whether a statement is an observation, claim, or interpretation" (§5.1). Role comes only from an explicit discriminator (§4). | **Align.** The canonical trust-vocabulary definition applies, plus REA's rule that role is never inferred from source, file name or container. |
| 13 | Source verification | Compressed summaries "do not replace source verification" (`docs/change/requests/CR-005-local-preflight-context-compression.md:19`). | `unverified`, `source_linked`, `source_mismatch`, `not_verifiable` or `unknown`. `source_linked` means the source supports the bounded record, "not ... that the source is correct about the world" (§5.4). | **Align.** Quotations use `source_linked`, `source_mismatch` or `unverified`. A transformation's self-reported fidelity is not verification. |
| 14 | Reproduction | Reproducibility standard (`triagecore_research_question.md:108`). A second reader derives expectations "without using a future reconciler's output as the oracle" (`monitoring-coverage-contract-v0.1.md:731`). | Requires a qualifying independent activity with recorded environment, inputs, method and output. "Repeating a report's text is not reproduction." `failed_to_reproduce` is never used for absence (§5.5). Quoted historical results remain `not_attempted` (§13). | **Align.** Answer keys carry `reproduction_state: not_attempted` until a second reader re-derives them. Replicate runs are repeated trials with the same method, not independent reproduction. Validator runs at a recorded commit reproduce the semantic checks. |
| 15 | Conflict and current use (contradiction) | Integrity failures "are ... not competing opinions" (`monitoring-coverage-contract-v0.1.md:237`). "Do not choose a favorable branch" (`:408`). | Conflict-state and current-use status are separate from verification and can be derived from discrepancy, adjudication and supersession records. "Contradicted != Deleted"; "Superseded != Erased" (§4, §5.6). | **Align.** An integrity conflict is not an opinion. Superseded revisions remain addressable in history: r0 is at `ea9ecbd`. |
| 16 | Corroboration | Basis versus corroborating evidence (`docs/operations/privacy-declaration-evidence-join-2026-08-29.md:45`). "Agreement between two producers is insufficient" (`monitoring-coverage-contract-v0.1.md:711`). | "SourceGrounding != IndependentReplication" (§4). Suspected semantic duplicates are preserved and linked, never silently merged (§7.3). | **Align.** Agreement is attention, never corroboration. Scorers' clustering of equivalent findings (M10) is a recorded judgment, not automatic detection. |
| 17 | Confidence | Not defined as a record field. | `high`, `medium`, `low` or `unknown`, with a rationale. `verified_fact` is forbidden, and self-reported model confidence promotes nothing (§6). | **Align.** Critic numbers are `reported_confidence_pct`, a measured variable for calibration (M6). Any confidence classification the council makes later uses REA's vocabulary. |
| 18 | Absence | MCI writes absent facts as `null` (`monitoring-coverage-contract-v0.1.md:99`, `:311`). TC's operational schema uses `null` for "no validator" (`docs/evidence_schema.md:54`). | No universal null. Distinct tags are allowed "only by field contract", and optional absence is omission (§9.2, DD-RE-006). | **Align with REA; corrects r0.** Council schemas contain no `null`. Each field names the tags it allows (`not_applicable`, `unknown`), or the field is omitted. |
| 19 | Derived analysis | Scoring and score interpretation happen outside TC (`eval_taxonomy.md:109`). | Regenerable from declared inputs, and never canonical evidence (§12). The rebuild criterion is §11.1. | **Align.** Mechanical synthesis, measures M1–M12 and validator reports are derived and regenerable. Validation is committed (`validation/`) so the checks can be rebuilt. |
| 20 | "Council" | `worker_council` is an execution runner (`triage_core/orchestration.py:82`; `triage_core/task_ledger.py:21`), and `council` is a `runner` value (`docs/evidence_schema.md:24`). | Not used. | **Keep distinct (SC-6).** Identifiers use the `pc-` prefix. |

## 4. The six invariants

| Invariant | TC repository precedent | REA v0.1 counterpart | Council rule, and where it is checked |
|---|---|---|---|
| Evidence is not authority | No verdict "is action permission" (`monitoring-coverage-contract-v0.1.md:223`). Governance functions are separated (`docs/architecture/triagecore_identity.md:75`). ACE: "The world can provide evidence. It cannot grant authority." (`docs/trust_boundary_eval_family.md:9`) | "ResearchLedgerRecordsAuthorityEvidence != ResearchLedgerCreatesAuthority" (§1). "LedgerRecorded != Authorized" (§4). No record creates authorization by existing (§20, criterion 12). | No structured field expresses a decision or approval, and `non_claims.authority` is constant. **Free text is not constrained**: overreach in prose is scored by people (M7). Schema check: V0. |
| Interpretation is not observation | Source-confirmed and runtime-observed kept apart (`local-heavy-diagnostic-2026-08-07.md:215`). | An interpretation is never stored as an observation (§7.10; counterexample 3). | Findings are interpretations. Quotations are claims checked against the packet. V5, V6. |
| Repetition is not independent corroboration | `monitoring-coverage-contract-v0.1.md:202`, `:711` | "Repeating a report's text is not reproduction" (§5.5). "SourceGrounding != IndependentReplication" (§4). | Declared lineage is projected to roots. Agreement is constant non-corroboration, and confidence is not aggregated. V0, V9, V10. M10 measures correlated error. |
| Missing evidence is not negative evidence | `privacy-declaration-evidence-join-2026-08-29.md:145`; an ambiguous timeout is "not proven nonexecution" (`monitoring-coverage-contract-v0.1.md:36`). | "Missing != Unknown != Redacted != NotApplicable"; "FailedReplication != AbsenceOfReplication"; "AbsenceOfEvaluation != EvaluationOutcome" (§4). | The support scale separates "not supported" from "undermined". No null. Feasibility creates no evaluation of H1–H4. Schema check, and the PC-F03/PC-F06 pair. |
| Disagreement is not erased by synthesis | Retain both verdicts and flag the disagreement (`monitoring-coverage-contract-v0.1.md:235-236`). | "Contradicted != Deleted"; "Superseded != Erased" (§4). Competing records remain accessible after adjudication (§7.11), which may not delete (§7.12). | Positions partition assessments, disagreements stay open, and adjudication preserves both codings. V7, V8. |
| A transformation cannot silently raise standing | `CR-005-local-preflight-context-compression.md:19`; "not semantic equivalence of a summary" (`monitoring-coverage-contract-v0.1.md:180`). | A converted copy is a new artifact (§7.1). Normalization changes the commitment (§8.3). Quoted results stay `not_attempted` (§13). | Transformations carry ceiling sources and their fidelity check. V11; FX11, FX18; PC-F05. |

## 5. Not imported: action-governance semantics

Unchanged from r0. The council does not take:

- **Control-plane decision vocabularies.** TC's `allow`, `deny` and
  `require_human_approval` (`eval_taxonomy.md:41-43`), and ACE's `allow`, `block` and
  `observe`.
- **The `authorized-next-action` category** (`evidence_bound_review_protocol.md:36`).
- **TC's runtime authority machinery:**
  - capability claiming;
  - human authorization receipts;
  - admission evidence;
  - route decisions;
  - mediated execution;
  - MCI exemptions;
  - signed ledger events.
- **The `worker_council` runner.**
- **CR lifecycle grants.**

REA Baseline v0.1 excludes the same territory for itself: authorization enforcement,
capability issuance or claiming, executor invocation and self-authorization (§21). The
council inherits that exclusion. It also does not adopt REA's checkpoint-signing or
tamper-evidence machinery, and it makes no tamper-proofing claim (§18).

## 6. Divergences from ACE, and what is adopted

These are as in r0. One wording change: "adjudicators" become "scorers", following
finding 2.

**Diverges.**

1. **Oracle location.** ACE keeps the oracle in the scenario file
   (`schemas/scenario_fixture.schema.json:5`). Council answer keys are scorer-only and
   physically separate.
2. **Who assigns codes.** ACE expects producers to export stable reason codes
   (`docs/reason_taxonomy.md:5`). Council critics write free text, and scorers assign
   codes.
3. **Trust model.** ACE trusts producer self-report (`README.md:13`). The validator checks
   critics' quotations.
4. **Decisions.** ACE scores decisions; the council has none.

**Adopted.**

- An independent oracle (`docs/reuse_manifest.md:10`).
- Allow-side controls (`README.md:28`).
- Self-tests are not evidence (`README.md:53`).
- Evaluating the evaluator (`docs/adversarial_actuals.md:5`). This is now a committed
  practice: every validator rule has a negative control (`validation/`).
- Oracle-alignment findings (`docs/oracle_alignment_findings.md:20-22`). These are now
  expressed as REA discrepancies.
- Stable codes kept apart from diagnostic detail (`reason_taxonomy.md:5`).

## 7. Semantic contract

These are proposed normative statements for council artifacts. "Must" states proposed
conformance for council work. It asserts nothing about TC, REA or ACE.

- **SC-1, vocabulary precedence** (revised in r1). Meanings come from these sources, in
  this order:
  1. the canonical [trust vocabulary](../../trust-vocabulary.md), for shared terms;
  2. REA v0.1 Stage B, for epistemic roles and statuses, where it defines a term;
  3. the TC repository's meaning, or a stated narrowing of it, where REA is silent;
  4. a council-local definition, only where none of these defines the term.

  This gives semantic alignment with REA, not conformance. Any REA revision triggers a
  re-reconciliation.
- **SC-2, no action governance.** Unchanged. This includes the `authorized-next-action`
  category.
- **SC-3, evaluation is not authority.** No council output confers authority. Every record
  carries `non_claims.authority: none`. That constant constrains the record's metadata, not
  its prose (SC-13).
- **SC-4, external-artifact boundary.** Unchanged. TC could ingest a council record only
  through a separately approved TC change request, as a static file across its evaluation
  handoff boundary (`docs/evals/evaluation_handoff_contract.md:75`).
- **SC-5, independent oracle.** Answer keys are derived from case packets alone. They
  become an oracle only when a human second reader reproduces their derivation and
  `reproduction_state` becomes `reproduced`.
- **SC-6, naming.** Unchanged: the `pc-` prefix, and never a bare `council` identifier.
- **SC-7, no TC primitives.** Unchanged. The council's epistemic terms stay outside TC.
  Aligning with REA does not change that: REA is a research substrate, not a TC primitive,
  and it carries no implementation authority.
- **SC-8, reproduction** (revised in r1). Restating or transforming a claim adds no
  standing. Reproduction requires a qualifying independent activity, with its environment,
  inputs, method and output recorded (REA §5.5). A failed reproduction is never inferred
  from absence.
- **SC-9, integrity is not opinion.** Unchanged.
- **SC-10, status discipline.** Unchanged. Revisions before any published checkpoint follow
  REA's draft-regeneration rule (DD-RE-005): r0 is superseded, not erased.
- **SC-11, read-only toward TC and ACE.** Unchanged.
- **SC-12, explicit absence** (new). Council formats use no universal null. A field names
  the absence tags its contract allows, or is omitted when optional. Missing, unknown,
  redacted and not-applicable stay distinct.
- **SC-13, guarantees match mechanisms** (new). Every claimed guarantee names its
  mechanism: schema, validator rule, or human scoring. Nothing mechanical checks the
  content of free text. A statement that the format "prevents" something applies only to
  what that mechanism actually checks.

## 8. Layering

| Layer | REA v0.1 (§3) | Council | Not a substitute for |
|---|---|---|---|
| Raw evidence | Immutable artifact bytes | Case packets and verbatim critic outputs, hashed | — |
| Records | A research ledger that is logically append-only | `pc-eer` records, scoring records, discrepancy and adjudication records | Truth |
| Derived analysis | Regenerable, not canonical | Mechanical synthesis, measures, validator reports | Evidence |
| Critics | — | Bounded analysis and provisional assessments | Human or institutional decision authority |
| Human scoring and adjudication | Adjudication of discrepancies (§7.12) | Scoring against answer keys, and adjudication of recorded discrepancies | Settling contested questions |
| TC action governance | Excluded from Baseline v0.1 (§21) | Not imported | — |

## 9. Open questions

1. **Carrier alignment.** Once REA selects a carrier encoding, should council records also
   be exportable as REA `EpistemicRecord` envelopes, for example one interpretation record
   per finding? Not before REA's design freeze (REA §24).
2. **Adjudication scope.** REA leaves open whether an adjudication may designate a
   preferred claim globally or only for a named analysis (§23.2, item 1). The council uses
   *named-analysis scope only*: an adjudication says which coding a named measure uses,
   and why.
3. **The record's name (D13).** Keep "epistemic evaluation record" from the handoff, or
   rename it to avoid the REA homonym, for example "epistemic critique record"?
4. **Confidence of scorers and adjudicators.** If these are recorded, should REA's ordinal
   vocabulary, with a rationale, be required?
5. **REA's own TC pin** (`codex/agents-governance-separation@8cff76d`) was not inspected.
   REA's claims about that checkout stay REA's, unverified here.
6. **Carried from r0.**
   - The mapping to TC's review-protocol categories.
   - Candidate trust-vocabulary terms.
   - Whether ACE should host council fixtures (recommended: no).
   - TC branch coverage: only two of 142 branches were inspected.

## 10. No-change verification

On 2026-10-28, `git status --short` printed nothing in the TC, ACE and
`triagecore-signed-intent` clones, and their HEADs were unchanged from section 1. r1
performed no operation against those repositories beyond reads. No branch, commit, push,
issue or comment was made in any of them. The REA file is not stored in this repository.

## Appendix A. Pinned hashes (SHA-256)

**REA v0.1 Stage B (operator file).** As received, SHA-256
`a0ece23a770d603e4220bc0847cdf02fdbb96e640022d46d8794ac4391f733e3`.

**TriageCore at `4e9f238`.** All entries from r0 still apply, unchanged. Added in r1:

| File | SHA-256 |
|---|---|
| `docs/evidence_schema.md` | `07287090645eff4ada25896a503fe4d651d87839f00a1228288b7898ad99cc62` |

Carried from r0:

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
| `docs/operations/local-heavy-diagnostic-2026-08-07.md` | `faa73f54d4eddbfa982a8292a5b372832482b0a176972b7b279edb352a5b1de2` |
| `docs/operations/privacy-declaration-evidence-join-2026-08-29.md` | `3d7552f4ba936d126d7d883622fefe21067fbb2dc80e93990858b94cf485aeba` |
| `docs/operations/privacy-propagation-2026-08-29.md` | `f368df4495cadee3b1de5d1d3ac47adf1c6d50596f471b8adc1c040ffaafca03` |
| `docs/operations/classifier-terminal-fallback-2026-08-29.md` | `7ef412afc5c39020c5e3d5bf49207bffb1be6a6c53ac3f4ba80fa0f4c1d5490f` |
| `docs/operations/control-plane-invariant-checklist.md` | `dc51be9e257e45c47da79f3e6ebebd9d1f3e579bdc0b4598fdd8f816fb171815` |
| `docs/security/runtime_integrity_model_provenance_policy.md` | `0d310931915ac1517c82a73d8608b298333fd90ee89b4fd99848ae18eb1b48e8` |
| `docs/current_backlog.md` | `73f8dd26c6b609f881f9b2dd60dc474b2baa07d8efdc8a81bf2343c667ae413c` |
| `triage_core/capability_claims.py` | `5667e30c1718048cb11c49500c92070f89e305ade92703d989b08b7b1846603f` |
| `triage_core/task_ledger.py` | `ab9be73a38e3e7f2cb4b1dec1a0436f5338380239ac19e2bd105126affa39f61` |
| `triage_core/orchestration.py` | `ab23cf09378ea450a7c574c370ce94bea4eece0f375e839faa02f1502498e875` |

r0's appendix also pins `docs/verification_guide.md`, `docs/change/requests/CR-134-…`,
`docs/operations/monitoring-coverage-baseline-2026-10-22.md`, `triage_core/compression.py`
and `triage_core/context_budget.py`. Those hashes are unchanged, and remain in r0 at
`ea9ecbd`.

**agent-control-evals at `b876a28`.** Unchanged from r0. See r0's appendix at `ea9ecbd`,
or recompute with `sha256sum` at that commit.
