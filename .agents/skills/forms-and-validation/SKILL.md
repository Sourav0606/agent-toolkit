---
name: forms-and-validation
description: Builds accessible, type-safe, resilient web forms with schema validation, error focus management, dirty state tracking, and unsaved changes prevention. Use when creating or updating user inputs, forms, checkout flows, or settings pages.
---

# Forms, Validation & Error UX

A comprehensive workflow for building bulletproof, accessible, type-safe web forms that prevent data loss and guide users gracefully through validation errors.

---

## 1. Core Principles

1. **Explicit Labeling**: Every input must have an associated `<label>` via `htmlFor`/`id` or `aria-label`. Never use `placeholder` as a replacement for a label.
2. **Accessible Error Linking**: Inputs with errors must link directly to their error messages using `aria-invalid="true"` and `aria-describedby="error-id"`.
3. **Focus on Error**: When form submission fails validation, automatically shift focus to the **first invalid field** so screen readers and keyboard users immediately know where to correct input.
4. **Prevent Double-Submission**: Disable or set `aria-busy="true"` on the submit button while pending, with a visible loading indicator.
5. **Protect Unsaved Changes**: Warn the user before navigating away if the form is dirty and unsubmitted.

---

## 2. Accessible Form Pattern

```tsx
import { useState, useRef } from "react";
import { z } from "zod";

const formSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormData = z.infer<typeof formSchema>;
type FormErrors = Partial<Record<keyof FormData, string>>;

export function LoginForm() {
  const [data, setData] = useState<FormData>({ email: "", password: "" });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = formSchema.safeParse(data);

    if (!result.success) {
      const fieldErrors: FormErrors = {};
      result.error.errors.forEach((err) => {
        const field = err.path[0] as keyof FormData;
        if (!fieldErrors[field]) fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);

      // Auto-focus first invalid input
      if (fieldErrors.email) emailRef.current?.focus();
      else if (fieldErrors.password) passwordRef.current?.focus();
      return;
    }

    setErrors({});
    setIsSubmitting(true);
    try {
      await apiSubmit(result.data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-4">
      {/* Field: Email */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email address <span aria-hidden="true" className="text-red-500">*</span>
        </label>
        <input
          ref={emailRef}
          id="email"
          type="email"
          value={data.email}
          onChange={(e) => setData({ ...data, email: e.target.value })}
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email ? "email-error" : undefined}
          required
          className="input-field"
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-sm text-red-600 mt-1">
            {errors.email}
          </p>
        )}
      </div>

      {/* Field: Password */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password <span aria-hidden="true" className="text-red-500">*</span>
        </label>
        <input
          ref={passwordRef}
          id="password"
          type="password"
          value={data.password}
          onChange={(e) => setData({ ...data, password: e.target.value })}
          aria-invalid={Boolean(errors.password)}
          aria-describedby={errors.password ? "password-error" : undefined}
          required
          className="input-field"
        />
        {errors.password && (
          <p id="password-error" role="alert" className="text-sm text-red-600 mt-1">
            {errors.password}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        aria-busy={isSubmitting}
        className="btn-submit"
      >
        {isSubmitting ? "Submitting..." : "Sign in"}
      </button>
    </form>
  );
}
```

---

## 3. Unsaved Changes Guard

Warn users before tab close or browser navigation if form state has been modified:

```tsx
import { useEffect } from "react";

export function useUnsavedChangesWarning(isDirty: boolean) {
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [isDirty]);
}
```

---

## 4. Verification Checklist

- [ ] Every form field has a distinct `<label htmlFor="...">`.
- [ ] Required fields indicate requirement both visually and semantically (`required` attribute).
- [ ] Error messages have `role="alert"` and are bound to the input via `aria-describedby`.
- [ ] Focus jumps to the first invalid field on failed submission.
- [ ] Buttons reflect loading state with `aria-busy="true"` and cannot be double-clicked.
