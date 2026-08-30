# makof.ru — design contract

This file is the source of truth for visual and conversion decisions on the public tutor landing page.

## Product and user job

- Surface: personal marketing landing page for an EGE Informatics tutor.
- Primary audience: parents and students in grades 10–11 considering preparation for EGE Informatics.
- Primary user job: decide whether Dmitry Makov is credible and whether the teaching format fits, then book a free trial lesson.
- Primary conversion: submit the AlfaCRM trial lesson form.
- One page, one main action. Secondary links only navigate within the page.

## Default design stack

Use these principles together:

1. Sepia for human, specific, non-AI copy.
2. Landing-page-design for offer hierarchy, proof placement and CTA discipline.
3. UI anti-slop for avoiding generic generated UI.
4. UI/UX quality for journey, mobile behavior, accessibility and state clarity.
5. CRO principles when real analytics and lead data are available.

Do not blindly copy stylistic prescriptions from external skills. This project's visual contract wins.

## Visual direction

- Style: calm editorial personal-service landing page.
- Background: white or very near-white only.
- Text: near-black.
- Muted text: neutral gray.
- Accent: one restrained orange.
- Typeface: Golos Text only.
- No gradients.
- No glassmorphism.
- No colored ambient blobs.
- No decorative shadows by default.
- No excessive rounding. Most sections and content groups should use whitespace and thin rules instead of cards.
- No generic SaaS visuals.
- No fake dashboards, icons or metrics.
- Real photos and screenshots are preferred to decorative graphics.

## Layout

- Desktop container: approximately 1180–1240 px.
- Medium-low information density.
- Sections should not all repeat the same layout.
- Use asymmetry where it improves hierarchy: editorial two-column introductions, large text paired with evidence, narrow copy beside wider media.
- Avoid repeated three-card feature rows.
- Avoid equal-height cards when content naturally varies.
- Section separation: whitespace and 1 px neutral rules.
- Headings should have meaningful line breaks and balanced wrapping.
- Body text should stay comfortably readable, generally no wider than about 65–70 characters.

## Typography

- Font: Golos Text.
- Headings: 600 weight. Avoid 800/900.
- Body: 400–500.
- Labels: 500–600, sentence case. Avoid decorative all-caps where possible.
- Keep line-height comfortable and sentence rhythm natural.
- Use `text-wrap: balance` on large headings and `text-wrap: pretty` on prose where supported.

## Conversion hierarchy

The page should answer buyer questions in roughly this order:

1. What is offered and for whom?
2. Can this teacher actually produce results?
3. How does preparation work in practice?
4. Who is the teacher and why trust him?
5. What do students and parents say?
6. Can I try this before paying?
7. What happens if the format does not fit?
8. Common objections and questions.
9. Clear final route to the same free trial form.

The top CTA, mid-page CTA and final CTA all lead to the same free trial form.

## Proof rules

- Never invent a score, testimonial, credential, date, number or context.
- Confirmed student score set currently used: 100, 90, 88, 78, 75, 72.
- Never add 93.
- 78 may mention preparation for two months.
- 75 and 72 should not receive invented background context.
- Teaching since 2019.
- ITMO education is valid proof.
- Safe wording for qualification: completed a 72-hour training program for subject commission experts in Informatics.
- Real screenshots and review images should be shown in their original form.

## Image handling

Repository HTML references files directly. Do not generate, resize, convert or split user images unless explicitly requested.

Expected paths:

- `assets/hero/hero.png`
- `assets/about/about.jpg`
- `assets/results/result-100.png`
- `assets/results/result-90.png`
- `assets/results/result-88.png`
- `assets/results/result-78.png`
- `assets/results/result-75.png`
- `assets/results/result-72.png`
- `assets/reviews/student-1.png` through `student-4.png`
- `assets/reviews/parent-1.png` through `parent-4.png`

Reviews use one image at a time with previous/next controls and mobile swipe. Do not force review screenshots into equal-height cards.

## Components and interaction

- Buttons: clear filled primary action, restrained text/navigation links elsewhere.
- Hover and focus states are required.
- Focus rings must remain visible.
- Score results can be opened to reveal the corresponding proof screenshot.
- Reviews are sliders, one original screenshot at a time.
- FAQ uses progressive disclosure and should remain visually quiet.
- AlfaCRM form is the conversion endpoint and must remain easy to reach.
- No dead `href="#"` controls.

## Mobile

- Body text remains at least 16 px where possible.
- Touch controls should be approximately 44 px or larger.
- Reorder content for the primary task rather than mechanically stacking desktop columns.
- Hero proof should stay visible without forcing horizontal scrolling.
- Score controls may become a two- or three-column grid.
- Review images remain uncropped.
- The signup form gets full available width.

## Copy

Apply Sepia by default:

- Plain, specific Russian.
- Delete filler and duplicated explanations.
- No chatbot residue.
- Avoid repetitive `не X, а Y` constructions.
- Avoid mechanical lists of exactly three items everywhere.
- Avoid uniformly polished paragraph rhythm.
- Use a clear judgment when one is needed.
- Do not insert fake imperfections.
- Do not invent specificity.
- Prefer the author's verified voice and wording habits.

## Anti-pattern checklist

Before shipping any broad UI change, check that the page does not contain:

- multiple competing primary CTAs;
- generic SaaS hero treatment;
- gradients or glass UI;
- walls of equal cards;
- repeated three-column feature layouts;
- invented social proof;
- unnecessary icons;
- excessive pill badges;
- decorative shadows and radius on every block;
- text explaining internal implementation details;
- broken mobile hierarchy;
- cropped review screenshots;
- dead links or invisible focus states.

## Verification

For every substantial redesign:

1. Inspect the current repository before editing.
2. Keep the primary user journey intact.
3. Verify desktop and mobile CSS rules.
4. Verify all CTAs resolve to the signup form.
5. Verify proof image paths remain unchanged unless the user explicitly asks otherwise.
6. Verify no 93-point result appears.
7. Verify the GitHub Pages deployment succeeds.
