# Limitations and evidence status

## Current public evidence

The repository now publishes:

- the architecture and evidence method;
- three role-neutral schemas;
- editable and rendered system diagrams;
- a technical report for the v7 task-bound Implementer fine-tuning experiment;
- a project brief and presentation; and
- a release-tree privacy validator.

The report includes controlled role evaluation and 15 paired HumanEval+ runs.
Correct role events increased from 0% to 90.70% on the common 86-task set, while
fixture pass did not improve. The HumanEval+ tuned-minus-base mean was -2.32
percentage points, within the programme three-point margin. The result was
task-dependent: several sub-task groups improved, while parsing and formatting,
aggregation, general transformation, and searching and ordering inform v8.

## What is not public yet

The repository does not yet provide:

- model weights or adapters;
- the admitted training corpus or evaluation inputs;
- a runnable and independently reproduced recipe;
- a complete mediated runtime;
- end-to-end Planner–Implementer–Reviewer performance;
- a security qualification or penetration test;
- model-family portability; or
- an unrestricted deployment claim.

## Method limitations

- Fine-tuning does not make model output deterministic or authorized.
- A model can follow a contract and still produce incorrect code.
- Family-disjoint splits reduce semantic leakage but do not eliminate it.
- Learned preferences can reduce flexibility outside trained coverage.
- Deterministic controls cost engineering effort and can become too narrow.
- Repeated tuning can regress base capability without retention tests.
- A schema-valid proposal can still be unsafe or semantically wrong.

## Planned sequence

1. Complete private-repository reconciliation and final evaluation.
2. Complete v8 admission and family-disjoint retesting.
3. Publish the selected quantised model and model card on Hugging Face.
4. Publish the bound recipe, scripts and reproducibility record here.
5. Implement and test the mediated runtime.
6. Add Planner and Reviewer adaptation and routing evaluation.
7. Extend the consumer-neutral flywheel and specialist modules.

The sequence can change when evidence requires it. Planned work remains
labelled as planned.
