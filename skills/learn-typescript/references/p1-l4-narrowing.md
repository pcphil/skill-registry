# P1-L4: Unions, Intersections, Narrowing

## Concept

A **union** `A | B` says "one of these, but I don't know which." You may only use members that exist on *every* branch. A **intersection** `A & B` says "all of these at once" — you get every member of both.

The counterintuitive part: union widens the set of *values* but narrows the set of usable *members*. Intersection does the reverse.

```ts
type Id = string | number;   // more values allowed, fewer methods available
type Admin = User & { role: "admin" };  // fewer values allowed, more properties available
```

**Narrowing** is how you get from `string | number` to `string`. TypeScript performs control-flow analysis: it tracks what each check proves and refines the type inside that branch. The built-in narrowing operations:

| Check | Narrows |
|-------|---------|
| `typeof x === "string"` | primitives |
| `x === null`, `x == null` | `null` / `null \| undefined` |
| `"prop" in x` | object union members by key |
| `x instanceof Date` | class instances |
| `if (x)` | removes `null`, `undefined`, `""`, `0`, `NaN`, `false` |
| `Array.isArray(x)` | arrays |

Two behaviours worth naming now. **Truthiness narrowing is lossy**: `if (count)` removes `0` alongside `undefined`, which is a real bug for numeric values — use `if (count !== undefined)`. And narrowing **resets across function boundaries**: a callback cannot rely on a check made outside it, because TypeScript cannot prove when the callback runs.

## Analogy

A union is a sealed envelope that holds either a cheque or a concert ticket. Before opening it, the only thing you can do is what works for both — carry it, weigh it, put it in a drawer. You cannot deposit it and you cannot get through the gate, because you don't yet know which it is.

Narrowing is opening the envelope. `typeof x === "string"` is the moment you look inside, and from then on — *within that room* — everyone knows it's a cheque. Walk into another room (a callback) and you're carrying a sealed envelope again, because nobody there watched you open it.

## Workshop

**File:** `narrowing.ts`

**Problem:** Write a formatter that accepts several input shapes and produces a display string, using narrowing rather than casts.

Starter:

```ts
type Ok = { status: "ok"; data: string };
type Err = { status: "error"; message: string };
type Response = Ok | Err;

// 1. Accepts string | number | null. Return the value as a display string:
//    - string: trimmed and uppercased
//    - number: fixed to 2 decimals
//    - null: the literal "N/A"
//    Use no casts and no `any`.
function display(value) {
  // your code
}

// 2. Accepts Response. Return data on success, "Error: <message>" otherwise.
//    Narrow using the status property.
function describe(response) {
  // your code
}

// 3. Fix this function. It has a real bug that the compiler does NOT catch,
//    and it should. Explain the bug in a comment, then fix it.
function label(count: number | undefined): string {
  if (count) {
    return `${count} items`;
  }
  return "unknown";
}

console.log(display("  hi  "), display(3.14159), display(null));
console.log(describe({ status: "ok", data: "payload" }));
console.log(label(0));
```

**Requirements:**

1. `display` and `describe` have annotated parameters and inferred return types of `string`.
2. No `as`, no `any`, no non-null assertion (`!`) anywhere in the file.
3. `label(0)` returns `"0 items"` after your fix, and you have written one sentence explaining why the original was wrong.
4. Add a fourth function `merge` that takes `Ok & { cached: boolean }` and returns a string using `data`, `status`, and `cached` — proving intersections give you every member.

## Acceptance Criteria

- `npx tsc --noEmit narrowing.ts` produces no output.
- Every branch of `display` is reached by a narrowing check, not a cast.
- `label(0)` produces `"0 items"` at run time. Verify by running it: `npx tsx narrowing.ts`.
- `merge` accesses all three properties without narrowing.

## Compiler Checks

Expected while working:

- `TS18047: 'value' is possibly 'null'.` — reported first, on the receiver.
- `TS2339: Property 'trim' does not exist on type 'string | number'.` — the core lesson: you may only touch members common to every branch until you narrow. Note that `null` is absent from this message; TS18047 already accounted for it, so the two diagnostics partition the problem between them rather than each naming the full union.
- `TS2339: Property 'data' does not exist on type 'Response'. Property 'data' does not exist on type 'Err'.` — before narrowing on `status`.
- `TS2366: Function lacks ending return statement and return type does not include 'undefined'.` — if a branch falls through.

Note that the `label` bug produces **no diagnostic**. `if (count)` is perfectly type-safe; it is just semantically wrong. Point this out explicitly — the compiler proves types, not intent.

## Common Mistakes

- Reaching for `as string` the moment `TS2339` appears. A cast silences the checker without proving anything; every cast is a place the type system stops helping.
- Using `typeof value === "null"` — `typeof null` is `"object"`. Compare with `value === null` instead.
- Narrowing outside a callback and expecting it to hold inside: `if (x) { arr.forEach(() => x.trim()) }` fails, because TypeScript cannot prove `x` is unchanged by the time the callback runs. Assign to a `const` first.
- Truthiness-narrowing a number or a string, silently dropping `0` and `""`.
- Writing `Ok | Err` where `Ok & Err` was meant, or vice versa. Say it out loud: "or" versus "and".

## Everyday vs Type-Fluency Note

**Everyday:** `typeof`, `in`, and truthiness cover the vast majority of real narrowing. The habit worth building is treating every `as` as a small admission of defeat — reach for a narrowing check first, and only cast when you genuinely know something the compiler cannot.

**Type-fluency:** Control-flow analysis has a real model: each binding carries a flow node, and assignments, checks, and closures create or invalidate refinements. Understanding *why* `let` narrowing is discarded inside a closure while `const` narrowing survives explains a large class of confusing errors. Narrowing on a `status` field is a preview of discriminated unions (P2-L5), which formalize this pattern and add exhaustiveness checking.

## Bridge

You can prove which member of a union you hold. Next lesson: functions — how parameters, returns, optionals, and rest arguments are typed, and why the compiler is stricter about function assignability than you expect.
