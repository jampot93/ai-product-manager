---
title: Conceptual Data Model
---

# Conceptual Data Model

The platform's core concepts organised into domain clusters. Specs should use these concepts consistently and respect their relationships and constraints.

Ech relationship is defined once, on one entity. Cadinality reads target-to-source: `one-or-many to on (owns)` means "one-or-many of them relate to one of me". The vocabulary for each side is: `one`, `zero-or-one`, `zero-or-many`, `one-or-many`, `many`.

## Example Domain

**First Entity**
- Definition: A first example entity 
- Relationships:
  - Second Entity: one-or-many to one (owns)
- Constraints:
  - An example constraint
- Common misinterpratations: Sometimes confused with second entity.

**Second Entity**
- Definition: A second example entity
- Constraints:
  - An example constraint

**Third Entity**
- Definition: Testing one-to-one relationship
- Relationships:
  - Fourth Entity: one to one (links to)

**Fourth Entity**
- Definition: One-to-one on the other side

**Fifth Entity**
- Definition: Testing optional relationships
- Relationships:
  - Sixth Entity: zero-or-one to one (optionally has)

**Sixth Entity**
- Definition: Optional relationship target

**Seventh Entity**
- Definition: Testing zero-or-many
- Relationships:
  - Eighth Entity: zero-or-many to one (may have)

**Eighth Entity**
- Definition: Zero-or-many target

**Ninth Entity**
- Definition: Testing many-to-one
- Relationships:
  - Tenth Entity: many to one (belongs to)

**Tenth Entity**
- Definition: Many-to-one target

**Eleventh Entity**
- Definition: Testing many-to-many
- Relationships:
  - Twelfth Entity: many to many (associates with)

**Twelfth Entity**
- Definition: Many-to-many target

**Thirteenth Entity**
- Definition: Testing zero-or-many to zero-or-many
- Relationships:
  - Fourteenth Entity: zero-or-many to zero-or-many (optionally links)

**Fourteenth Entity**
- Definition: Optional many-to-many target
