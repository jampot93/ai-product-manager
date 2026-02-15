---
name: write-product-spec
description: This skill should be used when creating, iterating, or finalising product specs within a project. It supports the full spec lifecycle from initial draft through prototyping iteration to spec readiness. A product spec is a product-focused document for stakeholder alignment - it never contains implementation detail.
---

# Write Product Spec

This skill guides the creation and iteration of product specs. A product spec desceribes the user experience and product decisions for stakeholder alignment. It never contains technical implementation detail. 

---

## Detecting Mode

When invoked, determine which mode to enter:
1. Check if the user has specified a project. If not, ask which project this is for.
2. Check for expising product spec files in the project directory (files matchin `*spec*.md` or `*-spec.md` in the project root or a `specs/` subdirectory).
   - **No existing spec found** - enter New Spec mode (Phase 1)
   - **Existing spec found** - enter Iteration mode (Phase 2). Read the existing spec to orient, then ask what has changed - new prototype findings, updated thinking, resolved qustions - before making edits.

---

## Phase 1: Input Gathering

Gather enough context to produce a meaningful first draft. Be conversational - ask, listen, follow up where things are vague or contradictory. Do not present a checklist.

Information to gather:
- **Problem definition** - point to the existing problem statement or ask for a description
- **User stories** - which stories does this product spec cover? These may be references to stories tracked elsewhere
- **Existing knowledge** - any prototype findings, spike outcomes, or constraints already known
- **Prototypes** - links to any prototypes already built
- **Optional sections** - determine whether Risks, Migration/Transition, Non-functional Requirements, or Validation Findings setions are relevant

When sufficient context has been gathered, state this and move to Phase 2.

---

## Phase 2: Drafting and Iteration

### First Draft

Read the spec template from [references/template.md](references/template.md). Generate the spec as a markdown file at `projects/{project-name}/specs/{project-name}-spec.md`, creating the `specs/` directory if needed.

In the first draft:
- Flag where evidence is thin
- Label assumptions explicitly
- Populate open questions with items that could be answered by prototyping

### Iteration Loop

The PM iterates on the spec over time. Between conversations they may prototype, test with users, or gather new information. When they return:

1. Read the current spec file to re-orient
2. Ask what has changed or what new information exists
3. Update the spec in place — never create new versions
4. When updating, also remove or revise what is no longer accurate. The spec should reflect current thinking, not accumulated thinking.

Three roles are available, directed by the PM:
- **writer** — update sections based on new information
- **challenger** — poke holes, question scope, flag weak evidence. Example challenges:
  - "These success metrics are outputs, not outcomes — how will we know this solved the problem?"
  - "User journey 3 implies a capability that contradicts the out-of-scope boundary"
  - "This assumption has not been validated — should it be an open question?"
  - "What would a sceptical stakeholder push back on at the review?"
- **editor** — check coherence across the whole spec after changes

If no role is directed, default to writer then offer to challenge.

---

## Phase 3: Finalise

When the PM indicates the spec is ready for review, perform a final coherence check:

- Verify open questions are resolved or acknowledged as accepted risks
- Verify user journeys are internally consistent and business rules within them do not contradict each other
- Verify nothing contradicts the out-of-scope boundaries
- Verify success metrics are tied to user stories
- Flag anything still marked as thin or assumed that should have been resolved

Make final edits, then flag any remaining concerns. Never decide the spec is ready — that is always the PM's call.

## Writing Constraints

These constraints apply at all times when writing or editing a spec:

- **Plain language only.** No jargon or technical terms unless they are domain terms stakeholders use.
- **No Implementation detail.** Describe how things work from the user's perspective only. Never describe how to build it.
- **Evidence over assertion.** Every claim about users or the market must cite a source or be explicitly labelled as an assumption.
- **Update in place.** The spec is a living document. When updating, revise and remove — never just append.
- **Flag readiness, never decide it.** Indicate when the spec appears ready for review, but the PM always makes that call.

---

## Section Length Guidance

- **Context** = a one-liner for the feature, then a short paragraph on why. If longer, it is re-stating the problem definition.
- **Main stories** = references only, preferably short.
- **User journeys** = as long as needed, but each journey should be scoped. If a single journey exceeds a page, consider splitting it. Business rules should be inline alongside the relevant flow, not separated out.
- **Out of scope** = bulleted list with brief rationale.
- **Dependencies** = bulleted list, brief.
- **Success metrics** = no more than five. More than five signals insufficient prioritisation. The Events to Track subsection should map each event to a metric above it.
- **Open questions** = as many as needed during iteration, should shrink over time.
- **Key assumptions** = bulleted list, each one falsifiable.

---



