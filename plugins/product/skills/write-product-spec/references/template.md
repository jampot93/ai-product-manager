# Product Spec Template

Use this teplate when generting a new product spec. All fixed section are required. Optional sections should be included only when the PM confirms they are relevant.

## Fixed Sections

```markdown
# {Product Spec Title}

**Last Updated:** {date}
**Prototypes:** {links to prototypes}

## Context

A one line description of the feature being specified, followed by a brief explanation of why we are doing this - grounded in the project's problem statement or strategic context. Enough for a reader to understand what this spec covers and why it matters without having attended every prior conversation.

## User Stories

References to the user stories this spec covers. Defines the slice of value, not the detail of each story.

## User journeys

Step-by-step flows showing how the experience works from the user's perspective. Includes happy paths and error / edge case paths. References prototypes where relevant. Where business rules govern behaviour within a jorouney (constraints, conditions, or product logic), include them inline alongside the relevant flow.

## Out of Scope

What this spec deliberately does not cover, and why. Bulleted list with brief rationale for each item.

## Dependencies

What this spec needs from other specs in the project or external parties. Includes anything that could block or requires coordination.

## Success Metrics

How we will know this worked. Outcome-based, tied back to user stories. No more than five - if there are more, prioritisation is needed.

### Events to Track

Key user actions and system events that need to be instrumented to measure the success metrics above. Each event should map to at least one success metric.

## Open Questions

What is unresolevd. Drives prototyping activity during iteration. Should be empty or contian only acknowledged risks by the time the spec goes to review.

## Key Assumptions

What we believe to be true that, if wrong, would materially change this spec. Each assumption should be falsifiable.
```

## Optional Sections

Add after Key Assumptions when relevant:

- **Risks** - What could go wrong even if assumptions hold and questions are answered.
- **Migration / Transition** - How existing users experience the change from current to new.
- **Non-functional Requirements** - User-facing quality expectations such as performance targets, accessibility standards, or availability need. Describe what the user should experience, not how to build it.
- **Validation Findings** - What was learned from prototyping, UX testing, customer interviews, advisory panels or competitive analysis that shaped the spec. Organised by source so readers can assess the strength of the evidence.
