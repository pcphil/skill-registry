# P2-L2: Generic Types, Interfaces & Classes

## Concept

Type parameters are not limited to functions. Aliases, interfaces, and classes all take them, which is how a container remembers what it contains.

```ts
type Box<T> = { value: T };
interface Repository<T> { get(id: string): T | undefined; add(item: T): void }
class Stack<T> { private items: T[] = []; push(item: T): void { this.items.push(item) } }
```

The crucial difference from generic functions: **there is nothing to infer from at the declaration site.** `Box<string>` must be written out. Inference only happens where values flow — a constructor call (`new Stack<number>()` or often just `new Stack()` if a value pins it) or a function call.

A generic type with an unfilled parameter is not a type. `let b: Box` is `TS2314: Generic type 'Box<T>' requires 1 type argument(s)`. Defaults soften this: `type Box<T = unknown>` makes `Box` legal.

Constraints work identically to functions, and self-referential generics enable recursive structures:

```ts
type TreeNode<T> = { value: T; children: TreeNode<T>[] };
```

For classes, two specifics matter under `strict`. `strictPropertyInitialization` requires every property to be assigned in the constructor or given an initializer — `TS2564` otherwise. And **parameter properties** are a shorthand that declares and assigns in one move:

```ts
class Entry<T> {
  constructor(public readonly key: string, private value: T) {}
}
```

Finally: `private` is a compile-time fiction, erased at build. `#private` fields are real JavaScript and enforced at run time. Prefer `#` when the boundary must hold against untyped callers.

## Analogy

A generic type is a labelled shipping container with a blank on the label: "CONTAINER OF ______". Stencilling in "COFFEE" gives you `Box<Coffee>` — a real, specific container. The blank label itself isn't a container you can load; that's why `let b: Box` fails.

A generic function is different: it's a courier who reads what you handed them and fills in the label for you. Nobody hands anything to a type declaration, so the declaration must be told.

## Workshop

**File:** `generic-types.ts`

**Problem:** Build a typed `Stack`, a generic `Result` type, and a small in-memory repository.

Starter:

```ts
// 1. Result<T, E> — a discriminated pair:
//      { ok: true; value: T } | { ok: false; error: E }
//    Give E a default of string.

// 2. Stack<T> class:
//      push(item: T): void
//      pop(): T | undefined
//      peek(): T | undefined
//      get size(): number
//    Items stored privately. Use #private, not `private`.

// 3. Repository<T extends { id: string }> interface with:
//      add(item: T): void
//      get(id: string): Result<T>          // error branch is a string message
//      all(): readonly T[]

// 4. InMemoryRepo<T extends { id: string }> implementing Repository<T>.
//    Use a Map internally. Satisfy strictPropertyInitialization.

// 5. Tree<T> type: a value plus an array of child Tree<T>.
//    Then write depth(node) returning the tree's depth. Generic, recursive.

// Proofs
type User = { id: string; name: string };
const repo = new InMemoryRepo<User>();
repo.add({ id: "u1", name: "Ada" });

const found = repo.get("u1");
if (found.ok) {
  console.log(found.value.name);   // must be typed User, no cast
} else {
  console.log(found.error.toUpperCase());  // must be typed string
}

const s = new Stack<number>();
s.push(1);
const top: number | undefined = s.pop();

// This must be an error. Keep it, with @ts-expect-error.
const bad = new InMemoryRepo<{ name: string }>();
```

**Requirements:**

1. All proofs compile; `found.value` is `User` inside the `ok` branch with no cast.
2. `Stack` uses `#items` and exposes `size` as a getter.
3. `InMemoryRepo` satisfies the interface exactly — no extra public surface.
4. `depth` is generic over `T` and does not care what `T` is.
5. The `InMemoryRepo<{ name: string }>` line is suppressed and the constraint violation is the reason.

## Acceptance Criteria

- `npx tsc --noEmit generic-types.ts` produces no output.
- `Result` has a default for `E`, so `Result<User>` is legal.
- `#items` is used; `npx tsx generic-types.ts` runs and the private field is genuinely inaccessible from outside.
- `depth` works on a `Tree<string>` and a `Tree<number>` without change.

## Compiler Checks

Expected:

- `TS2314: Generic type 'Result' requires 1 type argument(s).` — if `Result` is used bare before the default is added. (Older compilers print the parameter list, `'Result<T, E>'`; current ones print the bare name. Take whichever the learner's version gives.)
- `TS2741: Property 'id' is missing in type '{ name: string; }' but required in type '{ id: string; }'.` — the engineered error in the proof block. Note that a violated constraint on a **class** type argument surfaces as a missing-property error, not as `TS2344`; `TS2344: Type 'X' does not satisfy the constraint 'Y'` is what you get when the constraint is violated on a **type alias or mapped type** instead. Both are constraint failures; the phrasing differs by context.
- `TS2564: Property '#items' has no initializer and is not definitely assigned in the constructor.` — from `strictPropertyInitialization` if the Map is declared without an initializer.
- `TS2420: Class 'InMemoryRepo<T>' incorrectly implements interface 'Repository<T>'.` — with a follow-on line naming the missing or mismatched member.
- `TS18013: Property '#items' is not accessible outside class 'Stack' because it has a private identifier.` — if they try to reach it from outside. Worth demonstrating.
- `TS4104: The type 'readonly T[]' is 'readonly' and cannot be assigned to the mutable type 'T[]'.` — returning a mutable array where `readonly T[]` is declared is fine; the reverse is not. Have them try it in the failing direction to see this one.

## Common Mistakes

- Forgetting the type argument on a generic type and getting `TS2314`.
- Adding `<T>` to a class whose methods never use `T`. Same rule as functions: it must connect positions.
- Using `private` and assuming run-time privacy. `(stack as any).items` reaches straight in. `#items` does not.
- Declaring `#items: Map<string, T>` with no initializer, then being surprised by `TS2564`.
- Writing `pop(): T` instead of `T | undefined`. An empty stack has nothing to return, and the compiler will not catch the lie because `arr.pop()` is typed `T | undefined` and gets silently widened away by the annotation.
- Making `Result`'s branches share a shape without a discriminant, so narrowing fails. The literal `ok: true` / `ok: false` is what makes `if (found.ok)` work.

## Everyday vs Type-Fluency Note

**Everyday:** `Result<T, E>` and a typed repository are the two patterns worth taking away. `Result` in particular replaces throw-based error handling with something the compiler can check, and it composes well with the discriminated unions in P2-L5.

**Type-fluency:** Generic classes raise variance questions that generic functions do not — `Stack<Dog>` is not safely a `Stack<Animal>` because you could push a `Cat` into it, yet TypeScript's structural checking will often allow it because it does not track variance annotations except through the `in`/`out` modifiers added in 4.7. That unsoundness is deliberate and worth understanding. Recursive generic types like `Tree<T>` also hit the instantiation-depth limit (`TS2589`) when combined with conditional types, which Phase 3 touches.

## Bridge

Your containers carry their element types. Next lesson: the operators that let a type *read* another type — `keyof`, `typeof`, and indexed access — the foundation of every utility type.
