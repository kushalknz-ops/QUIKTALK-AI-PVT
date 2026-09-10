# Quiktalk AI Placeholder Quarantine Registry

This registry tracks all unverified business claims, pricing models, company credentials, audio files, and legal policies.

> [!WARNING]
> **Quarantine Rule**: No placeholder listed below may be removed, published to production, or used in live search indexing / JSON-LD schema without explicit owner sign-off and verification through the **Stage 2 Prod-Promotion Gate**.

| ID | Page / File | Current Draft Value | Real Value Needed | Owner | Status | Gate Requirement |
|---|---|---|---|---|---|---|
| **PH-01** | `pricing.html` | Starter $149/mo (100 min), Growth $299/mo (300 min), Custom Enterprise | Final commercial pricing tiers, minute allocations, setup fees & overage rates | Founders / Sales | **QUARANTINED (DRAFT)** | Must confirm real pricing tiers; `ENABLE_SCHEMA_PRICING=false` |
| **PH-02** | `index.html`, `case-studies.html` | Example benchmark metrics: 32% call recapture, <1s response, 40+ hrs saved/mo | Verified client deployment metrics or clearly labelled benchmark estimates | Operations | **QUARANTINED (ESTIMATE)** | Disclose benchmark methodology inline; no fake client quotes |
| **PH-03** | `case-studies.html` | Architectural case workflows: Auckland Roofing, North Shore Dental, West Auckland Automotive | Real case study client profiles or anonymized workflow studies | Founders / Client Success | **QUARANTINED (DRAFT)** | Real client sign-off or anonymized industry workflows |
| **PH-04** | `about.html`, `footer` | Auckland Central, New Zealand; Phone: +64 (placeholder); NZBN: Pending | Registered NZ entity legal name, physical NZ office address, direct business phone, NZBN | Legal / Ops | **QUARANTINED (DRAFT)** | Verified NZ Companies Office registration & phone line |
| **PH-05** | `index.html` (audio player) | Audio player UI stub showing "Sample slot — real recording pending (PH-05)" | Production MP3/WAV recordings of real AI voice agent calls (emergency trades & healthcare) | Voice AI Team | **QUARANTINED (STUB)** | High-fidelity call recordings without synthetic/fake caller deception |
| **PH-06** | `privacy-policy.html`, `terms.html` | Comprehensive Privacy Act 2020 (NZ) & Privacy Act 1988 (AU) compliant draft policies | Formal legal review & sign-off by qualified NZ/AU commercial legal counsel | Legal Counsel | **QUARANTINED (DRAFT)** | Written approval by legal counsel |
| **PH-07** | `.env`, `lib/leadHandler.js` | Empty / mock webhook dispatch (`LEAD_WEBHOOK_URL`, `ADMIN_EMAIL`) | Production CRM endpoint (HubSpot/GoHighLevel/n8n) & transactional email provider | DevOps / Engineering | **QUARANTINED (LOCAL)** | Stored exclusively in deployment environment variables |

---

## Quarantine Enforcement Mechanics

1. **Visual Draft Banner**: Every page rendering draft content (`pricing.html`, `privacy-policy.html`, `terms.html`, `about.html`, `case-studies.html`, `ai-voice-agents.html`) displays a prominent top bar:
   ```html
   <div class="draft-quarantine-banner">DRAFT — Local Validation Only. Pending Verification (PH-XX).</div>
   ```
2. **Search Indexing Kill-Switch**: All local and staging responses emit `X-Robots-Tag: noindex, nofollow` via `_headers` and `<meta name="robots" content="noindex, nofollow">` in `<head>`.
3. **Structured Data Kill-Switch**: `OfferCatalog`, `Review`, `AggregateRating`, and `LocalBusiness` address JSON-LD are strictly omitted until the linked PH item is marked `CLOSED`.
