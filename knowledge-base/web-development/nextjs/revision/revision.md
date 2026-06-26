Next.js Cheat Sheet & Revision Checklist
RSC Boundaries Checklist
* Server Component: Default state. Used for data loading, layouts, static text.
* Client Component: Marked with 'use client'. Used for event listeners, state hooks, browser APIs.
Data Mutations & Server Actions
* useTransition: Wraps server actions on the client-side to show loading spinner states without blocking layouts.
* revalidatePath('/dashboard'): Tells Next.js to purge cached layouts and fetch fresh data from backend services.