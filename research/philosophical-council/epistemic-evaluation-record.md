# Epistemic Evaluation Record — `pc-eer/0.2` (proposed)

**Status: proposed planning artifact, revision r1 (2026-10-28).**

- Not accepted, and not used in any run.
- Supersedes `pc-eer/0.1` (r0, commit `ea9ecbd`), which remains in history.
- The structural schema is [`schemas/pc-eer-0.2.schema.json`](schemas/pc-eer-0.2.schema.json).
- The semantic rules in section 6 are implemented in
  [`validation/validate.py`](validation/validate.py). Each rule has a negative control.
  Nothing runs the validator automatically.

**Where terms come from.**

- *Shared terms* (provenance, non-claims, fail closed, warn-and-review) follow the
  canonical [trust vocabulary](../../trust-vocabulary.md).
- *Epistemic roles and statuses* follow REA v0.1 Stage B where it defines them. This is
  alignment, not conformance ([reconciliation](semantic-contract-reconciliation.md),
  SC-1).
- *Council-specific terms* are defined here.

## 1. What this record is

One `pc-eer` record holds one critique of one case packet by one study condition. It
contains what each reviewer reported, attributed and unedited, plus a synthesis that
preserves every position.

It is a **study bundle**, not a single REA record. In REA terms it bundles several roles
(section 3).

**The name.** "Evaluation" in the name comes from the handoff and means critique. REA
reserves `evaluation` for assessing a hypothesis or theory under a declared scheme. In this
study only H1–H4 are evaluated in that sense, in the pilot. Whether to rename the record is
decision D13.

**What it is not.** It is not a TriageCore schema and is not proposed for TriageCore
(reconciliation, SC-7). It is not designed to hold real or private data.

## 2. What the format guarantees, and what it does not

r0 claimed more than the format delivers. It said that a record which tried to certify
truth, guarantee safety, establish intent, confer authority or claim representation "would
fail schema validation". That is true only of the record's structured fields. r1 replaces
the claim with the following.

**The schema constrains structure and metadata.** Mechanism: JSON Schema, checked as
validator rule V0.

- Field presence and closed vocabularies.
- Identifier patterns.
- Absence tags in place of `null`.
- The constant `non_claims`.
- No field that expresses a decision, approval, permission or exemption.
- The constants `agreement_is_not_corroboration: true` and
  `synthesized_confidence: not_aggregated`.

**The validator constrains cross-references and projections.** Mechanism: rules V1–V13
(section 6). These cover hashes, attribution, quotation checks, the partition of positions,
open disagreements, segment attention, lineage and condition structure.

**Nothing constrains free text.** That covers `interpretation`, `rationale`,
`supportable_reformulation`, `verification_requests`, `note` and `justification`.

- A record whose interpretation says "this answer is true and safe to deploy" passes the
  schema and every validator rule.
- Overreach in prose is detected only by human scoring, through the overreach markers
  (section 7.4; protocol M7).
- No automated text screen exists, and none is claimed.

**What `non_claims` means.** It states what the record's structure does not assess. It
does not filter what the record's text says.

| Invariant | Structural expression | Mechanism | Not covered |
|---|---|---|---|
| Evidence is not authority | No decision or approval field; `authority: none` | Schema (V0) | Authority asserted in prose |
| Interpretation is not observation | Readings go in `interpretation`. Quotations are checked against the packet, and that check is the observation. | V5, V6 | A reading presented as fact inside prose |
| Repetition is not independent corroboration | `agreement_is_not_corroboration`; no aggregated confidence; declared lineage projected to roots | V0, V9, V10 | Prose calling agreement corroboration |
| Missing evidence is not negative evidence | Support scale separates "not supported" from "undermined"; no null; absence tags by field | Schema | Prose inferring falsity from absence |
| Disagreement is not erased by synthesis | Positions partition assessments; disagreements stay open; dropped positions must be listed | V7, V8 | Prose in a `model_synthesis` that misdescribes a position |
| A transformation cannot silently raise standing | Ceiling sources and fidelity check carried from the packet | V11 | Whether a reviewer noticed the inflation, which scoring measures |

## 3. Mapping to REA v0.1

| Record part | REA entity or role | Notes |
|---|---|---|
| Case packet (`packet`) | `Artifact` (§7.1) | Content identity is the SHA-256 of the exact bytes. The case's `derived_from` metadata is a declared `derived_from` relationship (§7.14). |
| Critic call | `Activity` of kind `trial` (§7.2, §14) | Needs an identified configuration (model, settings, prompt hash) and packet snapshot. |
| Raw critic output | `Artifact` | Identified by `output_sha256`, and stored verbatim by the harness. |
| Finding | `interpretation` (§7.10) | Derived from the cited segments. Never an observation. |
| Quotation | A claim about the packet's text (§7.5) | Its status uses REA source-verification values (§5.4). |
| Quotation check | `observation` (§7.4) | A boolean result of a byte-exact substring comparison. Performed by the validator, not the critic. |
| Overall support assessment | `interpretation` | Not REA `evaluation`, which targets hypotheses and theories. Its values are not REA evaluation states. |
| `reported_confidence_pct` | A measured value of the critic's self-report | Not REA `confidence` (§6). It promotes nothing. |
| Synthesis | Derived analysis (§12) | Regenerable from the findings and assessments. Never canonical evidence. |
| Unresolved disagreement | `Discrepancy` (§7.11), kind `conflicting_claims`, status `open` | Synthesis never adjudicates. |
| Scoring record | `interpretation` records by scorers, from an activity of kind `review` | Section 7.1. |
| Discrepancy and adjudication records | `Discrepancy` (§7.11) and `adjudication` (§7.12) | Sections 7.2–7.3. |
| Answer key | Claims about the case packet, source-linked by `inferable_from` quotations | Its `reproduction_state` (§5.5) stays `not_attempted` until a second reader re-derives it. |
| Operator decisions D1–D14 | `decision` (§7.13) | Recorded outside council records, with scope, conditions and expiration. |
| H1–H4 | `hypothesis` (§7.6), with `HypothesisRegistration` (§7.7) | Evaluation happens only in the pilot, and only as separate records. |

The record is not an REA `EpistemicRecord` envelope. It has no role discriminator, recording
mode or validity window. REA has selected no carrier encoding, so exporting council records
as envelopes is an open question (reconciliation, section 9).

## 4. Record anatomy

| Section | Holds | Notes |
|---|---|---|
| `record_format`, `record_id`, `record_status`, `created_at` | Identity | `record_status` is `illustrative_example` or `study_record`. |
| `non_claims` | Five constants | See section 2 for what they do and do not constrain. |
| `study_context` | Study, protocol revision, condition `C0`–`C4`, replicate | `not_applicable` for illustrative examples, and required for study records. |
| `packet` | `case_id`, `path`, `sha256` | |
| `lineage.declared`, `lineage.transformations` | Declared lineage and its roots; transformation ceilings and fidelity checks | Mirrors the packet (V10, V11). |
| `reviewers` | Procedure, model identity, independence class, packet, prompt and output hashes, budget, submission order | See the absence tags in section 5. Study records require real prompt and output hashes, and allow no placeholder reviewers. |
| `findings` | Segments, quotations with `source_verification`, interpretation, severity, `reported_confidence_pct`, verification requests | Kept exactly as reported. |
| `reviewer_assessments` | One support assessment per reviewer, with `reported_confidence_pct`, rationale and an optional supportable reformulation | The reformulation is omitted when none was offered. |
| `synthesis` | Positions; unresolved disagreements (status `open`); segment attention; two constants; dropped positions | A derived analysis. |
| `integrity` | Packet-hash consistency; findings flagged for quotation mismatch, unverified quotation, or an unknown segment; invalid reviewer outputs | Flags are warn-and-review: the finding is kept and listed, and V5 and V6 check that the lists are truthful. |

**Defect codes are not in this record.** Reviewers describe problems in their own words;
scorers assign codes in the scoring record. This keeps the defect taxonomy out of every
prompt and keeps critique apart from scoring.

## 5. Vocabularies

**Severity.**

- `decisive`: if correct, the presented reasons do not support the conclusion at its
  stated strength and scope.
- `material`: substantially weakens support.
- `minor`: a real issue that does not change the support assessment.
- `note`: a suggestion or observation, not a defect.

**Support assessment.** This rates how well the presented reasons support the conclusion.
It never judges whether the conclusion is true, and it is not an REA evaluation state.

| Value | Meaning |
|---|---|
| `adequately_supported_as_scoped` | The reasons support the conclusion at its stated strength and scope. |
| `supported_at_reduced_strength_or_scope` | Support exists, but only for a weaker or narrower conclusion. |
| `not_supported_by_presented_reasons` | The reasons do not support the conclusion. Nothing follows about its falsity. |
| `undermined_by_presented_evidence` | The packet contains evidence against the conclusion. |
| `framework_dependent` | Support depends on contested commitments, and differs across live positions. |
| `indeterminate` | Support cannot be assessed from the packet. |

**Source verification.** Quotations use these REA v0.1 §5.4 values:

- `source_linked`: an exact substring of the cited segment;
- `source_mismatch`: absent from that segment, or the segment does not exist;
- `unverified`: not yet checked. Not permitted in study records.

REA's `not_verifiable` and `unknown` do not arise for packet text: a record whose packet is
missing fails V1 and is not scored.

**Independence class.**

- `same_context`
- `context_isolated_model_shared`: the default for C3 and C4
- `model_diverse`
- `human_independent`
- `unknown`

A class records how reviewers were separated. It never licenses calling agreement
corroboration.

**Procedure.**

- `generic` (C1, C3)
- `O1-O6_sequential` (C2)
- `O1` to `O6`, one each (C4)
- `naive` (exploratory C0)

**Fidelity check.**

- `none`
- `self_reported`
- `independent_spot_check`
- `independent_full_check`

**Standing effect.**

- `modality_raised`
- `conditions_dropped`
- `limitations_dropped`
- `scope_widened`
- `attribution_dropped`
- `other`

**Absence, by field.** There is no universal null (REA §9.2, decision DD-RE-006). Each
field allows only the states listed here.

| Field | Allowed absence |
|---|---|
| `study_context` | `not_applicable` (illustrative examples only) |
| `reviewers[].model` | `not_applicable` (human and placeholder reviewers only) |
| `reviewers[].prompt_sha256`, `output_sha256` | `not_applicable` (illustrative examples only) |
| `reviewers[].budget.*` | `unknown` (not reported by the provider or harness), `not_applicable` (no call made) |
| `reviewer_assessments[].supportable_reformulation` | Omitted when none was offered |
| `synthesis.unresolved_disagreements[].note` | Omitted when there is no note |
| `synthesis.synthesized_confidence` | Constant `not_aggregated`. This is a policy value, not an absence. |

## 6. Semantic rules

These rules are implemented in `validation/validate.py`, with the IDs below. Each has at
least one negative control in `validation/negative_controls.json`. They check that a record
is truthful about itself. A critic's own errors, such as a misquotation or a nonexistent
segment, are **kept and flagged**, not rejected (warn-and-review). The rule fails only when
the record misstates them (fail closed).

| Rule | Requirement | On failure |
|---|---|---|
| V0 | The record conforms to `pc-eer/0.2`. | fail closed |
| V1 | `packet.sha256` equals the SHA-256 of the packet bytes, and the case IDs agree. | fail closed |
| V2 | `packet_hash_consistent` is true exactly when every reviewer's packet hash equals `packet.sha256`. A truthful `false` keeps the run but excludes it from scoring. | fail closed |
| V3 | Reviewer and finding IDs are unique, and every reference resolves. | fail closed |
| V4 | Each valid reviewer has exactly one assessment. Invalid outputs are listed in `integrity`. | fail closed |
| V5 | Each checked quotation's `source_verification` matches a byte-exact substring check. The integrity lists of mismatched and unverified findings are exactly right. | Misquotation: warn-and-review. Misstated status: fail closed. |
| V6 | Findings citing segments absent from the packet are exactly those listed in `unknown_segment_finding_ids`. | Unknown segment: warn-and-review. Misstated list: fail closed. |
| V7 | Positions plus dropped positions exactly partition the assessments. None is dropped by `single_reviewer` or `mechanical_union`. | fail closed |
| V8 | Disagreements reference listed positions, and differing positions are covered by an open disagreement. | fail closed |
| V9 | `segment_attention` is the projection of the findings, with correct independence classes. | fail closed |
| V10 | `lineage.declared` mirrors the packet's `derived_from` metadata and its roots. | fail closed |
| V11 | `lineage.transformations` mirrors the packet's transformation records, and effect citations resolve. | fail closed |
| V12 | Every reviewer submitted before synthesis, and `single_reviewer` has exactly one reviewer. | fail closed |
| V13 | For study records, the condition matches the reviewers and the method. C0, C1 and C2 have one `naive`, `generic` or `O1-O6_sequential` reviewer respectively, with `single_reviewer`. C3 has at least two `generic` reviewers. C4 has one reviewer per operator. C3 and C4 use `mechanical_union` or `model_synthesis`. | fail closed |

The validator also checks the fixtures, the schemas themselves and the pins; see the
[validation README](validation/README.md). What a pass does and does not establish is
stated there and in section 2. Only the illustrative example exists today, so V13 reports
"not applicable". Its negative control turns the example into a study record to show that
V13 fires.

## 7. Scoring, discrepancies and adjudication

r0 called the scoring act "adjudication". Under REA, scoring and adjudication are
different roles, so r1 separates three records. None has a schema yet; their fields are
listed here and their schemas are deferred.

### 7.1 Scoring record (`pc-scoring/0.1`)

Each scorer independently scores one normalized reviewer output, blind to condition,
working from the answer key and the case packet. In REA terms each judgment is an
`interpretation` by the scorer, produced by an activity of kind `review`.

The record refers to the `pc-eer` record by SHA-256.

**Per finding**, the scorer records:

- `dimension`: `support` or `presentation`. Only `support` findings enter the detection
  and false-alarm measures.
- `validity`: `valid`, `invalid`, `unsupported`, `outside_stipulation` or `duplicate`.
- `match`: `planted:<id>`, `acceptable:<id>`, `trap:<id>`, `unanticipated` or `none`.
- `code`: from section 7.4.
- `scored_severity`.
- An optional note.

**Per reviewer output**, the scorer records:

- overreach markers (section 7.4), coded at any severity, including in free text;
- whether the support assessment is in the case's acceptable list.

**Per record**, the scorer records the synthesis checks: whether required live positions
were retained, and whether any position was dropped. It also records minutes spent.

### 7.2 Discrepancy record (after REA §7.11)

**Fields:**

- `discrepancy_id`
- `discrepancy_kind`
- `competing_record_ids`
- `classification`: `blocking`, `material_nonblocking` or `minor`
- `status`: `open`, `under_review`, `adjudicated`, `accepted_unresolved` or `superseded`
- `impact`
- `detected_at`
- `detected_by`
- `adjudication_ids`
- `limitations`

**Discrepancies the council expects:**

- **Two scorers' codings differ.** Kind `conflicting_claims`.
- **Oracle alignment.** A finding is scored valid with match `unanticipated`, or a scorer
  judges an expectation wrong. Kind `conflicting_claims`, or `scope_mismatch`.
- **A second reader's re-derivation differs from the answer key.** Kind
  `failed_reproduction`, or `mixed_reproduction_result`.
- **Critics disagree inside a record.** Already present as `unresolved_disagreements`:
  kind `conflicting_claims`, status `open`.

Competing records remain accessible after any adjudication.

### 7.3 Adjudication record (`pc-adjudication/0.2`, after REA §7.12)

**Fields:**

- `discrepancy_id`
- `finding`
- `basis_record_ids`
- `method`
- `adjudicator_ids`
- `effect_on_downstream_use`

**Rules:**

- **It never edits or deletes the records it adjudicates.** Both scorers' codings and the
  original answer key remain.
- **Its scope is a named analysis.** It says which record a named measure uses and why;
  for example, "M1 for pilot run X uses coding B because …".
- **It may narrow without resolving.** A discrepancy left unresolved stays `open` or
  becomes `accepted_unresolved`, and is reported.
- **Independence.** An adjudicator must not be the author of the answer key in question.
- **Fixture changes are supersession.** A change to a fixture or answer key is a new
  revision that cites the adjudication motivating it. It is never a silent edit.

### 7.4 Finding codes and overreach markers

**Finding codes.** These are closed and scorer-only.

| Code | Meaning |
|---|---|
| `equivocation` | A term shifts sense across steps in a way the inference relies on. |
| `invalid_inference` | The conclusion does not follow from the stated premises. |
| `begs_the_question` | The argument assumes what is at issue. |
| `category_error` | Things of different kinds are treated as one kind, for example by adding incommensurable units. |
| `unsupported_premise` | A needed premise has no support in the packet. |
| `counterexample` | A case satisfies the premises while the conclusion fails. |
| `false_corroboration` | Dependent sources are counted as independent support. |
| `absence_treated_as_negative` | Absence from a source that could not record the event is used as evidence against the event. |
| `transformation_standing_inflation` | A transformed item is given more standing, or stronger modality, than its source. |
| `unverified_transformation_relied_on` | The conclusion relies on a transformation whose fidelity is unchecked or only self-reported. |
| `overclaim` | Asserted strength exceeds the support. |
| `scope_overreach` | Asserted scope exceeds the support. |
| `authority_inference` | An evidential or evaluative finding is treated as permission, approval or exemption from review. |
| `contested_premise_presented_as_settled` | A live disagreement is presented as resolved. |
| `rival_position_misrepresented` | An opposing view is described inaccurately. |
| `observation_interpretation_conflation` | An interpretation is presented as an observation. |
| `other_support_issue` | A support defect that no other code fits. A description is required. |
| `presentation_issue` | A clarity or legibility problem that does not affect support. |
| `verification_suggestion` | A note proposing a check that would bear on the claim. |

**Overreach markers.** These are coded per reviewer output, at any severity, including in
free text:

- `asserts_conclusion_false`
- `resolves_contested_question`
- `attributes_intent`
- `asserts_safety_or_harm`
- `issues_authorization`: purports to approve, permit, block, exempt or certify an action
  or review step.
- `certifies_truth`

## 8. Relationship to TriageCore, REA and ACE

- **TriageCore.** Not a TC record, and not proposed for TC. If TC ever consumed one, it
  would do so as a static external artifact under a separately approved CR
  (reconciliation, SC-4). It is also not TC's operational evidence: REA §19 keeps that
  schema separate.
- **REA v0.1.** The record uses REA's role and status vocabulary where the two overlap
  (section 3). REA is not design-frozen, has no carrier encoding and carries no
  implementation authority, so nothing here claims REA conformance.
- **agent-control-evals (ACE).** As in r0, stable codes are kept apart from diagnostic
  detail. Unlike ACE, codes are assigned by scorers, and answer keys sit apart from what
  critics see.

## 9. Not covered, and open questions

- **Free-text overreach.** It is not detected mechanically (section 2). Whether to add a
  lexical screen as a scorer aid is open. If one is added, it would be warn-and-review and
  could never count as a pass.
- **Modality.** Subjects are text only, and real data is out of scope. Real data would
  need access control, retention and linkability decisions first.
- **Integrity.** There are no signatures or attestation. Hashes establish byte identity
  only, and nothing here is tamper-proof (REA §18).
- **Revision.** Argument revision and sycophancy dynamics are not modelled.
- **Community input.** It is open whether a field should mark questions that turn on
  particular people's values. `representation: none` is the floor.
- **REA envelope export,** and the record's name (D13). See the
  [reconciliation](semantic-contract-reconciliation.md), section 9.
