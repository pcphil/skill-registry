# P2-L1: Generic Functions & Constraints

## Concept

A generic function takes types as inputs the same way an ordinary function takes values. The type parameter is a placeholder the compiler fills in at each call site.

Compare three ways to write "return the first element":

```ts
function first1(arr: any[]): any { return arr[0]; }        // works, loses everything
function first2(arr: unknown[]): unknown { return arr[0]; } // safe, still useless to callers
function first3<T>(arr: T[]): T { return arr[0]; }          // relationship preserved
```

Only the third states the actual rule: *whatever kind of array you give me, you get that kind of element back*. `any` discards the relationship; `unknown` records ignorance; a type parameter records the connection.

**Inference** means you rarely pass type arguments explicitly. `first3([1, 2, 3])` infers `T = number` from the argument. Write `first3<number>([1,2,3])` only when inference gets it wrong or when there is nothing to infer from.

**Constraints** with `extends` restrict what `T` can be, which is what makes the body able to *do* anything:

```ts
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}
```

Without the constraint, `a.length` is an error — an unconstrained `T` could be `number`, which has no `length`. The constraint is a promise from the caller that buys you capability inside the body.

Defaults work too: `<T = string>`. And multiple parameters can constrain each other: `<T, K extends keyof T>` — the pattern behind almost every real utility, covered properly in P2-L3.

The judgement call: **a type parameter used only once is usually wrong.** `function log<T>(x: T): void` gains nothing over `x: unknown`. Generics earn their keep by connecting two or more positions — parameter to return, parameter to parameter.

## Analogy

Think of a courier who guarantees "whatever you hand me at the door, that exact item arrives." They do not need to know if it's a vase or a violin — the promise is about the *relationship* between what goes in and what comes out. That's `<T>(x: T) => T`.

`any` is a courier who says "I'll deliver something." Technically true. Useless as a guarantee.

A constraint is the courier adding "…as long as it fits in a standard box." Now they can promise more — they can tell you the shipping weight — because they know something about every parcel they'll accept.

## Workshop

**File:** `generics.ts`

**Problem:** Write five generic utilities. The test of each is whether type information survives the call.

Starter:

```ts
// 1. Return the last element, or undefined for an empty array.
//    last([1,2,3]) must be typed number | undefined
function last(arr) {
  // your code
}

// 2. Swap a pair. swap(["a", 1]) must be typed [number, string]
function swap(pair) {
  // your code
}

// 3. Group values by a key-producing function.
//    groupBy(["ant","bee","cow"], s => s.length)
//    must be typed Record<number, string[]>
function groupBy(items, keyFn) {
  // your code
}

// 4. Return whichever argument has the greater length.
//    Must accept two strings, or two arrays. Must reject two numbers.
function longest(a, b) {
  // your code
}

// 5. This function has a type parameter that earns nothing.
//    Rewrite it without generics and explain in a comment.
function describe<T>(value: T): string {
  return String(value);
}

// Proofs — these must compile and be correctly typed.
const n: number | undefined = last([1, 2, 3]);
const s: [number, string] = swap(["a", 1]);
const g: Record<number, string[]> = groupBy(["ant", "bee", "cow"], (x) => x.length);
const l: string = longest("hello", "hi");

// This must be an error. Keep it, with @ts-expect-error.
longest(1, 2);
```

**Requirements:**

1. All four proof assignments compile with no casts.
2. `longest` is constrained so `longest(1, 2)` fails.
3. `swap` returns a tuple with the element types actually reversed — not `[string | number, string | number]`.
4. `describe` is rewritten with a non-generic parameter type and a comment naming the rule ("a type parameter used once connects nothing").
5. No explicit type arguments at any call site — inference must carry all of it.

## Acceptance Criteria

- `npx tsc --noEmit generics.ts` produces no output.
- Hovering `swap(["a", 1])` shows `[number, string]`.
- `groupBy`'s key function parameter is inferred — the learner does not annotate `x` in the callback.
- `longest(1, 2)` is suppressed with `@ts-expect-error` and removing the comment produces exactly one error.

## Compiler Checks

Expected while working:

- `TS2339: Property 'length' does not exist on type 'T'.` — in `longest` before adding the constraint. The canonical "you need a constraint" diagnostic.
- `TS2345: Argument of type 'number' is not assignable to parameter of type '{ length: number; }'.` — the engineered failure in the proof section.
- `TS2322: Type '(string | number)[]' is not assignable to type '[number, string]'.` — if `swap` builds an array instead of a tuple; annotate the return as `[U, T]` or use `as const` on the returned array literal.
- `TS7006` on `arr`, `pair`, `items`, `keyFn` until annotated.
- `TS2536: Type 'K' cannot be used to index type 'T'.` — if they over-reach in `groupBy` and try to index with an unconstrained parameter.

## Common Mistakes

- Annotating the callback parameter in `groupBy` calls. If inference is working, `(x) => x.length` needs nothing; needing an annotation means the signature is wrong.
- Writing `function swap<T>(pair: [T, T])` — that forces both elements to the same type. Two parameters are needed: `<T, U>(pair: [T, U]): [U, T]`.
- Constraining with `extends any`, which is the same as no constraint.
- Adding type parameters everywhere on reflex. Ask of each one: does it connect two positions?
- Confusing `extends` in a constraint with class inheritance. Here it means "is assignable to".
- Returning `arr[arr.length - 1]` and typing it `T` rather than `T | undefined`. TypeScript will not object — array indexing is not length-checked — so the return annotation is the learner's responsibility.

## Everyday vs Type-Fluency Note

**Everyday:** Most useful generics look like `<T>(items: T[]) => something-with-T`. If you can write `groupBy` and `last` correctly, you can type nearly every helper you'll actually need. The one habit worth enforcing: never reach for `any` to escape a generic error — the error is usually asking for a constraint.

**Type-fluency:** Inference has a defined procedure — candidate collection from each inference site, then a "best common supertype" resolution, with literal types widening unless a `const` type parameter or a constraint prevents it. Knowing where inference sites *are* explains why `groupBy(items, keyFn)` infers the callback parameter but the same code with the arguments reversed sometimes does not. Contextual typing flows left to right through the parameter list.

## Bridge

You can make functions generic. Next lesson: making *types* generic — generic interfaces, type aliases, and classes, so a container can carry its element type.
