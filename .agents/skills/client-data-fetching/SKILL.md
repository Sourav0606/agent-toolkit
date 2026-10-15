---
name: client-data-fetching
description: Production async data fetching, client caching, optimistic UI updates, and race condition prevention. Use when connecting frontend components to APIs, managing server state, implementing debounced search, or infinite scrolling.
---

# Client Data Fetching & Async State

A disciplined engineering workflow for fetching remote data, caching server state, implementing optimistic updates, and preventing race conditions in web applications.

---

## 1. Core Principles

1. **Separate Server State from Local State**: Never sync remote API data into ad-hoc `useState` if a dedicated caching layer (TanStack Query, SWR, or RTK Query) is available.
2. **Prevent Race Conditions**: Always cancel stale inflight requests when a query or filter changes (using `AbortController`). Never let an earlier slow request overwrite a later fast request.
3. **Optimistic Updates Must Roll Back**: When modifying data locally before the server responds, always store the snapshot of previous state and revert if the request fails.
4. **All 5 Async States Handled**:
   - `idle`: Not yet triggered.
   - `loading`: First load with skeleton/spinner.
   - `success`: Data present.
   - `empty`: Request succeeded but dataset is empty (`[]`).
   - `error`: Actionable error with a retry button.

---

## 2. Preventing Race Conditions with `AbortController`

When building search inputs, tabs, or filtering:

```tsx
import { useEffect, useState } from "react";

export function useSearchUsers(query: string) {
  const [results, setResults] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetch(`/api/users?q=${encodeURIComponent(query)}`, {
      signal: controller.signal,
    })
      .then((res) => {
        if (!res.ok) throw new Error("Search failed");
        return res.json();
      })
      .then((data) => {
        setResults(data);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === "AbortError") return; // Ignored: replaced by newer query
        setError(err.message);
        setLoading(false);
      });

    // Cleanup: cancel inflight request when query changes or unmounts
    return () => controller.abort();
  }, [query]);

  return { results, loading, error };
}
```

---

## 3. Optimistic UI Updates (TanStack Query Pattern)

Instantly update the UI, but rollback if network fails:

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useToggleTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodoOnServer,

    // Step 1: Snapshot and optimistically apply
    onMutate: async (updatedTodo) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const previousTodos = queryClient.getQueryData<Todo[]>(["todos"]);

      queryClient.setQueryData<Todo[]>(["todos"], (old = []) =>
        old.map((t) => (t.id === updatedTodo.id ? { ...t, ...updatedTodo } : t))
      );

      return { previousTodos }; // Context object passed to onError
    },

    // Step 2: Rollback on error
    onError: (err, newTodo, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(["todos"], context.previousTodos);
      }
    },

    // Step 3: Re-sync with ground truth
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

---

## 4. Debounced Search Input Pattern

Avoid firing API requests on every keystroke:

```tsx
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delayMs: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}
```

---

## 5. Verification Checklist

- [ ] All inflight requests are cleanly aborted on unmount or query change via `AbortController`.
- [ ] Empty state is handled explicitly with an actionable message (not a blank canvas).
- [ ] Network errors offer an explicit "Retry" action.
- [ ] Optimistic mutations roll back immediately if the network request fails.
- [ ] Fast repeated inputs (e.g. search bars) are debounced (250ms–350ms).
