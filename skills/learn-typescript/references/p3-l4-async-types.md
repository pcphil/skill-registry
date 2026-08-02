# P3-L4: Async Typing — Promise, Awaited, Typed Errors

## Concept

An `async` function always returns a `Promise`. If you annotate the return type, it must be `Promise<T>` — `TS1064` otherwise. `await` unwraps one layer, and `Awaited<T>` unwraps recursively.

```ts
async function load(): Promise<string> { return "data"; }   // returning a bare string is fine
type Loaded = Awaited<ReturnType<typeof load>>;             // string
```

That `Awaited<ReturnType<typeof fn>>` idiom is the one to keep — it derives the resolved type from any async function.

The important thing about this lesson is what TypeScript **cannot** do: **there is no typed `throws`.** Every function's error channel is untyped. `Promise<T>` says what a success looks like and says nothing at all about failure. Under `strict`, a `catch` variable is `unknown` — the compiler's honest admission that anything can be thrown, including a string, `null`, or a number.

So typed error handling means moving errors into the *value* channel:

```ts
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };
async function safeLoad(): Promise<Result<string, string>> { … }
```

Now the failure is a discriminated union the compiler forces you to handle (P2-L5). This is the single most useful async pattern in TypeScript.

Details that bite:

- **`Promise.all`** returns a tuple type when given a tuple, preserving per-element types: `Promise.all([p1, p2])` is `Promise<[A, B]>`. Use `as const` or a tuple literal to keep it — an array variable degrades to `Promise<(A|B)[]>`.
- **`Promise.allSettled`** returns `PromiseSettledResult<T>[]`, itself a discriminated union on `status`.
- **A floating promise is silent.** Calling an async function without `await` or `.catch()` type-checks fine and swallows rejections. Only the `no-floating-promises` lint rule catches this; the compiler does not.
- **`await` on a non-promise** is legal and returns the value. That means a forgotten `async` on a helper often produces no error at all.
- **`void` versus `Promise<void>`**: a `void`-returning callback slot accepts a `Promise<void>`-returning function, so `arr.forEach(async x => …)` compiles and does not wait. Use a `for…of` loop with `await`.

## Analogy

A `Promise<T>` is a coat-check ticket. It tells you what you'll get back — a coat — and when you present it you either receive the coat or an apology. The ticket is printed with the coat's description. It is **not** printed with the list of things that could go wrong, because there is no such list: the cloakroom could be on fire, closed, or staffed by someone who hands you a shoe.

That is the untyped error channel. `Result<T, E>` is asking the cloakroom to hand you a small box that contains *either* the coat or a written reason — now the failure has a shape you can read, and you cannot walk off without opening the box.

## Workshop

**File:** `async-types.ts`

**Problem:** Build a small async data layer where every failure is typed, and demonstrate three async typing traps.

Starter:

```ts
interface User { id: string; name: string }

type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

type FetchError =
  | { kind: "network"; cause: string }
  | { kind: "http"; status: number }
  | { kind: "parse"; detail: string };

// 1. fetchUser(id: string): Promise<Result<User, FetchError>>
//    Simulate: id "u1" succeeds; "u404" gives http 404;
//    "unparseable" gives a parse error; anything else a network error.
//    Never throw. Never use `any` or a cast.

// 2. isUser(value: unknown): value is User  — reuse the P2-L6 technique.

// 3. loadUsers(ids: string[]): Promise<Result<User[], FetchError>>
//    Fetch all in parallel. If any fails, return the FIRST failure.
//    Use Promise.all.

// 4. describeError(error: FetchError): string
//    Exhaustive switch with a never check.

// 5. Derive these types — do not write them by hand:
//    type FetchedUser  = the resolved type of fetchUser
//    type UserSuccess  = the ok branch of FetchedUser's Result
//    type Loaded       = Awaited<ReturnType<typeof loadUsers>>

// 6. TRAP A: this compiles and is wrong. Explain why in a comment,
//    then write the correct version below it.
function logAll(ids: string[]): void {
  ids.forEach(async (id) => {
    const r = await fetchUser(id);
    console.log(r.ok);
  });
}

// 7. TRAP B: this compiles and loses type information. Explain and fix.
async function pair() {
  const promises = [fetchUser("u1"), fetchUser("u404")];
  return Promise.all(promises);
}

// 8. TRAP C: this compiles and silently swallows a rejection.
//    Explain and fix.
async function fireAndForget(): Promise<void> {
  fetchUser("u1");
}

// Proofs
const r = await fetchUser("u1");
if (r.ok) {
  console.log(r.value.name);
} else {
  console.log(describeError(r.error));
}

// These must be errors. Keep all three, with @ts-expect-error.
async function badReturn(): string { return "x"; }
const notAwaited: User = fetchUser("u1");
const wrongError: FetchError = { kind: "http", status: "404" };
```

**Requirements:**

1. `fetchUser` never throws; every failure is a `Result` with a `FetchError`.
2. `describeError` has a `never` exhaustiveness check.
3. All three derived types in step 5 use `Awaited`, `ReturnType`, and `Extract` — no hand-written shapes.
4. Each trap has a comment explaining the failure and a corrected version beside it. Trap A's fix is a `for…of` loop; Trap B's is a tuple; Trap C's is `await` or an explicit `.catch()`.
5. Top-level `await` requires `"module": "esnext"` (or wrapping in an async `main()`); note which the learner chose.

## Acceptance Criteria

- `npx tsc --noEmit async-types.ts` produces no output.
- `npx tsx async-types.ts` runs and prints a success, then a described error for each failure kind.
- No `as`, no `any`, no `!`.
- `UserSuccess` is derived via `Extract<FetchedUser, { ok: true }>`, not written out.
- Each of the three traps has both the broken version (annotated) and a working fix.

## Compiler Checks

Expected:

- `TS1064: The return type of an async function or method must be the global Promise<T> type. Did you mean to write 'Promise<string>'?` — from `badReturn`. The message names the fix.
- `TS2739: Type 'Promise<Result<User, FetchError>>' is missing the following properties from type 'User': id, name` — the missing-`await` error, which is one of the more legible diagnostics TypeScript produces.
- `TS2322: Type 'string' is not assignable to type 'number'.` — the wrong `status` in `wrongError`.
- `TS2322: Type 'Result<User, FetchError>' is not assignable to type 'never'.` — if `describeError`'s switch is incomplete.
- `TS1378: Top-level 'await' expressions are only allowed when the 'module' option is set to 'es2022', 'esnext', 'system', 'node16', 'node18', 'node20', 'nodenext', or 'preserve', and the 'target' option is set to 'es2017' or higher.` — unless they wrap in `main()`. Often paired with `TS1375: 'await' expressions are only allowed at the top level of a file when that file is a module, but this file has no imports or exports. Consider adding an empty 'export {}' to make this file a module.` Both must be satisfied.
- `TS18046: 'err' is of type 'unknown'.` — if they add a `try/catch` anywhere.

Note what produces **no** diagnostic: all three traps. `forEach(async …)`, the degraded `Promise.all`, and the floating promise all compile cleanly. Make this explicit — it is the lesson's central point. The compiler proves the success channel and leaves the rest to you.

## Common Mistakes

- Annotating an async function's return as `T` instead of `Promise<T>`.
- Forgetting `await` and passing a `Promise<User>` where a `User` is expected. Usually caught, but not when the target is `unknown`, `any`, or a `void` callback slot.
- `array.forEach(async …)` and expecting sequential execution or error propagation. Neither happens.
- Building an array variable then `Promise.all(arr)`, degrading a tuple into a union array. Pass the literal directly or type it as a tuple.
- Using `try/catch` around code that already returns a `Result` — pick one error strategy per layer.
- Typing a `catch` parameter as `Error`. It is `unknown`, and narrowing with `instanceof Error` is the correct move; a rejected promise can carry anything.
- Treating `Promise.all` as fault-tolerant. It rejects on the first failure; `allSettled` is the one that reports every outcome.

## Everyday vs Type-Fluency Note

**Everyday:** Two habits carry almost all the value. Return `Result<T, E>` from anything that can fail for an expected reason, and reserve `throw` for genuine bugs. And enable the `no-floating-promises` lint rule — it catches the one class of async bug the type system structurally cannot.

**Type-fluency:** `Awaited<T>` is a recursive conditional type with special handling for thenables — read its definition. `Promise` variance is worth thinking about: `Promise<T>` is covariant in `T`, and the `PromiseLike` interface is what makes third-party promise implementations interoperate. The unsoundness in `void`-returning callback positions accepting `Promise<void>` is deliberate (it makes `forEach(async …)` compile), documented, and the reason a lint rule exists to cover for it.

## Bridge

You have the whole type system: shapes, narrowing, generics, derivation, conditional and mapped types, declarations, and async. Next: the capstone — a fully typed API client that uses all of it, where a wrong endpoint, a wrong body, or an unhandled error state is a compile error.
