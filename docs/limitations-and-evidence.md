# Limitations and evidence status

## Current public evidence

This scaffold demonstrates the intended architecture, evidence standard,
release boundary and three role-neutral schemas. The release-tree validator
checks for selected private paths, role aliases, host identifiers and internal
artifact classes.

The scaffold does not demonstrate:

- a trained or promoted role model;
- a reproducible training result;
- a complete mediated runtime;
- end-to-end Planner–Implementer–Reviewer performance;
- a security qualification or penetration test;
- a released dataset;
- model-family portability; or
- deployment throughput, latency, memory, energy or cost.

## Method limitations

- Fine-tuning does not make model output deterministic or authorized.
- A model can follow a contract and still produce incorrect code.
- Synthetic fixtures can reward shortcuts when the oracle is weak.
- Family-disjoint splits reduce semantic leakage but do not eliminate it.
- Learned preferences can reduce flexibility outside trained coverage.
- Deterministic controls cost engineering effort and can become too narrow.
- Repeated tuning can regress base capability without retention tests.
- A schema-valid proposal can still be unsafe or semantically wrong.
- Public synthetic examples cannot prove private deployment requirements.

## Release evidence

Add a recipe or result only when the release includes:

- immutable inputs and revisions;
- a runnable procedure;
- checkpoint and resume behaviour;
- deterministic gates;
- frozen evaluation;
- raw or aggregate evidence appropriate for publication;
- licence and provenance review;
- resource measurements where claimed; and
- an explicit promotion, rejection or limitation statement.

## Planned sequence

1. Release a small synthetic executable example set and its validators.
2. Reproduce an Implementer full fine-tune and frozen evaluation, then release
   the pinned recipe and result record.
3. Add the Planner and Reviewer adaptation and routing evaluation.
4. Implement and test the mediated runtime.
5. Run the complete controlled comparison.
6. Port the frozen semantic corpus to other qualified model and framework
   targets.
7. Add specialist modules and a family-disjoint red-team suite.

The sequence can change when evidence requires it. Planned work must remain
labelled as planned.
