# P2-L6: unknown vs any vs never; Type Guards & Predicates

## Concept

Three types that look similar and behave as opposites.

| Type | Means | Assignable **to** it | Assignable **from** it | Effect |
|------|-------|---------------------|------------------------|--------|
| `any` | "stop checking" | everything | everything | disables the type system |
| `unknown` | "not yet known" | everything | nothing (until narrowed) | forces you to prove |
| `never` | "cannot happen" | nothing | everything | marks unreachable code |

`any` and `unknown` both accept every value. The difference is what you may then *do*. With `any`, everything — including `x.foo.bar()` on a number, which crashes at run time with no warning. With `unknown`, nothing until you narrow. `unknown` is the honest version of `any`, and it is almost always the right choice at a boundary.

`never` is the empty type: no value has it. It shows up as the return type of a function that always throws, as the residual in an exhaustiveness check (P2-L5), and as the result of an impossible intersection like `string & number`.

**Type predicates** are how you cross from `unknown` to a real type. A function returning `x is T` teaches the compiler's control-flow analysis a new narrowing rule:

```ts
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

Inside `if (isString(v))`, `v` is `string`. The predicate is a **promise, not a proof** — the compiler trusts your `return` expression without verifying that it actually establishes `T`. A wrong predicate is as dangerous as a cast, so the body must be genuinely exhaustive.

For object shapes, check every field you claim:

```ts
function isUser(value: unknown): value is { id: string; name: string } {
  return (
    typeof value === "object" && value !== null &&
    "id" in value && typeof value.id === "string" &&
    "name" in value && typeof value.name === "string"
  );
}
```

Two related forms: **assertion functions** (`asserts value is T`) narrow for the rest of the enclosing scope rather than inside a block, and require an explicit return type annotation. And under `strict`, a `catch` variable is `unknown` (via `useUnknownInCatchVariables`) — so error handling is now a narrowing problem, which is exactly right, because anything can be thrown.

## Analogy

`any` is a security guard who waves everyone through and stops filing reports. The queue moves fast right up until something goes badly wrong inside, and there is no record of how it got in.

`unknown` is a guard who lets everyone into the lobby but nobody past it without ID. Slower at the door, and nothing unverified reaches the building.

A type predicate is that guard's ID check. Note carefully: the building trusts the guard's word completely. If the guard glances at a library card and stamps "employee", the system has been defeated — and nobody upstairs will ever know. That is why the body of a predicate is the one place you must be pedantic.

`never` is a door bricked over. Not locked — bricked. If you find yourself standing behind it, the floor plan is wrong.

## Workshop

**File:** `type-guards.ts`

**Problem:** Parse untrusted JSON into a verified type without a single cast, and handle a thrown error safely.

Starter:

```ts
interface Config {
  host: string;
  port: number;
  tags: string[];
}

// 1. isString, isNumber, isStringArray — predicates over unknown.

// 2. isConfig(value: unknown): value is Config
//    Check every property and its type. Reuse the predicates above.

// 3. parseConfig(raw: string): Config
//    JSON.parse returns any — immediately widen it to unknown,
//    then validate. Throw a descriptive Error if invalid.
//    No casts anywhere.

// 4. toMessage(error: unknown): string
//    Handle: Error instance, string, object with a string `message`,
//    and anything else. Return a useful message for each.

// 5. assertIsConfig(value: unknown): asserts value is Config
//    Then show it in use: after calling it, the value is Config
//    for the rest of the function.

// 6. impossible(): never — a function that always throws.
//    Then explain in a comment why its return type is never and
//    not void.

// 7. This compiles but is a lie. Explain in a comment what it
//    permits at run time, then delete it.
function isConfigBad(value: unknown): value is Config {
  return typeof value === "object";
}

// Proofs
const good = parseConfig('{"host":"localhost","port":3000,"tags":["a"]}');
console.log(good.host.toUpperCase(), good.port.toFixed(0), good.tags.length);

try {
  parseConfig('{"host":"localhost","port":"3000","tags":[]}');
} catch (err) {
  console.log(toMessage(err));
}

// This must be an error. Keep it, with @ts-expect-error.
const raw: unknown = "hello";
raw.toUpperCase();
```

**Requirements:**

1. Zero `as`, zero `any`, zero `!` in the file. `JSON.parse`'s result is assigned to an `unknown`-typed variable immediately.
2. `isConfig` validates all three properties including array element types.
3. `toMessage` handles all four cases via narrowing, and the `catch` parameter stays `unknown`.
4. `assertIsConfig` has an explicit return type annotation and is demonstrated in a function body.
5. The `isConfigBad` explanation names at least one concrete value that passes it and then crashes — `null` is the obvious one.

## Acceptance Criteria

- `npx tsc --noEmit type-guards.ts` produces no output.
- `npx tsx type-guards.ts` prints the config fields, then a sensible error message for the bad input.
- Removing `value !== null` from `isConfig` still compiles — have the learner confirm this, because it is the lesson's most important point: predicates are unchecked.
- The engineered `raw.toUpperCase()` error is suppressed.

## Compiler Checks

Expected:

- `TS18046: 'raw' is of type 'unknown'.` — the engineered error. On older compilers this is `TS2571: Object is of type 'unknown'.`
- `TS18046: 'err' is of type 'unknown'.` — inside `catch` before narrowing, from `useUnknownInCatchVariables`.
- `TS2571`/`TS18046` on the `JSON.parse` result once assigned to `unknown` and used before validation.
- `TS2775: Assertions require every name in the call target to be declared with an explicit type annotation.` — if `assertIsConfig` is stored in a `const` without an annotation, or called via an unannotated alias. A common and confusing one.
- `TS2677: A type predicate's type must be assignable to its parameter's type.` — if the predicate claims a type unrelated to the parameter.
- `TS2322: Type '1' is not assignable to type 'never'.` — if the `never` function returns a value instead of always throwing. Nothing is assignable to `never`, so any `return` at all is an error; that is precisely what makes the annotation a guarantee.

Note what produces **no** diagnostic: a predicate whose body under-checks. `isConfigBad` compiles cleanly. Demonstrate this explicitly.

## Common Mistakes

- Typing a boundary as `any` because `unknown` "causes errors". The errors are the feature.
- Forgetting `value !== null`. `typeof null === "object"`, so every naive object check passes `null` and then crashes on property access.
- Writing a predicate that returns a boolean but claims a type it did not verify. The compiler will not help; only review will.
- Using `catch (err: any)` to skip narrowing. Keep it `unknown` and write `toMessage` once.
- Checking `"id" in value` and assuming the *type* of `value.id`. Presence and type are two separate checks.
- Annotating an assertion function's call site incorrectly, then fighting `TS2775` without reading it — the message is literal: the target needs an explicit type annotation.
- Typing an always-throwing function as `void`. `never` tells callers control does not return, which enables exhaustiveness and unreachability analysis.

## Everyday vs Type-Fluency Note

**Everyday:** One rule covers most of it — every value entering your program from outside (`JSON.parse`, `fetch`, `process.env`, form input, a message payload) is `unknown` until a guard proves otherwise. In production most teams delegate this to a schema library (zod, valibot) whose `parse` returns a properly typed value and throws otherwise; writing the guards by hand once is how you understand what those libraries are actually doing.

**Type-fluency:** Predicates and assertion functions extend control-flow analysis with user-defined rules, which makes them a deliberate soundness hole — the compiler defers to your claim without verification. Worth studying: how predicates interact with generics (`function isArrayOf<T>(v: unknown, g: (x: unknown) => x is T): v is T[]`), why assertion functions require the annotation (the narrowing effect must be visible in the declared type, not inferred from the body), and how `never` behaves as the bottom type in assignability and in union reduction — `string | never` collapses to `string`.

## Bridge

You can turn untrusted input into verified types. Next: the Phase 2 project — a fully typed event emitter that combines generics, `keyof`, mapped lookups, and discriminated payloads into one API where wrong event names and wrong payloads are both compile errors.
