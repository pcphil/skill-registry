# P3-L2: Mapped Types & Template Literal Types

## Concept

A mapped type iterates over keys and produces a new type:

```ts
type Mapped<T> = { [K in keyof T]: T[K] };   // identity — copies T
```

`[K in keyof T]` is a type-level `for` loop. Every standard utility is a variation:

```ts
type MyPartial<T>  = { [K in keyof T]?: T[K] };
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };
type MyPick<T, K extends keyof T> = { [P in K]: T[P] };
type MyRecord<K extends keyof never, V> = { [P in K]: V };
```

**Modifiers can be removed as well as added**, with `-`:

```ts
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
type Concrete<T> = { [K in keyof T]-?: T[K] };
```

**Key remapping** with `as` renames keys during the map, and a key mapped to `never` is dropped — which is how you filter:

```ts
type Getters<T> = { [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K] };
type OnlyStrings<T> = { [K in keyof T as T[K] extends string ? K : never]: T[K] };
```

**Template literal types** compute strings in type space:

```ts
type EventName<T extends string> = `on${Capitalize<T>}`;
type Route = `/api/${"users" | "posts"}/${string}`;
```

They distribute over unions in every slot, so `` `${"a"|"b"}-${"x"|"y"}` `` is all four combinations — which means they multiply, and a few union slots can produce a combinatorial explosion the compiler will refuse (`TS2590`).

Four intrinsic string types are built in: `Uppercase`, `Lowercase`, `Capitalize`, `Uncapitalize`. They are implemented in the compiler, not in TypeScript.

One gotcha: `keyof T` includes `number` and `symbol`, so template interpolation needs `string & K` to satisfy the string constraint.

## Analogy

A mapped type is an assembly line that rebuilds an object one property at a time. The plain version copies each part unchanged. Add `?` and every part becomes optional. Add `-readonly` and the line strips the welds off. Key remapping is a labelling station that renames each part as it passes — and a part relabelled `never` falls off the belt, which is how filtering works.

Template literal types are the label printer at that station: it composes new names from fragments. Feed it a set of prefixes and a set of suffixes and it prints every combination — which is convenient right up until you feed it two large sets and it prints ten thousand labels.

## Workshop

**File:** `mapped-types.ts`

**Problem:** Build a set of mapped-type utilities, then use key remapping and template literals to derive a getter/setter interface from a plain shape.

Starter:

```ts
interface Person {
  readonly id: string;
  name: string;
  age: number;
  email?: string;
  greet(): void;
}

// Implement from scratch. No built-in utilities.

// 1. Mutable<T>          — remove readonly from every key
// 2. Concrete<T>         — remove optionality from every key
// 3. MyOmit<T, K>        — hand-written, and key-checked
//    (unlike the standard Omit, yours must reject unknown keys)
// 4. Getters<T>          — { getName(): string; getAge(): number; ... }
//                          Skip method-valued keys.
// 5. Setters<T>          — { setName(v: string): void; ... }
// 6. NonFunctionKeys<T>  — union of keys whose values are not functions
// 7. DataOnly<T>         — T with all function-valued keys removed
// 8. Nullable<T>         — every property also accepts null
// 9. PrefixKeys<T, P>    — rename every key to `${P}_${K}`

// 10. Given these, build ApiRoutes: every combination of
//     "GET" | "POST" with "/users" | "/posts", as `${Method} ${Path}`.

// Proofs
type Assert<T extends true> = T;
type Eq<A, B> = (<X>() => X extends A ? 1 : 2) extends (<X>() => X extends B ? 1 : 2) ? true : false;

type P1 = Assert<Eq<Mutable<{ readonly a: string }>, { a: string }>>;
type P2 = Assert<Eq<Concrete<{ a?: string }>, { a: string }>>;
type P3 = Assert<Eq<NonFunctionKeys<Person>, "id" | "name" | "age" | "email">>;
type P4 = Assert<Eq<PrefixKeys<{ a: string }, "x">, { x_a: string }>>;
type P5 = Assert<Eq<ApiRoutes, "GET /users" | "GET /posts" | "POST /users" | "POST /posts">>;

const g: Getters<Person> = {
  getId: () => "1",
  getName: () => "Ada",
  getAge: () => 36,
  getEmail: () => undefined,
};

// These must be errors. Keep both, with @ts-expect-error.
type Bad1 = MyOmit<Person, "nmae">;
const m: Mutable<Person> = { id: "1", name: "a", age: 1, greet: () => {} };
m.id = "2";
```

**Requirements:**

1. All five assertions pass.
2. `MyOmit` constrains `K extends keyof T` so the typo is an error — fixing the flaw in the standard `Omit` noted in P2-L4.
3. `Getters` and `Setters` skip `greet` — a method should not become `getGreet`.
4. `Getters<Person>` handles the optional `email` correctly; note what its return type is and why.
5. The second engineered error is subtle: `Mutable<Person>` *should* allow `m.id = "2"`. Work out why the line errors as written, and fix the `@ts-expect-error` placement or the type accordingly. This is a deliberate trap — the learner must decide which line is actually wrong.

## Acceptance Criteria

- `npx tsc --noEmit mapped-types.ts` produces no output.
- No standard utility types used; every one is hand-written.
- `Getters<Person>` has exactly four members, no `getGreet`.
- The learner has resolved the step-5 trap and explained it in a comment: `Mutable` strips `readonly`, so `m.id = "2"` is legal and the `@ts-expect-error` on it is itself the error (`TS2578`).

## Compiler Checks

Expected:

- `TS2344: Type 'false' does not satisfy the constraint 'true'.` — any failing assertion.
- `TS2344: Type '"nmae"' does not satisfy the constraint 'keyof Person'.` — the engineered `MyOmit` error, which the standard `Omit` would not produce.
- `TS2578: Unused '@ts-expect-error' directive.` — the step-5 trap. This is the diagnostic that tells the learner their assumption was wrong, and it is a good demonstration of why `@ts-expect-error` is better than `@ts-ignore`.
- `TS2344: Type 'K' does not satisfy the constraint 'string'.` with follow-on lines walking down through `Type 'keyof T' is not assignable to type 'string'` to `Type 'number' is not assignable to type 'string'` — from `Capitalize<K>` without `string & K`. The chain spells out the cause: `keyof T` includes `number` and `symbol`.
- `TS2590: Expression produces a union type that is too complex to represent.` — if a template literal is fed too many union slots. Have them try `` `${string}${string}` `` variants to see the boundary.
- `TS2536` if a remapped key is used to index without a constraint.

## Common Mistakes

- Writing `[K in T]` instead of `[K in keyof T]` when `T` is an object type.
- Forgetting `string &` in template interpolation of `keyof T`.
- Expecting a mapped type to preserve methods when the map targets `T[K]` as a property — methods *are* properties here, so filtering them out requires an explicit `T[K] extends Function` check.
- Mapping over `keyof T` and losing the optionality or readonly-ness accidentally: `{ [K in keyof T]: T[K] }` preserves both modifiers as homomorphic behaviour, but adding `as` remapping breaks homomorphism and drops them. This is subtle and worth demonstrating.
- Assuming `Capitalize` works on a non-literal `string`. `Capitalize<string>` is just `string`.
- Building `never`-keyed entries and expecting an empty-string key. `never` keys are removed entirely.
- Treating template literal unions as free. They are eagerly expanded and can exhaust the compiler.

## Everyday vs Type-Fluency Note

**Everyday:** The mapped types you will actually write are `DeepPartial`, `Mutable`, and a filter that drops functions from a class before serializing it. Key remapping with template literals shows up in form builders and ORM query types — you will read it more than write it.

**Type-fluency:** Two mechanics repay real study. **Homomorphic mapped types** (`[K in keyof T]` over a bare type parameter) preserve `readonly` and `?` and distribute over unions and arrays — mapping over `T[] ` gives you an array, not an object. Adding `as` remapping makes the type non-homomorphic, silently changing that behaviour. Second, template literal types combined with `infer` enable type-level string parsing — splitting a path into route params, parsing a query string, validating a format at compile time. That is the technique behind typed routers and typed SQL builders.

## Bridge

You can compute types from types. Next lesson: the boundary where TypeScript meets code it did not check — modules, declaration files, and how to describe JavaScript that has no types of its own.
