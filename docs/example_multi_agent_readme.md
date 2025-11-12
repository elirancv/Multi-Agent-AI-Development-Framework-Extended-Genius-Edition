# 🤖 Multi-Agent AI Development Framework — Extended Genius Edition

[![Code Quality](badge.svg)](PROJECT_AUDIT_REPORT.html) [![Audit Status](ci_badge.svg)](PROJECT_AUDIT_REPORT.html)

This version defines a **full-scale, enterprise-style AI software organization**: not just 20 agents, but a **tiered catalog of Functional Agents, Domain Advisors, and Cross-Cutting Reviewers** — so every artifact in the system is planned, built, reviewed, scored, and evolved.

The goal: **no unreviewed output. no orphan agent. no vague role.** Everything has an owner, an advisor, and a place in the pipeline.

---

## 🧬 Role Model

We split the system into 3 layers:

1. **Functional Agents** — produce things (code, docs, plans, UI, APIs).
2. **Advisors / Legendary Mentors** — review, score, and improve per domain.
3. **Cross-Cutting Governance** — architecture, security, performance, compliance, evolution.

This lets you run:
- “MVP fast” → fewer advisors, lighter thresholds
- “Production strict” → all advisors, cross-cutting on
- “Research” → experimental agents, relaxed scoring

---

## 1. Functional Agents (Builders Layer)

These are the agents that actually *do* the work. Organize them by department.

### 1.1 Product & Discovery
- **ChatIntakeAgent** — parses the user’s natural-language request into initial intent
- **ProductManagerAgent** — features, scope, user stories, acceptance criteria
- **BusinessAnalystAgent** — business rules, stakeholders, constraints, edge cases
- **DomainResearchAgent** — quick market/tech/domain scan (optional in MVP)
- **RequirementsRefinerAgent** — turns messy prompt into PRD-ready text

### 1.2 Architecture & System Design
- **DennisRitchieArchitectAgent** — Unix-like, small, composable services
- **SystemArchitectAgent** — global components, boundaries, integrations
- **APIContractDesignerAgent** — OpenAPI schema, resource naming, versioning
- **DataModelerAgent** — entities, relations, migrations, data lifecycles
- **IntegrationEngineerAgent** — 3rd-party, webhooks, external APIs

### 1.3 Engineering (Backend / Frontend / Fullstack)
- **BackendDeveloperAgent** — FastAPI endpoints, services, application layer
- **FrontendDeveloperAgent** — vanilla JS + Tailwind + component layout
- **UIComponentBuilderAgent** — builds reusable UI components from UX spec
- **StateManagementAgent** — data-fetch, caching, client-side stores
- **FileScaffolderAgent** — creates proper repo structure and paths

### 1.4 Data, Observability & Performance
- **LoggingAndObservabilityAgent** — logging schema, tracing, health endpoints
- **PerformanceTuningAgent** — finds obvious perf bottlenecks in generated code
- **ConfigAndSecretsAgent** — .env handling, config folders, secure defaults

### 1.5 Documentation & Developer Experience
- **DocWriterAgent** — `README.md`, `ARCHITECTURE.md`, `SYSTEM_FLOW.md`
- **APIDocsAgent** — documents endpoints, payloads, error codes
- **ChangelogGeneratorAgent** — records changes per evolution run
- **OnboardingGuideAgent** — “how to run / how to extend”

### 1.6 Quality & Testing
- **QATestPlanAgent** — test matrix, cases, priorities
- **PytestGeneratorAgent** — actual unit/integration test stubs
- **StaticAnalysisConfigAgent** — ruff/flake8/mypy/black/isort configs

### 1.7 Delivery & DevOps
- **DevOpsAgent** — Dockerfile, docker-compose, uvicorn config
- **CICDPipelineAgent** — GitHub Actions / CI config
- **ReleaseNotesAgent** — documents build output for Hall of Fame

---

## 2. Domain Advisors (Review Layer)

Every functional agent should have a matching advisor. Here we make it **explicit**.

### 2.1 Product & Discovery Advisors
- **SteveJobsProductAdvisor** — user-first, elegance, scope-cutting
- **MartyCaganProductAdvisor** — product thinking, value vs features
- **DonNormanUXAdvisor** — usability, affordances, cognitive load

### 2.2 Architecture & Engineering Advisors
- **MartinFowlerArchitectureAdvisor** — patterns, refactoring, layering
- **RobertMartinCleanCodeAdvisor** — names, SRP, duplication
- **LinusTorvaldsCodeReviewAdvisor** — code strictness, repo structure
- **EricEvansDomainAdvisor** — domain-driven alignment (optional)

### 2.3 Documentation & Clarity Advisors
- **BrianKernighanClarityAdvisor** — shorten, clarify, remove noise
- **GraceHopperToolingAdvisor** — tooling, scripting, speed of dev
- **EdwardTufteVisualizationAdvisor** — dashboard, UI clarity, info density

### 2.4 Security & Reliability Advisors
- **MargaretHamiltonReliabilityAdvisor** — failure paths, defensive coding
- **KevinMitnickRedTeamAdvisor** — threat modeling (white-hat scope only)
- **OWASPComplianceAdvisor** — basic API/web hardening

### 2.5 Performance & Observability Advisors
- **BrendanGreggPerformanceAdvisor** — perf hints, logging, metrics
- **SREObservabilityAdvisor** — health, probes, alerts (conceptual)

---

## 3. Cross-Cutting / Governance Agents

These run **above** the others and normalize output.

- **MetaCoordinatorAgent** — gathers all reviews, normalizes by project mode
- **CEODecisionAgent** — PROCEED / RERUN / ROLLBACK / FINALIZE
- **EvolutionTrackerAgent** — writes to evolution tree
- **HallOfFameCuratorAgent** — compares to champions, promotes if better
- **ResumeAndCompletionMarkerAgent** — adds final markers to files
- **NameAlignmentAgent** — enforces that YAML class names = Python class names
- **RepoHygieneAgent** — enforces `src/`, `docs/`, `tests/`, no junk in root

This is where your `.cursorrules` logic plugs in.

---

## 4. Why This Matters

With only “Product / Architect / Dev / QA” you **miss**:

1. Agents that *normalize* UX, naming, and repo structure.
2. Advisors that *specialize* (Clean Code, Architecture, Security).
3. Cross-cutting checks that run on **every** pipeline stage.

By explicitly listing them, the orchestrator can:
- auto-instantiate them
- auto-map them
- auto-render them in the UI “20+ team members”

---

## 5. Updated Mapping (1:1 + Cross-Cutting)

```text
Functional Agent              → Primary Advisor
--------------------------------------------------------
ChatIntakeAgent               → BrianKernighanClarityAdvisor
ProductManagerAgent           → SteveJobsProductAdvisor
BusinessAnalystAgent          → MartyCaganProductAdvisor
RequirementsRefinerAgent      → DonNormanUXAdvisor

DennisRitchieArchitectAgent   → MartinFowlerArchitectureAdvisor
SystemArchitectAgent          → MartinFowlerArchitectureAdvisor
APIContractDesignerAgent      → RobertMartinCleanCodeAdvisor
DataModelerAgent              → EricEvansDomainAdvisor
IntegrationEngineerAgent      → MartinFowlerArchitectureAdvisor

BackendDeveloperAgent         → LinusTorvaldsCodeReviewAdvisor
FrontendDeveloperAgent        → DonNormanUXAdvisor
UIComponentBuilderAgent       → EdwardTufteVisualizationAdvisor
LoggingAndObservabilityAgent  → SREObservabilityAdvisor
PerformanceTuningAgent        → BrendanGreggPerformanceAdvisor
ConfigAndSecretsAgent         → OWASPComplianceAdvisor

DocWriterAgent                → BrianKernighanClarityAdvisor
APIDocsAgent                  → GraceHopperToolingAdvisor
QATestPlanAgent               → MargaretHamiltonReliabilityAdvisor
PytestGeneratorAgent          → MargaretHamiltonReliabilityAdvisor
DevOpsAgent                   → GraceHopperToolingAdvisor
CICDPipelineAgent             → GraceHopperToolingAdvisor
```

**Cross-cutting (applies to all):**
- RepoHygieneAgent
- MetaCoordinatorAgent
- CEODecisionAgent
- EvolutionTrackerAgent
- HallOfFameCuratorAgent

---

## 6. UI Representation (the “20+ Team” Panel)

Group in the frontend like this:

- **Discovery**
  - Chat Intake
  - Product Manager
  - Business Analyst
  - Requirements Refiner

- **Architecture**
  - System Architect
  - API Designer
  - Data Modeler
  - Integration Engineer

- **Engineering**
  - Backend Dev
  - Frontend Dev
  - UI Components
  - Observability
  - Performance

- **Quality & Safety**
  - QA Tester
  - Test Generator
  - Security
  - Red Team

- **Ops & Docs**
  - DevOps
  - CI/CD
  - Doc Writer

- **Governance**
  - Meta Coordinator
  - CEO
  - Evolution
  - Hall of Fame

This gives you ~25 visible roles, **plus** advisors behind the scenes.

---

## 7. Spec Snippet for Orchestrator

> Every functional agent in `multi_agent_dev/agents/` MUST declare a `primary_advisor` from `multi_agent_dev/advisors/`. The orchestrator MUST also run the cross-cutting advisors (Architecture, Security, Repo Hygiene) on every stage output. Pipelines that do not specify an advisor mapping MUST fail validation.

This makes the system self-enforcing.

---

## 8. Next Steps

- Save this file as `README.md` in your repo.
- Generate `docs/agents_and_advisors.md` from the same list for UI rendering.
- Update your pipeline YAML to require `advisor:` for every `agent:`.
