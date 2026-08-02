# P2-L5: Discriminated Unions & Exhaustiveness

## Concept

A discriminated union is a union of object types that all share one property holding a distinct literal type. That property is the **discriminant**, and it is what lets the compiler tell the members apart.

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number }
  | { kind: "line"; length: number };
```

Checking `shape.kind === "circle"` narrows to exactly that member, so `shape.radius` becomes available. This is P1-L4 narrowing, but *designed for* rather than discovered — the discriminant makes narrowing reliable instead of incidental.

Why this beats a single optional-heavy shape: `{ kind: string; radius?: number; width?: number }` permits nonsense (a circle with a width, a shape with nothing) and forces a narrowing check at every field. The union permits only valid combinations, which is the whole point — **make illegal states unrepresentable**.

**Exhaustiveness checking** is the payoff. In a `switch` over the discriminant, once every case is handled the remaining type in `default` is `never`. Assigning to a `never`-typed variable is an error unless the value genuinely is `never`:

```ts
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rect":   return shape.width * shape.height;
    case "line":   return 0;
    default: {
      const exhaustive: never = shape;
      throw new Error(`Unhandled: ${JSON.stringify(exhaustive)}`);
    }
  }
}
```

Add a fourth member to `Shape` and this function stops compiling — the compiler tells you exactly which switch needs updating. That is the single most valuable property in this lesson: adding a state becomes a compile error at every place that must change, instead of a run-time surprise.

`switch` is not required; an if/else chain works the same way. The `never` assignment is what does the work.

## Analogy

A discriminated union is a form where the first question determines which section you fill in. Tick "circle" and you get one field: radius. Tick "rectangle" and you get two. There is no version of the form where you supply a radius *and* a width — the form's structure forbids it.

The exhaustiveness check is the clerk at the desk who refuses to accept the stack of forms if a new tick-box was added upstream and nobody wrote a handler for it. Annoying at the moment it happens; the reason nothing gets silently dropped.

## Workshop

**File:** `discriminated-unions.ts`

**Problem:** Model a request lifecycle and a small event stream, then prove that adding a state breaks compilation in exactly the right places.

Starter:

```ts
// 1. RequestState discriminated union on `status`:
//      idle
//      loading   (startedAt: number)
//      success   (data: string, durationMs: number)
//      failure   (error: string, retryable: boolean)

// 2. render(state): string  — no casts, no optional chaining.
//      idle    -> "Ready"
//      loading -> "Loading…"
//      success -> the data
//      failure -> "Failed: <error>" plus " (retryable)" when retryable
//    Include an exhaustiveness check in the default branch.

// 3. Event union discriminated on `type`:
//      click  (x: number, y: number)
//      keypress (key: string)
//      scroll (deltaY: number)

// 4. handle(event): string — an if/else chain, not a switch.
//    Include an exhaustiveness check at the end.

// 5. canRetry(state): boolean — true only for a retryable failure.
//    Use narrowing, not optional chaining.

// 6. This models the same data badly. Write a comment naming two
//    invalid values it permits that RequestState forbids.
type BadState = {
  status: string;
  data?: string;
  error?: string;
  retryable?: boolean;
};

// Proofs
console.log(render({ status: "idle" }));
console.log(render({ status: "success", data: "payload", durationMs: 12 }));
console.log(render({ status: "failure", error: "timeout", retryable: true }));
console.log(handle({ type: "click", x: 1, y: 2 }));

// These must be errors. Keep both, with @ts-expect-error.
render({ status: "success" });
render({ status: "loading", data: "wrong field" });
```

**Requirements:**

1. Both functions have an exhaustiveness check using `const _: never = value`.
2. No `as`, no `!`, no `?.` anywhere in the file.
3. After everything compiles, add a fifth `RequestState` member `{ status: "cancelled"; reason: string }` and run the check. Record the error and which function it points at, then handle the case.
4. The `BadState` comment names two concrete invalid values.
5. `canRetry` narrows on `status` first, then reads `retryable`.

## Acceptance Criteria

- `npx tsc --noEmit discriminated-unions.ts` produces no output.
- Temporarily deleting one `case` from `render` produces `TS2322` on the `never` assignment. Have the learner do this and confirm — it is the proof the check works.
- The `cancelled` state is handled and the recorded error is documented in a comment.
- `handle` uses if/else, demonstrating the check is not switch-specific.

## Compiler Checks

Expected:

- `TS2345: Argument of type '{ status: "success"; }' is not assignable to parameter of type 'RequestState'.` with the follow-on `Type '{ status: "success"; }' is missing the following properties from type '{ status: "success"; data: string; durationMs: number; }': data, durationMs`. Note it resolves the discriminant first and then reports against *that member alone* rather than the whole union — the discriminant is doing real work even in the error message.
- `TS2353: Object literal may only specify known properties, and 'data' does not exist in type '{ status: "loading"; startedAt: number; }'.` — the loading-with-data object, again reported against the single matched member.
- `TS2339: Property 'data' does not exist on type 'RequestState'.` — if `render` reads `data` before narrowing.
- The exhaustiveness failure: `TS2322: Type '{ status: "failure"; error: string; retryable: boolean; }' is not assignable to type 'never'.` The message names the **unhandled member itself**, not the union — which is exactly why this pattern is so useful. Add the `cancelled` state and the same error reappears naming `cancelled`.
- `TS7006` on unannotated parameters.

## Common Mistakes

- Discriminating on a `string`-typed field instead of literals. `status: string` cannot narrow — the discriminant must be a literal type in every member.
- Omitting the exhaustiveness check and relying on a `default: return ""`. It compiles forever and silently swallows new states. This is the mistake the lesson is built to prevent.
- Writing `default: throw new Error()` without the `never` assignment. It fails at run time instead of compile time.
- Using a boolean discriminant with more than two states. Two is fine (`ok: true | false`); beyond that use string literals.
- Reaching for `?.` to dodge a narrowing error. It compiles and hides the modelling problem.
- Declaring the union members as separate interfaces and forgetting to include the discriminant in one of them — narrowing then silently degrades.

## Everyday vs Type-Fluency Note

**Everyday:** This is the highest-value pattern in the entire course. Reach for a discriminated union any time you have a "state" or "kind" or "type" field: API responses, reducer actions, form states, parse results. Pair it with the `Result<T, E>` type from P2-L2 and most error handling becomes compiler-checked.

**Type-fluency:** Narrowing on a discriminant works because TypeScript computes a per-member literal type for the shared key and matches against it. This only fires when the key's type is a *unit* type in every member. Understanding that explains the failures — a `status: string` member poisons narrowing for the whole union. The `never` trick works because `never` is the empty type and the bottom of the assignability lattice: nothing is assignable to it except `never` itself, so a non-empty residual type is automatically an error.

## Bridge

You can model closed sets of states exhaustively. Next lesson: what to do at the edges where data arrives untyped — `unknown` versus `any` versus `never`, and writing type guards that turn unverified input into verified types.
