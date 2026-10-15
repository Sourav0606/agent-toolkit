---
name: e2e-playwright
description: Builds resilient end-to-end browser tests using Playwright. Covers Page Object Models, semantic locators (getByRole, getByLabel), auto-waiting assertions, network mocking, and authentication state reuse.
---

# End-to-End Testing with Playwright

A best-practice playbook for writing robust, non-flaky end-to-end browser tests using Microsoft Playwright.

---

## 1. Locators: Semantic Over Fragile CSS

Always prioritize user-facing semantic locators that match how real users and assistive technologies navigate the page:

```typescript
// 1. BEST: Accessible Role and Label
page.getByRole('button', { name: 'Submit order' });
page.getByLabel('Email address');

// 2. GOOD: User-visible Text or Placeholder
page.getByText('Payment successful');
page.getByPlaceholder('Search products...');

// 3. FALLBACK: Explicit Test IDs (for non-semantic containers)
page.getByTestId('order-summary-card');

// 4. AVOID: Fragile XPath or deep CSS paths
// BAD: page.locator('div > div:nth-child(2) > .btn-primary')
```

---

## 2. Auto-Waiting Assertions (Zero `sleep()`)

Never use hardcoded sleep delays (`page.waitForTimeout(3000)`). They cause flakiness on slower CI workers and waste time on fast machines.

Always use Playwright's built-in web-first assertions that poll automatically:

```typescript
import { test, expect } from '@playwright/test';

test('completes checkout flow', async ({ page }) => {
  await page.goto('/checkout');

  await page.getByRole('button', { name: 'Place Order' }).click();

  // Auto-waits up to 5s for the element to appear, become visible, and match text
  await expect(page.getByRole('heading', { name: 'Confirmation' })).toBeVisible();
  await expect(page.getByTestId('order-id')).toHaveText(/ORD-\d{5}/);
});
```

---

## 3. Page Object Model (POM) Pattern

Encapsulate page structure and UI actions into reusable classes:

```typescript
// pages/LoginPage.ts
import { type Page, type Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email address');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, pass: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(pass);
    await this.submitButton.click();
  }
}
```

---

## 4. Network Mocking with `page.route`

Isolate tests from slow or rate-limited external third parties:

```typescript
test('handles payment gateway outage gracefully', async ({ page }) => {
  // Mock external Stripe endpoint to return 500
  await page.route('**/v1/charges', async (route) => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: { message: 'Gateway timeout' } }),
    });
  });

  await page.goto('/checkout');
  await page.getByRole('button', { name: 'Pay' }).click();

  await expect(page.getByRole('alert')).toHaveText(/Payment failed. Please try again./);
});
```

---

## 5. Reusing Auth State

Avoid logging in through the UI before every test. Save and restore authentication cookies/localStorage:

```typescript
// auth.setup.ts
import { test as setup } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('secret');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');

  await page.context().storageState({ path: authFile });
});
```
