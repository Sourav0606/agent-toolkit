---
name: framer-motion
description: Production-grade UI/UX animations, micro-interactions, responsive transitions, and layout morphs using Motion (Framer Motion). Use when adding animations, gestural feedback, page/modal transitions, or interactive UI polish to React/Next.js interfaces.
---

# Framer Motion & Responsive Animation

A complete reference and execution workflow for building fluid, physics-based, accessible UI/UX animations and responsive interactions using **Motion** (`motion/react` / `framer-motion`).

---

## Quick Reference & Setup

Always prefer modern Motion v12+ imports:

```tsx
// Modern Motion v12+ (preferred)
import { motion, AnimatePresence, useReducedMotion, useScroll, useTransform } from "motion/react";

// Legacy (framer-motion package)
import { motion, AnimatePresence } from "framer-motion";
```

---

## 1. Core Principles

1. **Subtle & Purposeful**: Animations must inform, direct focus, or confirm intent. Avoid gratuitous, slow motion that gets in the user's way.
2. **Snappy Micro-interactions**: Keep interactive feedback quick:
   - Hover / Tap: `150ms – 200ms`
   - Transitions / Modals: `200ms – 300ms`
   - Orchestrated page reveals: `300ms – 500ms` max
3. **GPU-Accelerated Only**: Animate `transform` (`x`, `y`, `scale`, `rotate`) and `opacity`. Never animate `width`, `height`, `top`, or `left` directly without `layout` flags.
4. **Accessibility First**: Always respect `prefers-reduced-motion` using `useReducedMotion()`.

---

## 2. Essential Animation Recipes

### A. Micro-interactions & Buttons
Provide immediate tactile feedback for clicks and hovers:

```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
  className="btn-primary"
>
  Save Changes
</motion.button>
```

### B. Staggered List Entrance (Variants)
Define variants outside components to avoid recreating objects on render:

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 300, damping: 24 },
  },
};

export function CardGrid({ items }: { items: Item[] }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={itemVariants} className="card">
          <h3>{item.title}</h3>
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### C. Modals & Dialogs with `AnimatePresence`
Smooth mounting and unmounting:

```tsx
<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div
      key="backdrop"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        key="modal"
        initial={{ opacity: 0, scale: 0.95, y: 16 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 16 }}
        transition={{ type: "spring", duration: 0.3, bounce: 0.2 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-surface rounded-xl shadow-2xl max-w-lg w-full p-6"
      >
        <h2>Modal Header</h2>
      </motion.div>
    </motion.div>
  )}
</AnimatePresence>
```

### D. Shared Element Layout Morphing (`layoutId`)
Perfect for active navigation tabs, segmented controls, and expanding cards:

```tsx
export function Tabs({ tabs, activeTab, onChange }: TabsProps) {
  return (
    <div className="flex gap-2 p-1 bg-surface-muted rounded-lg">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className="relative px-4 py-2 text-sm font-medium transition-colors"
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="active-tab-pill"
              transition={{ type: "spring", stiffness: 380, damping: 30 }}
              className="absolute inset-0 bg-surface rounded-md shadow-sm"
            />
          )}
          <span className="relative z-10">{tab.label}</span>
        </button>
      ))}
    </div>
  );
}
```

### E. Viewport Scroll Reveals (`whileInView`)
Trigger animations once the element scrolls into view:

```tsx
<motion.div
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.25 }}
  transition={{ duration: 0.4, ease: "easeOut" }}
>
  Content revealed on scroll
</motion.div>
```

---

## 3. Responsive & Mobile Adaptations

Mobile devices have different touch dynamics, smaller screens, and lower GPU headroom. Adapt animations responsively:

1. **Touch vs Hover**:
   - Do not rely on hover states for functionality.
   - Use `whileTap` for instant touch confirmation on mobile.
2. **Simplified Layout Morphs**:
   - Heavy `layoutId` transitions with many simultaneous siblings can cause frame drops on low-power mobile devices. Keep layout transitions to single focal elements (e.g. active tab indicator, modal backdrop).
3. **Responsive Breakpoints**:
   ```tsx
   const isMobile = window.innerWidth < 768;
   const distance = isMobile ? 8 : 20; // Shorter translation distance on mobile
   ```
4. **Keyboard Visibility**:
   - On mobile inputs, ensure animated sheets or floating toolbars do not clash with the virtual on-screen keyboard.

---

## 4. Accessibility & Reduced Motion

Honor user preference for reduced motion:

```tsx
import { motion, useReducedMotion } from "motion/react";

export function AccessibleCard() {
  const shouldReduceMotion = useReducedMotion();

  const animation = shouldReduceMotion
    ? { opacity: [0, 1] } // Cross-fade only, zero transform
    : { opacity: [0, 1], y: [16, 0] };

  return (
    <motion.div animate={animation} transition={{ duration: 0.2 }}>
      Card content
    </motion.div>
  );
}
```

---

## 5. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Alternative |
| :--- | :--- | :--- |
| **Animating `height` directly** | Triggers browser layout reflow on every frame (jank) | Use `layout` prop on `motion.div` or animate `scaleY` / `opacity` |
| **No `key` inside `AnimatePresence`** | Exit animations fail to trigger | Always provide a unique `key` to direct children of `AnimatePresence` |
| **Inline Variant Definitions** | Re-allocates objects on every re-render | Define variants at module scope or memoize |
| **Long Duration Animations ($>600\text{ms}$)** | Feels sluggish; users perceive the app as slow | Default to 150ms–300ms; use spring physics |
| **Ignoring `prefers-reduced-motion`** | Can cause vestibular motion sickness for users | Always wire up `useReducedMotion()` for structural movement |
