# P3-L3: Authentication

## Concept

A minimal auth flow: a login screen collecting email/password, an auth service that verifies credentials (against Firebase Auth, or a simplified mock service if you don't want a Firebase project yet), and app-level routing that shows the login screen when unauthenticated and the task list when authenticated.

Never store a raw password anywhere in the app — not in `SharedPreferences`, not in your database, not in memory longer than the login call needs it. What you persist across app restarts is a *session token* (or, with Firebase Auth, its SDK handles this for you via `FirebaseAuth.instance.authStateChanges()`), not the password itself.

If you don't want to set up a real Firebase project for this lesson, a mock `AuthService` with a hardcoded test account and an in-memory "logged in" flag is an acceptable stand-in for learning the *pattern* — the important part is the shape of the flow (login screen → service call → auth-state-driven routing), not which backend verifies it.

## Analogy

Authentication is like a building's front desk: you show ID once (login), and the desk gives you a visitor badge (session token) that gets you through doors for the rest of your visit — the desk doesn't re-check your full ID at every door, and it never keeps a copy of your ID photo lying around after issuing the badge.

## Workshop

**Task:**
1. Create `lib/screens/login_screen.dart`: email + password `TextFormField`s (reuse the Form/validator pattern from P2-L5), a login button.
2. Create `lib/services/auth_service.dart` with `Future<bool> login(String email, String password)` — either calling Firebase Auth's `signInWithEmailAndPassword`, or, for the mock version, comparing against one hardcoded test account and returning `true`/`false`. Read the mock account's credentials from environment/config (per P3-L1's rule), not a literal string, even for a mock.
3. Add an app-level check (in `main.dart` or a wrapper widget) that shows `LoginScreen` when not authenticated, `TaskListScreen` when authenticated — driven by an auth-state stream/flag, not manual navigation calls sprinkled everywhere.
4. Add a logout action (e.g., in the task list's `AppBar`) that clears the session and returns to the login screen.

## Acceptance Criteria / Edge Cases

- Incorrect credentials show a clear error message on the login screen, not a silent failure or crash.
- Successful login navigates to the task list without a manual `Navigator.push` call cluttering the login screen's submit handler (routing reacts to auth state, not the other way around).
- Logging out returns to the login screen and prevents access to the task list until logging in again (verify by trying to navigate back after logout).
- No raw password is ever written to local storage or logged to the console.

## Common Mistakes

- Storing the password in `SharedPreferences`/the database "just to remember it" — only ever persist a session token/flag from the auth provider.
- Wiring auth purely through manual navigation calls (`Navigator.push` on success) instead of driving the app's root widget off an auth-state stream — makes deep links and app-restart-while-logged-in cases fragile.
- Hardcoding the mock test account's password as a literal string instead of reading it from environment/config, breaking the habit built in P3-L1.

## Ship vs Portfolio Note

**Ship a real app:** use a real auth provider (Firebase Auth or equivalent) before shipping — the mock service here is explicitly a learning stand-in, not production-ready security.

**Learning/portfolio:** the mock version is fine to ship in a portfolio demo as long as it's clearly labeled as a demo account, not a real credential system.

## Bridge

The app now gates access behind login. Next: cloud sync — merging local and remote task state for a logged-in user.
