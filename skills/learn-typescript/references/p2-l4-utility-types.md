# P2-L4: Utility Types

## Concept

The standard library ships transformations built from `keyof`, indexed access, and mapped types. Nothing here is magic — you could write all of them, and in Phase 3 you will.

The ones that carry real weight:

| Utility | Does | Typical use |
|---------|------|-------------|
| `Partial<T>` | every property optional | patch / update payloads |
| `Required<T>` | every property required | after validation |
| `Readonly<T>` | every property `readonly` | frozen config |
| `Pick<T, K>` | keep only keys `K` | narrow a view |
| `Omit<T, K>` | drop keys `K` | strip `id` before insert |
| `Record<K, V>` | object with keys `K`, values `V` | lookup maps |
| `ReturnType<F>` | a function's return type | derive from an implementation |
| `Parameters<F>` | a function's parameters as a tuple | wrapping / forwarding |
| `Awaited<P>` | unwrap a promise | async return types |
| `NonNullable<T>` | remove `null` and `undefined` | after a guard |
| `Exclude<T, U>` / `Extract<T, U>` | filter a union | narrow literal unions |

Two behavioural notes that cause real bugs.

**`Pick` is key-checked; `Omit` is not.** `Pick<User, "nmae">` is an error. `Omit<User, "nmae">` compiles silently and omits nothing, because `Omit` is defined via `Exclude` over `keyof T`, which accepts any string. A typo'd `Omit` is invisible.

**`Partial` is shallow.** `Partial<{ a: { b: string } }>` makes `a` optional but leaves `b` required. Deep partial requires recursion (Phase 3).

The `ReturnType` pattern deserves its own mention because it inverts the usual dependency:

```ts
function makeUser(name: string) {
  return { id: crypto.randomUUID(), name, createdAt: new Date() };
}
type User = ReturnType<typeof makeUser>;
```

The type now follows the implementation automatically. Add a field to the return object and `User` grows. This is derivation rather than declaration, and it is how you eliminate the drift between a factory and its type.

## Analogy

Utility types are the standard kitchen prep verbs. You don't write a new recipe for "dice"; you apply dicing to whatever ingredient you have. `Pick` is trimming to the cut you want, `Omit` is removing the bone, `Partial` is "any of these garnishes, optional", `Record` is a labelled spice rack with a fixed set of labels.

And the `Omit` typo hazard has a kitchen analogue: an order that says "hold the pickels." Nobody objects, nothing is held, and the mistake only surfaces when you bite into it.

## Workshop

**File:** `utility-types.ts`

**Problem:** Model create/update/view operations on an entity using derived types only — no hand-written variant shapes.

Starter:

```ts
interface Article {
  id: string;
  slug: string;
  title: string;
  body: string;
  authorId: string;
  publishedAt: Date | null;
  viewCount: number;
}

// Derive every type below. Do not write an object shape by hand.

// 1. NewArticle — everything needed to create one, except
//    id, publishedAt, and viewCount (the server sets those).

// 2. ArticlePatch — the id is required, everything else optional.

// 3. ArticleListItem — only id, slug, title, publishedAt.

// 4. FrozenArticle — Article, fully readonly.

// 5. ArticlesBySlug — a lookup from slug string to Article.

// 6. Given this factory, derive Created from its return type.
function createArticle(input: NewArticle) {
  return {
    ...input,
    id: "generated",
    publishedAt: null as Date | null,
    viewCount: 0,
  };
}

// 7. Derive CreateArgs from createArticle's parameters (a tuple).

// 8. PublishState — from Article["publishedAt"], remove null.

// Proofs
const draft: NewArticle = {
  slug: "hello",
  title: "Hello",
  body: "...",
  authorId: "a1",
};

const patch: ArticlePatch = { id: "x1", title: "New title" };
const listed: ArticleListItem = { id: "x1", slug: "hello", title: "Hello", publishedAt: null };
const created: Created = createArticle(draft);
const args: CreateArgs = [draft];
const published: PublishState = new Date();

// These must be errors. Keep all three, with @ts-expect-error.
const frozen: FrozenArticle = created;
frozen.title = "nope";

const missingId: ArticlePatch = { title: "no id" };

const badPick: ArticleListItem = { id: "x1", slug: "s", title: "t", publishedAt: null, body: "extra" };
```

**Requirements:**

1. Every type in steps 1–8 is derived with utilities. Zero hand-written property lists.
2. `ArticlePatch` combines `Partial` with a required `id` — an intersection or `&` with `Pick`.
3. `Created` uses `ReturnType<typeof createArticle>`.
4. `PublishState` uses `NonNullable`.
5. Add a comment demonstrating the `Omit` typo hazard: write `Omit<Article, "titel">` and note that it compiles and omits nothing, then compare with `Pick<Article, "titel">`, which errors.

## Acceptance Criteria

- `npx tsc --noEmit utility-types.ts` produces no output.
- Adding a field to `Article` automatically flows into `NewArticle`, `ArticlePatch`, and `FrozenArticle` — have the learner add one, confirm, then remove it.
- The `Omit` hazard comment is present and accurate.
- All three engineered errors are suppressed and each fails for the stated reason.

## Compiler Checks

Expected:

- `TS2540: Cannot assign to 'title' because it is a read-only property.` — from `FrozenArticle`.
- `TS2322: Type '{ title: string; }' is not assignable to type 'ArticlePatch'.` with the follow-on line `Property 'id' is missing in type '{ title: string; }' but required in type 'Pick<Article, "id">'.` — proving the `id` stayed required through the `Partial`. Note the detail line names the `Pick`, not the alias: intersections report against the specific constituent that failed, which is why derived types can produce error messages that mention parts the learner never wrote by name.
- `TS2353: Object literal may only specify known properties, and 'body' does not exist in type 'ArticleListItem'.` — excess property check against a `Pick`. (`body` is not close to any remaining key, so there is no suggestion; a near-miss like `titel` would report `TS2561` with a "Did you mean" instead.)
- `TS2344: Type '"titel"' does not satisfy the constraint 'keyof Article'.` — from the `Pick` half of the hazard demo. The `Omit` half produces **no error at all**, which is the entire point.
- `TS2739` listing missing properties if `NewArticle` is built with `Pick` instead of `Omit` and misses a field.

## Common Mistakes

- Hand-writing `NewArticle` "just to be explicit". It compiles today and drifts tomorrow — this is the failure the lesson exists to prevent.
- Using `Partial<Article>` alone for a patch, leaving no required `id`, so a patch identifying nothing type-checks.
- Trusting `Omit` key names. Prefer `Omit<T, keyof Pick<T, "a" | "b">>` when it matters, or just be aware.
- Expecting `Partial` to be deep.
- `Record<string, Article>` where every lookup then appears defined. Under `strict` without `noUncheckedIndexedAccess`, `map["missing"]` is typed `Article`, not `Article | undefined` — a real source of run-time crashes.
- Forgetting `typeof` in `ReturnType<typeof fn>` and writing `ReturnType<fn>`, which gives `TS2749`.

## Everyday vs Type-Fluency Note

**Everyday:** `Pick`, `Omit`, `Partial`, and `Record` cover most day-to-day needs, and the `ReturnType<typeof factory>` idiom is worth adopting broadly — it makes the implementation the single source of truth. The rule to internalize: if two types must agree, derive one from the other rather than maintaining both.

**Type-fluency:** Read the actual definitions in `lib.es5.d.ts`. `Pick` is a mapped type, `Omit` is `Pick<T, Exclude<keyof T, K>>`, `Exclude` is a distributive conditional type. Once you can read those four lines, every utility type is transparent and you can write your own — `DeepPartial`, `RequireAtLeastOne`, `Mutable`. That is Phase 3's material, and `Omit`'s missing key constraint becomes an easy thing to fix yourself.

## Bridge

You can derive shapes from other shapes. Next lesson: discriminated unions and exhaustiveness — how to model "one of several possible states" so the compiler forces you to handle every one.
