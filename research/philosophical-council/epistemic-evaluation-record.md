# Epistemic Evaluation Record — `pc-eer/0.1` (proposed)

**Status: proposed planning artifact, revision r0 (2026-10-27).** Not accepted, not
implemented, and not used in any run. No validator exists in this repository. The
structural schema is [`schemas/pc-eer-0.1.schema.json`](schemas/pc-eer-0.1.schema.json).
The rules in section 6 were exercised once against the
[illustrative example](examples/pc-eer-illustrative.json) by a scratch script during
drafting. That script is not part of the repository, so it is evidence about the example,
not an enforcement mechanism.

Shared terms such as *provenance*, *non-claims*, *fail closed* and *warn-and-review* have
the meanings in the canonical [trust vocabulary](../../trust-vocabulary.md). This document
defines only council-specific terms.

## 1. What this record is

One `pc-eer` record holds one evaluation of one case packet by one study condition. It is
the artifact a council run would produce: what each reviewer reported, attributed and
unedited, plus a synthesis that preserves every position.

It is a **study instrument**, not a TriageCore schema, and it is not proposed for import
into TriageCore (see the [reconciliation](semantic-contract-reconciliation.md), SC-7). It
is not designed to hold real or private data.

**Deference.** The operator's research summary names a *Research Evidence Architecture &
Schema Contract v0.1* (Stage B) that separates artifacts, observations, claims,
hypotheses, evaluations, interpretations, adjudications and decisions. That contract was
not available to this session. Where it defines a term this record also uses, its
definition should take precedence for TC-compatible semantics, and this record should keep
only study-specific fields. Reconcile the two before accepting either.

## 2. The six invariants, made structural

Each handoff invariant is enforced by shape where possible, not only by instruction.

| Invariant | Structural rule in `pc-eer/0.1` | Rule |
|---|---|---|
| Evidence is not authority | No field can express a decision, approval, permission or exemption. `non_claims.authority` is the constant `none`. | schema |
| Interpretation is not observation | An observation is an exact quotation tied to a segment ID, so it can be checked mechanically. A reviewer's reading goes only in `interpretation`. | V5, V6 |
| Repetition is not independent corroboration | `synthesis.agreement_is_not_corroboration` is the constant `true`. `segment_attention` counts reviewers together with their independence class. Confidence is never aggregated (`synthesized_confidence` is `null`). Declared lineage is projected to its roots. | V9, V10 |
| Missing evidence is not negative evidence | The support scale separates `not_supported_by_presented_reasons`, which implies nothing about falsity, from `undermined_by_presented_evidence`. An empty list of reported effects means *none reported*, not *none occurred*. | schema |
| Disagreement is not erased by synthesis | Positions must exactly partition reviewer assessments. Anything omitted must be listed in `dropped_positions` with a justification, and that list must be empty for mechanical synthesis. Differing positions require a recorded unresolved disagreement. | V7, V8 |
| A transformation cannot silently raise standing | Each transformation carries `standing_ceiling_source_ids` and the packet's `fidelity_check`, and reported standing effects are tied to findings. | V11 |

The handoff's non-claims are also carried in the data. Every record states `truth:
not_assessed`, `safety: not_assessed`, `intent: not_assessed`, `authority: none` and
`representation: none`. A record that tried to certify truth, guarantee safety, establish
intent, confer authority or claim to represent a person or community would fail schema
validation.

## 3. Record anatomy

| Section | Holds | Notes |
|---|---|---|
| `record_format`, `record_id`, `record_status`, `created_at` | Identity | `record_status` is `illustrative_example` or `study_record`. |
| `non_claims` | Five constants | See section 2. |
| `study_context` | Study ID, protocol revision, condition `C0`–`C4`, replicate | `null` for examples. |
| `packet` | `case_id`, `path`, `sha256` of the exact packet bytes | The subject is segment family `A` inside the packet. |
| `lineage.declared` | Each evidence item's declared `derived_from` and its declared roots | A projection of the packet's metadata. Declared lineage is a source assertion, not verified dependence. |
| `lineage.transformations` | Ceiling sources, fidelity check, reported standing effects | Mirrors the packet's transformation records. |
| `reviewers` | Procedure, model identity, independence class, packet, prompt and output hashes, budget, submission order | `model.exact_version` must be immutable. Mutable aliases go only in `alias_labels` (TC precedent, reconciliation row 1). |
| `findings` | Segments, exact quotations, interpretation, severity, confidence 0–100, verification requests | Kept exactly as reported: no deduplication and no rewording. |
| `reviewer_assessments` | One overall support assessment per reviewer, with rationale and an optional supportable reformulation | The reformulation is the strongest claim the reviewer thinks the reasons do support. |
| `synthesis` | Positions, unresolved disagreements, segment attention, the two constants, dropped positions | Section 5 below. |
| `integrity` | Packet-hash consistency, unverified quotes, invalid reviewer outputs | Invalid outputs are retained, never silently dropped. |

**Defect codes are not in this record.** Reviewers describe problems in their own words.
Codes such as `false_corroboration` are assigned later, by human adjudicators, in a
separate adjudication record (section 7). This keeps the defect taxonomy out of every
prompt, so no condition is primed by it, and keeps evaluation separate from adjudication.

## 4. Vocabularies

**Severity.**

- `decisive`: if correct, the presented reasons do not support the conclusion at its
  stated strength and scope.
- `material`: substantially weakens the support.
- `minor`: a real issue that does not change the support assessment.
- `note`: a suggestion or observation, not a defect.

**Support assessment.** This rates how well the presented reasons and evidence support the
conclusion. It is never a judgment of whether the conclusion is true.

| Value | Meaning |
|---|---|
| `adequately_supported_as_scoped` | The reasons support the conclusion at its stated strength and scope. |
| `supported_at_reduced_strength_or_scope` | Support exists, but only for a weaker or narrower conclusion than the one stated. |
| `not_supported_by_presented_reasons` | The reasons do not support the conclusion. Nothing follows about its falsity. |
| `undermined_by_presented_evidence` | The packet contains evidence against the conclusion. |
| `framework_dependent` | Support depends on contested commitments, and the assessment differs across live positions. |
| `indeterminate` | Support cannot be assessed from the packet. |

**Independence class.**

- `same_context`
- `context_isolated_model_shared`: the default for C3 and C4.
- `model_diverse`
- `human_independent`
- `unknown`

The class records *how* reviewers are separated. It never licenses calling agreement
corroboration in v0.1.

**Procedure.**

- `generic` (C1, C3)
- `O1-O6_sequential` (C2)
- `O1` to `O6`, one each (C4)
- `naive` (exploratory C0)

The operators are defined in the [study protocol](study-protocol.md), section 5.

**Fidelity check.**

- `none`
- `self_reported`: the producer of a transformation vouches for it.
- `independent_spot_check`
- `independent_full_check`

**Standing effect.**

- `modality_raised`, for example *preliminary* restated as *shown*
- `conditions_dropped`
- `limitations_dropped`
- `scope_widened`
- `attribution_dropped`
- `other`

## 5. From reviewer output to record

Every condition uses the same reviewer output format: findings with segment IDs, exact
quotations, a free-text problem description, severity and confidence, plus one overall
assessment (protocol section 6.3). The record is built from those outputs mechanically:

1. **Store outputs before synthesis.** Store and hash each output before synthesis starts
   (`submitted_before_synthesis`).
2. **Check quotations.** Each quotation is compared byte-for-byte with its segment.
   Mismatches are flagged, not removed.
3. **Copy findings and assessments.** They are copied unchanged, with attribution.
4. **Synthesize** (`mechanical_union`):
   - Group reviewers by overall assessment value, one position per value.
   - If more than one position exists, record one unresolved disagreement of type
     `unclassified`.
   - Project segment attention from the findings.
   - Aggregate no confidence.

A `model_synthesis` record, used only in the exploratory arm, must list every reviewer
position that it omits in `dropped_positions`. Each omission is then a measured event
rather than a silent one.

## 6. Semantic rules (proposed; not implemented)

JSON Schema cannot express these rules. Each is marked **fail closed** or
**warn-and-review**, as defined in the trust vocabulary:

- *Fail closed*: the record is retained but not scored.
- *Warn-and-review*: the item is retained, flagged and counted, and a human looks at it.

| Rule | Requirement | On failure |
|---|---|---|
| V1 | `packet.sha256` equals the SHA-256 of the packet bytes, and the `case_id` values agree. | fail closed |
| V2 | `integrity.packet_hash_consistent` is true exactly when every reviewer's `packet_sha256` equals `packet.sha256`. | fail closed |
| V3 | Reviewer and finding IDs are unique, and every reference resolves. | fail closed |
| V4 | Each valid reviewer has exactly one assessment. Invalid outputs appear in `integrity.invalid_reviewer_outputs`. | fail closed |
| V5 | `quote_verified` is true exactly when the quotation is a substring of the cited segment. Unverified findings are listed in `integrity`. | warn-and-review |
| V6 | Every cited segment exists in the packet. | warn-and-review |
| V7 | Positions plus dropped positions exactly partition the reviewer assessments. Dropped positions are empty for `single_reviewer` and `mechanical_union`. | fail closed |
| V8 | Disagreements reference listed positions, and differing positions are covered by an unresolved disagreement. | fail closed |
| V9 | `segment_attention` equals the projection of the findings, with correct independence classes. | fail closed |
| V10 | `lineage.declared` mirrors the packet's `derived_from` metadata and its computed roots. | fail closed |
| V11 | `lineage.transformations` mirrors the packet's transformation records. Effect citations resolve. | fail closed |
| V12 | Every reviewer submitted before synthesis, and `single_reviewer` has exactly one reviewer. | fail closed |
| V13 | For study records, the condition matches the reviewers. C0 has one `naive` reviewer. C1 has one `generic` reviewer. C2 has one `O1-O6_sequential` reviewer. C3 has k `generic` reviewers. C4 has one reviewer per operator. C3 and C4 use `mechanical_union`. | fail closed |

A scratch negative test during drafting injected two faults into a copy of the example: a
silently dropped position and an altered quotation. Rules V5, V7 and V8 detected them. No
other claim is made about these rules.

## 7. Adjudication record (`pc-adjudication/0.1`, described; schema deferred)

Adjudication is a separate record. It refers to the evaluation record by SHA-256, so
evaluation and adjudication never share a file, and each adjudicator's record is kept.

**Per finding**, the adjudicator records:

- `dimension`: `support` or `presentation`. Only `support` findings enter detection and
  false-alarm measures.
- `validity`: one of
  - `valid`
  - `invalid`: misreads the packet or is wrong.
  - `unsupported`: asserts something with no basis in the packet, such as outside facts
    presented as packet findings.
  - `outside_stipulation`
  - `duplicate`
  - `contested`
- `match`: one of `planted:<id>`, `acceptable:<id>`, `trap:<id>`, `unanticipated` or
  `none`.
- `code`: from the closed finding-code list below.
- `adjudicated_severity`.
- A short `note`.

**Per reviewer output**, the adjudicator records:

- Any overreach markers (below).
- Whether the overall assessment is in the case's acceptable list.

**Per record**, the adjudicator records:

- The synthesis checks: whether required live positions are retained, and whether any
  position was dropped.
- Minutes spent.

**Reconciliation.**

- Adjudicators code independently, blind to condition, and then reconcile.
- The reconciled record keeps both initial codings, the reconciled code and its rationale.
- Items still unresolved stay `contested` and are reported separately. They are never
  forced to agreement.

**Finding codes (closed, adjudicator-only).**

| Code | Meaning |
|---|---|
| `equivocation` | A term shifts sense across steps in a way the inference relies on. |
| `invalid_inference` | The conclusion does not follow from the stated premises. |
| `begs_the_question` | The argument assumes what is at issue. |
| `category_error` | Things of different kinds are treated as the same kind, for example by adding incommensurable units. |
| `unsupported_premise` | A needed premise has no support in the packet. |
| `counterexample` | A case satisfies the premises while the conclusion fails. |
| `false_corroboration` | Dependent sources are counted as independent support. |
| `absence_treated_as_negative` | Absence from a source that could not record the event is used as evidence against the event. |
| `transformation_standing_inflation` | A derived or transformed item is given more standing, or stronger modality, than its source. |
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

**Overreach markers.** These are coded per reviewer output, at any severity:

- `asserts_conclusion_false`: infers falsity from failed support.
- `resolves_contested_question`
- `attributes_intent`
- `asserts_safety_or_harm`
- `issues_authorization`: purports to approve, permit, block, exempt or certify an action
  or review step. Recommending that a human decide, or recommending a check, is not
  authorization.
- `certifies_truth`

## 8. Relationship to TriageCore and agent-control-evals

- **TriageCore.** This record is not a TC record and is not proposed for TC. If TC ever
  consumed one, it would do so only as a static external artifact, under a separately
  approved TC CR. Its evaluation handoff contract already treats evaluator findings as
  external artifacts (reconciliation, SC-4).
- **agent-control-evals (ACE).** ACE separates stable reason codes from diagnostic detail,
  and this record keeps that split. It diverges from ACE in two places, both because the
  reviewers here are models:
  - Codes are assigned by adjudicators, not by the system under evaluation.
  - Expectations live in a different file from what reviewers see.

## 9. Not covered, and open questions

- **Modality.** Subjects are text only. Multimodal segments and locators are deferred.
- **Data.** Only synthetic data is in scope. Real data would need decisions on access
  control, retention, deletion and digest linkability first, as TC's MCI contract
  section 8 notes for its own profile.
- **Integrity.** There are no signatures or attestation. Hashes establish byte identity
  only; they do not establish correctness, authenticity or provenance.
- **Revision.** Argument revision and sycophancy dynamics, where an author revises after
  critique, are not modelled. That would be a separate study design.
- **Community input.** It is open whether a field should mark questions that turn on the
  values of particular people, so that no simulated reviewer stands in for them.
  `representation: none` is the v0.1 floor.
- **Model-synthesis confidence.** How to record a synthesizer's own confidence claims for
  measurement without letting them enter the record is open.
- **REA v0.1 Stage B.** Reconciliation with that contract is pending until it is supplied.
