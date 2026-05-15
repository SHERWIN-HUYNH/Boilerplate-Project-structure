<!--
Sync Impact Report
Version change: 1.1.0 → 2.0.0
Modified principles:
- I. Code Quality & Maintainability → I. Code Quality & Maintainability
- II. Testing Discipline → II. Testing Discipline
- III. Reliability & Performance Budgets → III. Reliability & Performance Budgets
- IV. Delivery Correctness & Idempotency → IV. Delivery Correctness & Idempotency
- V. Observability & Recoverability → V. Observability & Recoverability
Added sections:
- Benchmark & Proof Obligations
- Governance
Removed sections:
- AI Behavior, Safety & Reliability
- Prompt & Model Governance
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ⚠ pending .specify/templates/commands/constitution.md (template file is currently empty)
- ✅ .cursor/skills/speckit-constitution/SKILL.md (validated against update flow)
Follow-up TODOs:
- Define project-specific benchmark command and acceptance checks in spec/plan/tasks
- Confirm ratification date with project lead if governance history needs formal backfill
Reason for change: Repository scope is now a distributed messaging delivery service rather than an AI website, so the constitution must emphasize delivery correctness, throughput, idempotency, and recoverability.
-->
# Distributed Messaging Delivery Constitution

## Core Principles

### I. Code Quality & Maintainability
All production code MUST be small, readable, and easy to review. Components, services, and adapters MUST have a single responsibility, meaningful names, and clear boundaries. Shared logic MUST be extracted instead of duplicated. Any abstraction added to support the messaging delivery service MUST reduce complexity or repetition in a measurable way.

Rationale: Messaging systems fail in subtle ways when the codebase is coupled, opaque, or over-abstracted.

### II. Testing Discipline
Tests MUST be written for critical behavior before or alongside implementation. Every message lifecycle path MUST have deterministic automated coverage for success, temporary failure, permanent failure, retries, duplicate submission handling, and boundary conditions. Unit tests MUST cover logic, integration tests MUST cover cross-component behavior, and end-to-end tests MUST cover the benchmark and primary delivery flow. Bug fixes MUST include a regression test.

Rationale: Delivery systems must prove correctness under retry, failure, and high-volume conditions.

### III. Reliability & Performance Budgets
Each feature MUST define a measurable reliability and performance budget before implementation. Processing pipelines MUST remain responsive under target load, and heavy work MUST NOT block the main submission path. Queueing, batching, buffering, backpressure, and background processing SHOULD be used when they reduce latency or increase throughput without harming correctness.

Any feature that cannot meet its defined throughput, latency, memory, or durability thresholds MUST document the deviation as an approved exception with a mitigation plan before implementation begins.

Rationale: The service must complete large workloads within strict time limits while remaining stable.

### IV. Delivery Correctness & Idempotency
Each submitted message MUST produce exactly one final delivery result. Retry attempts, reprocessing, or crash recovery MUST NOT create duplicate final rows. Final status transitions MUST be explicit, deterministic, and auditable. The system MUST be able to explain whether a message was delivered, failed permanently, or is still pending during recovery.

Rationale: The benchmark and the product requirement both depend on one final row per submitted message.

### V. Observability & Recoverability
The system MUST provide basic logging, counters, and benchmark-visible metrics that allow operators to verify throughput, retry volume, duplicate final rows, and data loss. Crash recovery MUST preserve enough state to resume processing without losing accepted messages. Any storage or queueing mechanism MUST be chosen and documented with its recovery story in mind.

Rationale: A delivery service is only trustworthy if failures can be detected, diagnosed, and recovered from.

## Benchmark & Proof Obligations
The implementation MUST include a reproducible benchmark command that can be run from a clean start on a normal developer machine. The benchmark MUST prove completion of 1,000,000 messages within 10 minutes, with exactly one final output row per submitted message and zero unexplained data loss. The benchmark report MUST include worker count, batch size, queue/storage approach, output format, total duration, throughput, success count, failed count, retry count, duplicate final rows, and data loss count.

## Development Workflow & Quality Gates

New features MUST start from a written spec with explicit acceptance criteria. Implementation plans MUST check this constitution before design work begins. Tasks MUST be grouped so each user story can be built and tested independently. Code review MUST verify test coverage, delivery correctness, recoverability, and performance impact against the thresholds defined above. Any exception to these principles MUST be documented with a clear justification, an owner, and a follow-up resolution date. Undocumented exceptions MUST be treated as blocking defects.

## Governance
This constitution is the highest project-level engineering standard for the repository. If a request conflicts with these principles, the request MUST be re-scoped or explicitly justified before implementation.

### Amendment procedure
Amendments require:

An updated constitution file with a version bump following semantic versioning (MAJOR for removing or redefining a principle; MINOR for adding guidance or a new principle; PATCH for clarifying wording without changing intent).
A short explanation of the reason for the change prepended in the Sync Impact Report comment.
Review and approval by the project lead or designated architecture owner before merging.
A consistency propagation pass — all dependent templates (plan-template.md, spec-template.md, tasks-template.md, commands/*.md) MUST be checked and updated or marked N/A.

### Exception approval
Exceptions to any MUST rule MUST be approved in writing (PR description or linked decision record) by the architecture owner before implementation. Each approved exception MUST state: the principle being waived, the reason, the mitigation, and a resolution date.

### Pull request compliance
All pull requests MUST confirm compliance with the constitution, or explain approved exceptions. Reviewers MUST reject changes that violate testing discipline, delivery correctness, observability, or performance budgets unless the PR includes a documented exception and mitigation.

Version: 2.0.0 | Ratified: 2026-05-15 | Last Amended: 2026-05-15