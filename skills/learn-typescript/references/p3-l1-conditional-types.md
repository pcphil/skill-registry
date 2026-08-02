# P3-L1: Conditional Types & infer

## Concept

A conditional type is an `if` statement in type space:

```ts
type IsString<T> = T extends string ? true : false;
```

`extends` here means "is assignable to", not class inheritance. `IsString<"a">` is `true`; `IsString<number>` is `false`.

**`infer`** captures a type from a position during matching — pattern matching for types:

```ts
type ElementOf<T> = T extends (infer U)[] ? U : never;
type ElementOf1 = ElementOf<string[]>;    // string
type Unwrap<T> = T extends Promise<infer U> ? U : T;
```

Read it as: "if `T` has the shape `SomeArray<U>`, bind that `U` and give it back."

**Distribution** is the behaviour that surprises everyone. When a conditional type's checked type is a *naked* type parameter and you pass a union, the conditional applies to each member separately and the results are unioned:

```ts
type ToArray<T> = T extends unknown ? T[] : never;
type A = ToArray<string | number>;   // string[] | number[]   — NOT (string | number)[]
```

This is how `Exclude` works: `Exclude<T, U> = T extends U ? never : T`, applied member by member, with `never` members dropping out of the union.

To *prevent* distribution, wrap both sides in a tuple:

```ts
type NoDistribute<T> = [T] extends [unknown] ? T[] : never;
type B = NoDistribute<string | number>;  // (string | number)[]
```

Knowing which one you want is the whole skill. Distribution is what you want for filtering a union; suppression is what you want for testing a union as a single thing.

Two more essentials. **`never` distributes to nothing** — `Exclude<never, string>` is `never`, and a conditional over `never` produces `never`, not the false branch. And multiple `infer` sites in the same position produce a union (for covariant positions) or an intersection (for contravariant ones) — the mechanism behind `UnionToIntersection`.

## Analogy

A conditional type is a sorting machine on a conveyor: each item is measured against a template, and it goes left or right. `infer` is a caliper on that machine — as an item passes, it records a measurement you can use downstream.

Distribution is the detail that matters: hand the machine a *crate* of mixed items and it does not measure the crate. It opens it, runs every item through separately, and gives you back a set of results. Wrapping in a tuple is taping the crate shut so the machine measures the box instead.

## Workshop

**File:** `conditional-types.ts`

**Problem:** Rebuild several standard utility types from scratch, then use `infer` to extract types from function and promise shapes.

Starter:

```ts
// Implement each from scratch. Do not use the built-in version.

// 1. MyExclude<T, U>   — remove members of T assignable to U
// 2. MyExtract<T, U>   — keep only members of T assignable to U
// 3. MyNonNullable<T>  — remove null and undefined
// 4. MyReturnType<F>   — the return type of a function type
// 5. MyParameters<F>   — parameters as a tuple
// 6. MyAwaited<T>      — unwrap nested promises (recursive)
// 7. ElementOf<T>      — element type of an array
// 8. IsUnion<T>        — true if T is a union, false otherwise.
//    Hint: compare distributed and non-distributed forms.

// 9. DeepReadonly<T> — readonly at every level, recursive.
//    Leave functions and primitives alone.

// 10. Explain in a comment why these two differ:
type Naked<T> = T extends string ? "yes" : "no";
type Wrapped<T> = [T] extends [string] ? "yes" : "no";
type R1 = Naked<string | number>;
type R2 = Wrapped<string | number>;

// Proofs — each must compile with no error.
type Assert<T extends true> = T;
type Eq<A, B> = (<X>() => X extends A ? 1 : 2) extends (<X>() => X extends B ? 1 : 2) ? true : false;

type T1 = Assert<Eq<MyExclude<"a" | "b" | "c", "b">, "a" | "c">>;
type T2 = Assert<Eq<MyExtract<string | number | boolean, string | number>, string | number>>;
type T3 = Assert<Eq<MyNonNullable<string | null | undefined>, string>>;
type T4 = Assert<Eq<MyReturnType<() => number>, number>>;
type T5 = Assert<Eq<MyParameters<(a: string, b: number) => void>, [string, number]>>;
type T6 = Assert<Eq<MyAwaited<Promise<Promise<string>>>, string>>;
type T7 = Assert<Eq<ElementOf<boolean[]>, boolean>>;
type T8 = Assert<Eq<IsUnion<string | number>, true>>;
type T9 = Assert<Eq<IsUnion<string>, false>>;

// This must be an error. Keep it, with @ts-expect-error.
type T10 = Assert<Eq<MyExclude<"a" | "b", "b">, "a" | "b">>;
```

**Requirements:**

1. All nine assertions pass; `T10` fails and is suppressed.
2. `MyAwaited` handles `Promise<Promise<Promise<string>>>` — recursion, not a single unwrap.
3. `DeepReadonly` is applied to a nested object type and an attempted deep mutation is an error.
4. `IsUnion` works via the distribution comparison. Explain the mechanism in a comment.
5. The step-10 comment correctly explains distribution.

## Acceptance Criteria

- `npx tsc --noEmit conditional-types.ts` produces no output.
- Every utility is hand-written; no `Exclude`, `Extract`, `ReturnType`, `Parameters`, `Awaited`, or `NonNullable` from the standard library appears.
- The `Assert`/`Eq` pattern is used as given — it is the standard type-level test idiom and worth keeping.
- `DeepReadonly` has a demonstrated nested mutation error.

## Compiler Checks

Expected:

- `TS2344: Type 'false' does not satisfy the constraint 'true'.` — the shape of every failing assertion, including the engineered `T10`. When an assertion fails this is the message, and it tells you nothing about *why* — that is the cost of type-level testing, and worth naming.
- Runaway recursion in `MyAwaited` or `DeepReadonly` surfaces one of two ways depending on its shape: `TS2456: Type alias 'X' circularly references itself.` when the alias refers to itself outside a deferred position, or `TS2589: Type instantiation is excessively deep and possibly infinite.` when it genuinely instantiates too far. Tail-recursive conditionals often do *neither* — TypeScript special-cases them and allows roughly 1000 levels — so a missing base case can also simply produce a wrong type in silence. The fix in every case is a correct base case, never a workaround.
- `TS2540: Cannot assign to 'x' because it is a read-only property.` — the `DeepReadonly` proof.
- `TS1005` or `TS1110` on a malformed conditional — the `? :` syntax is easy to mis-nest when chaining.
- `TS2322` if `infer` is placed in a position the compiler cannot match.

## Common Mistakes

- Expecting `Exclude<"a" | "b", "b">` to behave like a set operation on a non-distributive conditional. Distribution is doing the work; `[T] extends [U]` breaks it.
- Placing the naked parameter behind something: `type X<T> = { v: T } extends { v: U } ? …` does not distribute, because the checked type is no longer a bare `T`.
- Forgetting the base case in a recursive conditional and hitting `TS2589`.
- Writing `T extends Promise<infer U> ? U : T` and calling it done — nested promises need `MyAwaited<U>` in the true branch.
- Using `infer` outside a conditional's `extends` clause. It is only legal there.
- Assuming a conditional over `never` takes the false branch. `Naked<never>` is `never`, because distributing over an empty union produces an empty union.
- Believing `Eq` is simple. The `<X>() => X extends A ? 1 : 2` trick exists because naive `A extends B ? B extends A ? true : false : false` gets `any` and union ordering wrong. Do not let the learner "simplify" it.

## Everyday vs Type-Fluency Note

**Everyday:** You will read conditional types far more often than you write them — in library `.d.ts` files and error messages. The two worth writing yourself are an `Awaited`-style unwrapper and a `DeepPartial`/`DeepReadonly`. Beyond that, reach for the standard library first.

**Type-fluency:** This is the heart of type-level programming. Master three things: the exact rule for when distribution occurs (naked type parameter in the checked position), how `infer` behaves in multiple and in contravariant positions, and the instantiation-depth limit that bounds recursion (roughly 50 levels for type instantiation, 1000 for tail-recursive conditionals since 4.5). The `Eq` helper above relies on deferred conditional identity — worth understanding, because it is the only reliable type equality test and it is not obvious why it works.

## Bridge

You can branch and destructure in type space. Next lesson: transforming every key of a type at once — mapped types, key remapping, and template literal types that compute new key names.
