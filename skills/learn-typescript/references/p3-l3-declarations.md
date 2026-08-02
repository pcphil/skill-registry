# P3-L3: Modules, Declaration Files & Ambient Types

## Concept

A `.d.ts` file contains types and no implementation. It is how TypeScript describes code it cannot see — untyped JavaScript libraries, globals injected by a host, or a compiled bundle whose source is gone.

The rule that governs everything else: **a file with a top-level `import` or `export` is a module; a file without one is a script, and its declarations are global.** This single distinction explains most "why can't it find my type?" confusion.

```ts
// shapes.d.ts — no imports/exports at top level: these are GLOBAL
declare type Point = { x: number; y: number };
declare const BUILD_ID: string;

// shapes.d.ts with `export {}` added: now a module, nothing is global
```

`declare` means "this exists at run time; trust me." No implementation is permitted, and nothing is emitted.

**Describing an untyped module.** Which tool you reach for depends on whether the module is *yours* or a package:

```ts
// A package with no types — an ambient module declaration, in any .d.ts
declare module "legacy-lib" {
  export function transform(input: string): string;
  export default transform;
}
```

For a **local** JavaScript file, an ambient declaration is not an option: `declare module "./legacy"` is `TS2436: Ambient module declaration cannot specify relative module name`. Relative specifiers resolve through the filesystem, so the declaration has to live there too — put `legacy.d.ts` beside `legacy.js` and write plain exports, no `declare module` wrapper:

```ts
// legacy.d.ts, sitting next to legacy.js
export function slugify(input: string, separator?: string): string;
export function version(): string;
```

That is the rule worth remembering: **ambient module declarations are for non-relative specifiers; sibling `.d.ts` files are for relative ones.**

**Module augmentation** reopens an existing module to add to it. This is where declaration merging (P1-L6) earns its keep, and it is why those types must be `interface`:

```ts
declare module "express" {
  interface Request {
    user?: { id: string };
  }
}
```

**Global augmentation** uses `declare global` from inside a module:

```ts
declare global {
  interface Window { analytics?: { track(e: string): void } }
  namespace NodeJS { interface ProcessEnv { API_KEY?: string } }
}
```

Note `API_KEY?: string`, not `string`. An environment variable may genuinely be absent, and typing it as present is a lie the compiler will then help you act on.

Two practical notes. `import type { X }` imports only the type and is guaranteed erased — necessary when `isolatedModules` or a bundler is in play. And `declare module "*.svg"` is how you teach the compiler about non-code imports your bundler handles.

## Analogy

A `.d.ts` file is a museum placard next to an artefact nobody can open. The placard describes what the thing is, what it does, and how to handle it — and if the placard is wrong, nothing stops you believing it. There is no verification step, because the artefact is sealed.

Module augmentation is adding a line to an existing placard rather than putting up a second one beside it. And the module-versus-script rule is the difference between a placard in a display case and a sign bolted to the museum wall: one is scoped to its exhibit, the other is visible from every room. Adding a single `export {}` moves the sign into the case.

## Workshop

**Files:** `shapes.d.ts` and `consumer.ts` (plus `legacy.js`, `legacy.d.ts`, `globals.d.ts`, `types-only.ts`)

**Problem:** Describe an untyped JavaScript module and a set of globals, then consume them from a typed file with no casts. This lesson deliberately exercises both declaration mechanisms, because choosing between them is the actual skill.

First create the untyped implementation, `legacy.js` — plain JavaScript, no types:

```js
// legacy.js
function slugify(input, separator) {
  return String(input).toLowerCase().trim().replace(/\s+/g, separator || "-");
}
function version() {
  return "1.4.2";
}
module.exports = { slugify, version };
```

**Step 1 — try the wrong tool first.** In `shapes.d.ts`, write `declare module "./legacy" { … }`. Run the check, record the error, and note why a relative specifier cannot be declared ambiently. Then delete it.

**Step 2 — `legacy.d.ts`,** a sibling of `legacy.js`, declaring `slugify` and `version` as plain exports.

**Step 3 — `shapes.d.ts`,** kept as a *script* (no top-level import or export):

```ts
// 1. Global type Point: x and y numbers.
// 2. Global const BUILD_ID: string.
// 3. declare module "*.svg" whose default export is a string.
```

**Step 4 — `globals.d.ts`,** a *module* (it ends with `export {}`), using `declare global` to add:

```ts
// 4. var __DEV__: boolean       -- so globalThis.__DEV__ is typed
// 5. interface Window { analytics?: { track(e: string): void } }
```

**Step 5 — `consumer.ts`:**

```ts
// 6.  Import from "./legacy" and use both functions. No casts.
// 7.  Use the global Point type without importing it.
// 8.  Read BUILD_ID, globalThis.__DEV__, and bare __DEV__.
// 9.  Import a .svg file and assign it to a string.
// 10. Write distance(a: Point, b: Point): number.
// 11. Add `import type { X } from "./types-only"` where types-only.ts
//     exports only a type. Confirm the import is erased — emit with
//     `npx tsc --outDir dist` and read dist/consumer.js.
```

**Requirements:**

1. `npx tsc --noEmit` over the project is clean, with `allowJs` off — the compiler learns about `legacy.js` from `legacy.d.ts` only.
2. The step-1 error is recorded in a comment with its actual text.
3. `shapes.d.ts` stays a script. Adding `export {}` to it must break `consumer.ts`; have the learner try it, record which errors appear and on which lines, then revert.
4. Renaming `legacy.d.ts` away must also break the build — have them try it and record that error too. It is *not* the same error as a module that does not exist at all, and the difference is instructive.
5. No `as`, no `any` in `consumer.ts`.
6. The emitted `dist/consumer.js` contains no reference to the type-only import.
7. `__DEV__` is declared with `var` inside `declare global`. Have the learner try `let` or `const` instead and explain the difference — only `var` declarations become properties of `globalThis`.

## Acceptance Criteria

- `npx tsc --noEmit` reports nothing across the project.
- Renaming `legacy.d.ts` away produces `TS7016` — proving the declaration was doing the work, not inference.
- `dist/consumer.js` has no import for the type-only module.
- The step-1 and script-vs-module experiments are both documented in comments with their actual error text.

## Compiler Checks

Expected:

- `TS2436: Ambient module declaration cannot specify relative module name.` — step 1, the engineered wrong-tool error.
- `TS7016: Could not find a declaration file for module './legacy'. '…/legacy.js' implicitly has an 'any' type.` — when `legacy.d.ts` is missing. Note it is **not** `TS2307`: the `.js` file resolves fine, so the module exists and only its types are absent. `TS2307: Cannot find module './legacy' or its corresponding type declarations.` is what you get when nothing resolves at all — worth showing both, since they call for different fixes (`TS7016` wants a declaration, `TS2307` wants a path or an install).
- `TS2304: Cannot find name 'Point'.` and `TS2304: Cannot find name 'BUILD_ID'.` — the errors that appear the moment `export {}` is added to `shapes.d.ts`, reported at every use site in `consumer.ts`. This is the payoff of the experiment.
- `TS7017: Element implicitly has an 'any' type because type 'typeof globalThis' has no index signature.` — reading `globalThis.__DEV__` before the `declare global` block exists, or after declaring `__DEV__` with `const`/`let` instead of `var`.
- `TS1046: Top-level declarations in .d.ts files must start with either a 'declare' or 'export' modifier.`
- `TS1183: An implementation cannot be declared in ambient contexts.` — if a function body is written in the `.d.ts`. These two fire together on the same line.
- `TS2664: Invalid module name in augmentation, module '…' cannot be found.` — when augmenting a module that does not resolve. The distinction between *declaring* a module that has no types and *augmenting* one that does is the trap here.

## Common Mistakes

- Adding an `import` to a `.d.ts` that declares globals, silently turning every global into a module-scoped type. The most common `.d.ts` mistake by a wide margin.
- Reaching for `declare module "./relative/path"`. Ambient module declarations take non-relative specifiers only; a local file needs a sibling `.d.ts`.
- Declaring a global with `const` or `let` and then reading it off `globalThis`. Only `var` declarations become `globalThis` properties.
- Writing implementations in a `.d.ts`. It is types only.
- Using `type` for something a consumer needs to augment. Augmentation requires `interface`.
- Typing `process.env.API_KEY` as `string`. It is `string | undefined` in reality, and lying makes the compiler stop protecting you at exactly the point it matters.
- Confusing `declare module "x" { }` (declaring a module that has no types) with `declare module "x" { }` inside a file that imports `"x"` (augmenting it). Same syntax, different meaning depending on whether the module resolves.
- Forgetting `import type` and having a bundler emit a run-time import of a file that only ever held types.
- Reaching for a `.d.ts` when the real answer is `@types/thelibrary` from DefinitelyTyped. Check there first.

## Everyday vs Type-Fluency Note

**Everyday:** Most projects need exactly three things from this lesson: a `.d.ts` for asset imports, one `declare global` block for genuinely global values, and `import type` where the bundler requires it. Before hand-writing a module declaration, check whether `@types/*` already exists.

**Type-fluency:** Module resolution is where the real complexity lives — `moduleResolution: "bundler" | "node16" | "nodenext"`, the `exports` field in `package.json`, `types` versus `typesVersions`, and dual CJS/ESM packages that need two sets of declarations. If you publish a library, this is the part that determines whether your consumers get types at all. `declare module` with a wildcard, ambient namespaces, and `export =` interop are the tools for the awkward cases.

## Bridge

You can describe code the compiler cannot see. Next lesson: typing asynchronous code — `Promise`, `Awaited`, and the fact that TypeScript cannot type what a function throws.
