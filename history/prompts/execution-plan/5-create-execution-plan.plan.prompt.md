---
id: 5
title: Create Execution Plan
stage: plan
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: execution-plan
branch: 002-execution-plan
user: claude-code
command: /sp.plan
labels: [execution_plan, plan, python, cli]
links:
  spec: specs/001-phase-1/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-execution-plan/plan.md
 - specs/002-execution-plan/research.md
 - specs/002-execution-plan/data-model.md
 - specs/002-execution-plan/quickstart.md
 - specs/002-execution-plan/contracts/api-contracts.md
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
You are a senior Python developer creating an execution plan.

Context:
- Phase-1 specs exist under /specs
- No code has been written yet
- This is a small, console-only application

Objective:
Create a clear, sequential implementation plan for Phase 1.

Plan Requirements:
1. Break work into logical steps:
   - Project structure setup
   - Task data model
   - CRUD operations
   - CLI menu and interaction
   - Validation and error handling
2. Each step must include:
   - Goal
   - Referenced spec files
   - Files affected
   - Validation checklist

Rules:
- NO code
- Keep plan simple and linear
- Do not reference Phase 2

Output:
A numbered Phase-1 execution plan.
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
```

## Response snapshot

I have successfully created a comprehensive implementation plan for the Phase 1 Execution Plan for Python Console Application. The following artifacts were created:

1. Implementation plan at `specs/002-execution-plan/plan.md`
2. Research document at `specs/002-execution-plan/research.md`
3. Data model at `specs/002-execution-plan/data-model.md`
4. Quickstart guide at `specs/002-execution-plan/quickstart.md`
5. API contracts at `specs/002-execution-plan/contracts/api-contracts.md`
6. Updated agent context in `.specify/memory/constitution.md`

The plan includes:
- Technical context with Python 3.13 and in-memory storage
- Constitution check ensuring all principles are followed
- Detailed project structure with source code organization
- Five sequential implementation steps:
  1. Project Structure Setup
  2. Task Data Model Implementation
  3. CRUD Operations Implementation
  4. CLI Menu and Interaction
  5. Validation and Error Handling
- Each step includes goals, referenced spec files, affected files, and validation checklists

All requirements from the user's input have been fulfilled with a clear, sequential approach that maintains simplicity and linear progression.

## Outcome

- ✅ Impact: Complete implementation plan created with sequential steps
- 🧪 Tests: none
- 📁 Files: specs/002-execution-plan/plan.md, research.md, data-model.md, quickstart.md, contracts/api-contracts.md
- 🔁 Next prompts: Ready for /sp.tasks to generate development tasks
- 🧠 Reflection: The plan comprehensively covers all requested elements with clear validation checklists.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):