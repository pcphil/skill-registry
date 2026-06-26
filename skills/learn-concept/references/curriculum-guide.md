# Curriculum Generation Guide

Reference for SKILL.md. Load this when generating a lesson sequence for a new concept or when crafting lesson content and analogies.

---

## Lesson Sequence Template

Generate 3–5 lessons ordered from mental model → mechanics → application. Use this as the skeleton, then adapt to the concept:

| Lesson | Title Pattern | Purpose |
|--------|--------------|---------|
| 1 | "What is [concept]" | Core mental model. What problem does it solve? What does it replace or improve on? |
| 2 | "How [concept] works" | Internal mechanics. Walk through the process step-by-step. |
| 3 | "Edge cases & gotchas" | Where it breaks, fails silently, or surprises people. |
| 4 | "Variants & relatives" | Closely related ideas — what's similar, what's different, when to pick each. |
| 5 | "When to use it" | Tradeoffs. Real-world decisions. What it costs. |

**Always include lessons 1–3.** Add 4 and/or 5 only if:
- The concept has meaningful variants (e.g. TCP vs UDP, BFS vs DFS, mutex vs semaphore)
- Tradeoff decisions are a key part of understanding it (e.g. caching strategies, database indexing)

---

## Analogy Generation Patterns

Analogies must be concrete, everyday, and map cleanly to the concept's structure — not just vaguely similar.

### What makes a good analogy

- **Structural match**: the analogy's parts map 1:1 to the concept's parts
- **Everyday setting**: no technical background needed to understand it
- **Single sentence** when used inline; can be 2–3 sentences if the lesson opens with it
- **Different from the definition**: the analogy builds intuition *before* the definition, so it must not just rephrase the definition

### Analogy patterns by concept type

**State machines / protocols**
- Pattern: physical processes with defined steps and no skipping
- Examples: vending machine (insert coin → select → dispense), traffic light cycle, airport security checkpoint

**Queues / buffers**
- Pattern: lines with ordering rules
- Examples: checkout line (FIFO), hospital triage (priority), boarding a plane by zone

**Caches / memoization**
- Pattern: shortcut storage that avoids expensive re-work
- Examples: sticky notes on a desk for frequently called phone numbers, a chef's mise en place, browser bookmarks

**Recursion**
- Pattern: a task that delegates to a smaller version of itself
- Examples: Russian nesting dolls, mirrors facing each other, legal definitions that reference themselves

**Hashing**
- Pattern: a fixed-size label derived from content
- Examples: library catalog call number, a building's floor plan turned into a postal code, fingerprints as identity shortcuts

**Trees / hierarchies**
- Pattern: parent-child containment with exactly one root
- Examples: company org chart, file system folders, family tree

**Graphs**
- Pattern: any-to-any connections with no single root
- Examples: road map (intersections = nodes, roads = edges), social network, airline routes

**Locking / concurrency**
- Pattern: exclusive access to a shared resource
- Examples: bathroom key at a diner (mutex), shared whiteboard with one marker (mutex), library's checkout system (semaphore with N copies)

**TCP / handshakes / protocols**
- Pattern: agreed ritual before exchanging important information
- Examples: two people bowing before a conversation, a phone call ("Can you hear me?" / "Yes, can you hear me?" / "Yes, go ahead"), signing a contract before work begins

**Indexes (database)**
- Pattern: pre-sorted lookup structure to avoid full scan
- Examples: book index at the back, alphabetical tabs in a binder, a phonebook sorted by last name

**Pub/sub / event systems**
- Pattern: broadcast with no direct knowledge of receivers
- Examples: radio station (broadcaster unaware of listeners), a town crier, newspaper subscriptions

**Compression**
- Pattern: encoding redundancy into shorter references
- Examples: saying "the book I mentioned earlier" instead of re-quoting it, abbreviations, ZIP codes instead of full city names

**Virtualization / abstraction layers**
- Pattern: a simplified interface hiding complex internals
- Examples: a car's steering wheel (hides engine/transmission), an ATM (hides banking backend), an elevator panel (hides cable/motor mechanics)

---

## Lesson Content Structure

Each lesson should contain these elements (in order):

1. **Analogy** — one concrete real-world metaphor (see patterns above)
2. **Formal definition** — what it actually is, 2–4 sentences
3. **Mechanics** — how it works step-by-step (numbered steps for processes, diagram-in-text for structures)
4. **Key properties or constraints** — the rules that define the concept (what's always true)
5. **Edge cases** (lesson 3 only) — what trips people up; what the concept does *not* guarantee

Keep each lesson tight. One concept per lesson. If you find yourself explaining two distinct ideas, split into two lessons.

---

## Adapting to Concept Type

**Algorithmic / code concepts** (e.g. memoization, recursion, BFS):
- Lesson 2 mechanics: trace through a small example step-by-step
- Lessons pair naturally with Build mode (coding task)

**Protocol / systems concepts** (e.g. TCP handshake, TLS, DNS):
- Lesson 2 mechanics: enumerate the phases or steps of the protocol
- Lessons pair well with either Quiz (explain back the steps) or Build (write pseudocode or a diagram description)

**Mathematical / theoretical concepts** (e.g. modular arithmetic, big-O, probability):
- Lesson 2 mechanics: work through a concrete numeric example
- Lesson 3 edge cases: counterintuitive results or common misconceptions

**Non-technical concepts** (e.g. opportunity cost, cognitive biases, supply and demand):
- Lesson 2 mechanics: walk through a concrete real-world scenario
- Lessons pair best with Quiz mode or writing tasks in Build mode
