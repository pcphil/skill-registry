# P1-L5: Functions — Parameters, Returns, Optional, Rest

## Concept

Annotate parameters; let return types infer. That is the default posture, and it holds until you are writing a public API boundary where you want the return type pinned so a refactor cannot silently change it.

Syntax you need:

```ts
function f(required: string, optional?: number, withDefault = 10, ...rest: boolean[]): string
```

- **Optional** `?` makes the type `number | undefined` *and* lets the argument be omitted.
- **Default** values make the parameter optional at the call site while the type stays non-optional inside the body — TypeScript narrows it for you.
- **Rest** must be last and must be an array or tuple type.
- Optional parameters must follow required ones.

Two ways to type a function value, and they are not interchangeable:

```ts
type Fn = (input: string) => number;              // function type expression
interface Fn2 { (input: string): number; ver: 1 } // call signature — can carry properties
```

**Overloads** declare several signatures for one implementation. The implementation signature is not callable from outside; it exists only to satisfy the compiler:

```ts
function parse(input: string): string[];
function parse(input: number): number[];
function parse(input: string | number): string[] | number[] {
  return typeof input === "string" ? input.split("") : [input];
}
```

The part that surprises people is **assignability**. A function with *fewer* parameters is assignable where one with more is expected — because ignoring an argument is always safe. That is why `["a","b"].map(s => s.length)` works even though `map` passes three arguments. Return types are covariant: returning something more specific is fine.

## Analogy

A function type is a job description, and hiring follows one rule: the new hire must handle everything the description promises, and may not demand more than it offers.

Someone who ignores two of the three tools you hand them is still qualified — that's why fewer parameters is safe. Someone who insists on a fourth tool you never mentioned is not. And a chef hired to "produce food" may hand you a specific dish; that's return covariance. A chef hired to cook *fish* who instead demands to be given "any food" is fine on input, because they can handle a superset — that's parameter contravariance, and it's the reason `strictFunctionTypes` exists.

## Workshop

**File:** `functions.ts`

**Problem:** Build a small set of text utilities exercising optional, default, and rest parameters, plus one overloaded function.

Starter:

```ts
// 1. Annotate. separator defaults to ", ". Returns the joined string.
//    Must accept any number of parts.
function join(separator, ...parts) {
  return parts.join(separator);
}

// 2. Annotate. `max` is optional. When omitted, do not truncate.
//    When given, cut to max chars and append "…" if truncation happened.
function truncate(text, max) {
  // your code
}

// 3. Write overloads for `first` so that:
//    first("hello")        is typed string
//    first([1, 2, 3])      is typed number
//    first([])             is typed number | undefined  -- think about this one
//    Implement it once.

// 4. Declare a Formatter function type: takes a string, returns a string.
//    Then assign an arrow function that ignores its parameter and
//    returns a constant. It must compile — explain in a comment why.
```

**Requirements:**

1. Every parameter is annotated or has a default; no implicit `any`.
2. `truncate("hello", 3)` returns `"hel…"`; `truncate("hello")` returns `"hello"`.
3. `first` uses real overload signatures, not a union return type.
4. The `Formatter` comment correctly explains parameter-count assignability.
5. Add one call proving `join()` with no parts compiles and returns `""`.

## Acceptance Criteria

- `npx tsc --noEmit functions.ts` produces no output.
- Hovering `first("hello")` shows `string`, not `string | number`.
- No return type annotations except where overloads require them.
- `npx tsx functions.ts` prints the expected values for each utility.

## Compiler Checks

Expected while working:

- `TS7006: Parameter 'separator' implicitly has an 'any' type.` and `TS7019: Rest parameter 'parts' implicitly has an 'any[]' type.`
- `TS1016: A required parameter cannot follow an optional parameter.` — if `max` is placed before `text`.
- `TS18048: 'max' is possibly 'undefined'.` — inside `truncate` before narrowing.
- `TS2394: This overload signature is not compatible with its implementation signature.` — when the implementation signature is narrower than the overloads it must cover.
- `TS2554: Expected 2 arguments, but got 1.` — if `max` is declared required rather than optional.

Clean run prints nothing.

## Common Mistakes

- Annotating a rest parameter as `...parts: string` instead of `...parts: string[]`.
- Giving a parameter both `?` and a default. A default already makes it optional; combining them is `TS1015`.
- Writing overload bodies. Only the implementation has a body; the signatures above it end in a semicolon.
- Making the implementation signature public API — it is invisible to callers, so `first(true)` is still an error even if the implementation accepts it.
- Annotating every return type out of habit. It duplicates information, and the annotation is the thing that goes stale.
- Expecting an error when passing a zero-parameter callback where a two-parameter one is expected. That is legal and intentional.

## Everyday vs Type-Fluency Note

**Everyday:** Annotate parameters, infer returns, use defaults over optionals when a sensible default exists. Prefer a single function taking a union over overloads — overloads are verbose and easy to get subtly wrong.

**Type-fluency:** Function assignability is where variance becomes concrete. Parameters are contravariant under `strictFunctionTypes` (for function *type* positions, though method syntax remains bivariant for historical reasons), returns are covariant, and `this` parameters are their own case. Generic functions add inference sites on top of all this — which is where the next phase begins.

## Bridge

You can type the values and the functions that move them. Next lesson: the two ways to name an object shape — `type` and `interface` — and the real differences between them.
