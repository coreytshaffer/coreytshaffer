# Validation — `pc-validate 0.4`

**Status: proposed planning tooling, committed in revision r1 and revised in r2–r4.** It checks the
planning documents and data in this directory. It is not, and does not test, any council
implementation. Nothing runs it automatically: there is no CI.

## Run

```sh
python3 research/philosophical-council/validation/validate.py
```

**Requirements.**

- Python 3.10 or later. The reference run used 3.13.17.
- `jsonschema`. The reference run used 4.26.0.

Without `jsonschema`, the schema rules are reported as NOT RUN and the run fails. It fails
closed rather than passing without them.

**Exit status.**

- `0`: every rule passed and every negative control was detected.
- `1`: any rule failed or could not run; any negative control was missed, imprecise or
  invalid; or some rule has no negative control.
- `2`: usage error.

## What it does

1. **Loads the files into memory.** These are the schemas, fixtures, examples, the two
   pinned documents and this directory's files. Nothing on disk is written.
2. **Runs every rule.** Each has a stable ID:
   - `F01`–`F04`: bytes and JSON syntax, including duplicate keys, which ordinary parsers
     silently resolve.
   - `SCH01`: the schema set and schema validity.
   - `FX01`–`FX20`: fixtures. Schema conformance, lineage, answer-key structure, exact
     `inferable_from` quotations, leaks into critic-visible packets, and the canary.
   - `EX01` and `V0`–`V13`: example packets and records. Schema conformance, the
     case-structure rules FX04–FX11 for example packets, then the record rules V1–V13 from
     the [record design](../epistemic-evaluation-record.md), section 6.
   - `PIN01`–`PIN02`: `fixtures/SHA256SUMS` matches the bytes and covers everything it
     must, the examples included.
3. **Applies the negative controls.** Each control in
   [`negative_controls.json`](negative_controls.json) injects one fault into an in-memory
   copy of the files. The rule it names must then fire. Examples: a fabricated quotation
   still marked `source_linked`, a minority position silently dropped, or a category word
   leaked into a case title. If a named rule does not fire, the validator has regressed. A
   rule with no control also fails the run, so every check has to show that it can fail.
   A control marked `exact` must fire its named rules and no others; otherwise it is
   IMPRECISE, and the run fails.
4. **Prints a report.** The header records the validator's and controls' SHA-256 and the
   Python and `jsonschema` versions. For a given checkout and environment the report
   contains no timestamps and no host paths, so a second run reproduces it exactly.

## Repeated entries

Every rule that claims an exact correspondence ("exactly once", a partition, a mirror)
checks for repeats before it compares sets. Repeats inside a list of IDs are rejected by the
schemas' `uniqueItems` (V0, FX01, FX02). Repeated entries in a list of objects are rejected by
the rule itself, and r1 missed several of those. The operator's review of r1 found two
mutations that passed every check, and an r2 audit of every set or keyed comparison found
the same defect in more rules (README, revision record, R2-D1 and R2-D2). In the drafting
run, the r1 rules missed every control below and the r2 rules detected each one.

| Check | Rule | Control | Fault injected |
|---|---|---|---|
| Each invalid output names a declared reviewer | V3 | NC-V3b | The operator's second mutation: an invalid output from `ghost` |
| Unique position IDs; each assessed reviewer held once | V7 | NC-V7b | The operator's first mutation: an exact copy of a position |
| No assessment in two entries | V7 | NC-V7c | One assessment split into two positions |
| Positions are counted, not their distinct IDs | V8 (and V7) | NC-V8b | Two differing positions share an ID, and their disagreement is deleted |
| Unique disagreement IDs | V8 | NC-V8c | An exact copy of a disagreement |
| One attention entry per segment | V9 | NC-V9b | An inflated entry followed by a correct one for the same segment |
| One lineage entry per evidence item | V10 | NC-V10b | Falsified roots followed by a correct entry for the same source |
| The index lists each case once | FX03 | NC-FX03c | A case listed twice |
| Unique transformation IDs in a case | FX11 | NC-FX11b | A repeated transformation record |

- **Shadowing.** NC-V9b and NC-V10b put a falsified entry before a correct one. A
  comparison that keeps the last entry per key never sees the falsified one, which is how
  r1 missed them.
- **V11 (added in r3).** r2's V11 repeat check had no committed control, because the
  first example's packet has no transformation. r3 adds a second example, a packet with
  transformation X1 (`examples/PC-TOY-02.case.json`) and a valid record over it
  (`examples/pc-eer-illustrative-02.json`). NC-V11b appends an exact duplicate of the X1
  entry. NC-V11c raises the first X1 entry's fidelity check from `self_reported` to
  `independent_spot_check` and appends a correct entry after it. Both are `exact`: each
  fires V11 and the pin check on the edited example, and nothing else. The r1 rules miss
  both.
- **Reviewer outcomes (r3 and r4, decision D16).** A reviewer has exactly one outcome, so
  an invalid output listed twice fails V4 (NC-V4b); the r1 and r2 rules miss it. The third
  example, `examples/pc-eer-illustrative-03.json`, is a valid record containing an
  assessment, an invalid output and a transport failure with `no_output`. NC-V4d gives
  its transport-failed reviewer an output-hash value other than `no_output`.
- **Allowed on purpose.** Two disagreements with different IDs over the same positions,
  since the same positions can conflict over distinct issues (decision D15). Each must
  state its scope; whether two scopes name the same issue is left to human review.
- **`json_append` and `exact`.** Controls can append to an array, so a control can state a
  mutation as it was found, for example "append an exact copy of a position". A control
  marked `exact` lists every rule it must fire, and no other rule may fire. Example files
  are pinned, so an exact control that edits one also lists `PIN01`. The controls format
  is `pc-negative-controls/0.4`.

## What a pass establishes, and what it does not

**A pass establishes:**

- that, at that checkout and in that environment, the files satisfy every listed rule;
- that every rule detected its injected fault.

**A pass does not establish:**

- **Correct answer keys.** That needs the human second-reader gate (protocol, G1). Until
  then every answer key records `reproduction_state: not_attempted`.
- **Free text without overreach.** The schemas and rules constrain structure and metadata
  only. A record's interpretation, rationale or note can still assert truth, safety,
  intent or authority in prose. Human scoring detects that (protocol, M7); nothing here
  screens text.
- **Anything about critics.** What a critic would detect or miss is untested.
- **Right semantics.** Whether the schemas encode the right semantics is a design
  question, reviewed by people.
- **A correct validator.** Pins establish the validator's byte identity, not its
  correctness, and a modified validator could report anything. Check `SHA256SUMS`
  independently with `sha256sum -c`, and read the code.
- **REA conformance.** Only the council formats are checked. REA v0.1 has no carrier
  encoding to conform to.

## Pins

`fixtures/SHA256SUMS` commits to the following bytes:

- the six case packets and six answer keys;
- every file in `examples/`: the two toy packets and the three illustrative records;
- the index;
- the documents named in `index.json` under `pinned_documents`. These are the protocol,
  the record design, the three schemas, and this directory's validator and controls.

The canonicalization contract is deliberately trivial:

- SHA-256 over the exact stored bytes;
- no normalization;
- LF line endings, kept by `.gitattributes`;
- paths relative to `fixtures/`.

A digest is meaningful only under that contract. The REA rule applies: a digest without a
canonicalization contract is an opaque number.

Regenerate the pins after any change to a pinned file:

```sh
cd research/philosophical-council/fixtures
sha256sum cases/PC-F0*.case.json expectations/PC-F0*.expected.json index.json \
  ../study-protocol.md ../epistemic-evaluation-record.md ../schemas/*.schema.json \
  ../examples/*.json ../validation/validate.py ../validation/negative_controls.json > SHA256SUMS
```

## Recording a run

A run is a checkout-bound reproduction of these checks, in the REA sense: record the commit
SHA, the command, the Python and `jsonschema` versions, and the full output. The revision
record in the [README](../README.md) gives the drafting run.

The r0 milestone ran similar checks from scratch scripts that were never committed. Its
statements that files "were checked" remain historical claims that nobody can reproduce.
This validator re-implements and extends those checks, so its results can be reproduced.

## Changing the rules

- **A new rule** needs at least one negative control; otherwise the run fails.
- **Exactness.** A rule that claims "exactly once", a partition or a mirror must check for
  repeats, or compare counts, before it compares sets.
- **Rule IDs.** They are cited in the record design and protocol. Renumbering one needs a
  revision of both.
- **Controls** are test data. Weakening one to make a run pass defeats its purpose. If a
  control is wrong, correct it in a revision that says why.
