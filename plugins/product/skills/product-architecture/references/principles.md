---
title: Product Principles
---

# Product Principles

Product invariants are structural rules that must not be violated. They represent fundamental decisions about how the product works and guide future feature development.

## Example Principle: Consistent Concept Usage

User-facing concepts should have a single, consistent meaning throughout the product.

**Why it matters**: When the same word means different things in different parts of the product, users build incorrect mental models and make mistakes. Features become harder to explain and document.

**Examples**:
- ✓ Good: "Project" always means a container for work, consistently across all features
- ✗ Bad: "Project" means a container in one area, but a single work item in another area

## Example Principle: Feature Discoverability Over Configuration

Features should be discoverable through natural product flow rather than hidden behind extensive configuration.

**Why it matters**: Users can't benefit from capabilities they don't know exist. Configuration sprawl makes the product feel complex and intimidating.

**Examples**:
- ✓ Good: Collaboration features appear contextually when multiple users are present
- ✗ Bad: Users must navigate to Settings > Advanced > Collaboration to enable team features

---

## Your Principles

Document your product invariants below. Each principle should explain:
1. What the rule is
2. Why it matters
3. Examples of following and violating it
