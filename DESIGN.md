<!-- SEED: re-run /impeccable document once there's code to capture the actual tokens and components. -->

---
name: Ignore the Blueprint
description: A personal blog about programming, life and everything.
---

# Design System: Ignore the Blueprint

## 1. Overview

**Creative North Star: "The Warm Editorial Page"**

A personal publishing space that reads like a quality broadsheet: content-first, typographically deliberate, visually quiet. The design is a frame, not a participant. Every element that isn't the text must justify its presence; most won't.

The atmosphere is warm without being soft. It projects the confidence of someone who knows their craft: a product designer who codes. No decorative flourishes, no template defaults, no forced approachability. The site earns trust through clarity, not charm.

This system explicitly rejects the generic developer blog aesthetic: identical card grids, over-saturated accent colors, gratuitous icons, and the visual noise of ad-supported publishing platforms. It also rejects cold-minimal neutrality: the palette carries warmth, the typography carries character.

**Key Characteristics:**
- Content commands every page; chrome and framing recede
- Publication-grade typography: serif display, sans body
- Warm-tinted neutrals with a single restrained accent
- Zero decorative elements; everything serves reading or navigation
- Typographic hierarchy does the heavy lifting; color rarely speaks

## 2. Colors

**The One Accent Rule.** The accent color appears on ≤10% of any given screen. Its rarity is the point. When it appears, it signals importance: a link, a current nav item, a critical UI state. It never decorates.

### Primary

- **Warm Editorial Accent** ([to be resolved during implementation]): The lone accent. Used sparingly for links, active nav states, and the single most important interactive element on any page. A warm terracotta, muted amber, or deep sienna direction, consistent with the "温柔" personality and ft.com's restrained editorial palette.

### Neutral

- **Warm Page** ([to be resolved during implementation]): Page background. Tinted slightly warm (chroma ~0.005) from the accent's hue family. Never pure white.
- **Warm Surface** ([to be resolved during implementation]): Card, aside, or code block backgrounds. Slightly darker than the page, carrying the same warm tint.
- **Ink** ([to be resolved during implementation]): Primary text. Near-black, tinted with the accent hue at very low chroma. Never #000.
- **Muted Ink** ([to be resolved during implementation]): Secondary text, captions, metadata. Lower contrast, same hue family.
- **Faint Rule** ([to be resolved during implementation]): Borders, dividers, horizontal rules. The lightest visible tone. Never #ccc.

## 3. Typography

**Display Font:** [font pairing to be chosen at implementation]
**Body Font:** [font pairing to be chosen at implementation]

**Character:** Serif display carries editorial authority for headlines; sans body ensures comfortable long-form reading. The pairing should feel like a quality publication, not a startup landing page. Weight and size contrast between levels follows a ratio ≥1.25.

### Hierarchy

- **Display** (serif, 300–400 weight, clamp size, tight line-height): Post titles on the article page. Used exactly once per page.
- **Headline** (serif, same family, heavier weight, smaller size than Display): Post titles on the index/listing page.
- **Title** (sans, 500–600 weight): Section headings within articles. Clear hierarchy signal without competing with the display face.
- **Body** (sans, 400 weight, 16–18px base, line-height 1.5–1.6, max 65–75ch): The workhorse. Optimized for prolonged reading.
- **Label** (sans, 400–500 weight, smaller size, tracked out slightly): Metadata, dates, tags, navigation items. Understated and quickly scannable.

**The Serif-Sans Boundary Rule.** Serif faces appear only in display and headline roles. Everything else is sans. Mixing serif and sans within body text or UI is prohibited.

## 4. Elevation

The system is flat by default. Depth is conveyed through tonal layering: darker surfaces sit behind lighter ones. No box shadows at rest. Shadows, if they appear at all, are reserved for interactive states (hover cards, focused inputs) and use low-opacity, diffuse values.

## 5. Do's and Don'ts

### Do:

- **Do** let the content fill the viewport; chrome should occupy the minimum necessary space
- **Do** use the accent color only where interaction or emphasis is truly needed; if everything is accented, nothing is
- **Do** maintain ≥1.25 scale ratio between adjacent typography levels
- **Do** cap body copy at 65–75 characters per line
- **Do** tint every neutral toward the accent hue; pure grayscale reads as cold

### Don't:

- **Don't** use generic tech blog templates or default Pelican/Jekyll theme aesthetics (per PRODUCT.md: anti-reference #1)
- **Don't** produce AI-generated, soulless page layouts with placeholder design language (per PRODUCT.md: anti-reference #2)
- **Don't** use pixel art, retro-web, or cutesy visual styles (per PRODUCT.md: anti-reference #3)
- **Don't** clutter the page with ads, sidebars, or visual noise (per PRODUCT.md: CSDN anti-reference #4)
- **Don't** sacrifice readability for information density (per PRODUCT.md: Reddit anti-reference #5)
- **Don't** use identical card grids with icon + heading + text patterns (per impeccable absolute ban)
- **Don't** use side-stripe borders greater than 1px as colored accents on any element (per impeccable absolute ban)
- **Don't** use gradient text, glassmorphism, or hero-metric templates (per impeccable absolute bans)
- **Don't** default to modals; exhaust inline and progressive disclosure alternatives first
