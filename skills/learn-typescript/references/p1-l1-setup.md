# P1-L1: Setup, tsconfig, Strict Mode, --noEmit

## Concept

TypeScript is not a runtime. It is a **checker** that reads your code, proves things about it, then erases every type annotation and hands plain JavaScript to the runtime. Nothing you write in the type system exists at run time.

That split explains the whole workflow. Two separate jobs:

| Job | Command | What it produces |
|-----|---------|------------------|
| Check types | `tsc --noEmit` | Errors only, no files |
| Check + compile | `tsc` | `.js` files next to your `.ts` files |
| Run directly | `npx tsx file.ts` | Program output, checking skipped |

Throughout this course we use `--noEmit`. We care about whether the types are *provable*, not about producing JavaScript.

`tsconfig.json` configures the checker. The single setting that matters most is `"strict": true`. It is an umbrella for about eight flags; two you will feel immediately:

- `noImplicitAny` — a parameter with no annotation and no inferable type is an error, not a silent `any`.
- `strictNullChecks` — `null` and `undefined` stop being assignable to every type. This is the flag that turns TypeScript from decoration into a real proof system.

Without `strict`, TypeScript will happily agree with almost anything you write. Learning TypeScript with `strict` off is learning a different, weaker language.

## Analogy

Think of a building inspector who walks the blueprints before anyone pours concrete. The inspector never touches the building — they read the plans, flag "this beam can't carry that load", and leave. The construction crew then builds from plans with all the inspector's annotations stripped off. That is `tsc`: it inspects, it reports, and the thing that actually runs has none of its markings.

`strict: false` is an inspector who signs off on everything without reading. You still get a stamp. It just doesn't mean anything.

## Workshop

**File:** `hello.ts`

**Problem:** Set up a checked TypeScript file and make the compiler talk to you. The goal of this lesson is not to write clever types — it is to see the toolchain reject bad code and then accept good code.

Set up first:

```bash
mkdir ts-course && cd ts-course
npm init -y
npm install --save-dev typescript
npx tsc --init
```

Open the generated `tsconfig.json` and confirm `"strict": true` is present and uncommented.

Now create `hello.ts` containing exactly this, and run `npx tsc --noEmit`:

```ts
function greet(name) {
  return "Hello, " + name;
}

let message: string = greet("world");
message = 42;

console.log(message.toUpperCase());
```

**Requirements:**

1. Run the check and read the errors. Do not fix anything yet — report how many errors you get and what they say.
2. Fix them one at a time, re-running `npx tsc --noEmit` after each fix, until the output is clean.
3. Keep `greet` returning a string and keep `message` a `string`.

## Acceptance Criteria

- `npx tsc --noEmit` produces no output at all.
- `greet` has an explicitly annotated parameter.
- No `any`, no `@ts-ignore`, no `@ts-expect-error` anywhere in the file.
- The `message = 42` line is gone or corrected to a string — not silenced.

## Compiler Checks

The starter file should produce two errors:

- `TS7006: Parameter 'name' implicitly has an 'any' type.` — from `noImplicitAny`. Fix by annotating `name: string`.
- `TS2322: Type 'number' is not assignable to type 'string'.` — from the reassignment. Fix by removing the line or assigning a string.

A clean run prints nothing and exits 0. Silence is success — this trips people up the first time.

If the learner sees no errors at all, `strict` is off. Have them check `tsconfig.json` before continuing; every later lesson assumes it.

## Common Mistakes

- Running `tsc` instead of `npx tsc` and hitting a globally installed version of a different vintage.
- Editing `tsconfig.json` but leaving `"strict"` inside a comment block — `tsc --init` comments out most options.
- Silencing `TS7006` with `name: any` — this passes the compiler and defeats the lesson.
- Expecting a success message. There isn't one.

## Everyday vs Type-Fluency Note

**Everyday:** `--noEmit` in a checking script and `strict: true` from day one is the whole setup story for most projects. Bundlers (Vite, esbuild, tsx) strip types without checking them, so `tsc --noEmit` in CI is what actually catches bugs.

**Type-fluency:** Worth knowing which flags `strict` turns on individually — `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`. Each has its own failure mode, and `strictFunctionTypes` in particular will matter when we reach variance.

## Bridge

You have a compiler that argues with you. Next lesson: what it actually knows about a value the moment you write it down — inference, primitives, and why `const x = "hi"` and `let x = "hi"` get different types.
