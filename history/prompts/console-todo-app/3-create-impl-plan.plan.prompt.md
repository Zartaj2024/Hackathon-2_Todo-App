---
id: 3
title: Create Impl Plan
stage: plan
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: console-todo-app
branch: 001-console-todo-app
user: claude-code
command: /sp.plan
labels: [todo_app, plan, python, cli]
links:
  spec: specs/001-console-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-console-todo-app/plan.md
 - specs/001-console-todo-app/research.md
 - specs/001-console-todo-app/data-model.md
 - specs/001-console-todo-app/quickstart.md
 - specs/001-console-todo-app/contracts/api-contracts.md
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
You are a senior Python engineer creating an execution plan.

Context:
- Phase-1 specs exist
- No code has been written

Objective:
Create a step-by-step implementation plan WITH explicit error-handling stages.

Plan Requirements:
1. Include steps for:
   - Input validation
   - Exception-safe logic
   - Graceful CLI recovery
2. Each step must define:
   - Goal
   - Spec references
   - Possible failure points
   - Validation checklist

Rules:
- NO code
- Plan must explicitly mention error-handling steps

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

I have successfully created a comprehensive implementation plan for the Console Todo Application. The following artifacts were created:

1. Implementation plan at `specs/001-console-todo-app/plan.md`
2. Research document at `specs/001-console-todo-app/research.md`
3. Data model at `specs/001-console-todo-app/data-model.md`
4. Quickstart guide at `specs/001-console-todo-app/quickstart.md`
5. API contracts at `specs/001-console-todo-app/contracts/api-contracts.md`
6. Updated agent context in `.specify/memory/constitution.md`

The plan includes:
- Technical context with Python 3.13 and in-memory storage
- Constitution check ensuring all principles are followed
- Detailed project structure with source code organization
- Phase 1 design steps for data model and service layer
- Phase 2 error handling implementation plan with explicit error-handling stages
- All required validation checkpoints and spec references

The implementation plan explicitly addresses error handling requirements including input validation, exception-safe logic, and graceful CLI recovery as requested.

## Outcome

- ✅ Impact: Complete implementation plan created with explicit error-handling stages
- 🧪 Tests: none
- 📁 Files: specs/001-console-todo-app/plan.md, research.md, data-model.md, quickstart.md, contracts/api-contracts.md
- 🔁 Next prompts: Ready for /sp.tasks to generate development tasks
- 🧠 Reflection: The plan comprehensively covers all requirements with focus on error handling and validation.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):