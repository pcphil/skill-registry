# P1-L7: Phase 1 Project — Typed Inventory Module

## Overview

**File:** `p1-project.ts`

Before starting, save to memory that the user has reached the Phase 1 project. After completing, save progress as "Phase 1 complete."

This is a single module built in three parts, not three throwaway exercises. Each part builds on the previous one and the whole file must compile clean under `npx tsc --noEmit --strict p1-project.ts` at every checkpoint.

Present one part at a time. Wait for a clean compile before moving to the next. Every Phase 1 concept appears: literal unions, interfaces, tuples, `readonly`, optional properties, narrowing, and functions with optional and rest parameters.

Hard constraint for the whole project: **no `any`, no `as`, no `!`, no `@ts-ignore`**. If the learner reaches for one, that is the signal to stop and narrow instead.

---

### Part 1: The Shapes

Define, in this order:

- `Category` — a literal union: `"tool" | "material" | "consumable"`.
- `Item` — an interface with `readonly sku: string`, `name: string`, `category: Category`, `quantity: number`, `unitPrice: number`, and optional `reorderLevel: number`.
- `Warehouse` — an interface with `name: string` and `items: Item[]`.
- `StockLevel` — a tuple `[sku: string, quantity: number]`.

Then create one `Warehouse` populated with at least four items spanning all three categories, at least one with `reorderLevel` and at least one without.

**Checkpoint:** clean compile, and an attempt to reassign `sku` on any item produces `TS2540`. Have them try it, confirm the error, then remove the line.

---

### Part 2: The Queries

Write four functions. Annotate parameters; let return types infer.

1. `totalValue(warehouse)` — sum of `quantity * unitPrice` across all items.
2. `byCategory(warehouse, category)` — the items in one category.
3. `needsReorder(warehouse)` — items whose `quantity` is at or below their `reorderLevel`. Items with no `reorderLevel` never need reordering.
4. `stockLevels(warehouse)` — an array of `StockLevel` tuples.

`needsReorder` is the real exercise. `reorderLevel` is `number | undefined`, so the comparison does not type-check until narrowed. Truthiness narrowing is wrong here — a `reorderLevel` of `0` is meaningful and `if (item.reorderLevel)` silently discards it. Require an explicit `!== undefined` check and ask them to say why.

**Checkpoint:** clean compile, and `needsReorder` behaves correctly for an item with `reorderLevel: 0` and `quantity: 0`. Have them add that case and run it with `npx tsx p1-project.ts`.

---

### Part 3: The Report

Write `report(warehouse, ...categories)`:

- With no categories, cover every item.
- With one or more, cover only those categories.
- Return a single multi-line string: one line per item as `<sku>  <name>  x<quantity>  $<total>`, then a final total line.
- Prices formatted to two decimals.

Then write `summarize(warehouse, label?)` returning `"<label>: N items, $X"`, defaulting the label to the warehouse name.

**Checkpoint:** clean compile; `report(w)` and `report(w, "tool", "consumable")` both work; `summarize(w)` uses the warehouse name.

---

## Acceptance Criteria

- `npx tsc --noEmit --strict p1-project.ts` produces no output.
- Zero occurrences of `any`, `as`, `!` (non-null assertion), or a suppression comment.
- `Category` is a literal union; `Item` and `Warehouse` are interfaces; `StockLevel` is a labelled tuple.
- `needsReorder` uses `!== undefined`, not truthiness, and the learner can explain why.
- `report` accepts zero or more categories via a rest parameter.
- `npx tsx p1-project.ts` runs and prints a sensible report.

## Compiler Checks

Diagnostics they should expect to hit and fix along the way:

- `TS18048: 'item.reorderLevel' is possibly 'undefined'.` — in `needsReorder` before narrowing. This is the central diagnostic of the project.
- `TS2540: Cannot assign to 'sku' because it is a read-only property.` — engineered in Part 1.
- `TS2345: Argument of type '"widget"' is not assignable to parameter of type 'Category'.` — if they pass a bad category to `byCategory`.
- `TS2322: Type 'string[]' is not assignable to type 'StockLevel[]'.` — if `stockLevels` returns the wrong shape.
- `TS7006` on any unannotated parameter.

## Review Focus

When reviewing, read the file and run the compiler, then check in this order:

1. Clean compile with no suppressions.
2. `needsReorder` narrowing — the `0` case is the thing most learners get wrong, and it passes the compiler either way.
3. Whether return types were left to infer. Over-annotation here is worth a note, not a rejection.
4. Whether `Category` was modelled as a union rather than `string` or an `enum`.

## Everyday vs Type-Fluency Note

**Everyday:** This is roughly the shape of real application code — interfaces for entities, literal unions for closed sets, narrowing at every optional field. If they can write this without `any`, they can write production TypeScript.

**Type-fluency:** Notice how much repetition the query functions contain: four functions that differ only in what they extract. That repetition is exactly what generics remove, and the tuple/interface duplication is what mapped types remove. Point this out — the discomfort is the motivation for Phase 2.

## Bridge

Phase 1 complete. You can describe any concrete shape and prove which one you hold. But every function you wrote works on exactly one type. Phase 2 opens with generics — writing one function that works across types without losing the type information.
