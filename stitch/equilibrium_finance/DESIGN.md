# Design System Strategy: The Editorial Ledger

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Architectural Financialist."** 

We are moving away from the cluttered, "dashboard-heavy" look of traditional fintech. Instead, we treat financial data with the reverence of a high-end architectural journal. The goal is to instill trust through precision, clarity, and intentional breathing room. This system breaks the "template" look by using exaggerated typographic scales, intentional asymmetry in data visualization, and a "layered paper" approach to depth. We do not use lines to separate ideas; we use space and tonal shifts to guide the eye.

## 2. Color & Tonal Depth
Our palette is anchored in a deep, authoritative teal (`primary: #004d4c`) that signals stability. To ensure the experience feels premium rather than "default," we follow these core principles:

- **The "No-Line" Rule:** 1px solid borders are strictly prohibited for sectioning. Structural boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section should sit directly on a `surface` background to create a soft, sophisticated edge.
- **Surface Hierarchy & Nesting:** Treat the UI as physical layers of fine paper. 
    - Base Level: `surface` (#f7faf9).
    - Inset Sections: `surface-container-low` (#f1f4f3).
    - Prominent Cards/Interaction Zones: `surface-container-lowest` (#ffffff).
- **Glassmorphism & Texture:** For floating elements like navigation bars or modal overlays, use `surface` with a 70% opacity and a `20px` backdrop-blur. This allows the sophisticated teal and tertiary tones to bleed through, softening the interface.
- **Signature Gradients:** For primary CTAs and hero data points, use a subtle linear gradient transitioning from `primary` (#004d4c) to `primary_container` (#006766) at a 135-degree angle. This adds a "lithographic" quality that flat colors lack.

## 3. Typography
We utilize a high-contrast pairing of **Manrope** (Display/Headlines) and **Inter** (Body/UI) to create an editorial feel.

- **The Authority (Manrope):** Used for `display-lg` through `headline-sm`. These should be set with a slightly tighter letter-spacing (-0.02em) to feel "locked in" and professional. Use `display-md` (2.75rem) for main account balances to give them the gravity they deserve.
- **The Utility (Inter):** Used for `title`, `body`, and `label`. Inter provides maximum legibility for transaction lists. 
- **Hierarchy through Scale:** Instead of bolding everything, use the typography scale. A `title-lg` (1.375rem) in `on_surface` is often more effective than a bolded smaller font.
- **Micro-Copy:** `label-sm` (#0.6875rem) should be used sparingly for metadata, always in `on_surface_variant` to keep the visual noise low.

## 4. Elevation & Depth
In this system, depth is felt, not seen. We avoid the "floating box" aesthetic of 2010-era web design.

- **Tonal Layering:** Depth is achieved by "stacking." A card using `surface_container_lowest` (#ffffff) placed on a background of `surface_container` (#ebeeed) creates a natural lift.
- **Ambient Shadows:** When a shadow is required (e.g., a floating Action Button), use a highly diffused shadow: `0 24px 48px -12px`. The shadow color must be a tinted version of our `on_surface` color at 6% opacity, rather than pure black, to simulate natural light.
- **The "Ghost Border" Fallback:** If a border is required for accessibility (e.g., input fields), use the `outline_variant` token at 15% opacity. Never use a 100% opaque border.

## 5. Components

### Buttons
- **Primary:** Gradient fill (`primary` to `primary_container`), `on_primary` text. Shape: `md` (0.375rem). 
- **Secondary:** `secondary_container` fill with `on_secondary_container` text. No border.
- **Tertiary:** Text-only using `primary`, with a `surface_variant` background appearing only on hover.

### Cards & Transaction Lists
- **The "No-Divider" Rule:** Forbid the use of horizontal rules (`<hr>`). Separate transactions using the `spacing-4` (1rem) scale and subtle background alternating between `surface` and `surface_container_low`.
- **Status Indicators:** Use `error` (#ba1a1a) for over-budget and a custom success green (derived from the teal family) for on-track. These should be presented as small, `full` rounded chips or simple 8px "pips."

### Input Fields
- **Styling:** Use `surface_container_highest` for the input track. Upon focus, transition the background to `surface_container_lowest` and apply a 1px "Ghost Border" using the `primary` color at 20% opacity.
- **Micro-Interactions:** Labels should use `label-md` and sit 0.5rem above the input, never inside, to maintain a clean "ledger" look.

### Data Visualization (Expense Tracking)
- **The Asymmetric Grid:** Don't align all charts to a center axis. Use the `spacing-16` and `spacing-24` tokens to create wide gutters, allowing charts to "bleed" toward the edges of the container for a modern, expansive feel.

## 6. Do's and Don'ts

### Do
- **Do** use `spacing-12` (3rem) and `spacing-16` (4rem) to separate major sections. White space is a functional element, not wasted space.
- **Do** use `tertiary` (#6c3518) as a "spark" color for secondary actions like "Export" or "Edit," providing a warm contrast to the cool teal.
- **Do** ensure all interactive elements have a minimum touch target of 44px, even if the visual element is smaller.

### Don't
- **Don't** use pure black (#000000) for text. Always use `on_surface` (#181c1c) to maintain the soft editorial tone.
- **Don't** use standard "drop shadows" on cards. Rely on background color shifts (`surface` hierarchy) first.
- **Don't** use high-contrast dividers. If you feel the need for a line, increase the `spacing` token by one level instead.