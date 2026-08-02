# P2-L7: Phase 2 Project — Typed Event Emitter

## Overview

**File:** `p2-project.ts`

Before starting, save to memory that the user has reached the Phase 2 project. After completing, save progress as "Phase 2 complete."

One module, three parts. The target is an emitter where **the event name constrains the payload type** — `emit("user:login", { userId: "u1" })` compiles, `emit("user:login", { wrong: true })` does not, and `emit("nope", …)` does not either. Getting there requires generics, `keyof`, indexed access, and a constrained type parameter working together, which is why this is the Phase 2 capstone.

Present one part at a time. Wait for a clean compile before moving on.

Hard constraint: **no `any`, no `as`, no `!`, no suppression comments** except where a part explicitly engineers an error.

---

### Part 1: The Event Map

Define an interface mapping event names to payload types:

```ts
interface AppEvents {
  "user:login": { userId: string; at: Date };
  "user:logout": { userId: string };
  "cart:add": { sku: string; quantity: number };
  "error": { message: string; code: number };
}
```

Then derive, using operators rather than hand-written unions:

- `EventName` — the union of event names.
- `PayloadOf<K>` — a generic type resolving to the payload for a given name.
- `Listener<K>` — a function type taking that payload and returning `void`.
- `AnyEvent` — a discriminated union of `{ name: K; payload: PayloadOf<K> }` for every `K`. This one is harder than it looks; if the learner produces `{ name: EventName; payload: SomeUnion }` instead, that is the wrong answer and Part 3 will expose why.

**Checkpoint:** clean compile. `PayloadOf<"cart:add">` resolves to the cart payload — verify by assigning a correctly-shaped literal to it and confirming a wrong one errors.

---

### Part 2: The Emitter

Build a `TypedEmitter` class over the event map:

- `on<K extends EventName>(name: K, listener: Listener<K>): () => void` — returns an unsubscribe function.
- `once<K extends EventName>(name: K, listener: Listener<K>): void`.
- `off<K extends EventName>(name: K, listener: Listener<K>): void`.
- `emit<K extends EventName>(name: K, payload: PayloadOf<K>): void`.
- `listenerCount(name: EventName): number`.

Store listeners in a `Map`. Satisfy `strictPropertyInitialization`. Use `#private` for internal state.

The interesting problem is the storage type. A `Map` cannot express "the key determines the value type" across heterogeneous entries, so the internal store will need a deliberately looser type while the *public* methods stay precise. That tension is the real lesson: **the precision belongs at the API boundary, and the narrowest possible internal cast-free workaround goes inside.** Guide them toward a store typed over a union or a per-key `Set<Listener<never>>`-style approach and have them explain their choice. Accept any solution with no `any` and no `as` in the public signatures.

**Checkpoint:** clean compile; these must all hold, verified by the learner:

```ts
const bus = new TypedEmitter();
bus.on("user:login", (p) => console.log(p.userId, p.at));  // p inferred, no annotation
bus.emit("user:login", { userId: "u1", at: new Date() });
```

And each of these must error — keep them with `@ts-expect-error`:

```ts
bus.emit("user:login", { userId: "u1" });          // missing `at`
bus.emit("user:login", { wrong: true });           // wrong shape
bus.emit("nope", {});                              // unknown event
bus.on("cart:add", (p) => console.log(p.userId));  // wrong payload field
```

---

### Part 3: The Log

Add:

- `history(): readonly AnyEvent[]` — every event emitted, in order.
- `replay(handler)` — a handler that must exhaustively switch on `event.name`, with a `never` exhaustiveness check.
- `filterByName<K extends EventName>(name: K)` returning `readonly PayloadOf<K>[]`.

`replay` is where a badly-built `AnyEvent` fails: if `AnyEvent` is `{ name: EventName; payload: UnionOfAllPayloads }`, narrowing on `name` will *not* narrow the payload, and `event.payload.userId` stays an error. If it is a proper distributed union, narrowing works. If the learner hit this, do not fix it for them — point at the symptom and let them redesign Part 1.

Then add a fifth event to `AppEvents` and confirm `replay`'s exhaustiveness check fails, naming the new member.

**Checkpoint:** clean compile; the added-event experiment documented in a comment.

---

## Acceptance Criteria

- `npx tsc --noEmit --strict p2-project.ts` produces no output.
- No `any`, no `as`, no `!` in any public signature. Internal storage may use a documented looser type, explained in a comment.
- `bus.on("user:login", (p) => …)` infers `p` with no annotation.
- All four engineered `emit`/`on` errors are present and suppressed.
- `replay` narrows `event.payload` from `event.name` — the proof that `AnyEvent` was built as a distributed union.
- `npx tsx p2-project.ts` runs: subscribe, emit, unsubscribe, emit again, replay the history.

## Compiler Checks

The diagnostics that carry the lesson:

- `TS2345: Argument of type '{ userId: string; }' is not assignable to parameter of type '{ userId: string; at: Date; }'. Property 'at' is missing…` — payload constrained by event name. This is the project's central diagnostic.
- `TS2345: Argument of type '"nope"' is not assignable to parameter of type 'keyof AppEvents'.`
- `TS2339: Property 'userId' does not exist on type '{ sku: string; quantity: number; }'.` — wrong field in a listener, proving the callback parameter was inferred from the name.
- `TS2322: Type '{ name: "metrics:report"; payload: … }' is not assignable to type 'never'.` — the exhaustiveness failure after adding the fifth event.
- `TS2564` if the Map is declared without an initializer.
- `TS2536: Type 'K' cannot be used to index type 'AppEvents'.` — if `PayloadOf` or a method drops `extends EventName`.

## Review Focus

Read the file and run the compiler, then check in this order:

1. Clean compile with suppressions only where the project asked for them.
2. Whether `AnyEvent` distributes. Test it directly: does narrowing on `name` narrow `payload`? If not, Part 1 needs redoing regardless of whether Part 3 compiles.
3. Whether `as` or `any` leaked into a public signature. Internal only, documented, is acceptable.
4. Whether listener callbacks are annotated. If the learner wrote `(p: { userId: string; at: Date }) => …`, inference is not reaching them and the signature is wrong.
5. Whether `on` actually returns a working unsubscribe — a type-level pass with a broken runtime is still a fail. Check the run output.

## Everyday vs Type-Fluency Note

**Everyday:** This pattern — a name-to-payload interface plus `<K extends keyof Map>` methods — is exactly how real typed emitters, message buses, IPC channels, and analytics clients are built. It is the most reusable thing in Phase 2. The takeaway is the design principle: put an interface at the seam, derive every signature from it, and wrong usage becomes a compile error rather than a run-time surprise.

**Type-fluency:** The `AnyEvent` problem is a distributive-union problem, and solving it by hand (`{ [K in EventName]: { name: K; payload: AppEvents[K] } }[EventName]`) is a mapped type plus an indexed access used as a union-flattening trick. If the learner reached for that, they have independently derived the core Phase 3 technique — say so. If they did not, this is the motivating example for the next lesson.

## Bridge

Phase 2 complete. You can write types that compute from other types by hand, one operator at a time. Phase 3 is where types become programmable: conditional types with `infer`, mapped types that transform every key, and template literal types that compute strings — the tools that would have made `AnyEvent` a one-liner.
