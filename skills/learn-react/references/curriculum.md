# React Tutor — Curriculum

Each lesson follows the same structure:
- **Objective** — what the learner will be able to do
- **Example** — minimal runnable snippet (Vite or CRA compatible)
- **Exercise** — what the user must build
- **Acceptance criteria** — what correct output/behaviour looks like

---

## Lesson 1: JSX & Functional Components

**Objective:** Understand what JSX is, why React uses it, and how to write a functional component.

**Example:**
```jsx
// App.jsx
function Greeting() {
  return <h1>Hello, React!</h1>;
}

export default function App() {
  return <Greeting />;
}
```

**Exercise:**
Create a `Profile` component that renders your name in an `<h2>` and a short bio in a `<p>`.

**Acceptance criteria:**
- Component is a plain function that returns JSX
- Both elements render in the browser without errors
- No class components used

---

## Lesson 2: Props

**Objective:** Pass data into components using props and understand one-way data flow.

**Example:**
```jsx
function Badge({ username, role }) {
  return (
    <div>
      <strong>{username}</strong> — {role}
    </div>
  );
}

export default function App() {
  return <Badge username="alice" role="admin" />;
}
```

**Exercise:**
Make the `Profile` component from Lesson 1 accept `name` and `bio` as props, then render two different profiles from `App`.

**Acceptance criteria:**
- Props are destructured (or accessed via `props.x`)
- Two `<Profile>` instances each display different data
- No hardcoded strings inside the component body

---

## Lesson 3: State with useState

**Objective:** Add local state to a component and re-render on change.

**Example:**
```jsx
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

**Exercise:**
Build a `LikeButton` component that starts at 0 likes and increments by 1 each click. Display "❤️ {n} likes".

**Acceptance criteria:**
- State is declared with `useState`
- Clicking the button updates the displayed number
- State is not mutated directly

---

## Lesson 4: Event Handling

**Objective:** Handle user events (click, input, submit) the React way.

**Example:**
```jsx
export default function AlertButton() {
  function handleClick(e) {
    e.preventDefault();
    alert('Clicked!');
  }
  return <button onClick={handleClick}>Click me</button>;
}
```

**Exercise:**
Create a `ColorBox` component: a 200×200 div that changes background color to a random hex value each time it is clicked.

**Acceptance criteria:**
- Handler is defined as a named function (not inline arrow)
- Background color visibly changes on every click
- No direct DOM manipulation (`document.getElementById` etc.)

---

## Lesson 5: useEffect & Side Effects

**Objective:** Run code after render and understand the dependency array.

**Example:**
```jsx
import { useState, useEffect } from 'react';

export default function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setSeconds(s => s + 1), 1000);
    return () => clearInterval(id); // cleanup
  }, []); // run once on mount

  return <p>Elapsed: {seconds}s</p>;
}
```

**Exercise:**
Build a component that fetches a random joke from `https://official-joke-api.appspot.com/random_joke` on mount and displays the setup and punchline.

**Acceptance criteria:**
- Fetch is inside `useEffect` with an empty dependency array
- A loading state is shown while the request is in flight
- Cleanup is not required here but the student should explain why

---

## Lesson 6: Lists & Keys

**Objective:** Render dynamic lists correctly using `.map()` and stable keys.

**Example:**
```jsx
const fruits = ['Apple', 'Banana', 'Cherry'];

export default function FruitList() {
  return (
    <ul>
      {fruits.map(fruit => (
        <li key={fruit}>{fruit}</li>
      ))}
    </ul>
  );
}
```

**Exercise:**
Given an array of `{ id, title, done }` todo objects, render a `<ul>` where completed items are struck through (`<s>`).

**Acceptance criteria:**
- Each `<li>` has a unique, stable `key` (use `id`, not index)
- Completed items render inside `<s>` tags
- No console warning about missing keys

---

## Lesson 7: Conditional Rendering

**Objective:** Show or hide UI based on state using `&&`, ternary, and early return patterns.

**Example:**
```jsx
export default function Notification({ message }) {
  if (!message) return null;
  return <div className="alert">{message}</div>;
}
```

**Exercise:**
Build a `LoginStatus` component that receives an `isLoggedIn` boolean prop and renders either "Welcome back!" or a "Log in" button. Clicking the button should flip the state in the parent.

**Acceptance criteria:**
- Both branches are rendered correctly
- At least two of the three patterns (&&, ternary, early return) are demonstrated across the exercise
- No redundant state duplication

---

## Lesson 8: Controlled Forms

**Objective:** Own form input values with state instead of the DOM.

**Example:**
```jsx
import { useState } from 'react';

export default function NameForm() {
  const [name, setName] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    alert(`Hello, ${name}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={e => setName(e.target.value)} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Exercise:**
Build a signup form with `username` and `password` fields. On submit, validate that both fields are non-empty and that the password is at least 8 characters; display an inline error message if not.

**Acceptance criteria:**
- Both inputs are controlled (value + onChange)
- `e.preventDefault()` is called on submit
- Error messages appear without a page reload
- Password field uses `type="password"`

---

## Lesson 9: Context API

**Objective:** Share state across the component tree without prop drilling.

**Example:**
```jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext('light');

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>I am {theme}</button>;
}

export default function App() {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={theme}>
      <ThemedButton />
      <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
        Toggle
      </button>
    </ThemeContext.Provider>
  );
}
```

**Exercise:**
Create a `UserContext` that stores `{ name, role }`. Wrap the app in a provider and consume the context in a deeply nested `UserCard` component (at least 2 levels deep) without passing props.

**Acceptance criteria:**
- Context is created with `createContext`
- Provider wraps the subtree that needs access
- `useContext` is used to consume — no prop drilling
- Changing context value re-renders consumers

---

## Lesson 10: Custom Hooks

**Objective:** Extract reusable stateful logic into a custom hook.

**Example:**
```jsx
import { useState, useEffect } from 'react';

function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);
  useEffect(() => {
    const handler = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, []);
  return width;
}

export default function App() {
  const width = useWindowWidth();
  return <p>Window width: {width}px</p>;
}
```

**Exercise:**
Extract the fetch-joke logic from Lesson 5 into a `useJoke()` custom hook that returns `{ joke, loading, refresh }`. The `refresh` function should fetch a new joke on demand.

**Acceptance criteria:**
- Hook name starts with `use`
- Hook encapsulates all `useState` and `useEffect` calls
- Calling `refresh()` fetches a new joke without remounting the component
- The component itself contains no direct fetch logic
