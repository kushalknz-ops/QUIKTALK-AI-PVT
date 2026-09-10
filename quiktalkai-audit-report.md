# FULL WEBSITE AUDIT — quiktalkai.com (www.quiktalkai.com)
**Audited:** 9 September 2026 · **Testing type:** Non-destructive, publicly available access only
**Auditor roles applied:** QA, Security, Technical/On-Page SEO, AEO/GEO, UX/CRO, Performance, Accessibility, Marketing, Analytics

> **Read me first — evidence conventions used throughout this report:**
> - ✅ **Tested/Observed** — directly verified by request/code inspection during this audit.
> - 🔍 **Inferred** — established by combining observations with standard web-platform behaviour.
> - ⚠️ **Unverified / Not verifiable with available access** — explicitly flagged. **No data in this report is fabricated.** There was no browser-rendering lab available (PageSpeed Insights API returned HTTP 429 quota-exceeded; no headless browser in the sandbox), so Core Web Vitals are **estimated from resource analysis, not measured**. No Google/Bing index data, search rankings, traffic, backlink counts, or revenue data were retrievable and none are claimed.

---

## 1. EXECUTIVE SUMMARY

### 1.1 Overall Score: **49 / 100 — Grade C−**

| Dimension | Score /100 |
|---|---|
| Overall Website Health | 52 |
| Technical SEO | 30 |
| On-Page SEO | 55 |
| AEO (Answer Engine Optimisation) | 32 |
| GEO (Generative Engine Optimisation) | 15 |
| Content | 38 |
| UX / UI | 62 |
| CRO | 30 |
| Performance | 65 |
| Mobile | 60 |
| Accessibility | 35 |
| Security | 62 |
| Privacy / Compliance | 40 |
| Analytics & Tracking | 5 |
| Marketing | 30 |
| Technical Quality | 55 |

**Why this score is not inflated:** the site is visually striking, technically clean in places (Cloudflare CDN, compression, single static page, instant TTFB), but it has **one P0-level defect that destroys its entire business purpose** — the lead form does not submit anywhere — plus a wholesale absence of SEO/AEO/GEO foundations (11-day-old domain, no sitemap, no robots.txt, no schema, no analytics, no privacy pages, no social proof, no pricing).

### 1.2 Top 10 Problems

| # | Problem | Severity |
|---|---|---|
| 1 | **The lead form (`#leadForm`) never sends data anywhere** — `handleFormSubmit()` only fakes button text. Zero fetch/XHR/endpoint exists in the page. Every demo request is lost. | P0 |
| 2 | **`Privacy Policy` and `Terms of Service` links point to `#about`** — no such pages exist; the site collects personal data (name, business, phone, email, website) while claiming "NZ & AU Privacy Act Compliant". | P0/P1 |
| 3 | **Zero analytics/tracking** — no GA4, GTM, Meta Pixel, Clarity, Hotjar, or any event tracking. Conversion rate is unmeasurable; retargeting/advertising is impossible. | P1 |
| 4 | **Brand entity is incoherent** — "Quiktalk AI" (title/logo), "QuickTalk AI" (FAQ/footer), "QuikTalk AI" (nav) on the same page; "QuickTalk AI" is also an unrelated iOS app with 1,597 reviews (brand collision). | P1 |
| 5 | **No pricing anywhere** — direct NZ competitors (Talkify $129–$199/mo, Bizzy Boss $147/mo) publish full pricing on-page with schema. "You'll get exact pricing on your demo call" is a major conversion blocker. | P1 |
| 6 | **No robots.txt, no XML sitemap, no canonical, no structured data at all** — the crawl/indexation foundation is missing despite 100% indexable content. | P1 |
| 7 | **No social proof** — zero testimonials, reviews, case studies, customer logos, or live demo number; no address, no phone number, no company/legal entity, no social links. Trust signals are absent for a product that records business calls. | P1 |
| 8 | **Unsupported claims** — "100% ROI guaranteed within 60 days", "Answers 100 incoming calls simultaneously", "$42,000+/year salary", ROI calculator outputs ($15,500/mo) with undisclosed assumptions ($500/job, 30% missed, 70% recapture). | P1 |
| 9 | **Accessibility failures** — placeholders-only form (no labels/autocomplete), no keyboard focus styles, div-based FAQ (not operable by keyboard), no `prefers-reduced-motion`, contrast failure on 11px metadata, no skip link/`<main>`, no `noscript` (JS-off users see a stuck preloader). | P1 |
| 10 | **Security hardening gaps** — no HSTS at edge, no CSP, no X-Frame-Options/Referrer-Policy/Permissions-Policy; DMARC `p=none`; no DKIM found at common selectors; `.git`/`.env` verified absent but origin (`quicktalk-ai.onrender.com`) is directly reachable. | P1/P2 |

### 1.3 Top 10 Opportunities

1. **Fix the form with a real endpoint** (Cloudflare Pages Function / Web3Forms / Formspree / n8n webhook) + double-opt-in email → instantly restores revenue capture. Highest ROI action on the site.
2. **Publish transparent pricing** ($X/mo by call volume) + a "compare vs human receptionist" cost table — matches what the best NZ competitor (talkify.nz) does and converts better than "call us".
3. **Add FAQPage + Organization/LocalBusiness + Service + Breadcrumb JSON-LD** — the FAQ already exists on-page; schema is the single biggest AEO win available.
4. **Add a real, working demo**: publish a live callable NZ number or "call the AI now" widget instead of the simulated-text-only demo → unique differentiator vs competitors (Talkify publishes a live number; Quiktalk's "simulator" is a canned text cycle).
5. **Stand up a multi-page content architecture** — /ai-voice-agents, /industries/roofing, /pricing, /case-studies — to compete for the exact keyword set competitors already own.
6. **Add analytics + conversion events** (demo CTR, form submit, phone click, email click) so the funnel can be optimised at all.
7. **Publish privacy policy + terms + company details** (legal name, NZ address, NZBN if applicable) → unlocks compliance claims, trust, and Google Business Profile eligibility.
8. **Fix brand consistency + register social handles** (LinkedIn company page, X, Instagram) + sameAs schema → entity clarity for AI engines.
9. **Fix the asset pipeline** (196–605 KB PNG logo used as favicon and hero asset; 608 KB sync three.js) — page weight drops by ~70% with trivial effort.
10. **Publish original proof content** — a "2026 NZ missed-call survey" or public call-answer latency benchmark, plus a dated pricing calendar → citation-worthy first-party data for AEO/GEO.

### 1.4 Critical Security Concerns
- **No confirmed vulnerability was found.** Attack surface is minimal (static page, no server endpoints, no forms backend, no cookies, no user input echoed). Confirmed-exposure checks: `/.env`, `/.git/HEAD`, `/.git/config`, `/assets/` listing, `/api/` — all 404 on origin and edge.
- **Likely/potential risks (non-destructive scope):** missing security headers (CSP, HSTS at edge, XFO, Referrer-Policy, Permissions-Policy); DMARC record is `p=none` (no enforcement) and no DKIM was found at common selectors (`default`, `google`, `selector1`, `k1`, `mail`) — domain spoofing for phishing is possible; origin subdomain `quicktalk-ai.onrender.com` exposes the hosting platform and bypasses Cloudflare's edge protections if its DNS is ever linked; the mail `admin@quiktalkai.com` is only protected by SPF (`~all` softfail).
- **Requires manual pen-testing (NOT performed):** authenticated/administrative surfaces (none exposed), the demo-agent voice backend (not referenced on the public site).

### 1.5 Biggest SEO Problems
1. No sitemap, no robots.txt, no canonical, no structured data (0 JSON-LD blocks found).
2. Single-page site: one URL must rank for every keyword; no service/industry landing pages; footer "SERVICES" items are anchor links to `#demo`, not pages.
3. Domain is 11 days old with no external links, no social presence, no directory/citation footprint — zero authority baseline.
4. Brand name inconsistency across title/body/FAQ harms entity recognition.
5. No OG/Twitter meta → broken sharing previews (LinkedIn/FB/X) for a link-based B2B sales motion; no `apple-touch-icon`/`favicon.ico` (404).

### 1.6 Biggest UX Problems
- Fake loading preloader (animated progress to "100%" that is not tied to any real load) blocks the page for ~1s; it never hides if JS fails (no `<noscript>`).
- 10–11px uppercase letter-spaced button/label text; the primary heading claims contradict the microcopy; persistent full-viewport WebGL canvas runs on every device incl. mobile (GPU/battery).
- FAQ is JS-only div toggles; sections have no `<h2>` labels for landmarks; no active nav state; the "simulator" is canned text, not a real call.
- Inline `onmouseover`/`onmouseout` inline styles in the footer (janky hover styling, poor maintainability).

### 1.7 Biggest Conversion Problems
- **The only conversion path is the form, and it does not submit.** Confirmed by code inspection: `handleFormSubmit()` = `preventDefault()` → text swap → `disabled = true`. No network call of any kind exists in the document.
- No pricing → no comparison frame; no social proof/reviews; no phone number to call; no live demo; no trust seals; email-only contact; policy links that don't lead to policies; 6-field form (2 below-friction optional fields) with placeholder-only labels and no `autocomplete`.

### 1.8 Biggest Performance Problems
- three.min.js: **608 KB raw / 157 KB brotli**, loaded synchronously (end of body) with no `defer`/`async` — blocks main-thread parse/execution on every device, plus a permanent `requestAnimationFrame` GPU loop (no IntersectionObserver/visibility-based pause) on a full-viewport canvas up to 2× DPR.
- `assets/logo.png` is a **1024×1024 RGBA PNG (observed 196 KB–605 KB across fetches) used as favicon + brand mark + avatar**; 4 `<img>` usages of the same file; no WebP/AVIF, no `srcset`, no explicit width/height on all variants, no `loading="lazy"` on below-fold images.
- `cache-control: public, max-age=0, s-maxage=300` — browsers revalidate every asset on every visit (ETag 304 round-trips).
- Estimated first-load transfer ≈ **375–780 KB** (HTML 21 KB gz + three.js 157 KB br + logo) — heavy for a brochure page.
- **Core Web Vitals: not measured (no lab/browser available). Estimated** from analysis: LCP likely **"Good"** (text-based hero; the canvas is WebGL, not an img) **~1.5–2.5 s on mid-tier mobile**; INP **likely "Needs improvement"** on low-end devices due to 608 KB synchronous JS + continuous rAF; CLS **likely low** (system fonts, no font swap, but images lack intrinsic dimensions — small shift risk). These are **estimates, not measurements**.

### 1.9 Biggest AEO/GEO Opportunities
- Add **FAQPage schema** to the existing 11-question FAQ (highest-value AEO action), plus a "What is an AI voice receptionist?" definition block answer-first near an H2.
- Add **Organization + LocalBusiness(Auckland) + Service + sameAs** JSON-LD; publish company/address/founder details.
- Standardise branding to one name; secure matching social handles; get listed in NZ business directories (LinkedIn, Google Business Profile, NZBN register) for entity grounding.
- Publish **dated, first-party data** (e.g., call-answer latency benchmark methodology, "state of missed calls in NZ" — original research is the currency of AEO/GEO citations).
- Keep AI crawlers unblocked (they currently are — no robots.txt at all is permissive, but a proper robots.txt + `llms.txt` is recommended as an experimental bonus; treat as optional).

### 1.10 Estimated Business Impact
- **Confirmed-at-code-level:** 100% of demo-request form submissions are lost today. At even 1 demo request/day → **~30 lost sales conversations/month** — the entire traffic the site generates is wasted.
- **Unquantified but real:** no analytics means no way to know traffic, bounce, or conversion; no local/SEO foundation on an 11-day domain means organic visibility ≈ 0 for at least 6–12 months without significant content/authority work; competitors with published pricing and live demos will win every comparison search.
- If the form, pricing, proof, schema and analytics fixes ship within 30 days, the realistic near-term upside is converting the same traffic that currently converts to **zero**.

---

## 2. METHODOLOGY, SCOPE & LIMITS

**Performed (all read-only, respectful of crawl limits):**
- Full HTML/CSS/JS source analysis of `https://www.quiktalkai.com/` (85.7 KB raw / 21 KB gzip).
- HTTP header & status-code testing across www/non-www, http/https, origin vs edge.
- 20+ common path probes (sitemap, robots, privacy, pricing, blog, `.env`, `.git`, directory listing) — all 404 except noted.
- DNS records (A/AAAA/CNAME/NS/MX/TXT/DMARC/DKIM common selectors), TLS certificate inspection (issuer, validity, SANs, protocol support), WHOIS (domain age).
- Resource weight/caching analysis; contrast-ratio calculation for key colour pairs; keyboard/ARIA static analysis; JS execution-order analysis (hoisting, throw paths).
- Web research: brand mentions, competitor pricing/positioning (talkify.nz, bizzyboss.co.nz), keyword landscape.

**Not performed / not verifiable with available access:**
- Real-browser rendering, Lighthouse/CrUX/PSI field data (API quota exceeded **HTTP 429**), cross-browser matrix (Chrome/Edge/Firefox/Safari), real-device mobile testing, screen-reader testing, indexation/crawl-status verification in Google Search Console (no GSC access), backlink index data (Ahrefs/Semrush/Moz), real form submission to any backend (**there is no backend to submit to**), email delivery testing (no messages were sent — per testing rules), live demo call testing (no number published), paid Google/Meta account data, and any authenticated area (none exists).

---

## 3. SITE DISCOVERY & ARCHITECTURE

### 3.1 Site Profile
| Attribute | Finding |
|---|---|
| Purpose | Lead generation for an AI phone-receptionist service (24/7 AI voice agents) |
| Target audience | NZ & AU small businesses: trades (roofing/HVAC/plumbing), dental/healthcare, law/finance, auto, restaurants, real estate |
| Primary conversion action | "Build my free demo agent" form submission (**currently non-functional**) |
| Secondary actions | Email to admin@quiktalkai.com; anchor CTAs to `#demo` |
| Structure | **Single-page site** — 1 HTML document, ~8 in-page sections, zero sub-pages |
| Pages found | 1 (all other paths 404, including `/about`, `/contact`, `/pricing`, `/blog`) |
| CMS/Framework | None — hand-built static HTML/CSS/JS (no framework markers, no build artefacts) |
| Hosting | Cloudflare Pages (edge: `server: cloudflare`, `rndr-id`, `cf-cache-status`) with DNS `www` CNAME → `quicktalk-ai.onrender.com` (Render origin behind Cloudflare) |
| CDN | Cloudflare (HTTP/2 + HTTP/3 confirmed, `alt-svc: h3`) |
| JS frameworks | None — vanilla JS + Three.js (full bundle, 608 KB raw) |
| CSS | Inline `<style>` block (30.4 KB), no framework |
| Analytics | **None found** |
| External scripts | **1** (`assets/three.min.js`) — no third-party scripts, no pixels, no widgets |
| External links from the page | **0** — no outbound citations, no social links |
| Forms | 1 (`#leadForm`, dead) |
| Login/signup/e-commerce | None |

### 3.2 Page Architecture
```
https://www.quiktalkai.com/
├── #hero           "Never miss another call." — H1, dual CTA, stats, call simulator box
├── #process        How it works — 4 steps
├── #industries     6 industry cards
├── #comparison     Human vs AI table + ROI calculator       ← claims-heavy
├── #integrations   Tool grid + "what's included" checklist
├── #about          Auckland-built, guarantees (1 paragraph — thin)
├── #faq            11-question accordion (best content on the site)
└── #demo           Lead form (BROKEN) + microcopy
```

### 3.3 Page Priority Classification
| Priority | Pages | Notes |
|---|---|---|
| Critical | Homepage/#demo form | The entire site; form is P0-broken |
| High | FAQ section | Best AEO raw material; needs schema |
| Medium | Industries, Integrations, Comparison | Content candidates to become standalone landing pages |
| Low | About, Simulator | Thin; About is one paragraph |
| Potentially redundant | Simulator (canned text, not a demo) | Replace with a real callable demo or remove |
| Broken | Privacy/Terms links (`#about`), form | Confirmed |
| Orphaned | None (single page) | — |
| Duplicate | None (single page) | — |
| Thin | About, Integrations "what's included", hero stats | — |
| Unnecessary | `assets/logo.png` as favicon (605 KB image) | — |

---

## 4. COMPLETE QA TESTING RESULTS

### 4.1 Navigation
| Test | Result |
|---|---|
| Header nav (desktop) | ✅ Works — 8 anchor links, all targets exist |
| Mobile burger menu | ✅ Opens/closes via `toggleMenu()` (`display:flex` on `.open`); ⚠️ no `aria-expanded`, no Escape-to-close, no focus trap, body scroll not locked, active state not marked |
| Footer navigation | ✅ All anchors resolve (but Privacy/Terms point to `#about` — **wrong target**) |
| Dropdowns/mega menus | ➖ None exist |
| Breadcrumbs | ➖ None (single page) |
| Internal links | ✅ 100% of internal links resolve (they're in-page anchors) |
| External links | ✅ 0 external links exist (see §19 — also a missed opportunity) |
| Back/forward nav | 🔍 Standard anchor behaviour — hash changes work; no SPA router, no history issues |
| On-page search | ➖ N/A |
| Pagination/filters/sorting | ➖ N/A |
| Tabs/accordions | ⚠️ FAQ accordion works via JS (`toggleFaq`) but **fails with JS disabled** (answers `display:none`, no `<details>` fallback); no keyboard support; no `aria-expanded`/`aria-controls` |
| Modals/popups | ⚠️ Mobile menu behaves as an overlay; no modal dialog semantics or focus management |

### 4.2 Forms — `#leadForm`
| Test | Result |
|---|---|
| Required fields | ✅ `required` on name, business name, phone, email, message |
| Optional fields | ✅ Company website (no `required`) |
| Validation | ✅ Native browser validation only (no custom errors/formatting) |
| Invalid input / empty submission | ✅ Native HTML5 blocks; no custom error messages |
| Incorrect email format | ✅ Native `type=email` blocks |
| Phone validation | ⚠️ `type=tel` only — accepts any string; no pattern/length/normalisation (NZ/AU formatting inconsistent) |
| Character limits | ❌ None — unlimited-length inputs, no `maxlength` |
| Special characters/emoji | 🔍 No server-side handling exists; nothing to test |
| Copy/paste behaviour | 🔍 Standard inputs; no paste handling (no issue) |
| Error messages | ❌ None custom — browser defaults only |
| Success messages | ❌ **Misleading** — "✓ DEMO REQUEST SUBMITTED" is displayed **without any data being sent** |
| Duplicate submissions | ⚠️ Button disabled after fake submit, but page refresh resets everything (and no data was ever stored) |
| Refresh behaviour | 🔍 No persistence — all fields cleared on refresh; no `localStorage` resume |
| Form persistence | ❌ No draft persistence (lost lead on accidental refresh) |
| Spam protection | ❌ None (no CAPTCHA, honeypot, or rate limiting) — though there is no backend to abuse |
| Submission handling | ❌ **`handleFormSubmit(e)` only calls `e.preventDefault()`, swaps button text, and disables the button. No fetch, no XHR, no FormData, no endpoint.** Verified: zero network-call patterns in the entire document |
| Email notification | ❌ N/A — nothing is submitted |
| Database/API submission | ❌ N/A |
| Redirects / thank-you page | ❌ N/A — no redirect, no thank-you page, leads "succeed" invisibly |

### 4.3 Interactive Functionality
| Element | Result |
|---|---|
| CTAs (hero/nav/footer) | ✅ All scroll correctly |
| Call simulator | ⚠️ Cycles 3 hard-coded script strings; does not simulate speech/audio; not a real demo |
| ROI calculator | ✅ Slider 30–1000 calls updates labels; ⚠️ hard-coded assumptions ($500 avg job, 30% missed, 70% recaptured) are **not disclosed in the UI** |
| 3D hero (Three.js) | ⚠️ Runs on all devices; **no WebGL capability check, no try/catch** — on WebGL-less devices `new THREE.WebGLRenderer()` throws; page degrades (hero section shows background only) but other JS survives (function declarations hoisted) — verified via execution-order analysis |
| Downloads/videos/audio | ➖ None |
| Login/registration/password | ➖ N/A |
| Cart/checkout/payment | ➖ N/A |
| User dashboards | ➖ N/A |

### 4.4 Edge Cases (explicitly tested/analysed)
| Case | Result |
|---|---|
| JS disabled | ❌ **Preloader never hides** (`#pre` removal requires JS; **no `<noscript>`**). Users see a permanent black screen with "0%". FAQ answers also permanently hidden |
| Slow connection | 🔍 Preloader is time-based (fake progress), content becomes visible only after ~0.8–1.0 s + script completes |
| Missing WebGL | ⚠️ 3D scene throws (no fallback image/static hero) |
| Rapid double-click submit | ⚠️ Button text changes but no duplicate network call occurs (nothing is sent) |
| Very long input | ❌ No `maxlength` |
| Refresh mid-form | ❌ All field content lost |
| Keyboard-only navigation | ❌ No visible focus ring on links/buttons (`:focus` styles exist **only** on `.input-field`); FAQ items not keyboard-operable |
| Zoom 200% / text scaling | 🔍 `px`-based layout with `clamp()` headings — likely adequate; untested in a real browser |

---

## 5. RESPONSIVE & MOBILE

- ✅ Two breakpoints exist: `@media (max-width: 900px)` and `@media (max-width: 600px)` — grids collapse, burger menu appears, rail hidden.
- ✅ Viewport meta correct (`width=device-width, initial-scale=1, viewport-fit=cover`).
- ✅ No horizontal scrolling expected (body `overflow-x: hidden`; grids collapse to 1 column on mobile). *Static analysis only — not browser-tested.*
- ⚠️ **Full-viewport WebGL canvas at up to 2× devicePixelRatio, continuously rendering** — significant battery/thermal impact on phones. No pause on tab-hide (`visibilitychange`: 0) or scroll-away (`IntersectionObserver`: 0). **Do not ship this to mobile without a static fallback or an `IntersectionObserver`/`matchMedia` throttle.**
- ⚠️ Micro-copy and button text at **10–11px uppercase with 0.2em letter-spacing** — hard to read on small screens.
- ⚠️ Burger button is **26×16 px** — below the WCAG 2.5.8 24×24 px minimum touch target.
- ⚠️ Mobile menu: no scroll lock, no Escape close, no active-section indication.
- ⚠️ The form on mobile is 5 required fields + textarea with placeholders only (no labels/autocomplete) — high fill friction; and it doesn't submit anyway.
- ❌ No `apple-touch-icon` (iOS home-screen icon absent), no `theme-color` (browser chrome colour not set), no favicon.ico.

---

## 6. UX / UI AUDIT

**Strengths:** coherent premium dark "champagne gold" design system (CSS custom properties, consistent tokens), strong visual hierarchy per section, clear single H1, generous spacing, brand-consistent imagery. As a "look" it is genuinely above average.

**Findings:**
1. **Fake loading experience** — the preloader's progress bar advances on a `setInterval` with random increments, not real load progress. Deceptive UX pattern; delays content by ~1 s; blocks everything if JS fails. *(What's wrong → matters because users feel the site is slow/fake; affects all users; fix: remove preloader or tie to real `load`/use `DOMContentLoaded` fade; priority P2.)*
2. **Information architecture is one long scroll** — no separate pages for services, pricing, or proof; the footer "SERVICES" items (AI Voice Agents, AI Systems & Automations, AI Consulting, Web & Software Development) all link to `#demo`, so visitors can't learn about four of the five services they sell. *(Fix: build service pages...; priority P1.)*
3. **No pricing transparency** — see §8. *(P1.)*
4. **Trust gap** — no address, no phone number (mail only), no company legal name, no founder/team, no reviews, no case studies, no customer logos, no security/privacy explanation for call recording. For a service that will record your business's phone calls, this is the single biggest content gap. *(P1.)*
5. **Typography** — body 14px `#a1a1aa` on near-black (contrast 7.7:1 — passes), but 10–11px uppercase CTAs and 11px `#71717a` microcopy (contrast ≈ 4.1:1 — **fails WCAG AA for normal text**). *(P2.)*
6. **Hover-only styling** — footer links change colour via inline `onmouseover`/`onmouseout` (also an inline-handler/СSP smell). *(P3.)*
7. **No active-nav/scroll-spy** — users lose their place in a 16-screen page. *(P3.)*
8. **Simulator mislabelled** — button says "TEST SIMULATED CALL", content is typed text; expectations vs experience mismatch. *(P3.)*

---

## 7. CRO AUDIT

| CRO element | Status |
|---|---|
| Primary CTA ("GET MY DEMO AGENT") | ✅ Visible above fold and in sticky navbar; ⚠️ leads to a **dead form** |
| Value proposition | ✅ Clear in H1 ("Never miss another call. Our AI answers 24/7 — and books the job.") |
| Above-the-fold content | ✅ Strong promise + 3 stat chips (24/7, 0.4 s, 3 days, free demo) |
| Trust signals | ❌ Guarantees list only; no reviews/testimonials/logos/case studies |
| Pricing | ❌ Opaque ("exact pricing on your demo call") — **competitors publish prices** |
| Lead form | ❌ **Non-functional** + 6 fields + placeholders only |
| Objection handling | ⚠️ FAQ covers 11 objections well (good), but is hidden behind JS toggles and has no schema |
| Social proof | ❌ **Zero** |
| Guarantees | ⚠️ "100% ROI guaranteed within 60 days" — bold, unsupported, and legally risky claim; prefer verifiable guarantees |
| Secondary CTA | ⚠️ "SEE LIVE SIMULATION" — demo is canned text, not live |
| Exit points | ⚠️ None addressed (no exit-intent care, but also no retargeting pixels) |

**Conversion blockers (ranked):** (1) form not submitting — **entire funnel is broken**; (2) no pricing; (3) no proof; (4) opaque "what happens next" (no calendar booking, no "call us" alternative); (5) 6 fields with no labels/autocomplete; (6) no visible response SLA (claim exists in microcopy only); (7) no phone number to talk to a human.

---

## 8. TECHNICAL SEO AUDIT

| Check | Result |
|---|---|
| robots.txt | ❌ **404** (Cloudflare/Render returns 404 "Not Found"). No rules at all — permissive by default, but no Crawl-delay, no explicit allow, and no sitemap declaration |
| XML sitemap | ❌ `/sitemap.xml`, `/sitemap_index.xml` → **404** |
| Canonical | ❌ No `<link rel="canonical">` (single page, low risk, but should exist) |
| Indexability | ✅ Default indexable (no `noindex`); static HTML means content is served without JS rendering |
| HTTPS | ✅ HTTP→HTTPS 301 (all four host variants tested) |
| HTTP→HTTPS / www consistency | ⚠️ Correct but chained: `http://quiktalkai.com → https://quiktalkai.com → https://www.quiktalkai.com` (2 hops; collapse to 1) |
| TLS | ✅ Valid Google Trust Services certs (www: valid to Dec 1 2026; root: separate cert valid to Dec 2 2026); TLS 1.2 confirmed; **TLS 1.0/1.1 refused** (tested — protocol errors returned); HTTP/3 confirmed |
| Status codes | ✅ 200 on homepage; real 404s (text/plain) elsewhere; no soft-404s observed |
| Redirect chains/loops | ⚠️ 2-hop chain for root; **no loops** (verified) |
| URL structure | ✅ Clean single URL; ⚠️ no hierarchical structure for subpages (none exist) |
| Duplicate URLs/content | ✅ None (single page; www/non-www canonicalised via 301) |
| Hreflang/international | ➖ Single language — no hreflang needed; but NZ/AU targeting has no geo signals (`en` only, no local schema, no geotargeting meta — not that meta is used anymore) |
| Structured data | ❌ **0 JSON-LD blocks** — no Organization, LocalBusiness, FAQPage, Service, Breadcrumb, Review, or VideoObject |
| Open Graph / Twitter | ❌ **None** — social shares render as bare links |
| Meta title | ✅ "Quiktalk AI — Personalised 24/7 AI Voice Agents" (57 chars, strong) — ⚠️ brand spelling inconsistent with body |
| Meta description | ✅ Present, ~152 chars, well-written |
| H1 | ✅ Exactly one H1; ⚠️ H2s unnumbered (fine), but H1 includes "never miss another call" — no commercial keyword ("AI receptionist/voice agent") in H1 |
| Heading hierarchy | ⚠️ Single `h4` ("OUR CORE GUARANTEES") out of sequence (h2→h4 jump) |
| Image alt text | ✅ All 4 images have alt; ⚠️ generic ("Quiktalk AI Logo" etc.) — no descriptive alt, no keyword context |
| Internal linking | ⚠️ Single page → no internal link graph; footer services are anchors |
| JS-rendered content | ✅ Content is server-rendered/static — fully crawlable without JS (verified raw HTML contains all text) |
| Crawl depth | ✅ Depth 0 — trivial |
| Crawlability of form/JS errors | 🔍 Googlebot gets HTTP 200 with identical HTML (no cloaking — tested with Googlebot UA) |

---

## 9. ON-PAGE SEO

Per-page analysis (the only page):

- **Title:** good length and promise; recommend one that carries the commercial keyword: e.g. **"AI Receptionist NZ & AU | Quiktalk AI — 24/7 AI Voice Agents"** (~55 chars).
- **Meta description:** good; recommend adding price/geo hook: *"Custom AI voice agents for NZ & AU businesses. Answer every call 24/7, qualify leads, book jobs into your calendar. Free demo agent — live in 3 days."*
- **H1:** "Never miss another call. Our AI answers 24/7 — and books the job." — emotive but keyword-less. Recommend: **"24/7 AI Voice Receptionists for NZ & AU Businesses"** with the H1 promise as a supporting sentence.
- **H2s:** cover process, industries, comparison, integrations, about, FAQ, demo — good topical spread for one page.
- **Search intent:** the page matches informational-comparison intent ("why you need this"), but has **no transactional/comparison content** (pricing) and no long-tail pages.
- **Keyword targeting:** no explicit targeting of "AI receptionist NZ", "AI phone answering service Auckland", "AI voice agent Australia" — the exact queries (checked against competitor sites that rank for them) are absent from any heading/title.
- **Keyword cannibalisation:** N/A (one page).
- **Thin/duplicate content:** About section is one paragraph + three bullet guarantees — the thinnest section; no duplicates.
- **Title/meta suggestions for future pages** (see §36 SEO action plan for full list).

---

## 10. CONTENT QUALITY AUDIT

- **Accuracy/evidence:** ❌ Unsupported claims: "100% ROI guaranteed within 60 days"; "Answers 100 incoming calls simultaneously"; "$42,000+ / year salary" (NZ human-receptionist market data indicates roughly NZ$55–65k p.a. — the comparison understates local cost and doesn't state currency); "0.4s answer speed" (has a footnote — good practice); calculator outputs with undisclosed assumptions.
- **Originality:** ✅ Hand-written, specific, NZ-localised (mentions Fergus, Tradify, ServiceM8, Cliniko, Halaxy, Medtech — credible domain knowledge and a genuine strength).
- **E-E-A-T:** ❌ No author(s), no credentials, no company legal entity, no physical address, no case studies, no data sources, no external reference links (0 external links on the page).
- **Freshness:** ⚠️ Undated content; last-modified header = 2026-09-09 (the site deploy date) — no datable evidence or changelog.
- **Generic AI-like content:** ✅ Text reads human and specific — no AI-slop patterns detected.
- **Completeness:** ❌ Missing: pricing, onboarding detail, refunds/cancellation terms, security/privacy of call data, real recordings, SLA.

---

## 11. AEO — ANSWER ENGINE OPTIMISATION

| AEO requirement | Status |
|---|---|
| Question-based headings | ✅ FAQ "Questions owners ask us every week" — 11 questions |
| Direct answers near headings | ✅ Answers are concise 2–3 sentences (good) |
| FAQPage schema | ❌ **Missing** — the single highest-leverage AEO fix; answers are currently JSON-unreachable for answer engines |
| Definitions ("what is an AI receptionist?") | ⚠️ Implicit in FAQ Q1 but no crisp "X is a…" definition block with a keyword-rich H2 |
| Step-by-step instructions | ✅ Process section (4 steps) — but no HowTo schema |
| Structured information | ⚠️ Tables/lists present; no schema |
| Supporting evidence/sources | ❌ None |
| Voice-search phrasing | ⚠️ Mix of natural phrasing; Q7/Q8 are long — good for voice |
| Snippet-optimised body copy | ⚠️ No keyphrase mentions of "AI receptionist [price]" in headings (competitors' snippets answer "what does an AI receptionist cost in NZ?") |

**Recommended AEO content structures:** add a `"What is an AI voice receptionist?"` ~50-word definition directly under the H2 (answer-first); convert the comparison block into an H3-question ("How much does a human receptionist cost vs an AI?"); mark up all FAQs with FAQPage; consider HowTo schema on the 4-step process; add "cost in NZ" answer block (🔍 factual basis required before publishing).

---

## 12. GEO — GENERATIVE ENGINE OPTIMISATION

| GEO factor | Status |
|---|---|
| Entity clarity | ❌ **Three brand spellings on one page** ("Quiktalk", "QuickTalk", "QuikTalk") — an LLM will struggle to resolve the entity |
| Brand identity | ⚠️ Logo exists (headset/chrome style) but no visual/verbal identity consistency |
| Topical authority | ⚠️ Good single-page depth, zero supporting pages/articles |
| Factual consistency | ⚠️ Contradiction risk: title says "Personalised 24/7 AI Voice Agents" vs footer "AI voice receptionists"; FAQ spelling "QuickTalk AI" differs from domain "quiktalkai.com" |
| Brand mentions (web) | ⚠️ None found in search results for "quiktalkai" (only an unrelated "QuickTalk AI" language app with 1,597 reviews was found — **name collision**) |
| Citation-worthiness | ❌ No original data/research, no URLs cited by others; domain has zero found backlinks and is 11 days old |
| First-party information | ⚠️ Test-call speed claim (needs a public, dated benchmark to be citable) |
| Authoritativeness signals | ❌ No author, no company page, no social profiles, no directories |
| Structured content/schema | ❌ None |
| AI crawler accessibility | ✅ Allowed by default (no robots blocks) — but no `llms.txt` (experimental, optional) |
| Knowledge-graph readiness | ❌ No Organization schema, no sameAs, no Wikipedia/Wikidata presence — entity will not be recognised reliably |

**GEO verdict:** effectively **not ready** — and that is expected for an 11-day-old domain. The fastest wins: unify brand name, add Organization+LocalBusiness schema with sameAs, build LinkedIn/X/Instagram + Google Business Profile, publish one piece of original research, and start acquiring local citations.

---

## 13. LOCAL SEO

- ⚠️ Business claims "Built in Auckland" but **no address, no phone number, no Google Business Profile link, no LocalBusiness schema, no location page, no service-area page** — local search presence is effectively zero.
- ❌ No NAP (name/address/phone) block anywhere — the mailto is the only contact detail.
- ❌ No reviews strategy, no GBP optimisation, no local citations.
- ✅ Strength: NZ/AU-specific industry language (Fergus, Tradify, ServiceM8, SimPRO, Cliniko, Halaxy, Timely, Fresha, Medtech, D4W, EXACT, Best Practice) — genuinely localised copy that supports topical relevance **once** pages exist to host it.
- Recommended: keyword domain `AI receptionist Auckland/NZ` pages + GBP listing + NAP in footer + LocalBusiness schema; NZBN if registered; note that `quiktalkai.com` is a `.com` without geo signals.

---

## 14. PERFORMANCE & CORE WEB VITALS

**Weights (measured via HTTP):**
| Resource | Size (wire) | Compression | Notes |
|---|---|---|---|
| `/` HTML | 85.7 KB raw / **21 KB gzip** | ✅ gzip/br | Inline `<style>` = 30.4 KB (no external CSS request — good) |
| `assets/three.min.js` | **608 KB raw / 157 KB brotli** | ✅ | **Synchronous** `<script>` (end of body), no `defer`/`async`, full library bundle |
| `assets/logo.png` | **196 KB–605 KB observed** (1024×1024 RGBA) | ❌ PNG | Used as favicon + brand mark + avatar; 4 `<img>` refs; no WebP/AVIF, no srcset, no lazy-loading, no width/height on all imgs |
| TTFB (edge, cached) | 0.60 s (first), ~0.2 s (warm) | — | CF `s-maxage=300` |
| TTFB (origin, direct) | 0.19–0.25 s ×3 | — | Render origin healthy, no cold-start observed (⚠️ warm instance; free-tier cold starts remain a risk) |
| HTTP/2 + HTTP/3 | ✅ | — | `alt-svc: h3` |
| Cache headers | ❌ `max-age=0, s-maxage=300` | — | Browsers revalidate everything every visit; 304 round-trips on all assets |
| Total requests | 3 (HTML+JS+PNG) | ✅ | Minimal request count is a real strength |

**Core Web Vitals — ⚠️ ESTIMATED, NOT MEASURED** (no browser lab available; PSI API 429):
- **LCP: likely Good-ish on fast connections** (hero LCP is text; H1 renders early) — small risk the logo image is LCP on some render paths.
- **INP: risk of "Needs improvement" on low-end mobile** — 608 KB synchronous JS parse/exec at startup (`renderer` + PMREM env-map generation is CPU-expensive), continuous rAF loop, mousemove listener on every event, per-frame `document.body.scrollHeight` read.
- **CLS: likely low** (system font stack = no font swap; but images lack intrinsic dimensions in HTML on at least one usage → small risk).
- **TBT: elevated on mobile** — synchronous three.js + WebGL compile at load.

**Top fixes (by expected impact):** (1) serve three.js via a lightweight custom scene or import maps + `defer`, or lazy-load on idle; (2) convert logo to AVIF/WebP + responsive `srcset` + explicit dimensions + `loading="lazy"` where below fold; (3) real favicon (32×32) and stop using a 1024² PNG as favicon; (4) `cache-control: public, max-age=86400, immutable` for `assets/` + far-future hashed filenames; (5) pause the WebGL loop on `document.hidden` and when hero is off-screen (`IntersectionObserver`).

---

## 15. SECURITY AUDIT (non-destructive)

| Check | Result |
|---|---|
| HTTPS/TLS | ✅ Valid certs (Google Trust Services; www + root separately), TLS 1.2+; TLS 1.0/1.1 rejected; HTTP→HTTPS 301 enforced |
| HSTS | ⚠️ **Present at origin** (`strict-transport-security: max-age=315360000; includeSubdomains; preload` on quicktalk-ai.onrender.com) **but stripped at Cloudflare edge** (absent on www response) — act: enable HSTS in Cloudflare dashboard |
| HSTS preload | ⚠️ Origin declares preload; edge does not serve it — preload eligibility compromised |
| Security headers | ❌ Only `X-Content-Type-Options: nosniff`. Missing: **CSP, X-Frame-Options/`frame-ancestors`, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener/Embedder** |
| Mixed content | ✅ None (all resources relative/https; only 3 requests) |
| Cookies | ✅ None set at all (no session surface; nothing to secure) |
| CORS | ➖ No API endpoints |
| Admin/debug exposure | ✅ No admin paths, no debug pages, no directory listing (`/assets/` 404), no `.env`/`.git`/`.htaccess` (verified 404 on origin + edge), no x-powered-by/server version leakage beyond `server: cloudflare` |
| Error-message leakage | ✅ 404s are plain "Not Found" (10 bytes) — no stack traces; no verbose errors |
| Inline script handlers | ⚠️ `onclick`/`oninput`/`onsubmit` inline handlers throughout + no CSP → any injected script would run unchecked. Inline handlers also block the strongest CSP posture |
| XSS | 🔍 Low risk surface: zero user input is rendered back (form doesn't submit); no reflection points found. **No confirmed XSS** |
| SQLi / SSRF / file upload | ➖ No server-side inputs, no uploads, no dynamic endpoints — **not applicable / no surface** |
| CSRF / auth | ➖ No state-changing endpoints or accounts |
| Open redirects | ✅ None found (redirects are fixed 301 hosts) |
| Email security | ⚠️ SPF: `v=spf1 include:_spf.mail.hostinger.com ~all` (softfail). **DMARC: `v=DMARC1; p=none`** — no enforcement → any sender can spoof quiktalkai.com. **No DKIM found** at `default/google/selector1/k1/mail._domainkey` (selectors may exist under other names — ⚠️ not verifiable exhaustively) |
| Origin exposure | ⚠️ `quicktalk-ai.onrender.com` serves directly (bypasses CF WAF/rate-limit layer if relied upon) — treat as "published" infrastructure |
| Third-party scripts | ✅ Only 1 (Three.js, self-hosted) — minimal supply-chain surface |
| Outdated components | ⚠️ Three.js pinned as a bundled minified file — no version detection possible in minified bundle (could not identify REVISION string); recommend upgrading to a maintained release in an import-map setup |

**Verdict:** no confirmed vulnerability; security posture is "small surface, thin hardening". Ranked likely risks: (1) DMARC p=none + no DKIM found → spoofing/phishing of the brand; (2) missing security headers; (3) HSTS not served at edge; (4) inline-handler architecture blocks a strict CSP.

---

## 16. PRIVACY & COMPLIANCE

- ❌ **No Privacy Policy page, no Terms of Service page** — footer links point to `#about`. A business collecting name, business, phone, email, and website of prospective customers **must** publish a privacy policy (NZ Privacy Act 2020 IPPs; AU Privacy Act; GDPR if any EU visitors). 
- ⚠️ The site **claims** "NZ & AU Privacy Act Compliant" and "Strict data sovereignty" with zero supporting documentation — a compliance claim without a policy is both a legal and a credibility risk.
- ✅ No cookies / no third-party trackers → no consent-management stack needed (yet). ⚠️ The moment GA4/pixels are added, a **consent banner will be required** (NZ has no strict opt-in law but Australian Privacy Act + GDPR for EU visitors make a CMP advisable).
- ❌ No data-retention statement, no "how we use your data", no rights/contact for privacy requests, no DPO/contact beyond a bare email address.
- ⚠️ Call-recording disclosure is handled only in FAQ copy — no per-jurisdiction verification documented.
- **Recommendation:** publish `/privacy-policy` and `/terms` (plain-language, NZ/AU-focused), add a checkbox consent for marketing comms on the form, and add a lawful-basis statement for call recording.

---

## 17. ACCESSIBILITY (WCAG 2.1 AA — static analysis)

| Criterion | Result |
|---|---|
| 1.1.1 Non-text content | ✅ Alt text on all 4 images (⚠️ not descriptive) |
| 1.3.1 Info & relationships | ❌ Form inputs have **no `<label>`/`aria-label`** (placeholders only); FAQ uses `<div>`+`onclick` with no button/role semantics; no `<main>` landmark; 8 sections with no accessible names |
| 1.4.3 Contrast | ❌ `#71717a` on `#060608` ≈ **4.1:1** — fails 4.5:1 (used for 11px microcopy); ✅ main body text `#a1a1aa` ≈ 7.7:1 passes; ✅ gold CTA on black ≈ 11.7:1 |
| 1.4.4 Resize text | 🔍 px-based fonts; likely OK to 200% but not browser-tested |
| 2.1.1 Keyboard | ❌ FAQ not keyboard-operable; mobile menu has no Escape/close key; ⚠️ burger has `aria-label` (good) |
| 2.4.7 Focus visible | ❌ **No focus styles on links/buttons** — only `.input-field:focus` exists (1 selector in 30 KB CSS) |
| 2.5.8 Target size | ❌ Burger 26×16 px < 24×24 min |
| 3.3.1/3.3.2 Error identification/labels | ❌ No visible labels; only native validation |
| 4.1.2 Name/role/value | ❌ Nav links use generic names; no `aria-expanded` on burger/FAQ; success message not announced (`aria-live` absent) |
| Motion | ❌ No `prefers-reduced-motion` support anywhere (0 occurrences); smooth scroll + continuous 3D animation + preloader all ignore it |
| Landmarks/skip links | ❌ No skip-to-content link; no `<main>` |
| Screen readers | 🔍 Not testable here; static analysis shows structural gaps (div FAQ, placeholder labels) |
| Zoom/mobile keyboards | ⚠️ `type=email/tel` help iOS keyboards (good); no `autocomplete`/`inputmode` attributes (bad — autofill friction) |

**WCAG severity:** P1/potential AA failures: 1.3.1, 2.1.1, 2.4.7, 3.3.2, plus 1.4.3.

---

## 18. ANALYTICS & TRACKING

**Finding: there are none.** ✅ Observed: the document contains zero references to gtag/GA/GTM/facebook/pixel/clarity/hotjar/segment/plausible/matomo/fathom; the only external script is `three.min.js`; no event listeners on CTAs.

Consequences: unknown traffic, unknown conversion rate, no attribution, **cannot run paid ads effectively** (no conversion pixel), no heatmaps/session records, no email/pixel retargeting. For a new business this is a foundational gap — you cannot optimise what you cannot measure. **P1.**

Recommended stack (lightweight): GA4 or Plausible + GTM; events: `demo_cta_click`, `simulator_play`, `form_submit_attempt`, `form_submit_success` (after real backend), `email_click`, `slider_interaction`; Meta pixel + LinkedIn Insight Tag only after consent banner is implemented.

---

## 19. MARKETING AUDIT

| Element | Status |
|---|---|
| Positioning | ✅ Clear ("AI answers 24/7 and books the job") — genuinely differentiated message vs "answering services" |
| Messaging consistency | ⚠️ Brand spelling chaos; promise vs delivery gap (demo is canned text) |
| Offers/lead magnet | ✅ Free demo agent — strong offer; ❌ unreachable (dead form) |
| Email capture/automation | ❌ None configured (form dead; no welcome sequence, no nurture) |
| Social proof | ❌ Zero |
| Content marketing | ❌ No blog, no guides, no case studies |
| Landing pages | ❌ One page for every audience/industry |
| Retargeting | ❌ No pixels |
| Organic acquisition | ⚠️ 11-day domain; no content assets; see SEO risks |
| Paid acquisition readiness | ❌ No tracking → no ads readiness |
| Differentiation vs competitors | ⚠️ Unique "Build demo agent in 3 days on your number" angle is strong — but competitors (talkify.nz) already publish live-demo numbers, pricing, comparison tables and reviews |

**Biggest marketing opportunities:** (1) make the form work + add a real callable demo number (competitive differentiator); (2) publish pricing transparently; (3) collect and display early customer reviews; (4) start a "missed calls" benchmark/topics engine; (5) LinkedIn outbound + GBP + local SEO; (6) WhatsApp/SMS demo funnel for AU/NZ SMBs.

---

## 20. COMPETITOR ANALYSIS

⚠️ Based on public web research (9 Sep 2026); no rank/backlink data, no fabricated numbers.

**Direct NZ/AU competitors:**
1. **Talkify (talkify.nz)** — closest direct competitor. Published pricing ($89 PA / $129 business founding rate → $199, 200 min, 10c/min overage; $499 custom from), live callable demo numbers (03 242 1262 / 0800 numbers), full schema (LocalBusiness + OfferCatalog + aggregate rating + FAQ), multi-page keyword architecture (/ai-receptionist, /ai-answering-service, /ai-phone-agent, /ai-receptionist-for-tradies), te reo Māori support, NZ data-sovereignty messaging, sameAs social links, reviews (3× 5★), dated pricing pages, comparison tables. Operating since 2024.
2. **Bizzy Boss (bizzyboss.co.nz)** — trades-focused: $147/mo intro + ~$90 usage + $250 setup; schema with offers; simple positioning for tradies.

**Where Quiktalk AI can outperform:** (a) "100% owned by you / zero vendor lock-in" angle (their best differentiator — push it with a contract sample); (b) deeper industry granularity (6 industries vs generic); (c) "built on your existing number with conditional call forwarding" (Talkify emphasises this less); (d) if the "live in 3 days" claim is real, publish a dated onboarding timeline; (e) NZ+AU dual-market focus.

**Where they're behind right now:** everything listed in §8/§11/§12 — pricing, schema, pages, proof, entity clarity, live demo.

---

## 21. BACKLINK & OFF-PAGE SEO

- ⚠️ **Not verifiable with available access** — no backlink index tool access.
- Observable: domain registered 2026-08-29; **zero social profiles, zero business directories found, zero press mentions** in web search; the only "QuickTalk AI" entity with visibility is an unrelated app (THREE PANDA DIGITAL).
- Recommended ethical programmes (12-month): (1) LinkedIn company page + founder posts (domain experts — NZ voice AI); (2) NZ SMB directories (NZBN register listing, industry association pages, local chamber); (3) guest content on trades/healthcare software blogs (Fergus, Tradify, ServiceM8, Cliniko ecosystems); (4) original "NZ missed calls" survey → PR to NZ Herald/RNZ tech desks + trade press; (5) partnerships with marketing agencies/receptionist services (referral links).

---

## 22. IMAGE & MEDIA OPTIMISATION

| Item | Finding |
|---|---|
| Logo file | 1024×1024 RGBA PNG, **196–605 KB** used as favicon + 4× inline brand mark at ≤38 px — 50–100× heavier than needed |
| Formats | PNG only; no WebP/AVIF, no `srcset`, no `sizes` |
| Dimensions in HTML | ❌ No `width`/`height` on most images (CLS risk) |
| Lazy loading | ❌ None (all images above/near fold, but 0 `loading="lazy"`) |
| Alt text | ✅ Present; generic wording |
| Videod/audio | ➖ None (simulator is text-only) — a missed opportunity: **no recorded demo call audio anywhere** |
| Filenames | `logo.png` — non-descriptive; prefer `quiktalk-ai-logo-64.png` etc. |

---

## 23. CODE & TECHNICAL QUALITY

- ✅ Valid, hand-crafted, readable code; CSS design tokens well organised; no framework bloat; zero console-worthy misuse detected statically (no undefined vars at parse; no deprecated APIs spotted; `scroll-behavior: smooth` OK).
- ❌ No `defer`/`async` on the 608 KB script; no error handling (`try/catch` count: **0**); no WebGL capability check.
- ❌ Inline event handlers (`onclick`, `oninput`, `onsubmit`, `onmouseover`) — harder to maintain, block strict CSP, and duplicate the (unused) programmatic listeners in the same script.
- ⚠️ Potential layout thrash: `document.body.scrollHeight` read every animation frame.
- ⚠️ No build pipeline, no asset hashing, no cache-busting, no code splitting, no source maps; `cache-control: max-age=0`.
- ⚠️ Hard-coded business data in JS (e.g., `avgJobValue = 500`) — should be config/data-attributes.
- ⚠️ No tests, no CI, no monitoring (no uptime/error tracking; no analytics even).
- ⚠️ HTML meta `http-equiv="Cache-Control/Pragma/Expires"` are largely ignored by modern browsers (harmless but ineffective — the real caching is header-driven).

---

## 24. BROKEN LINK & ERROR AUDIT

| URL | Status | Finding | Fix |
|---|---|---|---|
| `/privacy-policy`, `/terms-of-service` | 404 (as links they resolve to `#about`) | **Wrong destination** | Create real pages; update links |
| `/robots.txt`, `/sitemap.xml` | 404 | No files | Create both |
| `/favicon.ico`, `/apple-touch-icon.png` | 404 | Browsers request automatically | Add icons |
| `#about`, `#demo`, `#faq`, etc. | ✅ 200 (anchors) | All resolve | — |
| All other probed paths | 404 | Correct behaviour | Optional: branded 404 page |
| Redirect chain `http://root → https://root → https://www` | 301×2 | Extra hop | Single 301 to final host |
| Broken downloads/videos/forms | ➖ N/A | — | — |

**No 500 errors, no redirect loops, no broken images observed.**

---

## 25. DOMAIN & INFRASTRUCTURE

| Check | Result |
|---|---|
| Registrar | Hostinger; **created 2026-08-29** (11 days old), expires 2027-08-29 |
| Nameservers | `artemis.dns-parking.com` / `hermes.dns-parking.com` (Hostinger parking DNS) |
| www DNS | CNAME → `quicktalk-ai.onrender.com` → 216.24.57.x (Cloudflare proxied) |
| Root DNS | 216.24.57.1 (Hostinger parking IP behind Cloudflare redirect) |
| CDN | Cloudflare (HTTP/2 + H3, brotli, 5-min edge cache) |
| Origin | Render (not verifiable which tier; direct origin TTFB 0.19–0.25 s ✅; free-tier cold-start risk ⚠️) |
| Email DNS | MX → Hostinger (mx1/mx2); SPF `~all`; **DMARC p=none**; DKIM not found at common selectors ⚠️ |
| Subdomains | None found beyond www (no `blog.`, `app.`, `demo.` records; ⚠️ only common names checked — no exhaustive zone transfer attempted) |
| Exposed services | Only 443 (www + origin). No FTP/admin ports probed (not needed; no evidence of exposure) |

---

## 26. EMAIL & COMMUNICATION

- ⚠️ Contact email `admin@quiktalkai.com` (mailto in footer). Mailbox existence **not tested** (per rules — no messages sent). MX = Hostinger → the account plausibly works, but deliverability to NZ/AU inboxes depends on SPF/DKIM/DMARC — currently **DMARC p=none + no found DKIM** ⇒ gutter-level deliverability protection.
- ❌ No confirmation emails / automated emails (nothing fires — the form doesn't submit).
- ⚠️ No unsubscribe mechanism (none needed — no email exists yet; required the moment a newsletter is added).
- **Suggestion:** auth the domain (DKIM set by Hostinger), publish DMARC `p=quarantine` once alignment verified, use a transactional sender (Resend/Postmark) with a verification + double-opt-in flow.

---

## 27. E-COMMERCE — **N/A** (no shop, no payments; nothing to audit)

---

## 28. INTERNATIONALISATION — **N/A** (single language `en`; NZ/AU only; no currency/locale selectors). ⚠️ Note: calculator is NZD-only while claiming AU service coverage.

---

## 29. AI & FUTURE SEARCH READINESS

Readiness: **Low** (expected for launch week). Established best practices the site should adopt now: FAQ/Organization/LocalBusiness schema, consistent NAP + entity data, author/expert pages, original research with dates, machine-readable pricing (OfferCatalog), public, dated benchmarks. Experimental later: `llms.txt` (optional), AI-crawler `robots.txt` clauses, conversational-answer formatting. AI crawlers are currently **unblocked by absence of restrictions** (any `/` path returns the static content — including to GPTBot-style UAs by default).

---

## 30. BUSINESS RISK AUDIT

| Risk | Severity | Impact | Likelihood | Effort to fix | Rank |
|---|---|---|---|---|---|
| Lead form captures zero leads | **Critical** | 100% conversion failure | Certain (verified) | Low (1 day) | 1 |
| No privacy/ToS while collecting personal data | High | Legal + trust | Certain | Low | 2 |
| No analytics | High | Blind operation; no optimisation; no ads | Certain | Low | 3 |
| No pricing vs transparent competitors | High | Lost deals at decision stage | High | Low | 4 |
| Brand entity mismatch + collision | High | AI-search invisibility; confused audience | Certain | Low–Med | 5 |
| Unsupported "guaranteed ROI" claims | High | Legal/advertising-standards exposure; trust damage | Med | Low | 6 |
| No SEO foundation (11-day domain, no sitemap/schema/pages/links) | High | No organic growth for 6–12 months | Certain | Med–High | 7 |
| Missing security headers + DMARC p=none | Med | Phishing/spoofing, browser warnings | Med | Low | 8 |
| 608 KB sync JS + WebGL on mobile | Med | Slow low-end devices, battery drain | High | Med | 9 |
| HSTS not served at edge | Low–Med | Downgrade exposure | Med | Trivial | 10 |

---

## 31. MASTER ISSUE TABLE

> ID format: `QTK-###`. Evidence column cites what was directly observed. Everything in this table was verified during this audit; no speculative rows.

| ID | Category | URL | Issue | Evidence | Severity | Impact | Recommended Fix | Effort |
|---|---|---|---|---|---|---|---|---|
| QTK-001 | Functional CRO | `/#demo` | **Lead form never submits** — `handleFormSubmit()` only swaps button text; no fetch/XHR/FormData/endpoint exists in 86 KB of HTML/JS | Code inspection: function body = `e.preventDefault()`, text change, `btn.disabled = true`; 0 occurrences of `fetch(`/`XMLHttpRequest`/`FormData` in document; form has no `action` | **P0** | 100% of leads lost; site cannot convert | Wire form to backend: Cloudflare Pages Function `/api/lead` (or Web3Forms/Formspree/Tally + n8n webhook): validate server-side, store in CRM/Sheets/DB, send confirmation, redirect to thank-you state. See §34 QTK-001 code | ~0.5 day |
| QTK-002 | Privacy | Footer | Privacy Policy & Terms of Service links point to `#about`; no policy pages exist | `<a href="#about">Privacy Policy</a>` ×2 / `Terms of Service`; `/privacy-policy` and `/terms-of-service` → 404 | **P0** | Collects PII (name, business, phone, email, website) with no lawful disclosure; "Privacy Act Compliant" claim unsupported | Create /privacy-policy + /terms (plain-language, NZ/AU), link correctly; add marketing-consent checkbox | 1–2 days |
| QTK-003 | Analytics | All | No analytics/tracking of any kind | 0 references to gtag/GA/GTM/pixel/clarity/hotjar in whole document; only external script = three.min.js | **P1** | No traffic/conversion measurement; no retargeting; no ads | GA4 (or Plausible) + GTM; events: demo CTA click, form submit success, email click; consent banner when tracking starts | 1 day |
| QTK-004 | Brand/GEO | Entire site | Three brand spellings: "Quiktalk AI", "QuikTalk AI", "QuickTalk AI"; "QuickTalk AI" is also an unrelated iOS app (1,597 reviews) | Title/logo = Quiktalk; nav = Why QuikTalk AI; FAQ/footer = QuickTalk AI; web search: apps.apple.com QuickTalk AI (THREE PANDA DIGITAL) | **P1** | Entity confusion for humans, Google, AI engines | Pick one name (recommend "Quiktalk AI" matching domain), update all copy/logo alt text, register matching LinkedIn/X/IG handles, add sameAs | 0.5 day |
| QTK-005 | Technical SEO | `/` | No robots.txt, sitemap.xml, canonical, or structured data (0 JSON-LD) | All three paths → 404; `<head>` has only charset/viewport/description meta | **P1** | Crawl/indexation + rich-result + AI answer extraction all blocked | Add robots.txt (allow all, sitemap ref), sitemap.xml, canonical, and JSON-LD (see §34 QTK-005) | 0.5–1 day |
| QTK-006 | CRO/SEO | All | No pricing published; competitors publish full pricing | FAQ: "You'll get exact pricing on your demo call"; talkify.nz: $129–$199/mo published + OfferCatalog schema; bizzyboss.co.nz: $147/mo | **P1** | Deal-stage drop-outs; no comparison frame; no price schema | Launch transparent volume-based pricing + /pricing page with OfferCatalog + Service schema; keep "custom" tier for enterprise | 2–3 days |
| QTK-007 | E-E-A-T/Trust | `#about`, footer | No company details: no address, phone, legal entity, founders, or social links; contact = email only | Footer contact = `mailto:admin@quiktalkai.com` only; About = 1 paragraph; 0 external/social links in HTML | **P1** | Trust deficit for a call-recording service; no local SEO; no entity grounding | Add NZ business details (legal name, address, phone), LinkedIn/X/Instagram links, founder bios in About; add phone number site-wide | 1–2 days |
| QTK-008 | Content/Compliance | `#comparison` | Unsupported claims: "100% ROI guaranteed within 60 days", "answers 100 incoming calls simultaneously", "$42,000+/year salary" (currency/region unstated), calculator assumptions undisclosed ($500/job, 30% missed, 70% recaptured hard-coded in JS) | JS: `const avgJobValue = 500` / `* 0.3` / `* 0.7`; copy as quoted; NZ market salary data indicates NZ$55–65k p.a. | **P1** | Advertising-standards exposure; credibility gap; disclaimers absent | Rewrite claims to be verifiable and dated; disclose calculator assumptions inline; add sources/attribution | 1 day |
| QTK-009 | CRO | `#demo` | No social proof anywhere (no reviews, testimonials, case studies, logos, live demo number) | 0 testimonial/case-study elements in HTML; simulator is canned text | **P1** | Key purchase-stage objection unaddressed | Collect 3–5 early-customer video/text testimonials with schema (Review/AggregateRating), publish real recorded call demo, or public callable number | 1–2 weeks |
| QTK-010 | Accessibility | Forms/FAQ/nav | WCAG failures: no labels/autocomplete; div-based FAQ; no focus-visible styles (only `.input-field:focus`); no reduced-motion; no `<main>`; no skip link; no aria-expanded; burger 26×16 px | 1 `:focus` selector in 30 KB CSS; `0` `prefers-reduced-motion`; FAQ = `div.faq-q onclick`; `<main>` count 0 | **P1** | Exclusion of keyboard/SR users ≈ 1–2% of visitors; legal risk (NZ Human Rights Act context); quality signal | Labels+autocomplete; real `<button aria-expanded>` FAQ with CSS fallback; `:focus-visible` global; `prefers-reduced-motion` media query; `<main>` + skip link; 44 px targets | 1–2 days |
| QTK-011 | Security | www & origin | Missing reply headers: no HSTS at edge (origin has it!), no CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy; inline handlers block strict CSP | Header diff: origin sends `strict-transport-security: max-age=315360000; includeSubdomains; preload`; www response does not; www sends only `x-content-type-options: nosniff` | **P1** | Downgrade/clickjacking/MIME risks; phishing brand-surface | Cloudflare: HSTS max-age 6 months, XFO/`frame-ancestors 'self'`, Referrer-Policy strict-origin-when-cross-origin, Permissions-Policy minimal; migrate to external handlers + CSP `script-src 'self'` | 0.5–1 day |
| QTK-012 | Email security | DNS | DMARC `p=none`; no DKIM at common selectors; SPF `~all` | `_dmarc.quiktalkai.com` TXT = `v=DMARC1; p=none`; `default|google|selector1|k1|mail._domainkey` empty; SPF = `v=spf1 include:_spf.mail.hostinger.com ~all` | **P1** | Brand spoofing/phishing; poor deliverability for admin@ | DMARC p=quarantine → p=reject after alignment verified; DKIM via Hostinger/transactional sender; monitor | 0.5 day |
| QTK-013 | Performance | `/` | 608 KB raw (157 KB br) **synchronous** three.js full bundle + continuous full-viewport WebGL loop with no visibility/scroll pause; no capability check | `content-length` 608,081; `<script src="assets/three.min.js">` no defer/async; `requestAnimationFrame` loop; `IntersectionObserver: 0`, `visibilitychange: 0`, `try/catch: 0` | **P2** | Slow low-end devices; battery drain; INP risk; no fallback | Lazy-load on idle/IntersectionObserver; defer; detect WebGL + `document.hidden` pause; static hero fallback | 1–2 days |
| QTK-014 | Performance | `assets/logo.png` | 1024×1024 RGBA PNG (196–605 KB) used as favicon and brand mark at 38 px; no WebP/AVIF, srcset, or dimensions; no lazy loading | PIL: 1024×1024 RGBA; content-length up to 604,972; `<link rel="icon" href="assets/logo.png">`; 4 `<img>` refs | **P2** | Hundreds of KB wasted; CLS risk; slow tab icon | Export 32×32 favicon.ico/png + 128 apple-touch-icon + ≤2× WebP/AVIF logo variants w/ srcset + width/height + lazy load below fold | 0.5 day |
| QTK-015 | Performance | `/` | `cache-control: public, max-age=0, s-maxage=300` on HTML+assets — browser revalidation every visit; no immutable hashed assets | Headers on `/`, three.min.js, logo.png | **P2** | Repeat-visit latency; 304 churn | `max-age=604800, immutable` for hashed assets (`assets/app-v1.2...`), 300 s for HTML | 0.5 day |
| QTK-016 | SEO/AEO | `#faq` | FAQ content exists but has no FAQPage schema; no HowTo schema on 4-step process; no Organization/LocalBusiness/Service schema; no OG/Twitter meta | 0 JSON-LD; head meta = charset/viewport/description only | **P1** | No rich results; no AI-answer extraction; dead social shares | Add JSON-LD graph: Organization + LocalBusiness (Auckland) + Service + FAQPage + HowTo (optional); OG/Twitter tags + 1200×630 image | 1 day |
| QTK-017 | CRO | `#hero` | "GET MY DEMO AGENT" + "SEE LIVE SIMULATION" both scroll to sections, but the demo is text-only canned scripts; hero has no phone number or "hear it now" audio | `simDialogs` = 3 hard-coded strings; no `<audio>`; no tel: links | **P2** | Mismatch of promise (hear your agent) vs experience | Add playable TTS/audio snippet or real callable NZ demo number + `tel:` CTA | 1–2 days |
| QTK-018 | UX | `/` | Fake preloader (random `setInterval` progress) with no `<noscript>` — permanent black screen if JS fails; blocks ~1 s | `progress += Math.floor(Math.random()*15)+8`; `noscript` count = 0 | **P2** | Perceived slowness; total content loss without JS | Replace with load-event fade or remove; add `<noscript>` style to hide `#pre` | 0.5 day |
| QTK-019 | SEO/IA | Footer | Services ("AI Voice Agents", "AI Systems & Automations", "AI Consulting & Roadmaps", "Web & Software Development") all link to `#demo`; no dedicated pages/URLs for 4 of 5 services | Footer anchors verified | **P2** | No crawlable service-level content; zero long-tail coverage | Create service pages (with Service schema) + internal links | 1 week+ |
| QTK-020 | Content | `#about` | About section = 1 paragraph + 3 guarantees; no team, founders, credentials, or company history | Section text extracted | **P2** | Weak E-E-A-T for expert-led product | Expand: founders, why-Auckland, process, security posture, onboarding stories | 1 week |
| QTK-021 | Infrastructure | Redirects | 2-hop redirect chain `http://quiktalkai.com → https://quiktalkai.com → https://www.quiktalkai.com` | Header capture (301+301) | **P3** | Minor crawl/entry latency; lost link equity fraction | Single 301 to `https://www.quiktalkai.com/` for both http and root | 0.5 day |
| QTK-022 | SEO | `/` | No `apple-touch-icon`/`theme-color`; `/favicon.ico` 404 (browser requests it) | Probes: 404s | **P3** | Poor mobile bookmark/branding | Add icons + theme-color `#060608` | 0.5 hr |
| QTK-023 | Quality | Typesetting | 10–11 px uppercase letter-spaced button text; 11 px microcopy at 4.1:1 contrast; no `maxlength` on fields; no `autocomplete`/`inputmode` | CSS `.btn-main` font-size 11px etc.; color `--muted #71717a` on `#060608` ≈ 4.1:1 | **P2** | Legibility + autofill friction + form errors | Raise to ≥13–14 px; lighten muted colour; add autocomplete (name/email/tel/url/organization) + maxlength + inputmode | 0.5 day |
| QTK-024 | Growth | Sitewide | 0 outbound links, 0 citations, no LinkedIn/X/Instagram/GBP — no discovery surface for the brand | External hrefs in document: `mailto:` only | **P2** | No source/reference ecosystem; no press/PR pickup | Add citations to tools (Fergus/Tradify docs), industry bodies, and all social profiles; build GBP | Ongoing |
| QTK-025 | Reliability | Origin | Hosting stack is Render (free-tier cold-start risk ⚠️ unverified tier) + Hostinger parking DNS; no uptime monitoring | CNAME www → quicktalk-ai.onrender.com; NS = dns-parking.com; no monitoring found | **P3** | Potential intermittent availability; no alerting | Verify Render tier; add uptime monitoring (UptimeRobot) + status page; consider moving DNS to Cloudflare | 0.5 day |

---

## 32. QUICK-WIN ACTION PLAN

### Fix immediately (this week — P0/P1)
1. **QTK-001** — Wire the lead form to a real endpoint. (0.5 day) *Everything else is downstream of this.*
2. **QTK-002** — Publish real Privacy Policy + Terms pages; fix footer links; add consent checkbox. (1–2 days)
3. **QTK-003** — Install analytics (GA4/Plausible + event tracking) *after* consent mechanics. (1 day)
4. **QTK-004/005** — Standardise brand spelling; add robots.txt + sitemap + canonical + core JSON-LD. (1 day)
5. **QTK-011/012** — Cloudflare security headers (incl. HSTS switch-on) + DMARC quarantine + DKIM. (0.5 day)

### Fix this week (high-value technical + marketing)
6. **QTK-013/014/015** — Asset pipeline: defer/lazy three.js, WebP/AVIF + srcset logo, real favicon, far-future cache. (1–2 days)
7. **QTK-006** — Publish pricing page (even launch pricing) with OfferCatalog schema. (2–3 days)
8. **QTK-016** — OG/Twitter meta + share image; FAQPage + Organization + LocalBusiness schema. (1 day)
9. **QTK-017** — Ship a real, audible demo (TTS clip or callable NZ number). (1–2 days)
10. **QTK-008** — Rewrite unsupported claims; disclose calculator assumptions. (1 day)

### Fix this month (medium-term)
11. **QTK-010** — Accessibility pass (labels, focus-visible, FAQ semantics, reduced-motion, targets, landmarks). (1–2 days)
12. **QTK-007/024** — Company details, phone number, social profiles, GBP listing, NZ directories. (1 week)
13. **QTK-009** — First testimonials + case study page + Review schema. (2 weeks)
14. **QTK-019/020** — Service pages (4) + expanded About. (1–2 weeks)
15. **QTK-025** — Uptime monitoring; DNS hygiene. (0.5 day)

### Long-term (strategic)
16. Content engine: "missed calls in NZ" research, industry landing pages (trades/dental/legal), comparison page vs human receptionists.
17. Authority building: PR, partnerships, guest content, original benchmarks (public, dated).
18. Product-led growth: real-time demo booking from the site, self-serve pricing calculator, integration directory pages (Fergus/Tradify/Cliniko).
19. GEO programme: entity consolidation, sameAs network, citation monitoring, llms.txt (experimental).

---

## 33. DEVELOPER ACTION PLAN

### QTK-001 — Working lead form (P0, difficulty: easy)
**Problem:** form never submits. **Location:** inline JS `handleFormSubmit(e)`, `#leadForm`.
**Root cause:** handler only animates the button.
**Recommended implementation** (Cloudflare Pages Function — keep stack as-is):
```js
// replace handleFormSubmit with:
async function handleFormSubmit(e) {
  e.preventDefault();
  const form = e.target, btn = document.getElementById('submitBtn');
  const payload = Object.fromEntries(new FormData(form).entries());
  payload._page = location.href;
  btn.disabled = true; btn.innerText = 'SUBMITTING...';
  try {
    const r = await fetch('/api/lead', { method: 'POST',
      headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (!r.ok) throw new Error();
    btn.innerText = '✓ DEMO REQUEST RECEIVED';
    btn.style.background = '#34d399';
    window.dispatchEvent(new Event('lead:success')); // analytics hook
    form.reset();
  } catch (err) {
    btn.disabled = false; btn.innerText = 'SOMETHING WENT WRONG — TRY AGAIN';
  }
}
```
Plus: add `name`, `autocomplete` (`name`, `organization`, `tel`, `email`, `url`), `maxlength`, `inputmode`; server-side validation + rate limiting (or use Web3Forms/Formspree with honeypot + Turnstile); store to CRM/Sheets + **send a confirmation email** (`admin@` + prospect). **Expected result:** every submission captured + measurable.

### QTK-013/014/015 — Performance (P2, medium)
- `import * as THREE` via import map + `defer`, or load `three.min.js` only after `requestIdleCallback`/`IntersectionObserver` on hero; `powerPreference: 'high-performance'`.
- Pause loop: `document.addEventListener('visibilitychange', ...)` + stop rAF when hero off-screen.
- Wrap renderer creation in `try/catch` with a static gradient fallback.
- Logo: export `logo-64.png`, `logo-192.webp`, `logo-384.avif`, `logo-32.ico`; `srcset` + `width/height`; `loading="lazy"` below fold; `rel="icon"` → `/favicon-32.png`.
- Cache: rename assets to `assets/app-<hash>` + `Cache-Control: public, max-age=604800, immutable`; HTML stays 300 s.
- Replace meta `http-equiv` cache tags with real header config (they're ignored by modern browsers).

### QTK-011 — Headers (P1, easy)
Cloudflare → SSL/TLS → Edge Certificates: enable **HSTS** (max-age 15552000; includeSubdomains), and add Transform Rules / headers:
```
Strict-Transport-Security: max-age=15552000; includeSubdomains
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy: default-src 'self'; style-src 'unsafe-inline'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'
```
(Requires moving inline handlers to listeners — see also §23.) **Expected result:** A+ header posture, clickjacking/downgrade protection.

### QTK-005/016 — Schema (P1, easy)
```json
{
  "@context": "https://schema.org", "@graph": [
  {"@type":"Organization","name":"Quiktalk AI","url":"https://www.quiktalkai.com/",
   "logo":"https://www.quiktalkai.com/assets/logo-192.webp","email":"admin@quiktalkai.com",
   "address":{"@type":"PostalAddress","addressLocality":"Auckland","addressCountry":"NZ"},
   "areaServed":[{"@type":"Country","name":"New Zealand"},{"@type":"Country","name":"Australia"}],
   "sameAs":["https://www.linkedin.com/company/...","https://x.com/..."]},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What does Quiktalk AI do?",
   "acceptedAnswer":{"@type":"Answer","text":"..."}}]},
  {"@type":"Service","name":"24/7 AI Voice Agent","provider":{"@id":"..."},
   "areaServed":["New Zealand","Australia"],"offers":{"@type":"Offer","price":"XXX","priceCurrency":"NZD"}}
]}
```
Plus `<link rel="canonical">`, OG/Twitter meta, `og:image` (1200×630), `theme-color #060608`, per-section `aria-labelledby`.

### QTK-010 — Accessibility (P1, medium)
Labels for all inputs (screen-reader-only class), `aria-expanded` + `aria-controls` on FAQ buttons (use `<button>`), global `:focus-visible { outline: 2px solid #e5c158; outline-offset: 3px }`, `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; scroll-behavior: auto } #gl { display:none } }`, `<main id="main">` + skip link, `aria-live="polite"` on submit status, 44 px targets for burger.

### QTK-021 — Redirect consolidation
Cloudflare Redirect Rule: `http://quiktalkai.com/*` and `https://quiktalkai.com/*` → single 301 to `https://www.quiktalkai.com/$1`.

---

## 34. SEO ACTION PLAN (prioritised)

| Priority | Action | Why |
|---|---|---|
| 1 | robots.txt + sitemap.xml + canonical | Foundation; currently absent |
| 2 | JSON-LD (Organization, LocalBusiness, Service, FAQPage, Breadcrumb) | Rich results + AEO/GEO extraction |
| 3 | Keyword-targeted title/H1/meta set | Retitle with "AI Receptionist NZ / AU" commercial terms |
| 4 | Page architecture: `/ai-voice-agents`, `/pricing`, `/industries/{6}`, `/case-studies`, `/blog/` | Compete for competitor-owned queries |
| 5 | Pricing page + OfferCatalog | Price-inclusive SERP answers (competitive necessity) |
| 6 | Local SEO: GBP, NAP footer, LocalBusiness schema, Auckland/NZ page | Zero local presence today |
| 7 | Internal linking + related-links modules | Only 1 page now; build graph as pages appear |
| 8 | Backlinks (ethical): LinkedIn, NZ directories, industry blogs, PR on original research | Domain 11 days old; zero authority |
| 9 | AEO content: definition blocks, "cost in NZ" answer, FAQ expansion (20+ Qs), HowTo schema | Answer-engine extraction |
| 10 | GEO: one brand name, sameAs network, entity pages, dated first-party data | Cite-ability for LLMs |

---

## 35. MARKETING ACTION PLAN

| Priority | Action |
|---|---|
| 1 | Fix form → measure → iterate: events for CTA clicks, submits, email clicks |
| 2 | Publish pricing; add "compare vs human receptionist" interactive table (quoted NZ salaries) |
| 3 | Live demo first: callable NZ number or audio clip in hero — become "the one you can actually hear" |
| 4 | Social proof programme: 3–5 video testimonials; GBP reviews; LinkedIn company page + founders; case-study PDFs |
| 5 | Lead nurture: welcome email + demo booking link (Calendly/Cal.com) + WhatsApp follow-up for AU/NZ SMBs |
| 6 | Content engine: 1 authoritative pillar ("AI receptionists for NZ trades") + industry pages + monthly benchmarks |
| 7 | Retargeting (Meta/LinkedIn) once consent banner + pixels live |
| 8 | Partnerships: receptionist agencies, trades-supply channels, practice-management software resellers |
| 9 | PR: "NZ missed-call study" with public methodology → trade + mainstream press (including RNZ/NZH tech desks) |

---

## 36. 30-DAY PRIORITY ROADMAP

**Week 1 (survival):** QTK-001 form backend + thank-you state · QTK-002 privacy/terms pages + consent checkbox · QTK-003 analytics + events.
**Week 2 (foundations):** QTK-004 brand unification + socials · QTK-005 robots/sitemap/canonical · QTK-016 schema + OG/Twitter · QTK-011 headers/HSTS · QTK-012 email auth · QTK-021 redirect consolidation.
**Week 3 (conversion):** QTK-006 pricing page · QTK-017 real demo audio/number · QTK-007 NAP + phone + company details · QTK-008 claim rewrites + calculator disclaimers.
**Week 4 (quality + reach):** QTK-013/014/015 performance · QTK-010 accessibility pass · QTK-009 first testimonials + GBP · 4 service pages draft.

## 37. 90-DAY GROWTH ROADMAP

**Month 2:** ship service pages + /industries (6) + blog (2–3 posts); publish "NZ missed-call benchmark" research; LinkedIn content cadence; directory/citation sprint (NZBN, chambers, trade lists); GA4 conversion milestones defined.
**Month 3:** case studies + Review schema; industry-specific landing pages with FAQ schema; partner/referral pilot; first PR push; AEO audit of top 10 questions per industry; GEO checkpoint: entity consistency, sameAs verified, citations measured; uptime + error monitoring + error tracking live; performance re-baseline (target: <150 KB critical, INP <200 ms mid-tier mobile).

---

## 38. FINAL VERDICT

## Overall Website Grade: **C−** (49/100)

1. **Is the website technically healthy?** Mostly — fast edge delivery, clean static build, valid TLS, no errors; but the **one thing that matters (the form) is broken**, and caching/asset weight need work.
2. **Is it SEO-ready?** **No.** No sitemap, robots.txt, schema, or subpages; 11-day-old domain with no authority; brand name inconsistent. Long road ahead (realistic 6–12 months to meaningful organic traction).
3. **Is it AEO-ready?** Partially — excellent FAQ content exists, but zero schema means answer engines can't extract it reliably. Fixing schema is a week-one win.
4. **Is it GEO-ready?** **No.** Entity signals absent, brand naming inconsistent, name collision with an existing app, no citations, no sameAs, no data. Realistically 6+ months of entity building.
5. **Is it conversion-ready?** **Absolutely not** — the only conversion element cannot convert. This is the site's most urgent defect and also its best opportunity: fixing it in a day restores 100% of the funnel.
6. **Is it mobile-ready?** Reasonably — responsive layout is competent — but the always-running WebGL canvas and tiny button text hurt mid/low-end devices.
7. **Is it accessible?** **No** — multiple WCAG AA failures (focus visibility, form labels, FAQ semantics, contrast, reduced motion).
8. **Is it secure based on the tests performed?** **Adequate on the outside, thin on hardening.** No confirmed vulnerability (small static surface), but missing security headers, HSTS absent at the edge, DMARC `p=none`, no found DKIM, and an exposed origin hostname. Recommend a manual pen test once the form backend ships.
9. **What are the 5 most important things to fix?** ① The broken lead form. ② Privacy/Terms + consent. ③ Working demo + pricing (conversion blockers). ④ Schema + sitemap/robots + brand consistency (SEO/AEO/GEO foundation). ⑤ Analytics + security headers/HSTS/DMARC.
10. **What could generate the biggest business improvement?** **Becoming the NZ AI-receptionist you can actually hear and price.** Five competitors publish prices; none of the traction-earning assets (proof, schema, pages, data) exist yet. Fix the form (day 1), ship pricing + a live callable demo (week 2), and publish one piece of original NZ call-answer research (month 2) — this combination, executed consistently, converts the same traffic that currently converts to **zero**, and gives answer engines something real to cite.

---

*Report prepared 9 Sep 2026. Evidence: direct HTTP and source-code inspection of quiktalkai.com, DNS/TLS/WHOIS lookups, and public web research. All performance figures are observed transfer sizes; all Core Web Vitals are estimates, not measurements. Indexation, rankings, traffic, backlink counts, and email deliverability are not verifiable with available access and are stated as such. No destructive or intrusive tests were performed.*
