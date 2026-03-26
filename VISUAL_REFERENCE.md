# Visual Reference Guide - The Architectural Financialist

Quick visual reference for all redesigned components and layouts.

## 📱 Page Layouts

### Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│  [💼] Expense Tracker      [Dashboard] [Transactions] [Reports] ⚙️   │  ← Sticky Header
├─────────────────────────────────────────────────────────────────────┤
│  [📋] Expenditure Summary                    [↻ Refresh] [✚ Add Expense]│
│
│  ┌────────────────────┐  ┌──────────────────────────────────────────┐
│  │  Budget Overview   │  │   7-Day Spending Trend                   │
│  │                    │  │                                          │
│  │ Total Spent        │  │   ▁ ▃ ▂ ▅ ▆ ▃ ▇                        │
│  │ ₹2,450.00          │  │   Mon Tue Wed Thu Fri Sat Sun           │
│  │                    │  │                                          │
│  │ Remaining          │  │   [Hover for values]                    │
│  │ ₹2,550.00          │  │                                          │
│  │                    │  │                                          │
│  │ Budget: ₹5,000     │  │                                          │
│  │ ████████░ 49%      │  │                                          │
│  └────────────────────┘  └──────────────────────────────────────────┘
│
│  ┌────────────────────────────────────────────────────────────────────┐
│  │  Recent Transactions                         [View All →]         │
│  │                                                                    │
│  │  🍽️  Food           Today              -₹150.00  ↪ Delete        │
│  │  🚗  Transport      Yesterday            -₹250.00  ↪ Delete      │
│  │  🎬  Entertainment  2 days ago           -₹800.00  ↪ Delete      │
│  │  💡  Utilities      Last week            -₹500.00  ↪ Delete      │
│  │  🛍️   Shopping      Last week          -₹1,200.00  ↪ Delete      │
│  └────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────┘
```

### Transactions
```
┌─────────────────────────────────────────────────────────────────────┐
│  Transaction History                        [✚ Add Expense]         │
├─────────────────────────────────────────────────────────────────────┤
│  Filters:                                                           │
│  [🔍 Search...] [Category ▼] [From 📅] [To 📅] [✕ Clear Filters]   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  │ CAT │ CATEGORY      │ DESCRIPTION   │ DATE │ METHOD    │ AMOUNT │
│  ├──────────────────────────────────────────────────────────────────┤
│  │ 🍽️  │ Food          │ Lunch         │ 15/1 │ Cash     │ -₹150  │
│  │ 🚗  │ Transport     │ Cab           │ 14/1 │ Card     │ -₹250  │
│  │ 🎬  │ Entertainment │ Movie tickets │ 13/1 │ Digital  │ -₹500  │
│  │ 💡  │ Utilities     │ Electricity   │ 12/1 │ Transfer │ -₹2000 │
│  │     │               │               │      │          │        │
│  └──────────────────────────────────────────────────────────────────┘
│  No matching expenses - Try adjusting filters
└─────────────────────────────────────────────────────────────────────┘
```

### Reports
```
┌─────────────────────────────────────────────────────────────────────┐
│  Budgets & Reports                          [↻ Refresh]            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────────────────────────┐
│  │ Budget Overview    │  │ Spending Distribution                  │
│  │                    │  │                                        │
│  │ Food               │  │ 🟦 Food            ₹1,500  42.9%      │
│  │ ₹1,500 / ₹3,000    │  │ 🟩 Transport       ₹800    22.9%      │
│  │ ████████░ 50%      │  │ 🟨 Entertainment   ₹500    14.3%      │
│  │                    │  │ 🟪 Utilities       ₹400    11.4%      │
│  │ Transport          │  │ 🟫 Shopping        ₹200    5.7%       │
│  │ ₹800 / ₹2,000      │  │ 🟧 Health          ₹100    2.8%       │
│  │ ████░░░░░ 40%      │  │                                        │
│  │                    │  │                                        │
│  └────────────────────┘  └────────────────────────────────────────┘
│  ┌────────────────────────────────────────────────────────────────────┐
│  │ Monthly Spending Trend                                            │
│  │                                                                    │
│  │        ▇                                                           │
│  │        █                                 ▃                        │
│  │        █  ▂  ▃  ▂      ▁  ▂  ▄  ▅      ▅  ▂  ▃  ▄              │
│  │      ▁ █  █  █  █  ▁   █  █  █  █      █  █  █  █              │
│  │      │ █  █  █  █  │   █  █  █  █      █  █  █  █              │
│  │    Dec Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec           │
│  └────────────────────────────────────────────────────────────────────┘
│  ┌────────────────────┐  ┌────────────────────────────────────────┐
│  │ Top Expenses       │  │ Summary                                │
│  │                    │  │                                        │
│  │ 1️⃣  Utilities ₹2000│  │ Total Spent      ₹3,500               │
│  │ 2️⃣  Food       ₹1500│  │ Transactions     127                 │
│  │ 3️⃣  Transport   ₹800│  │ Avg. Transaction ₹27.56              │
│  │ 4️⃣  Entertainment₹500  │ Top Category     Food                │
│  │ 5️⃣  Shopping    ₹200│  │                                        │
│  └────────────────────┘  └────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────┘
```

### Settings
```
┌─────────────────────────────────────────────────────────────────────┐
│  Settings                                   [💾 Save Changes]       │
├─────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────┐
│  │ User Preferences   │  │ Categories         │  │ Data Export  │
│  │                    │  │                    │  │              │
│  │ Currency:          │  │ 🍽️  Food          │  │ [📥 CSV]     │
│  │ [₹ INR ▼]          │  │ 🚗 Transport    ✕  │  │              │
│  │                    │  │ 🎬 Entertainment ✕  │  │ [📥 JSON]    │
│  │ Monthly Budget:    │  │ 💡 Utilities     ✕  │  │              │
│  │ [5000     ]        │  │ 🛍️  Shopping     ✕  │  │ About        │
│  │                    │  │ 🏥 Health       ✕  │  │              │
│  │ ☑ Email Notif      │  │ 📁 Other        ✕  │  │ Version 1.0  │
│  │ ☑ Budget Alerts    │  │                    │  │ Support:     │
│  │                    │  │ [New Category ➕]  │  │ support@...  │
│  └────────────────────┘  └────────────────────┘  └──────────────┘
│
│  ✓ Settings saved successfully! (Toast notification)
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Palette

### Primary Colors
```
████ #004d4c  Primary (Teal)        - Main actions, icons
████ #006766  Primary Container     - Darker variant
```

### Secondary Colors
```
████ #486363  Secondary (Gray)      - Secondary actions
████ #c7e6e4  Secondary Container   - Lighter variant
```

### Tertiary Colors
```
████ #6c3518  Tertiary (Brown)      - Accents
████ #894c2d  Tertiary Container    - Darker variant
```

### Surface Hierarchy (Top to Bottom)
```
████ #ffffff         Surface Container Lowest (Cards - highest)
████ #f1f4f3         Surface Container Low (Hover states)
████ #ebeeed         Surface Container (Inputs)
████ #e6e9e8         Surface Container High (Buttons, inputs)
████ #e0e3e2         Surface Container Highest (Focus states)
████ #f7faf9         Surface (Background)
```

---

## 🎯 Button Styles

### Primary Button
```
Button Text          Gradient Background    On Click
[✚ Add Expense]      Primary → Primary      Scale 0.95
                     Container Gradient
```

### Secondary Button
```
Button Text          Background             On Hover
[↻ Refresh]          Secondary Container    Opacity change
```

### Tertiary Button
```
Button Text          Border                 On Hover
[✕ Clear]           Primary (20% opacity)   Background color
```

---

## 📝 Typography

### Headlines (Manrope)
```
H1: 3.5rem    "Expenditure Summary"
H2: 2.75rem   "Dashboard"
H3: 1.875rem  "Recent Transactions"
H4: 1.375rem  "Budget Overview"
```

### Body (Inter)
```
Body:    1.0rem      Normal text content
Label:   0.875rem    Form labels, badges
Caption: 0.75rem     Dates, hints
```

---

## 🎭 Component States

### Input Field
```
Default:    [________________]  Bordered, gray background
Focus:      [████████████████]  Blue tint, glow effect
Error:      [████████████████]  Red tint, error message
Disabled:   [________________]  Grayed out, not clickable
```

### Progress Bar
```
Empty:      [░░░░░░░░░░░░░░░░]
50%:        [████████░░░░░░░░]
Full:       [████████████████]
Gradient:   [🎨🎨🎨🎨░░░░░░░░]
```

### Transaction Item
```
Hover:
┌────────────────────────────────────────────────┐
│ 🍽️  Food          Today             -₹150.00   │  Background color shifts
└────────────────────────────────────────────────┘

Active/Delete:
┌────────────────────────────────────────────────┐
│ 🍽️  Food          Today             -₹150.00 ✕ │  Red delete icon
└────────────────────────────────────────────────┘
```

---

## 🎬 Animations

### Page Load
```
Fade In: 200ms → Full opacity
```

### Modal Open
```
Slide Up: 300ms → Position 0
Opacity:  0 → 1
```

### Button Click
```
Scale:    Down 0.95 → Up 1.0 (100ms)
Transform: -2px → 0px (Y axis)
```

### Hover Effects
```
Background: 200ms transition
Color:      200ms transition
Shadow:     200ms transition
Transform:  Scale 1.05 or Y-2px
```

---

## 📐 Spacing System

```
1x   = 0.25rem (4px)   - Tight spacing
2x   = 0.5rem  (8px)   - Small gaps
3x   = 0.75rem (12px)  - Comfortable spacing
4x   = 1rem    (16px)  - Standard spacing
6x   = 1.5rem  (24px)  - Breathing room
8x   = 2rem    (32px)  - Section gaps
12x  = 3rem    (48px)  - Major sections
16x  = 4rem    (64px)  - Page spacing
```

---

## 🎪 Component Grid

```
Desktop (12-column grid):
┌──────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌─────────────────────────┐   │
│  │   1/3 col    │  │     2/3 columns         │   │
│  │   (span 4)   │  │     (span 8)            │   │
│  └──────────────┘  └─────────────────────────┘   │
│  └────────────────────────────────────────────┘   │
│     Full width (span 12)                         │
└──────────────────────────────────────────────────┘

Tablet (2-column):
┌──────────────────┐
│  ┌──────┐ ┌──┐  │
│  │ Card │ │Ca│  │
│  └──────┘ └──┘  │
│  ┌──────────────┐ │
│  │   Full       │ │
│  └──────────────┘ │
└──────────────────┘

Mobile (1-column):
┌──────────────┐
│  ┌──────────┐ │
│  │   Card   │ │
│  └──────────┘ │
│  ┌──────────┐ │
│  │  Card    │ │
│  └──────────┘ │
│  ┌──────────┐ │
│  │   Full   │ │
│  └──────────┘ │
└──────────────┘
```

---

## 🎪 Icon Examples

```
📋 Dashboard        (dashboard)
📝 Transactions     (receipt_long)
📊 Reports         (assessment)
⚙️  Settings        (settings)
✚ Add              (add)
✕ Delete           (delete)
↻ Refresh          (refresh)
💾 Save            (save)
🔍 Search          (search)
📥 Download        (download)
💼 Wallet          (wallet)
🍽️  Restaurant      (restaurant)
🚗 Transport       (directions_car)
🎬 Movie           (movie)
💡 Utilities       (lightbulb)
🛍️  Shopping        (shopping_bag)
❤️  Health         (favorite)
```

---

## 🎨 No-Line Rule Examples

### ✅ Correct (No visible borders)
```
Card background: #ffffff (card color)
Border: 1px solid rgba(0, 77, 76, 0.1)  ← Almost invisible!
Separation: Via background color difference
```

### ❌ Avoid (Visible borders)
```
Card background: #ffffff
Border: 1px solid #ccc  ← Too dark, looks outdated
```

---

## 🌬️ Glassmorphism Examples

### Header
```
Background:     rgba(247, 250, 249, 0.7)  ← 70% opacity
Backdrop filter: blur(20px)                ← Frosted glass effect
Shadow:         0 24px 48px -12px rgba(24,28,28,0.06)
```

### Effect
```
Before:  [Blurred content behind]
After:   [Frosted glass effect with blur]
Result:  Premium, modern appearance
```

---

## 📐 Breakpoints & Behavior

```
Desktop (> 1024px)
├─ Full navigation text visible
├─ 12-column bento grid
├─ Multi-column cards
└─ Optimized spacing

Tablet (640px - 1024px)
├─ Full navigation text visible  
├─ 2-column grids
├─ Double-stacked cards
└─ Adjusted spacing

Mobile (< 640px)
├─ Navigation icons only
├─ Single column layout
├─ Full-width cards
├─ Tappable button sizes
└─ Minimal spacing
```

---

## ✨ Visual Consistency Checklist

- [x] All primary buttons use same gradient
- [x] All cards have same border radius (0.5rem)
- [x] All shadows use same blur radius (24px)
- [x] All text colors from palette
- [x] All spacing from scale (4px, 8px, 12px, etc.)
- [x] All icons from Material Symbols
- [x] All animations same timing (200-300ms)
- [x] All focus states visible
- [x] All hover states smooth
- [x] All empty states with icons

---

This visual guide ensures consistency across all components and pages.  
**Reference this when adding new features or components!**
