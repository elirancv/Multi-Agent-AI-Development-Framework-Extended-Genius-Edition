# Agents & Advisors Catalog

This document lists all functional agents, their primary advisors, and the cross-cutting reviewers that the orchestrator should run on every stage. It is meant to be **machine-readable by the orchestrator** and **human-readable in the UI**.

---

## 1. Functional Agents

### 1.1 Product & Discovery
- **ChatIntakeAgent**
  - Role: Parse user input, detect intent, extract constraints
  - Primary Advisor: `BrianKernighanClarityAdvisor`
- **ProductManagerAgent**
  - Role: Define scope, user stories, acceptance criteria
  - Primary Advisor: `SteveJobsProductAdvisor`
- **BusinessAnalystAgent**
  - Role: Stakeholders, business rules, edge cases
  - Primary Advisor: `MartyCaganProductAdvisor`
- **DomainResearchAgent**
  - Role: Quick domain scan, assumptions, references
  - Primary Advisor: `MartyCaganProductAdvisor`
- **RequirementsRefinerAgent**
  - Role: Turn messy prompt into PRD-ready document
  - Primary Advisor: `DonNormanUXAdvisor`

### 1.2 Architecture & System Design
- **DennisRitchieArchitectAgent**
  - Role: Minimal, composable architecture
  - Primary Advisor: `MartinFowlerArchitectureAdvisor`
- **SystemArchitectAgent**
  - Role: Overall system topology, services, boundaries
  - Primary Advisor: `MartinFowlerArchitectureAdvisor`
- **APIContractDesignerAgent**
  - Role: OpenAPI, routes, naming, versioning
  - Primary Advisor: `RobertMartinCleanCodeAdvisor`
- **DataModelerAgent**
  - Role: Entities, relations, migrations, lifecycle
  - Primary Advisor: `EricEvansDomainAdvisor`
- **IntegrationEngineerAgent**
  - Role: 3rd-party APIs, webhooks, glue logic
  - Primary Advisor: `MartinFowlerArchitectureAdvisor`

### 1.3 Engineering (Backend, Frontend, UI)
- **BackendDeveloperAgent**
  - Role: FastAPI endpoints, services, adapters
  - Primary Advisor: `LinusTorvaldsCodeReviewAdvisor`
- **FrontendDeveloperAgent**
  - Role: Vanilla JS + Tailwind UI
  - Primary Advisor: `DonNormanUXAdvisor`
- **UIComponentBuilderAgent**
  - Role: Reusable UI components per UX spec
  - Primary Advisor: `EdwardTufteVisualizationAdvisor`
- **StateManagementAgent**
  - Role: Data fetch, caching, client state
  - Primary Advisor: `MartinFowlerArchitectureAdvisor`
- **FileScaffolderAgent**
  - Role: Create repo/project tree in correct folders
  - Primary Advisor: `RepoHygieneAdvisor` (see Cross-Cutting)

### 1.4 Data, Observability & Performance
- **LoggingAndObservabilityAgent**
  - Role: Logging schema, tracing, health checks
  - Primary Advisor: `SREObservabilityAdvisor`
- **PerformanceTuningAgent**
  - Role: Detect and suggest performance improvements
  - Primary Advisor: `BrendanGreggPerformanceAdvisor`
- **ConfigAndSecretsAgent**
  - Role: .env, config files, secure defaults
  - Primary Advisor: `OWASPComplianceAdvisor`

### 1.5 Documentation & DX
- **DocWriterAgent**
  - Role: README, ARCHITECTURE, SYSTEM_FLOW
  - Primary Advisor: `BrianKernighanClarityAdvisor`
- **APIDocsAgent**
  - Role: Endpoint docs, payloads, errors
  - Primary Advisor: `GraceHopperToolingAdvisor`
- **ChangelogGeneratorAgent**
  - Role: Change log per evolution run
  - Primary Advisor: `GraceHopperToolingAdvisor`
- **OnboardingGuideAgent**
  - Role: Developer onboarding, how-to-run
  - Primary Advisor: `BrianKernighanClarityAdvisor`

### 1.6 Quality & Testing
- **QATestPlanAgent**
  - Role: Test scenarios, priorities, coverage mapping
  - Primary Advisor: `MargaretHamiltonReliabilityAdvisor`
- **PytestGeneratorAgent**
  - Role: Actual test files / stubs
  - Primary Advisor: `MargaretHamiltonReliabilityAdvisor`
- **StaticAnalysisConfigAgent**
  - Role: Ruff/flake8/mypy/black/isort configs
  - Primary Advisor: `RobertMartinCleanCodeAdvisor`

### 1.7 Delivery & DevOps
- **DevOpsAgent**
  - Role: Dockerfile, docker-compose, runtime config
  - Primary Advisor: `GraceHopperToolingAdvisor`
- **CICDPipelineAgent**
  - Role: GitHub Actions / CI config
  - Primary Advisor: `GraceHopperToolingAdvisor`
- **ReleaseNotesAgent**
  - Role: Document build output for Hall of Fame
  - Primary Advisor: `BrianKernighanClarityAdvisor`

---

## 2. Domain Advisors

These are “legendary” or domain-specific reviewers.

- **SteveJobsProductAdvisor** — product elegance, ruthless scope cuts
- **MartyCaganProductAdvisor** — product value, feasibility, viability
- **DonNormanUXAdvisor** — user experience clarity, hierarchy, flows
- **MartinFowlerArchitectureAdvisor** — architecture, patterns, modularity
- **RobertMartinCleanCodeAdvisor** — naming, duplication, SRP
- **LinusTorvaldsCodeReviewAdvisor** — code strictness, repo structure
- **EricEvansDomainAdvisor** — domain-driven alignment
- **BrianKernighanClarityAdvisor** — shorten, clarify, simplify text
- **GraceHopperToolingAdvisor** — tooling, scripts, DX
- **EdwardTufteVisualizationAdvisor** — dashboards, information layout
- **MargaretHamiltonReliabilityAdvisor** — fault tolerance, defensive design
- **KevinMitnickRedTeamAdvisor** — threat modeling (white-hat scope)
- **OWASPComplianceAdvisor** — API/web basic hardening
- **BrendanGreggPerformanceAdvisor** — performance and profiling
- **SREObservabilityAdvisor** — health, probes, observability

Each advisor must return a **structured review**:
- `score: float`
- `approved: bool`
- `critical_issues: list[str]`
- `suggestions: list[str]`
- `summary: str`
- `severity: "low" | "medium" | "high"`

---

## 3. Cross-Cutting Reviewers

> **Note:** Orchestrator rules are defined in `.cursor/rules/orchestrator.mdc`. These agents must run on **every stage** (or at least at major checkpoints).

- **MetaCoordinatorAgent**
  - Normalizes advisor output according to project mode (MVP / Production / Research)
  - Produces normalized critical issues and severity
- **CEODecisionAgent**
  - Takes normalized feedback and decides: `PROCEED | RERUN | ROLLBACK | FINALIZE`
- **EvolutionTrackerAgent**
  - Writes node to evolution tree, links to parent, stores outcome score
- **HallOfFameCuratorAgent**
  - Compares current outcome to champion builds, promotes if better
- **RepoHygieneAgent** (a.k.a. FilePlacementReviewer)
  - Verifies files are stored under `src/`, `docs/`, `tests/`, `config/`, `pipeline/`
  - Rejects junk in repo root
- **NameAlignmentAgent**
  - Ensures pipeline YAML names match real Python class names

These cross-cutting agents make the system **self-enforcing**.

---

## 4. Orchestrator Hints

> **Note:** These rules are enforced in `.cursor/rules/orchestrator.mdc`. See that file for authoritative validation rules.

- If an agent has **no** declared `primary_advisor`, the pipeline should fail validation.
- If project mode is `production_stability`, run **all** cross-cutting reviewers.
- If project mode is `mvp_fast_delivery`, you may skip heavy advisors (e.g. Performance) but MUST still run `RepoHygieneAgent` and `NameAlignmentAgent`.
- Every successful stage should write a completion marker so resume is possible.

---

## 5. UI Usage

- Render this list as a **directory of roles** in the dashboard.
- Show Functional Agents as “active workers”.
- Show Advisors as “reviewers” (behind the scenes).
- Show Cross-Cutting as “system guardians”.

This keeps the UX consistent with a “20+ team members” view.
