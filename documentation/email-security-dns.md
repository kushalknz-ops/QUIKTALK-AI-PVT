# Quiktalk AI — Email Security & DNS Authentication Specification (QTK-012)

**Document Status:** Stage 2 DNS Staging Specification (Gated)  
**Domain:** `quiktalkai.com`  
**Primary Contact:** `admin@quiktalkai.com`

---

## 1. Current Audit State vs. Target Architecture

| Mechanism | Current State Observed in Audit | Target State (Staging / Prod) | Action Required |
|---|---|---|---|
| **SPF** | `v=spf1 include:_spf.mail.hostinger.com ~all` (Softfail) | `v=spf1 include:_spf.mail.hostinger.com include:<transactional-relay> -all` (Hardfail) | Update record to hardfail `-all` once all legitimate mail sources (Hostinger + transactional API) are added. |
| **DKIM** | No DKIM found at default selectors (`google`, `k1`, `selector1`, `default`) | 2048-bit RSA key published at designated selector (e.g. `hostinger._domainkey` / `resend._domainkey`) | Enable DKIM signing in Hostinger mail control panel & any transactional email service. |
| **DMARC** | `v=DMARC1; p=none` (Monitoring only; 0 enforcement against spoofing) | Phase 1: `p=quarantine; pct=100; rua=mailto:dmarc-reports@quiktalkai.com`<br>Phase 2: `p=reject; pct=100` | Implement staged rollout below to prevent domain impersonation. |

---

## 2. Staged DMARC Rollout Procedure

To prevent delivery interruption while securing `admin@quiktalkai.com` from spoofing:

### Stage A: Monitoring & Alignment Verification (Days 1–14)
Verify that Hostinger mailbox outgoing mail passes SPF and DKIM alignment:
```dns
_dmarc.quiktalkai.com. IN TXT "v=DMARC1; p=none; sp=none; rua=mailto:dmarc-reports@quiktalkai.com; adkim=r; aspf=r;"
```

### Stage B: Quarantine Enforcement (Days 15–30)
Instruct receiving mailservers (Google Workspace, Microsoft 365, iCloud) to quarantine unaligned spoofed messages:
```dns
_dmarc.quiktalkai.com. IN TXT "v=DMARC1; p=quarantine; sp=quarantine; pct=100; rua=mailto:dmarc-reports@quiktalkai.com; ruf=mailto:dmarc-forensics@quiktalkai.com; adkim=r; aspf=r;"
```

### Stage C: Full Reject Enforcement (Day 31+)
Fully lock down the domain against any unauthorized sender:
```dns
_dmarc.quiktalkai.com. IN TXT "v=DMARC1; p=reject; sp=reject; pct=100; rua=mailto:dmarc-reports@quiktalkai.com; adkim=s; aspf=s;"
```

---

## 3. MX & Inbound Mail Routing

Confirm Hostinger MX records remain priority-ordered:
```dns
quiktalkai.com. IN MX 10 mx1.hostinger.com.
quiktalkai.com. IN MX 20 mx2.hostinger.com.
```

---

## 4. Verification Checklist Before Stage 2 Gate

- [ ] Send test email from `admin@quiktalkai.com` to `https://www.mail-tester.com/`.
- [ ] Verify score 10/10 with valid DKIM signature.
- [ ] Confirm DMARC alignment passes in Google and Outlook headers (`Authentication-Results: dmarc=pass`).
