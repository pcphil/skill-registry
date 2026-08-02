# P1-L2: Primitives, Inference, Literal Types

## Concept

TypeScript infers a type for every value you write. You rarely need to annotate; you need to know what it inferred.

The primitives: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`. Lowercase always — `String` is the wrapper object and is almost never what you want.

The important idea is **literal types**. `"hello"` is not just a `string`; it is the type `"hello"`, a type with exactly one member. Whether you get the literal type or the wide type depends on mutability:

| Declaration | Inferred type | Why |
|-------------|---------------|-----|
| `const a = "hi"` | `"hi"` | Can never change, so the narrow type is safe |
| `let b = "hi"` | `string` | Could be reassigned, so TypeScript widens |
| `let c: "hi" = "hi"` | `"hi"` | Annotation defeats widening |
| `const d = { k: "hi" }` | `{ k: string }` | The property is mutable even though `d` is `const` |

That last row surprises everyone. `const` freezes the binding, not the object, so properties widen. `as const` opts out:

```ts
const e = { k: "hi" } as const;  // { readonly k: "hi" }
```

Literal types are what make unions useful. `type Status = "idle" | "loading" | "done"` is a real, checkable type precisely because each member is a literal.

## Analogy

A wide type is a job posting: "we need a string." A literal type is a name on a guest list: "we need the string `admin`." Both are constraints, but one admits infinitely many candidates and the other admits exactly one.

`let` is a job posting because the position can be refilled tomorrow — TypeScript has to describe everyone who could ever hold it. `const` is a name on a list, because that slot is settled forever.

## Workshop

**File:** `primitives.ts`

**Problem:** Model a log level and a log entry using literal types, and make the compiler reject invalid levels.

Starter:

```ts
// 1. Replace this with a union of the four literal levels.
type LogLevel = string;

// 2. Annotate the parameters. Do not change the body.
function formatLog(level, message) {
  return `[${level.toUpperCase()}] ${message}`;
}

// 3. These four calls must compile.
console.log(formatLog("debug", "starting"));
console.log(formatLog("info", "listening on 3000"));
console.log(formatLog("warn", "retrying"));
console.log(formatLog("error", "connection lost"));

// 4. This call must be an error. Leave it in the file — do not delete it.
console.log(formatLog("critical", "meltdown"));

// 5. Declare DEFAULT_LEVEL so its inferred type is the literal "info",
//    not string. Do not annotate it.
const DEFAULT_LEVEL = "info";
```

**Requirements:**

1. `LogLevel` is a union of exactly `"debug"`, `"info"`, `"warn"`, `"error"`.
2. `formatLog` takes a `LogLevel` and a `string`.
3. The `"critical"` call reports an error — mark it with `// @ts-expect-error` on the line above so the file still compiles clean. This is the one place in the course where a suppression comment is the right answer, because you are asserting that an error *must* occur.
4. Add a line proving `DEFAULT_LEVEL` is assignable to `LogLevel`.

## Acceptance Criteria

- `npx tsc --noEmit primitives.ts` produces no output.
- `LogLevel` is a literal union, not `string` and not an enum.
- The `"critical"` call is still present, preceded by `@ts-expect-error`.
- Removing the `@ts-expect-error` comment reintroduces exactly one error. Have the learner try it.

## Compiler Checks

Expected while working:

- `TS7006: Parameter 'level' implicitly has an 'any' type.` — until step 2 is done.
- `TS2345: Argument of type '"critical"' is not assignable to parameter of type 'LogLevel'.` — this is the error the lesson is engineering. Note that TypeScript names the literal type `'"critical"'` in the message, quotes and all.
- `TS2578: Unused '@ts-expect-error' directive.` — appears if they add the suppression to a line that does *not* error. It makes `@ts-expect-error` self-checking, unlike `@ts-ignore`.

Clean run prints nothing.

## Common Mistakes

- Writing `type LogLevel = "debug" || "info"` — the union operator in types is `|`, not `||`.
- Using `String` instead of `string`.
- Reaching for `enum`. Enums are a runtime construct that emits JavaScript; literal unions are erased entirely and are the idiomatic choice.
- Declaring `let DEFAULT_LEVEL = "info"` and wondering why its type is `string`.
- Using `@ts-ignore` instead of `@ts-expect-error`. `@ts-ignore` stays silent forever, including after the underlying bug is fixed.

## Everyday vs Type-Fluency Note

**Everyday:** Annotate function parameters and public return types; let everything else infer. Over-annotating locals is noise that goes stale. Literal unions are the workhorse for status fields, action names, and config keys.

**Type-fluency:** Widening is a real algorithm with rules worth internalizing — literal widening on mutable bindings, fresh-object-literal freshness checks, and `as const` producing deeply readonly literal types. The interaction between widening and generic inference is the source of most "why did it infer `string` here?" confusion later in the course.

## Bridge

You can now describe a single value precisely. Next lesson: describing collections — arrays, tuples, and object types — and the difference between "an array of strings" and "exactly two strings".
