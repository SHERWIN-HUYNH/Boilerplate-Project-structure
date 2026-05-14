AI Website Constitution
Core Principles
I. Code Quality & Maintainability
All production code MUST be small, readable, and easy to review. Components, services, and prompts MUST have a single responsibility, meaningful names, and clear boundaries. Shared logic MUST be extracted instead of duplicated. Any abstraction added to support the AI website MUST reduce complexity or repetition in a measurable way.
Rationale: AI features become difficult to evolve when the codebase is coupled, opaque, or over-abstracted.
II. Testing Discipline
Tests MUST be written for critical behavior before or alongside implementation. Every user-facing AI flow MUST have deterministic automated coverage for success, failure, and boundary conditions. Unit tests MUST cover logic, integration tests MUST cover cross-component behavior, and end-to-end tests MUST cover the primary user journey. Bug fixes MUST include a regression test.
Rationale: AI-enabled products are inherently variable; strong tests keep behavior stable and safe.
III. UX Consistency
All screens, interactions, copy, loading states, empty states, and error states MUST follow the same design system and interaction patterns. AI output MUST be presented in a way that is understandable, predictable, and clearly distinguished from system messages or user content. User actions MUST always have visible feedback, and the app MUST avoid abrupt layout shifts or confusing transitions.
Rationale: Users trust the product when the experience feels coherent and the AI is easy to interpret.
IV. Performance Budgets
Each feature MUST define a measurable performance budget before implementation using the baseline thresholds defined in the "Performance & UX Requirements" section below. UI interactions MUST remain responsive, AI requests MUST have explicit latency expectations, and heavy work MUST NOT block the main user path. Streaming, caching, debouncing, pagination, lazy loading, and background processing SHOULD be used when they reduce perceived latency or cost without harming clarity.
Any feature that cannot meet the defined thresholds MUST document the deviation as an approved exception with a mitigation plan before implementation begins.
Rationale: AI features can be expensive and slow; performance must be designed in, not added later.
V. AI Behavior, Safety & Reliability
AI capabilities MUST be constrained by explicit prompts, schemas, validation, and fallback behavior. The system MUST never assume the model output is correct, complete, or safe without verification. User-visible AI responses MUST be checked for format, relevance, and policy compliance before rendering or executing any follow-up action. When the model fails or confidence is low, the product MUST degrade gracefully and tell the user what happened.
User input MUST be sanitized and MUST NOT be forwarded to the model in a form that could reconstruct private session context from other users. All AI-generated actions that modify user data MUST require explicit user confirmation before execution.
Rationale: AI output is probabilistic and must be treated as untrusted input. User data must be protected at the boundary between product and model.
VI. Prompt & Model Governance
Every system prompt and few-shot example used in production MUST be version-controlled alongside application code and treated as a first-class artifact. Prompt changes MUST go through the same review and testing process as code changes — including regression tests against known-good outputs.
The product MUST declare a supported model version (or version range) per feature. When a model is deprecated or updated, affected features MUST be re-evaluated and re-tested before the new model version is promoted to production. Silent model substitution is PROHIBITED.
Rationale: Prompts and model versions are the primary control surface for AI behavior. Unreviewed prompt drift or silent model upgrades are the equivalent of deploying untested code.
Performance & UX Requirements
The following thresholds are the baseline for all performance budgets (Principle IV). Features MUST meet these thresholds or document an approved exception.
Page load & rendering

Largest Contentful Paint (LCP): MUST be ≤ 2.5 s on a simulated 4G connection.
Cumulative Layout Shift (CLS): MUST be ≤ 0.1 across all pages.
Time to Interactive (TTI): MUST be ≤ 4 s on a mid-range mobile device.

AI request latency

Time to first token (streaming): MUST be ≤ 3 s under normal load.
Full AI response (non-streaming): MUST complete within 10 s or surface a visible timeout state.
Timeout handling: All AI requests MUST implement a hard timeout of 15 s; the UI MUST notify the user and offer a retry path when this limit is hit.

Interaction responsiveness

UI response to user input: MUST remain ≤ 100 ms for all synchronous interactions.
Long-running AI operations MUST be cancellable or safely restartable when practical.

Additional UX requirements

Primary pages MUST remain usable under slow network conditions.
AI responses with variable latency MUST show loading, streaming, or progress feedback.
Core UI states MUST include loading, empty, error, retry, and success variants.
Visual design MUST remain consistent across desktop and mobile breakpoints.
Accessibility MUST be preserved for all AI interactions, including keyboard navigation and readable status announcements.

Development Workflow & Quality Gates

New features MUST start from a written spec with explicit acceptance criteria.
Implementation plans MUST check this constitution before design work begins.
Tasks MUST be grouped so each user story can be built and tested independently.
Code review MUST verify test coverage, UX consistency, and performance impact against the thresholds defined above.
Any exception to these principles MUST be documented with a clear justification, an owner, and a follow-up resolution date. Undocumented exceptions MUST be treated as blocking defects.
Prompt changes MUST be tracked in version control with a descriptive commit message and linked to the spec or bug that motivated the change.

Governance
This constitution is the highest project-level engineering standard for the repository. If a request conflicts with these principles, the request MUST be re-scoped or explicitly justified before implementation.
Amendment procedure
Amendments require:

An updated constitution file with a version bump following semantic versioning (MAJOR for removing or redefining a principle; MINOR for adding guidance or a new principle; PATCH for clarifying wording without changing intent).
A short explanation of the reason for the change prepended in the Sync Impact Report comment.
Review and approval by the project lead or designated architecture owner before merging.
A consistency propagation pass — all dependent templates (plan-template.md, spec-template.md, tasks-template.md, commands/*.md) MUST be checked and updated or marked N/A.

Exception approval
Exceptions to any MUST rule MUST be approved in writing (PR description or linked decision record) by the architecture owner before implementation. Each approved exception MUST state: the principle being waived, the reason, the mitigation, and a resolution date.
Pull request compliance
All pull requests MUST confirm compliance with the constitution, or explain approved exceptions. Reviewers MUST reject changes that violate testing discipline, UX consistency, prompt governance, or performance budgets unless the PR includes a documented exception and mitigation.
Version: 1.1.0 | Ratified: 2026-05-13 | Last Amended: 2026-05-13