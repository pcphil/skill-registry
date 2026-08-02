# P1-L3: Arrays, Tuples, Object Types

## Concept

Three ways to describe a group of values, each with a different guarantee:

| Form | Syntax | Guarantees |
|------|--------|-----------|
| Array | `string[]` or `Array<string>` | Every element is a `string`. Length unknown. |
| Tuple | `[string, number]` | Exactly two elements, in that order, of those types. |
| Object | `{ id: number; name: string }` | Those properties, with those types. |

**Arrays** are homogeneous and length-agnostic. `arr[99]` on a three-element array type-checks as `string` even though it is `undefined` at run time — TypeScript does not track length by default. (`noUncheckedIndexedAccess` changes this; it is not part of `strict`.)

**Tuples** track position. `[string, number]` means index 0 is a `string` and index 1 is a `number`, and index 2 does not exist. They support optional (`[string, number?]`) and rest (`[string, ...number[]]`) elements, and can be labelled for readability: `[name: string, age: number]`.

**Object types** are **structural**. TypeScript does not care what you named the type — it cares what shape the value has. Any value with a `number` `id` and a `string` `name` is assignable to `{ id: number; name: string }`, regardless of where it came from. This is the single deepest idea in the TypeScript type system, and it is why TypeScript feels different from Java or C#.

Two modifiers you need immediately:

```ts
type User = {
  readonly id: number;   // assignment after creation is an error
  nickname?: string;     // string | undefined, and may be omitted
};
```

One rule that looks like an exception to structural typing: **excess property checking**. A *fresh* object literal assigned directly to a typed target may not carry unknown properties. Assign it to a variable first and the check disappears — because the check exists to catch typos, not to enforce exactness.

## Analogy

An array is a bag of identical parts: you know everything inside is a 10mm bolt, but not how many. A tuple is a labelled tray from a flat-pack kit: slot one holds the long screw, slot two holds the washer, and a missing slot means the kit is wrong.

Structural typing is hiring by audition, not by diploma. If a candidate can play the part, they get the role — nobody checks which school issued the certificate. Nominal typing (Java, C#) checks the diploma.

## Workshop

**File:** `collections.ts`

**Problem:** Model a small inventory of products and a fixed-size coordinate, then observe structural typing and excess property checking first-hand.

Starter:

```ts
// 1. Define a Product object type:
//    - id: readonly number
//    - name: string
//    - price: number
//    - tags: array of strings
//    - discount: optional number

// 2. Define Coordinate as a tuple of exactly two numbers, labelled x and y.

// 3. Annotate and implement. Return the sum of every product's price.
function totalPrice(products) {
  // your code
}

// 4. These must compile.
const widget: Product = {
  id: 1,
  name: "Widget",
  price: 9.99,
  tags: ["tools", "sale"],
};

const origin: Coordinate = [0, 0];

// 5. Each of the following must be an error. Keep them all,
//    each preceded by @ts-expect-error.
widget.id = 2;
const bad: Coordinate = [0, 0, 0];
const typo: Product = {
  id: 2,
  name: "Gadget",
  price: 5,
  tags: [],
  discont: 0.1,
};

console.log(totalPrice([widget]));
```

**Requirements:**

1. All five errors in step 5 are marked with `@ts-expect-error` and the file compiles clean.
2. `totalPrice` accepts `Product[]` and returns `number`. Do not annotate its return type — let it infer, then hover to confirm it inferred `number`.
3. Add a comment above the `typo` case naming which rule catches it.
4. Prove structural typing: build an object literal with `id`, `name`, `price`, and `tags` assigned to a variable with **no** annotation, then pass it to `totalPrice`. It must compile.

## Acceptance Criteria

- `npx tsc --noEmit collections.ts` produces no output.
- `Product` uses `readonly` on `id` and `?` on `discount`.
- `Coordinate` is a tuple with two labelled elements, not `number[]`.
- The structural-typing proof from requirement 4 is present and compiles without an annotation on the intermediate variable.

## Compiler Checks

Expected diagnostics, one per suppressed line:

- `TS2540: Cannot assign to 'id' because it is a read-only property.`
- `TS2322: Type '[number, number, number]' is not assignable to type 'Coordinate'. Source has 3 element(s) but target allows only 2.`
- `TS2561: Object literal may only specify known properties, but 'discont' does not exist in type 'Product'. Did you mean to write 'discount'?` — excess property checking. Note the code: TypeScript reports **TS2561** when the unknown key is close to a real one and it can suggest a correction, and **TS2353** (same sentence, "and" instead of "but", no suggestion) when it cannot. Worth demonstrating that assigning the same literal to an untyped variable first, then to a `Product`, makes this error vanish either way.

If `totalPrice` is left unannotated: `TS7006: Parameter 'products' implicitly has an 'any' type.`

## Common Mistakes

- Writing `Coordinate = number[]` and expecting length checking. Arrays do not track length.
- Assuming `readonly` is deep. `readonly tags: string[]` still permits `tags.push(...)` — you need `readonly string[]` for that.
- Believing excess property checking is exactness. It only fires on fresh object literals, and it is easy to accidentally route around it.
- Writing `discount: number | undefined` and thinking it equals `discount?: number`. The first *requires* the key to be present (possibly holding `undefined`); the second lets it be omitted.
- Indexing past the end of an array and trusting the type. `arr[99]` is typed `string`, not `string | undefined`, unless `noUncheckedIndexedAccess` is on.

## Everyday vs Type-Fluency Note

**Everyday:** Objects and arrays cover almost everything. Reach for tuples when a function genuinely returns a fixed pair — React's `useState` is the canonical example. Prefer `readonly` on identity fields.

**Type-fluency:** Structural assignability is the foundation everything later rests on: variance in function parameters, generic constraint satisfaction, and why two independently declared identical interfaces are interchangeable. Also worth exploring `noUncheckedIndexedAccess`, which makes indexing return `T | undefined` and turns array access into a narrowing problem — which is exactly the next lesson.

## Bridge

You can describe shapes. But a value that is `string | undefined` cannot be used as a `string` until you prove which one it is. Next lesson: unions, intersections, and narrowing — how the compiler follows your control flow.
