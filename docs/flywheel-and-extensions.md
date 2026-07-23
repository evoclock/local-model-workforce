# Flywheel and extensions

## Evidence flywheel

The system does not train automatically from raw incidents.

1. Preserve the task, artifacts and receipts.
2. Attribute the first failure to planning, contract construction,
   implementation, tools, environment, review or evaluation.
3. Determine whether the correction belongs in model training, evaluation,
   MCP, hooks, documentation or more than one layer.
4. Build an executable family and a distinct hidden analogue.
5. Run provenance, privacy, diversity, leakage and independent-review gates.
6. Assign the whole family to one split.
7. Retrain only through an authorized and resumable recipe.
8. Promote, retune or reject from frozen results.

Locally green schema checks do not prove task success or cross-family
independence. The review must compare causal shapes, patches and outcomes across
the batch.

## Long-horizon and red-team cases

The red-team suite must test complete outcomes, not isolated actions. Priority
cases include:

- prompt injection and untrusted tool output;
- credential reconstruction or policy circumvention across steps;
- authority amplification through delegation;
- unsafe data movement or disclosure;
- fabricated receipts and stale evidence;
- partial failure, replay and idempotency;
- supply-chain and dependency substitution;
- irreversible actions without current approval; and
- evaluators that reward shortcuts instead of the required result.

Attack cases remain frozen evaluation data until a separate correction family
is verified and admitted.

## Specialist modules

A specialist module adds domain capability without weakening the shared role
and security contracts.

Each module starts with methodological preferences. The preferences define:

- methods to prefer, avoid or use only under stated conditions;
- evidence and reproducibility requirements;
- metrics and visual standards;
- common failure modes and invalid shortcuts;
- operating constraints and tool boundaries;
- acceptance or escalation criteria; and
- executable evaluation oracles.

The curriculum converts those choices into capabilities. Executable families
then cover materially different states, implementations, denials, corrections
and reviews. A family-disjoint evaluation tests whether the model applies the
method to unfamiliar tasks.

Broad domain labels are not sufficient. Base models already contain substantial
general software, data-science, machine-learning and AI knowledge. A module
should target distinctive methodology and operating practice, such as:

- **software delivery**: prior-art checks, bounded implementation, testing,
  Definition of Done, reproducibility, security and proportional design;
- **MLOps**: portable artifacts, lineage, promotion, rollback, monitoring and
  environment drift;
- **model risk**: data and label drift, bias, calibration, uncertainty, subgroup
  performance and tail behaviour;
- **risk and fraud**: temporal validation, leakage, severe class imbalance,
  asymmetric cost, delayed labels and investigator capacity;
- **AI systems**: RAG and GraphRAG evaluation, retrieval routing, provenance,
  prompt injection, agentic-tool evaluation and deployment trade-offs; and
- **decision systems**: contextual bandits, offline evaluation, safe exploration,
  reward design and policy monitoring.

Scientific modules follow the same method. Genomics, bioinformatics,
phylogenetics, population genetics and biological modelling need explicit
scientific assumptions, mathematical checks and domain-valid evidence.

We do not mix conflicting methodological preferences without an explicit routing
rule.

## Probability telemetry

Supervised fine-tuning does not require stored logits. Full logits are useful
for distribution-matching distillation and exact token-distribution
comparisons. Selected token probabilities can support calibration, difficult
routing analysis and policy replay.

Capture detailed probability data only when the case has a declared consumer,
reliable gold evidence and material transfer value. Do not retain large logits
for duplicates, deterministic decisions or cases without a valid outcome.
