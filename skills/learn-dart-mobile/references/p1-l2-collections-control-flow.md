# P1-L2: Collections & Control Flow

## Concept

Dart's core collections: `List<T>` (ordered, indexable), `Map<K, V>` (key-value pairs), `Set<T>` (unique, unordered). All are generic — `List<String>` only holds strings, checked at compile time.

Control flow is familiar (`if`/`else`, `for`, `while`) but Dart adds collection-oriented sugar: `for-in` loops, collection `if`/`for` inside list literals (`[if (x) 'a', for (final y in ys) y]`), and a rich set of `Iterable` methods — `.map()`, `.where()`, `.fold()` — that transform collections without manual loops.

`for (final task in tasks)` is preferred over index-based loops when you don't need the index. Use `.where()` to filter, `.map()` to transform, and chain them instead of writing multi-line imperative loops when the transformation is simple.

## Analogy

A `List` is a numbered row of lockers — order matters, and you can ask for locker #3 directly. A `Set` is a bag of unique tokens — no duplicates, no particular order, you can only ask "is this token in the bag?". A `Map` is a filing cabinet with labeled folders — you look things up by label (key), not by position.

## Workshop

**Continue in the same `.dart` file (or a new one, e.g. `task_list.dart`).**

**Task:** Model a small in-memory task list:
- Create a `List<Map<String, dynamic>>` where each map has `title` (String) and `done` (bool).
- Seed it with at least 5 tasks, some done and some not.
- Write a function `List<String> incompleteTitles(List<Map<String, dynamic>> tasks)` that returns the titles of all tasks where `done == false`, using `.where()` and `.map()` — not a manual for-loop with an if-check appending to a new list.
- Print the count of incomplete tasks and their titles.

## Acceptance Criteria / Edge Cases

- Uses `.where(...).map(...)` chain (or equivalent functional style), not a hand-rolled loop with `.add()`.
- Correctly handles an empty task list (returns an empty list, not an error).
- Correctly handles all-done and all-incomplete cases.

## Common Mistakes

- Using `List<dynamic>` for the whole list instead of `List<Map<String, dynamic>>` — loses type safety on the map keys.
- Forgetting `.toList()` after `.where()`/`.map()` — those return lazy `Iterable`s, not `List`s, which matters if you need indexing or `.length` immediately.
- Mutating the list while iterating over it directly (modify a copy or collect changes separately).

## Ship vs Portfolio Note

**Ship a real app:** this raw `Map`-based modeling is intentionally temporary — lesson 3 replaces it with a proper `Task` class. Real apps should never pass loosely-typed maps around for domain data; it's a common source of typo bugs (`'titel'` vs `'title'`) that the compiler can't catch.

**Learning/portfolio:** notice the pain of stringly-typed keys here — that discomfort is the motivation for the next lesson's class-based model.

## Bridge

Maps work, but typos in string keys won't be caught by the compiler and there's no way to add behavior to the data. Next: OOP — you'll define a proper `Task` class.
