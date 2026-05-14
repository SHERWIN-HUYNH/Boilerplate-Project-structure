<!-- Sync Impact Report
Version change: 0.0.0 -> 1.0.0
Modified principles:
- [PROJECT_NAME] Constitution -> AI Website Constitution
- [PRINCIPLE_1_NAME] -> Code Quality & Maintainability
- [PRINCIPLE_2_NAME] -> Testing Discipline
- [PRINCIPLE_3_NAME] -> UX Consistency
- [PRINCIPLE_4_NAME] -> Performance Budgets
- [PRINCIPLE_5_NAME] -> AI Behavior, Safety & Reliability
Added sections:
- Performance & UX Requirements
- Development Workflow & Quality Gates
Removed sections:
- Placeholder template comments and unresolved tokens
Templates requiring updates:
- ✅ updated .specify/templates/plan-template.md (constitution check remains compatible)
- ✅ updated .specify/templates/spec-template.md (mandatory user scenarios, requirements, and success criteria remain aligned)
- ✅ updated .specify/templates/tasks-template.md (task phases already support quality, testing, UX, and performance work)
- ⚠ pending .specify/templates/commands/*.md (no command templates present in current workspace snapshot)
Follow-up TODOs:
- None
-->
# AI Website Constitution

## Core Principles

### I. Code Quality & Maintainability
All production code MUST be small, readable, and easy to review. Components, services, and prompts MUST have a single responsibility, meaningful names, and clear boundaries. Shared logic MUST be extracted instead of duplicated. Any abstraction added to support the AI website MUST reduce complexity or repetition in a measurable way.

Rationale: AI features become difficult to evolve when the codebase is coupled, opaque, or over-abstracted.

### II. Testing Discipline
Tests MUST be written for critical behavior before or alongside implementation. Every user-facing AI flow MUST have deterministic automated coverage for success, failure, and boundary conditions. Unit tests MUST cover logic, integration tests MUST cover cross-component behavior, and end-to-end tests MUST cover the primary user journey. Bug fixes MUST include a regression test.

Rationale: AI-enabled products are inherently variable; strong tests keep behavior stable and safe.

### III. UX Consistency
All screens, interactions, copy, loading states, empty states, and error states MUST follow the same design system and interaction patterns. AI output MUST be presented in a way that is understandable, predictable, and clearly distinguished from system messages or user content. User actions MUST always have visible feedback, and the app MUST avoid abrupt layout shifts or confusing transitions.

Rationale: Users trust the product when the experience feels coherent and the AI is easy to interpret.

### IV. Performance Budgets
Each feature MUST define a measurable performance budget before implementation. UI interactions MUST remain responsive, AI requests MUST have explicit latency expectations, and heavy work MUST not block the main user path. Streaming, caching, debouncing, pagination, lazy loading, and background processing SHOULD be used when they reduce perceived latency or cost without harming clarity.

Rationale: AI features can be expensive and slow; performance must be designed in, not added later.

### V. AI Behavior, Safety & Reliability
AI capabilities MUST be constrained by explicit prompts, schemas, validation, and fallback behavior. The system MUST never assume the model output is correct, complete, or safe without verification. User-visible AI responses MUST be checked for format, relevance, and policy compliance before rendering or executing any follow-up action. When the model fails or confidence is low, the product MUST degrade gracefully and tell the user what happened.

Rationale: AI output is probabilistic and must be treated as untrusted input.

## Performance & UX Requirements

- Primary pages MUST remain usable under slow network conditions.
- AI responses with variable latency MUST show loading, streaming, or progress feedback.
- Core UI states MUST include loading, empty, error, retry, and success variants.
- Long-running AI operations MUST be cancellable or safely restartable when practical.
- Visual design MUST remain consistent across desktop and mobile breakpoints.
- Accessibility MUST be preserved for all AI interactions, including keyboard navigation and readable status announcements.

## Development Workflow & Quality Gates

- New features MUST start from a written spec with explicit acceptance criteria.
- Implementation plans MUST check this constitution before design work begins.
- Tasks MUST be grouped so each user story can be built and tested independently.
- Code review MUST verify test coverage, UX consistency, and performance impact.
- Any exception to these principles MUST be documented with a clear justification and follow-up plan.

## Governance

This constitution is the highest project-level engineering standard for the repository. If a request conflicts with these principles, the request MUST be re-scoped or explicitly justified before implementation.

Amendments require an updated constitution file, a version bump, and a short explanation of the reason for change. Minor updates add or refine guidance without breaking prior intent. Major updates redefine the operating rules or remove a principle.

All pull requests MUST confirm compliance with the constitution, or explain approved exceptions. Reviewers MUST reject changes that violate testing discipline, UX consistency, or performance budgets unless the PR includes a documented exception and mitigation.

**Version**: 1.0.0 | **Ratified**: 2026-05-13 | **Last Amended**: 2026-05-13
