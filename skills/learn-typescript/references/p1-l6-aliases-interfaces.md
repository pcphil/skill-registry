# P1-L6: Type Aliases vs Interfaces

## Concept

Both name a shape. For plain object types they are nearly interchangeable, and the compiler treats them identically for assignability — structural typing does not care which keyword you used.

The real differences:

| Capability | `type` | `interface` |
|-----------|--------|-------------|
| Object shapes | yes | yes |
| Unions, intersections, primitives, tuples | yes | no |
| Mapped and conditional types | yes | no |
| `extends` another shape | via `&` | via `extends` |
| Declaration merging | no | yes |
| Reopened by a consumer to augment | no | yes |
| Error messages | often expanded inline | usually shows the name |

Two of these matter in practice.

**Declaration merging**: two `interface User` declarations in the same scope merge into one. Two `type User` declarations are `TS2300: Duplicate identifier`. Merging is what lets you augment third-party types (`declare module "express" { interface Request { user?: User } }`). It is also a footgun — a typo'd interface name silently merges instead of erroring.

**Expressiveness**: only `type` can alias a union, a primitive, a tuple, or a computed type. `type Status = "on" | "off"` has no interface equivalent.

**Extension semantics differ subtly.** `interface B extends A` checks compatibility at declaration time and errors on a conflicting property. `type B = A & { ... }` produces an intersection — a conflicting property becomes `never` rather than an error, which fails later and further away.

The practical rule: `interface` for object shapes that might be extended or augmented, especially public API; `type` for everything else. Consistency inside a codebase matters more than the choice.

## Analogy

`interface` is a shared bulletin board with the shape's name at the top — anyone can walk up and pin another note to it, and the shape everyone reads is the sum of all notes. That is declaration merging: useful when a plugin needs to add a field to a framework's type, dangerous when you pin your note to the wrong board and nobody tells you.

`type` is a printed label on a jar. It says exactly one thing, it says it once, and printing a second label with the same name is an error, not a merge. In exchange, the label can describe things a bulletin board cannot — "either sugar or salt", "exactly three olives."

## Workshop

**File:** `aliases-interfaces.ts`

**Problem:** Model a small plugin system, using each construct where it is actually the right tool, and demonstrate declaration merging.

Starter:

```ts
// 1. Declare an interface `Plugin` with:
//    name: string, version: string, enabled: boolean

// 2. Extend it with an interface `LoggingPlugin` that adds
//    log(message: string): void

// 3. Declare a type alias `PluginState` as the union
//    "installed" | "active" | "failed".
//    Try writing this as an interface first and record the error you get.

// 4. Declare a type alias `Registry` mapping plugin names to Plugin.
//    Use an index signature.

// 5. Demonstrate declaration merging: declare `interface Plugin` a second
//    time, adding `state: PluginState`. Then create a Plugin object —
//    it must now require all four properties.

// 6. Write `describe(plugin: Plugin): string` returning
//    "<name>@<version> [<state>]".

// 7. Add this and explain in a comment why it is an error and which
//    of the two constructs would have allowed it:
type Plugin2 = { a: string };
type Plugin2 = { b: string };
```

**Requirements:**

1. Steps 1–6 compile clean; step 7 is marked with `@ts-expect-error` and has an explanation comment.
2. A `Plugin` object literal missing `state` produces an error — proving the merge took effect.
3. `Registry` uses an index signature and is populated with at least two plugins.
4. Add a one-line comment on `PluginState` recording the error from writing it as an interface.

## Acceptance Criteria

- `npx tsc --noEmit aliases-interfaces.ts` produces no output.
- `Plugin` is declared twice and both declarations contribute properties.
- `PluginState` is a `type`, with the interface attempt documented, not left in the file.
- `describe` reads `state`, which only exists because of the merge.

## Compiler Checks

Expected:

- `TS2300: Duplicate identifier 'Plugin2'.` — reported on **both** declarations. This is the error the lesson is engineering, so it needs `@ts-expect-error` on both lines.
- `TS2739: Type '{ name: string; version: string; enabled: boolean; }' is missing the following properties from type 'Plugin': state` — after the merge, proving it happened.
- `TS1005: '{' expected.` — from attempting `interface PluginState = "installed" | "active"`. It is a *parse* error, not a type error: the grammar has no place for `=` in an interface, so the compiler fails before it ever considers the union. Worth naming, because a syntax error here is the clearest possible evidence that interfaces cannot alias a union. Note that a parse error also halts checking for the rest of the file, so have the learner remove the line before reading other diagnostics.
- `TS2411: Property 'name' of type 'string' is not assignable to 'string' index type 'number'.` — if a declared property conflicts with the index signature in `Registry`.

## Common Mistakes

- Believing `interface` is faster or "more correct". Structurally they are the same; pick by capability.
- Using `type` for a shape a consumer will need to augment, then discovering augmentation is impossible.
- Accidental merging: a second `interface Props` in the same file quietly merges instead of erroring, and the resulting type demands properties nobody intended.
- Expecting `type B = A & { x: string }` to error when `A` already has `x: number`. It does not — `x` becomes `never`, and the failure surfaces at the assignment site instead.
- Adding an index signature that conflicts with a named property: every named property must be assignable to the index signature's type.

## Everyday vs Type-Fluency Note

**Everyday:** Use `interface` for object shapes, `type` for unions and anything computed. Do not spend meeting time on this — the compiler does not care, and consistency beats the argument.

**Type-fluency:** The differences that actually bite are declaration merging (essential for module augmentation, hazardous by accident), the `extends`-vs-`&` conflict semantics, and how each renders in error messages — interfaces keep their name in diagnostics while aliased intersections often expand into a wall of structure. Aliases also participate in mapped and conditional types, which is where Phase 3 lives.

## Bridge

You have every tool for describing concrete shapes. Next: the Phase 1 project — put setup, literals, collections, narrowing, functions, and interfaces together into one small typed module with no `any` in sight.
