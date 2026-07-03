# Trust Vocabulary

Canonical definitions for terms used across my repositories. Each project links here
for the shared vocabulary and defines only domain-specific terms locally, so
definitions don't drift between repos.

## Local-first
Data lives and is processed on the operator's machine first. Publication or
transmission is a separate, deliberate step — never a side effect.
*Not:* offline-only, or a claim that no cloud services are ever used.

## Fail closed
When validation, permission, provenance, or freshness is uncertain, the system
blocks, quarantines, or withholds rather than shipping clean-looking output.
*Not:* a blanket claim that every check is automated. Each repo documents which
gates are enforced in code and which are manual review steps.

## Warn-and-review
A validator surfaces a warning that requires human judgment before republish or
promotion, without hard-blocking. This is weaker than fail-closed, and docs must
never describe warn-and-review behavior as fail-closed.

## Human review gate
A required manual decision point before data or an action crosses a boundary
(publication, execution, export), with the decision recorded.
*Not:* a rubber stamp or an implied approval default.

## Public/private boundary
An explicit split between what may publish and what stays local — enforced by
ignore rules and validator checks, not merely described in docs.

## Provenance
Every record carries its source, time, method, and review status. Derived or
copied data is labeled with its origin.

## Non-claims
Each project states plainly what it is not (e.g., not official public-health
guidance, not agent safety, not a certified GHG inventory). Non-claims are
first-class documentation, kept adjacent to the claims they bound.

## Claims match code
Documentation describing enforcement is checked against what the code actually
enforces. Aspirational controls are labeled "proposed / not implemented" rather
than written as if they exist.
