# Project Specification

## Title
Privacy-Preserving NLP for Sensitive Text

## Problem
Unstructured healthcare and student text may contain identifiers. Manual removal is slow. This prototype automates detection and pseudonymization for a small, defined set of entity classes.

## Objectives
1. Detect selected sensitive entities.
2. Combine spaCy NER with deterministic patterns.
3. Replace values with stable placeholders.
4. Process synthetic data locally.
5. Export anonymized text and a non-sensitive detection summary.
6. Provide basic precision/recall/F1 evaluation later.

## Functional requirements
- single text input
- CSV input with configurable text column
- entity detection
- anonymized text generation
- repeated-value consistency within a document
- CSV outputs

## Non-functional requirements
- local processing
- no external API
- reproducible Python environment
- human-readable output
- explicit privacy limitations

## Success criteria
A professor demo should show multiple entity types, consistent replacement, CSV processing, and basic evaluation on synthetic ground truth.

## Boundaries
This is not a legal compliance tool and not a guarantee that all sensitive information has been removed. Real patient/student data is outside the academic demo scope.
