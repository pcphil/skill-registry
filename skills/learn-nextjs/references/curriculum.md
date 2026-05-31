# Next.js App Router — Curriculum

Each lesson follows the same structure:
- **Objective** — what the learner will be able to do
- **Example** — minimal runnable snippet (Next.js App Router + TypeScript)
- **Exercise** — what the user must build
- **Acceptance criteria** — what correct output/behaviour looks like

---

## Lesson 1: Project Structure

**Objective:** Understand the Next.js App Router file conventions and how they differ from a Vite + React setup.

**Example:**
```
app/
├── layout.tsx    ← root layout (wraps every page)
├── page.tsx      ← home route (/)
├── about/
│   └── page.tsx  ← /about route
└── globals.css
next.config.ts
```

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

```tsx
// app/page.tsx
export default function Home() {
  return <h1>Welcome to my Next.js app</h1>;
}
```

**Exercise:**
Create a new Next.js project with `npx create-next-app@latest --typescript --app`. Explore the generated files. Modify `app/page.tsx` to show your project's name and a one-line description.

**Acceptance criteria:**
- Project created with App Router (not Pages Router)
- `app/layout.tsx` exists with `RootLayout` that wraps `{children}`
- `app/page.tsx` renders custom content
- Dev server runs without errors (`npm run dev`)

---

## Lesson 2: Routing

**Objective:** Create routes using the file-system convention, including nested and dynamic routes.

**Example:**
```tsx
// app/blog/page.tsx — maps to /blog
export default function BlogIndex() {
  return <h1>All Posts</h1>;
}

// app/blog/[slug]/page.tsx — maps to /blog/anything
export default function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <h1>Post: {slug}</h1>;
}
```

**Exercise:**
Add three routes to your project: `/about`, `/projects`, and `/projects/[id]`. The dynamic route should display the `id` from the URL. Add navigation links between pages using `next/link`.

**Acceptance criteria:**
- Each route has its own `page.tsx` in the correct directory
- `/projects/42` displays "Project 42" (or similar using the param)
- `params` is typed as `Promise<{ id: string }>` and awaited
- Navigation uses `<Link>` from `next/link`, not `<a>` tags

---

## Lesson 3: Layouts & Templates

**Objective:** Share UI across routes using layouts and understand nesting behavior.

**Example:**
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>
        <a href="/dashboard">Overview</a>
        <a href="/dashboard/settings">Settings</a>
      </nav>
      <main>{children}</main>
    </div>
  );
}
```

**Exercise:**
Create a layout for your `/projects` section that includes a sidebar with links to 3 project pages. The sidebar should persist when navigating between projects.

**Acceptance criteria:**
- `app/projects/layout.tsx` wraps all project routes
- Sidebar renders on `/projects`, `/projects/1`, `/projects/2` etc.
- Root layout still wraps the projects layout (nesting works)
- No duplicated navigation between root and projects layouts

---

## Lesson 4: Server vs Client Components

**Objective:** Understand the server component default, when to add `"use client"`, and the rendering boundary.

**Example:**
```tsx
// Server Component (default) — can fetch data, access backend
// app/stats/page.tsx
export default async function StatsPage() {
  const count = await getVisitorCount(); // direct backend call
  return <p>Visitors: {count}</p>;
}

// Client Component — needed for interactivity
// app/components/Counter.tsx
"use client";

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>Clicks: {count}</button>;
}
```

**Exercise:**
Create a page that displays a static heading (server component) and includes an interactive toggle button (client component) that shows/hides a section of content.

**Acceptance criteria:**
- Page file is a server component (no `"use client"`)
- Toggle component is in a separate file with `"use client"` at the top
- `useState` is only in the client component
- Page imports and renders the client component — both render correctly

---

## Lesson 5: Data Fetching

**Objective:** Fetch data in server components using async/await with typed responses.

**Example:**
```tsx
// app/users/page.tsx
interface User {
  id: number;
  name: string;
  email: string;
}

export default async function UsersPage() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  const users: User[] = await res.json();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name} — {user.email}</li>
      ))}
    </ul>
  );
}
```

**Exercise:**
Build a page that fetches posts from `https://jsonplaceholder.typicode.com/posts` and displays the first 10 as a list with title and body. Type the response with an interface.

**Acceptance criteria:**
- Fetch happens at the top level of an async server component (not inside useEffect)
- Response is typed with a `Post` interface
- Only first 10 posts are displayed
- No `"use client"` directive — this is pure server rendering

---

## Lesson 6: Loading & Error States

**Objective:** Use Next.js conventions for loading and error UI with Suspense boundaries.

**Example:**
```tsx
// app/users/loading.tsx
export default function Loading() {
  return <p>Loading users...</p>;
}

// app/users/error.tsx
"use client";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>Something went wrong: {error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

**Exercise:**
Add `loading.tsx` and `error.tsx` to your posts page from Lesson 5. Test the loading state by adding a delay, and the error state by temporarily using a bad URL.

**Acceptance criteria:**
- `loading.tsx` shows a loading message while the page fetches
- `error.tsx` has `"use client"` and accepts `error` + `reset` props
- Error boundary catches the bad fetch and displays the error message
- Reset button re-attempts the render

---

## Lesson 7: Server Actions

**Objective:** Handle form submissions and data mutations using Server Actions.

**Example:**
```tsx
// app/actions.ts
"use server";

export async function addItem(formData: FormData) {
  const name = formData.get("name") as string;
  // In a real app: save to database
  console.log("Added:", name);
}
```

```tsx
// app/items/page.tsx
import { addItem } from "../actions";

export default function ItemsPage() {
  return (
    <form action={addItem}>
      <input name="name" placeholder="Item name" required />
      <button type="submit">Add</button>
    </form>
  );
}
```

**Exercise:**
Create a feedback form with `name` and `message` fields. Write a Server Action that logs the submission. Display the form on a `/feedback` page. After submission, show a success message.

**Acceptance criteria:**
- Server Action is in a separate file with `"use server"` at the top
- Form uses `action={serverAction}` (not `onSubmit`)
- Form data is extracted via `FormData`
- No client-side JavaScript needed for the basic form submission

---

## Lesson 8: API Route Handlers

**Objective:** Create typed API endpoints using route handlers.

**Example:**
```tsx
// app/api/hello/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Hello from the API" });
}

export async function POST(request: Request) {
  const body = await request.json();
  return NextResponse.json({ received: body }, { status: 201 });
}
```

**Exercise:**
Create an API route at `/api/projects` that returns a JSON array of 3 project objects (hardcoded). Add a POST handler that accepts a project name and returns it with a generated ID.

**Acceptance criteria:**
- Route file is `app/api/projects/route.ts`
- GET returns an array of typed project objects
- POST reads the request body and returns a response with status 201
- Both handlers use `NextResponse.json()`

---

## Lesson 9: Middleware

**Objective:** Intercept and modify requests before they reach route handlers or pages.

**Example:**
```tsx
// middleware.ts (at project root, not inside app/)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith("/admin")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
```

**Exercise:**
Add middleware that logs every request path to the console and adds a custom `x-request-time` header to all responses. Use the `matcher` config to limit it to your project routes (exclude static files).

**Acceptance criteria:**
- `middleware.ts` is at the project root
- Request pathname is logged for each matched request
- Response includes the custom header (verify in browser dev tools)
- `config.matcher` is defined and excludes `_next/static`

---

## Lesson 10: Dynamic Rendering & Static Params

**Objective:** Control static vs dynamic rendering and pre-generate dynamic routes at build time.

**Example:**
```tsx
// app/blog/[slug]/page.tsx
interface Post {
  slug: string;
  title: string;
  content: string;
}

const posts: Post[] = [
  { slug: "hello", title: "Hello World", content: "First post" },
  { slug: "nextjs", title: "Learning Next.js", content: "App Router is great" },
];

export async function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) return <p>Not found</p>;
  return <article><h1>{post.title}</h1><p>{post.content}</p></article>;
}
```

**Exercise:**
Add `generateStaticParams` to your `/projects/[id]` page from Lesson 2. Define 3 project objects and pre-generate their pages. Add a not-found state for unknown IDs.

**Acceptance criteria:**
- `generateStaticParams` returns an array of `{ id }` objects
- Each pre-generated page renders correct project data
- Unknown IDs show a "not found" message
- `params` is typed as `Promise<{ id: string }>` and awaited

---

## Lesson 11: Metadata & SEO

**Objective:** Add page-level and dynamic metadata for SEO using Next.js conventions.

**Example:**
```tsx
// app/layout.tsx — static metadata
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: { default: "My App", template: "%s | My App" },
  description: "A Next.js application",
};

// app/blog/[slug]/page.tsx — dynamic metadata
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  return { title: slug, description: `Post about ${slug}` };
}
```

**Exercise:**
Add a default title and description to your root layout. Then add dynamic metadata to your `/projects/[id]` page that sets the title to the project name.

**Acceptance criteria:**
- Root layout exports a `metadata` object with `title.default` and `title.template`
- Dynamic page exports `generateMetadata` that returns page-specific title
- Browser tab shows the correct title on each page
- `Metadata` type is imported from `"next"`

---

## Lesson 12: Deployment Patterns

**Objective:** Understand build output, environment variables, and production readiness.

**Example:**
```tsx
// Using environment variables
// .env.local (not committed)
// NEXT_PUBLIC_API_URL=https://api.example.com
// SECRET_KEY=server-only-secret

// In a server component:
const secret = process.env.SECRET_KEY; // only available server-side

// In a client component:
const apiUrl = process.env.NEXT_PUBLIC_API_URL; // available client-side (prefixed)
```

**Exercise:**
Create a `.env.local` file with one public and one secret variable. Use the public variable in a client component and the secret in a server component. Run `npm run build` and verify the output.

**Acceptance criteria:**
- `.env.local` exists with both `NEXT_PUBLIC_*` and non-prefixed variables
- Public variable is accessible in client component
- Secret variable is only used in server component (not exposed to client)
- `npm run build` completes without errors
- `.env.local` is in `.gitignore`
