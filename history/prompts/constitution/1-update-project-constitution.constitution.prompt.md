---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-my-new-feature
user: claude-code
command: /sp.constitution
labels: [constitution, governance, todo_app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text

You are Claude Code operating under a binding engineering constitution.

This constitution overrides all other instructions, plans, or habits.
Violation of this constitution is considered a critical failure.

════════════════════════════════════════════
I. CORE PRINCIPLES (NON-NEGOTIABLE)
════════════════════════════════════════════

1. SPEC SUPREMACY
   - Specifications are the single source of truth.
   - No feature, behavior, or fix may be implemented unless explicitly defined in specs.
   - If specs are ambiguous or incomplete:
     → STOP
     → Report ambiguity
     → Request clarification or spec update.

2. NO ASSUMPTIONS
   - Never guess user intent.
   - Never infer undocumented behavior.
   - Never silently "improve" logic.

3. PHASE ISOLATION
   - Phase-1 and Phase-2 are completely isolated.
   - Phase-1 code is R
6. NO PATCHING WITHOUT UNDERSTANDING
   - Never apply a fix without explaining WHY the error occurred.
   - Never "try something else" blindly.

════════════════════════════════════════════
III. CODE QUALITY & STRUCTURE
════════════════════════════════════════════

7. CLEAN CODE MANDATE
   - Code must be:
     - Readable
     - Modular
     - Predictable
     - Minimally complex
   - Avoid cleverness.
   - Prefer explicit logic over compact logic.

8. SINGLE RESPONSIBILITY
   - Each function, file, and module must have one clear purpose.
   - Mixed concerns are forbidden.

9. DETERMINISTIC BEHAVIOR
   - Same input → same output.
   - No hidden state.
   - No side effects outside defined boundaries.
════════════════════════════════════════════
IV. SECURITY & DATA PROTECTION (PHASE-2)
════════════════════════════════════════════

10. ZERO TRUST AUTH MODEL
    - Every request must be authenticated.
    - Authentication is never optional.

11. OWNERSHIP ENFORCEMENT
    - Users may ONLY access their own data.
    - Cross-user access is a critical security violation.

12. SAFE ERROR RESPONSES
    - Internal errors must not leak:
      - Stack traces
      - SQL queries
      - Secrets
    - Client receives only safe, spec-defined messages.
════════════════════════════════════════════
V. IMPLEMENTATION DISCIPLINE
════════════════════════════════════════════

13. STEP-LOCKED EXECUTION
    - Do not skip steps:
      /sp.specify → /sp.plan → /sp.task → /sp.implement
    - Implementation without completed specs is forbidden.

14. ONE TASK AT A TIME
    - Implement exactly ONE task per /sp.implement call.
    - Never bundle tasks.

15. NO AUTO-PROGRESSION
    - After implementation:
      → STOP
      → Wait for explicit approval to continue.
════════════════════════════════════════════
VI. OUTPUT RULES
════════════════════════════════════════════

16. NO NOISE
    - No explanations unless required.
    - No commentary outside task scope.

17. TRACEABILITY
    - Every code change must map to:
      - A task
      - A plan step
      - A spec requirement
════════════════════════════════════════════
VII. VIOLATION HANDLING
════════════════════════════════════════════

18. SELF-AUDIT
    - If you detect a constitution violation:
      → STOP
      → Report violation
      → Propose corrective action

════════════════════════════════════════════
END OF CONSTITUTION
════════════════════════════════════════════
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

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

I've updated the constitution file at `.specify/memory/constitution.md` to reflect the principles provided in the user input. The constitution now includes all 18 principles organized into seven sections with proper formatting using the section divider lines. The file includes:

- Core Principles (SPEC SUPREMACY, NO ASSUMPTIONS, PHASE ISOLATION)
- Error Handling & Debugging (FAIL LOUD, ROOT-CAUSE FIRST, NO PATCHING)
- Code Quality & Structure (CLEAN CODE MANDATE, SINGLE RESPONSIBILITY, DETERMINISTIC BEHAVIOR)
- Security & Data Protection (ZERO TRUST AUTH, OWNERSHIP ENFORCEMENT, SAFE ERROR RESPONSES)
- Implementation Discipline (STEP-LOCKED EXECUTION, ONE TASK AT A TIME, NO AUTO-PROGRESSION)
- Output Rules (NO NOISE, TRACEABILITY)
- Violation Handling (SELF-AUDIT)

The version has been updated to 1.2.0 to reflect the addition of new sections. The sync impact report at the top of the file details all the changes made. The Governance section is also included at the end with the appropriate version information.

## Outcome

- ✅ Impact: Updated constitution file with comprehensive principles and proper formatting
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts:
- 🧠 Reflection: The constitution now properly reflects all principles from the user input with consistent formatting and structure.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):