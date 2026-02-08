---
id: 6
title: Create Tasks
stage: tasks
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: execution-plan
branch: 002-execution-plan
user: claude-code
command: /sp.tasks
labels: [execution_plan, tasks, python, cli]
links:
  spec: specs/001-phase-1/spec.md
  plan: specs/002-execution-plan/plan.md
  tasks: specs/002-execution-plan/tasks.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-execution-plan/tasks.md
 - specs/002-execution-plan/plan.md
 - specs/001-phase-1/spec.md
 - specs/002-execution-plan/data-model.md
 - specs/002-execution-plan/contracts/api-contracts.md
tests:
 - none
---

## Prompt

```text
You are a task-decomposition engine for Claude Code.

Context:
- Phase-1 execution plan is approved
- Specs are finalized
- No implementation exists yet

Objective:
Break Phase 1 into small, atomic implementation tasks.

Task Requirements:
1. Each task must:
   - Reference specific Phase-1 spec files
   - Be independently implementable
   - Be testable via console output
2. Tasks should cover:
   - Task model creation
   - Add/view/update/delete logic
   - CLI menu handling
   - Error handling for invalid IDs
3. Each task must define:
   - Inputs (spec references)
   - Outputs (files changed)
   - Validation steps

Rules:
- NO code
- Prefer many small tasks over large ones

Output:
An ordered task list ready for /sp.implement.
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: You are a task-decomposition engine for Claude Code.

Context:
- Phase-1 execution plan is approved
- Specs are finalized
- No implementation exists yet

Objective:
Break Phase 1 into small, atomic implementation tasks.

Task Requirements:
1. Each task must:
   - Reference specific Phase-1 spec files
   - Be independently implementable
   - Be testable via console output
2. Tasks should cover:
   - Task model creation
   - Add/view/update/delete logic
   - CLI menu handling
   - Error handling for invalid IDs
3. Each task must define:
   - Inputs (spec references)
   - Outputs (files changed)
   - Validation steps

Rules:
- NO code
- Prefer many small tasks over large ones

Output:
An ordered task list ready for /sp.implement.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

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

I have successfully created a comprehensive task decomposition for the Phase 1 Execution Plan for Python Console Application. The following artifacts were created:

1. Task list at `specs/002-execution-plan/tasks.md`
2. The task list includes 80 individual tasks organized across 7 phases:
   - Phase 1: Setup (T001-T007)
   - Phase 2: Foundational (T008-T013)
   - Phase 3: User Story 2 - Task Data Model (T014-T020)
   - Phase 4: User Story 3 - CRUD Operations (T021-T035)
   - Phase 5: User Story 4 - CLI Interface (T036-T050)
   - Phase 6: User Story 5 - Error Handling (T051-T070)
   - Phase 7: Polish & Cross-Cutting (T071-T080)

Each task follows the required format with:
- Sequential task IDs (T001, T002, etc.)
- Parallelizability markers ([P]) where appropriate
- User story labels ([US2], [US3], etc.) for story-specific tasks
- Clear descriptions with file paths
- Proper checkboxes for tracking

The tasks cover all requirements from the user input:
- Task model creation (in User Story 2 phase)
- Add/view/update/delete logic (in User Story 3 phase)
- CLI menu handling (in User Story 4 phase)
- Error handling for invalid IDs (in User Story 5 phase)

All tasks reference the appropriate spec files and are designed to be independently implementable and testable.

## Outcome

- ✅ Impact: Complete task decomposition created with 80 atomic tasks
- 🧪 Tests: none
- 📁 Files: specs/002-execution-plan/tasks.md
- 🔁 Next prompts: Ready for /sp.implement to execute tasks
- 🧠 Reflection: The tasks are organized by user story and follow the checklist format precisely.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):