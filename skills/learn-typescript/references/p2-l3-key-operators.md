# P2-L3: keyof, typeof, Indexed Access

## Concept

Three operators that let types read other types. Together they are how you stop writing types by hand and start deriving them.

| Operator | Reads | Example | Result |
|----------|-------|---------|--------|
| `keyof T` | the keys of a type | `keyof { a: 1; b: 2 }` | `"a" \| "b"` |
| `typeof x` | the type of a *value* | `typeof config` | the config's shape |
| `T[K]` | the type at a key | `User["name"]` | `string` |

**`keyof`** produces a union of literal key types. On a type with an index signature `{ [k: string]: T }` it produces `string | number` — the `number` because JavaScript coerces numeric keys.

**`typeof`** here is the *type-level* operator, unrelated to the runtime `typeof` in an `if`. Same keyword, two different languages sharing one file. It is the bridge from value world to type world:

```ts
const config = { host: "localhost", port: 3000 };
type Config = typeof config;              // { host: string; port: number }
type ConfigKey = keyof typeof config;     // "host" | "port"
```

That second line is the single most useful idiom in this lesson. It reads right to left: take the type of this value, then take its keys.

**Indexed access** `T[K]` works with unions and with `number` on arrays:

```ts
type Values = User[keyof User];        // union of all property types
type Element = string[][number];       // string  — how you get an array's element type
```

Combine them and you get the safe-accessor pattern that appears in every real codebase:

```ts
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

`K extends keyof T` is what makes this both safe and precise: the compiler rejects unknown keys *and* returns the exact type of the requested property rather than a union.

## Analogy

`keyof` is asking for the index of a book — you get the list of chapter titles, not the chapters. `T[K]` is then turning to a specific chapter. And `typeof` is scanning a physical object to produce its blueprint: you have a machine on the bench, and you want the schematic derived from it rather than drawn by hand.

The reason this matters: a hand-drawn schematic drifts from the machine. A scanned one cannot. `keyof typeof config` can never disagree with `config`.

## Workshop

**File:** `key-operators.ts`

**Problem:** Build a type-safe property accessor and derive a settings type from a runtime object rather than declaring it twice.

Starter:

```ts
const defaults = {
  host: "localhost",
  port: 3000,
  secure: false,
  retries: 3,
};

// 1. Derive Settings from `defaults` — do not write the shape by hand.
// 2. Derive SettingKey as the union of its keys.

// 3. get: type-safe accessor. get(defaults, "port") must be typed number,
//    and get(defaults, "nope") must be an error.
function get(obj, key) {
  // your code
}

// 4. pluck: given an array of objects and a key, return an array of
//    that property's values.
//    pluck([{id:1},{id:2}], "id") must be typed number[]
function pluck(items, key) {
  // your code
}

// 5. setOne: return a copy of obj with one key replaced.
//    The new value must be constrained to that key's type.
//    setOne(defaults, "port", 8080) is fine.
//    setOne(defaults, "port", "8080") must be an error.
function setOne(obj, key, value) {
  // your code
}

// 6. Derive SettingValue as the union of all value types in Settings.

// Proofs
const p: number = get(defaults, "port");
const h: string = get(defaults, "host");
const ids: number[] = pluck([{ id: 1 }, { id: 2 }], "id");
const updated: Settings = setOne(defaults, "port", 8080);
const anyValue: SettingValue = true;

// These must be errors. Keep both, with @ts-expect-error.
get(defaults, "nope");
setOne(defaults, "port", "8080");
```

**Requirements:**

1. `Settings` is derived with `typeof`, not written out. Adding a key to `defaults` must extend `Settings` automatically — have the learner add one, confirm, then remove it.
2. `get` returns `T[K]`, so `get(defaults, "port")` is `number` and not `string | number | boolean`.
3. `pluck` uses two type parameters with `K extends keyof T`.
4. `setOne` constrains its value parameter to `T[K]`.
5. `SettingValue` is derived via `Settings[keyof Settings]`.

## Acceptance Criteria

- `npx tsc --noEmit key-operators.ts` produces no output.
- Hovering `get(defaults, "port")` shows `number`, not a union.
- Both engineered errors are suppressed; removing either comment produces exactly one error.
- No literal key strings appear in any type declaration — every key type is derived.

## Compiler Checks

Expected:

- `TS2345: Argument of type '"nope"' is not assignable to parameter of type '"host" | "port" | "secure" | "retries"'.` — note the compiler expands `keyof Settings` in the message, which is a useful way to see what `keyof` produced.
- `TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.` — from `setOne` with a mismatched value, proving `T[K]` resolved to the specific key's type.
- `TS2536: Type 'K' cannot be used to index type 'T'.` — if `K` is declared without `extends keyof T`. This is the diagnostic that teaches why the constraint is mandatory.
- `TS2322: Type 'T[K][]' is not assignable to type 'number[]'.` — if `pluck`'s parameters are wired to the wrong type.
- `TS2749: 'defaults' refers to a value, but is being used as a type here. Did you mean 'typeof defaults'?` — the most common slip in this lesson, and the error message names the fix.

## Common Mistakes

- Writing `type Settings = defaults` and hitting `TS2749`. Values need `typeof` to cross into type space.
- Writing `keyof defaults` instead of `keyof typeof defaults`. `keyof` operates on types, so the value must be lifted first.
- Declaring `K extends string` rather than `K extends keyof T` — it compiles the signature but the body cannot index, and callers get no key checking.
- Returning `T[keyof T]` from `get` instead of `T[K]`. It compiles, and it silently gives every caller a useless union. This is the subtle failure worth flagging in review.
- Confusing type-level `typeof` with runtime `typeof`. Position decides: after a `:` or in a `type` declaration it is type-level.
- Assuming `keyof` on an interface with an index signature gives literal keys. It gives `string | number`.

## Everyday vs Type-Fluency Note

**Everyday:** `keyof typeof someObject` is the idiom to memorize — it derives a key union from a real object, so config keys, route tables, and lookup maps can never drift from their types. `<T, K extends keyof T>` is the shape of most real utilities.

**Type-fluency:** Indexed access distributes over unions (`T[A | B]` is `T[A] | T[B]`), which is what makes `Settings[keyof Settings]` collapse to a value union. `keyof` on a union gives the *intersection* of keys, not the union — one of the more surprising dualities in the system, and worth proving to yourself. These operators are also the raw material for mapped types, which is Phase 3.

## Bridge

You can read a type's keys and pull out the type at any key. Next lesson: the utility types the standard library already builds from exactly these operators — `Partial`, `Pick`, `Omit`, `Record`, `ReturnType`.
