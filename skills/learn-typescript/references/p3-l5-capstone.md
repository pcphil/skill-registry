# P3-L5: Capstone — Fully Typed API Client

## Overview

**File:** `p3-capstone.ts`

Before starting, save to memory that the user has reached the Phase 3 capstone. After completing, save progress as "Phase 3 complete — curriculum finished."

One module, four parts. The target: a client where a single route table drives everything. Given

```ts
client.request("GET /users/:id", { params: { id: "u1" } })
```

the compiler must know the path parameters from the route string, reject a missing or misspelled param, know the response type, and force the caller to handle every failure state. A wrong route, a wrong body, a missing param, or an unhandled error is a compile error.

This is the hardest thing in the course. Present one part at a time and expect the learner to get stuck in Part 2 — that is the intended difficulty, and the hint sequence below is graduated for it.

Hard constraint: **no `any`, no `as` in any public signature, no `!`, no suppression comments** except where a part engineers an error. One documented internal cast is acceptable in the fetch implementation, since the network boundary genuinely is untyped — require a comment justifying it.

---

### Part 1: The Route Table

Define the contract as data:

```ts
interface Routes {
  "GET /users": { response: User[] };
  "GET /users/:id": { response: User };
  "POST /users": { body: NewUser; response: User };
  "PATCH /users/:id": { body: Partial<NewUser>; response: User };
  "DELETE /users/:id": { response: void };
  "GET /users/:id/posts/:postId": { response: Post };
}
```

with `User`, `NewUser`, and `Post` defined, and `NewUser` derived from `User` with `Omit`.

Derive:

- `Route` — the union of route keys.
- `ResponseOf<R>` — the response type for a route.
- `BodyOf<R>` — the body type, or `never` when the route has none. Use a conditional type on the presence of the `body` key.
- `ApiError` — a discriminated union: `network`, `http` (with `status`), `parse`, `validation` (with `field`).

**Checkpoint:** clean compile. `ResponseOf<"GET /users">` is `User[]`; `BodyOf<"GET /users">` is `never`; `BodyOf<"POST /users">` is `NewUser`.

---

### Part 2: Path Parameter Extraction

This is the centrepiece. Write a type that reads path parameters out of the route string at compile time:

```ts
type PathParams<R extends string> = /* your code */;

// PathParams<"GET /users">                        -> {}  (or never/Record<never,never>)
// PathParams<"GET /users/:id">                    -> { id: string }
// PathParams<"GET /users/:id/posts/:postId">      -> { id: string; postId: string }
```

This requires a recursive conditional type with `infer` and template literal patterns — everything from P3-L1 and P3-L2 combined.

**Graduated hints.** Give one at a time, only when the learner is genuinely stuck:

1. The pattern to match is `` `${string}:${infer Param}/${infer Rest}` `` for a parameter followed by more path, and `` `${string}:${infer Param}` `` for a trailing one. Order matters — test the more specific pattern first.
2. Recurse on `Rest`, and intersect the results: `{ [K in Param]: string } & PathParams<Rest>`.
3. The base case is a route with no `:` — return `{}`.
4. Intersections of object types display badly in tooltips. A `Prettify<T> = { [K in keyof T]: T[K] } & {}` wrapper flattens them for readability, which makes debugging this type far easier.

**Checkpoint:** these assertions pass, using the `Assert`/`Eq` helpers from P3-L1:

```ts
type C1 = Assert<Eq<PathParams<"GET /users">, {}>>;
type C2 = Assert<Eq<Prettify<PathParams<"GET /users/:id">>, { id: string }>>;
type C3 = Assert<Eq<Prettify<PathParams<"GET /users/:id/posts/:postId">>, { id: string; postId: string }>>;
```

---

### Part 3: The Client

Build `ApiClient` with a single `request` method whose options type is computed from the route:

- Routes with no params and no body take no options argument, or an empty object.
- Routes with params require `params` with exactly the right keys.
- Routes with a body require `body` of the right type.
- The return type is `Promise<Result<ResponseOf<R>, ApiError>>` — never throws.

The signature will look something like:

```ts
request<R extends Route>(
  route: R,
  options: RequestOptions<R>
): Promise<Result<ResponseOf<R>, ApiError>>
```

where `RequestOptions<R>` conditionally includes `params` and `body`. Making the options argument *optional* when neither is needed is the finishing touch — a rest-tuple parameter (`...args: HasOptions<R> extends true ? [RequestOptions<R>] : []`) is one way.

Implementation: interpolate the params into the path, call `fetch`, validate the response with a guard from P2-L6, and map every failure onto an `ApiError` variant. This is where the one documented internal cast is permitted.

Add `handle(result, handlers)` requiring an exhaustive handler for every `ApiError` kind plus success, enforced with a `never` check.

**Checkpoint:** clean compile, and every line below behaves as marked:

```ts
const api = new ApiClient("https://example.test");

await api.request("GET /users");
await api.request("GET /users/:id", { params: { id: "u1" } });
await api.request("POST /users", { body: { name: "Ada", email: "a@b.c" } });
await api.request("GET /users/:id/posts/:postId", { params: { id: "u1", postId: "p1" } });

// @ts-expect-error — unknown route
await api.request("GET /nope");
// @ts-expect-error — missing required param
await api.request("GET /users/:id", { params: {} });
// @ts-expect-error — misspelled param
await api.request("GET /users/:id", { params: { ID: "u1" } });
// @ts-expect-error — body on a route that takes none
await api.request("GET /users", { body: { name: "x" } });
// @ts-expect-error — wrong body shape
await api.request("POST /users", { body: { nmae: "Ada" } });
```

---

### Part 4: Consume It

Write `main()` that:

- Fetches a user list and prints the names.
- Fetches one user by id.
- Creates a user and prints the result.
- Handles every `ApiError` kind through `handle`, with the exhaustiveness check active.

Then add a seventh route to `Routes` and confirm nothing breaks. Then add a new `ApiError` kind and confirm `handle` fails to compile, naming the unhandled variant. Document both results.

---

## Acceptance Criteria

- `npx tsc --noEmit --strict p3-capstone.ts` produces no output.
- All three `PathParams` assertions pass.
- All five engineered request errors are present and suppressed; removing any one suppression produces exactly one error.
- `params` keys are derived from the route string — verify by adding `/:slug` to a route and confirming `params` immediately demands `slug`.
- No `as` or `any` in any public signature. At most one internal cast, with a comment justifying it.
- `handle` has a working `never` exhaustiveness check, proven by the Part 4 experiment.
- `npx tsx p3-capstone.ts` runs against a stub or mocked `fetch` and prints output for both a success and a failure path.

## Compiler Checks

The diagnostics that prove the design:

- `TS2345: Argument of type '"GET /nope"' is not assignable to parameter of type 'keyof Routes'.`
- `TS2741: Property 'id' is missing in type '{}' but required in type '{ id: string; }'.` — path params derived from the string, the capstone's central result.
- `TS2561: Object literal may only specify known properties, but 'ID' does not exist in type '{ id: string; }'. Did you mean to write 'id'?` — a near-miss key gets the suggesting variant; an unrelated key gets `TS2353` with the same sentence and no suggestion.
- `TS2353` or `TS2561` again for a body on a bodyless route, or `TS2554: Expected 1 arguments, but got 2.` depending on how `RequestOptions` was built.
- `TS2322: Type '{ kind: "timeout"; }' is not assignable to type 'never'.` — the Part 4 exhaustiveness experiment.
- `TS2456: Type alias 'PathParams' circularly references itself.` or `TS2589: Type instantiation is excessively deep and possibly infinite.` — if `PathParams` recurses without a base case. Which one appears depends on the recursion's shape, and a tail-recursive version may produce neither and simply resolve wrong. The fix is the base case, never a workaround.
- `TS2590: Expression produces a union type that is too complex to represent.` — if `RequestOptions` is built by unioning over every route rather than conditionally per route.

## Review Focus

Read the file and run the compiler, then check in this order:

1. Clean compile, suppressions only where the capstone asked.
2. `PathParams` actually parses the string. Test it live: add `/:slug` to a route and confirm `params` demands it. A hand-written per-route param map passes the assertions but fails the point of the exercise — check for this specifically.
3. Whether `as` leaked into a public signature. One documented internal cast at the `fetch` boundary is fine; anything in `request`'s signature is not.
4. Whether `handle`'s exhaustiveness check is real (`const _: never = x`) or decorative (`default: return ""`).
5. Whether it runs. A type-level triumph that throws on the first call is incomplete.
6. Whether `BodyOf` correctly yields `never` for bodyless routes rather than `undefined` or `{}` — the difference determines whether passing a body is an error.

## Everyday vs Type-Fluency Note

**Everyday:** This is a real pattern, not an exercise. tRPC, Hono's RPC client, and the typed clients generated from OpenAPI specs all work this way — one contract object, every signature derived from it. Most teams consume such a client rather than write one, and having built one you will read their error messages fluently. In production, pair it with a schema library so run-time validation is derived from the same source.

**Type-fluency:** Part 2 is genuine type-level string parsing: recursive conditional types, `infer` in template literal patterns, and accumulation via intersection. The same technique types route builders, SQL query builders, format strings, and CSS-in-JS property names. Worth studying next: tail-recursive conditional types and the 1000-depth limit that makes deep recursion viable since 4.5, `NoInfer` for blocking unwanted inference sites, and `const` type parameters for preserving literal types through generic calls.

## Curriculum Complete

Save progress as "Phase 3 complete — curriculum finished." Then summarize for the learner:

- What they built: 19 workshop files, three phase projects, one capstone.
- The through-line: every phase removed hand-written types in favour of derived ones. Phase 1 declared shapes, Phase 2 derived them from other shapes, Phase 3 computed them from data.
- Where to go next: applying this in a framework (`learn-react`, `learn-nextjs`), or reading `lib.es5.d.ts` and the type definitions of a library they use.

Then return to default assistant behaviour. This skill's workflow does not apply to subsequent requests.
