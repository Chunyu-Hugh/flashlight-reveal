---
version: alpha
name: 墨卷 (Ink Scroll)
description: >-
  光照之处，墨色生辉 — A warm, editorial interactive art piece. 
  A spotlight reveals hidden color within monochrome shanshui paintings.
  The aesthetic is a scholar's study: parchment tones, serif headers
  reminiscent of book titles, terracotta accents echoing Chinese seals (印章),
  and generous whitespace like the margins of a scroll.
colors:
  primary: "#141413"
  secondary: "#5e5d59"
  tertiary: "#c96442"
  neutral: "#f5f4ed"
  accent: "#d97757"
  surface: "#faf9f5"
  border: "#f0eee6"
  dark-surface: "#30302e"
  ink-black: "#1a1a18"
  jade-green: "#6b8e6e"
  slate-blue: "#7b8fa8"
typography:
  h1:
    fontFamily: "Noto Serif SC, serif"
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  h2:
    fontFamily: "Noto Serif SC, serif"
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  h3:
    fontFamily: "Noto Serif SC, serif"
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.35
  body-lg:
    fontFamily: "system-ui, sans-serif"
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "system-ui, sans-serif"
    fontSize: 0.9375rem
    fontWeight: 400
    lineHeight: 1.55
  caption:
    fontFamily: "system-ui, sans-serif"
    fontSize: 0.75rem
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.02em"
  ui-label:
    fontFamily: "system-ui, sans-serif"
    fontSize: 0.6875rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.04em"
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#faf9f5"
    rounded: "{rounded.md}"
    padding: 10px 24px
  button-primary-hover:
    backgroundColor: "#b8583a"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 8px 16px
  card-mode:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
  spotlight-ring:
    borderColor: "rgba(201,100,66,0.18)"
    borderWidth: 2px
  scene-dot:
    backgroundColor: "{colors.secondary}"
    size: 8px
  scene-dot-active:
    backgroundColor: "{colors.tertiary}"
    size: 8px
---

## Overview

墨卷 (Ink Scroll) is an interactive browser-based art installation. The core
mechanic is simple: a monochrome line-drawing (the "ink layer") sits on top of
a colored shanshui painting (the "color layer"). The user controls a circular
"spotlight" through one of 11 interaction modes (camera, mouse, gesture, audio,
etc.). Inside the spotlight, the ink layer is clipped away to reveal the full-color
scene beneath — as if a beam of light is bringing the scroll to life.

The visual aesthetic rejects tech-futurism in favor of scholarly warmth:
parchment backgrounds, serif type, terracotta accents, and generous whitespace.
No particle effects, no neon, no gratuitous animation. Every visual choice
serves the metaphor of "illuminating an ancient scroll."

**Brand voice:** Warm, scholarly, unhurried. Like a museum curator describing
an exhibit in a quiet gallery.

## Colors

- **Primary (#141413):** The deepest warm black — text, headings, dark surfaces.
  Not pure #000; the barely-perceptible warmth prevents it from feeling sterile.
- **Secondary (#5e5d59):** Olive-tinted medium gray. Body text, descriptions,
  metadata. Warmer than standard gray, cooler than brown.
- **Tertiary (#c96442):** Terracotta — the sole chromatic accent. Used for
  primary CTAs, the scene-nav active dot, and the spotlight ring. Evokes the
  red ink of Chinese seals (印章) on a scroll.
- **Neutral (#f5f4ed):** Parchment — the primary page background. A warm cream
  with yellow-green undertones, like aged mulberry paper.
- **Accent (#d97757):** Coral — lighter variant of terracotta, used for hover
  states and subtle highlights.
- **Surface (#faf9f5):** Ivory — card backgrounds and elevated surfaces.
  Barely lighter than parchment, creating whisper-subtle layering.
- **Border (#f0eee6):** Cream border — the gentlest possible containment line.
- **Dark-Surface (#30302e):** Warm charcoal — dark mode containers and
  secondary dark elements.
- **Ink-Black (#1a1a18):** Used for the ink layer (edge-detected line art).
  Slightly warmer than primary to suggest actual ink on paper.
- **Jade-Green (#6b8e6e):** Muted green accent for the bamboo scene indicator.
- **Slate-Blue (#7b8fa8):** Muted blue accent for the snow scene indicator.

## Typography

Serif for authority and art; sans for utility and UI. This is the core
typographic split: **Noto Serif SC** (Google Fonts, free) carries all artistic
and editorial content — scene names, titles, the brand wordmark. **System sans**
handles UI labels, mode names, and technical information.

Line heights are generous (1.5–1.6 for body, 1.15–1.35 for headings),
creating a reading rhythm closer to a book than a dashboard. Headings use
negative letter-spacing to create dignified compression; body text is set
relaxed.

## Layout & Spacing

- **Base unit:** 8px, with a warm, organic scale.
- **Container:** Centered, max ~1200px.
- **Section rhythm:** 48–80px vertical gaps. Whitespace is the primary
  compositional tool — content breathes.
- **The canvas:** Full-bleed, edge-to-edge. The interactive surface IS the
  page — no chrome or framing. UI is an overlay, not a frame.

## Elevation & Depth

No traditional drop shadows. Depth comes from:
1. **Background color shifts:** Parchment → Ivory → warm charcoal
2. **Whisper borders:** `1px solid #f0eee6` — barely visible containment
3. **The spotlight ring:** `2px solid rgba(201,100,66,0.18)` — the only
   border that carries chromatic color

The most dramatic depth effect is the ink layer itself: the edge-detected
line art creates a natural "depth" through contrast, without any CSS shadow.

## Shapes

- Buttons, inputs: 8px radius (comfortably rounded)
- Cards: 12px radius
- Scene dots: circular (50%)
- Spotlight: circular (infinite radius)
- UI panel: 8px radius with backdrop blur

## Components

### Start Screen
A centered modal-like panel on the parchment background. Serif header with
the brand name, a brief tagline, and the mode grid. The "展开画卷" CTA is the
only terracotta button — the sole high-emphasis action.

### Mode Cards
Small ivory cards (12px radius, whisper border) arranged in a grid. Each card
shows an icon, mode name, and hardware requirement. The active mode gets a
terracotta border. Hover: subtle scale + border darkening.

### UI Overlay
A semi-transparent panel (rgba(0,0,0,0.45) with backdrop-blur) in the top-left
corner. Shows current mode, scene, style, radius, and FPS. Typography is small
sans-serif with terracotta highlights for key values.

### Scene Navigation
Five circular dots centered at the bottom of the screen. Active dot is 
terracotta (#c96442); inactive dots are secondary gray. Auto-hides after 2
seconds of inactivity.

### Spotlight
A circular clipping region. The border is a thin terracotta ring. Inside,
the color layer is revealed; outside, the ink layer remains visible.

## Do's and Don'ts

### Do
- Use parchment (#f5f4ed) as the primary background — the warmth IS the identity
- Use Noto Serif SC for all artistic/editorial text
- Use terracotta (#c96442) only for high-signal moments: CTA, active state, spotlight ring
- Keep neutrals warm-toned — every gray has a yellow-brown undertone
- Use whisper borders (1px solid #f0eee6) instead of heavy outlines
- Maintain generous whitespace — content should breathe like a scroll
- Let the ink layer provide visual texture through contrast, not effects

### Don't
- No particle effects, confetti, or decorative animation
- No neon/glow effects
- No cool blue-grays — every neutral is warm-toned
- No sharp corners (<4px) — softness is core to the identity
- No heavy drop shadows — depth comes from color and contrast
- No transitional animations longer than 0.4s
- Don't use pure #000 or #fff — always use the warm variants
