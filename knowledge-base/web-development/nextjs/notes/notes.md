Next.js App Router Architecture Notes
Deep dive into App routing, rendering paradigms, server actions, and caching metrics
Module 1: App Router & Layouts
Next.js App Router operates on a file-system basis under the app/ directory. Nested layouts allow preservation of states, layout caching, and avoid page content shift on route navigation.
Module 2: Rendering Paradigms: RSC vs Client
React Server Components (RSC) render on the server, saving bundle size by excluding imported dependencies from the client-side JavaScript payload.

|Metric/Feature|React Server Component (RSC)|Client Component ('use client')|
|---|---|---|
|Execution Location|Server Only|Server (on initial build) + Client Hydration|
|State Hooks (useState)|Not Allowed|Fully Allowed|
|Bundle Size Impact|0 bytes (dependencies stay on server)|Adds imports to client JS bundle sizes|
|Data Fetching|Can fetch directly via async/await from DB|Fetches via API routes or fetch client calls|

Module 3: Caching Mechanics
Next.js optimizes performance via 4 distinct caching layers:
* Request Deduplication: Automatically caches duplicate GET request payloads within the same render lifecycle.
* Data Cache: Persists data fetches across request lifecycles. Invalidated using revalidatePath or tags.
* Full Route Cache: Server-side HTML and RSC payload cache for static paths compiled during builds.
* Router Cache: Client-side in-memory browser cache storing layout/page definitions per session.