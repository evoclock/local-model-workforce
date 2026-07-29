# Security policy

## Release status

This repository publishes project documentation and evaluation reports. It
does not yet release a model, dataset, training recipe or mediated runtime.
Do not infer a security guarantee from the publication.

## Design boundary

Model output is untrusted input. A learned preference is not authorization.
Filesystem mutation, command execution, external communication, credential use
and irreversible actions require typed contracts and deterministic mediation.

The runtime must retain outcome-level constraints across multiple steps.
Splitting, encoding, delegation or changing tools does not make a previously
denied outcome permissible.

## Reporting

Do not put credentials, private data or an active exploitation procedure in a
public issue. Use GitHub private vulnerability reporting for sensitive reports.
