# Quiktalk AI — Origin Lockdown & Uptime Monitoring Guide
# QTK-025, Stage 2

This document specifies how to enforce origin lockdown and configure synthetic monitoring to protect SEO integrity and detect downtime proactively.

---

## 1. Origin Lockdown (Cloudflare Pages Architecture)

By selecting **Option A (Cloudflare Pages)**:

1. **Decommission Old Render Origin**:
   - Once DNS points to Cloudflare Pages (`www.quiktalkai.com`), log into Render dashboard.
   - Suspend or delete the old `quicktalk-ai.onrender.com` web service.
   - If keeping Render temporarily during cutover:
     - Inject an environment variable or header rule returning `X-Robots-Tag: noindex, nofollow` on all responses from the `*.onrender.com` hostname.
     - Add 301 redirection from any request to `https://www.quiktalkai.com$request_uri`.

2. **Access Protection on Staging Host (`<project>.pages.dev` / `staging.quiktalkai.com`)**:
   - In Cloudflare Zero Trust / Access:
     - Create an Access Application for `staging.quiktalkai.com` and `*.pages.dev`.
     - Require team PIN / email authentication so public search crawlers and external visitors cannot access or index staging.
   - Verify that staging emits `X-Robots-Tag: noindex, nofollow` on all routes.

---

## 2. Dry-Run Synthetic Uptime Monitoring

Uptime monitoring must be configured using tools such as **BetterStack**, **UptimeRobot**, or **Checkly**.

### Monitor 1: Public Root Availability
- **URL**: `https://www.quiktalkai.com/`
- **Method**: `GET`
- **Interval**: `60 seconds`
- **Expected Status**: `200 OK`
- **Keyword Assertion**: `Quiktalk AI`

### Monitor 2: Health Check API Endpoint
- **URL**: `https://www.quiktalkai.com/api/health`
- **Method**: `GET`
- **Interval**: `60 seconds`
- **Expected Status**: `200 OK`
- **JSON Assertion**: `"status": "ok"`

### Monitor 3: Synthetic Lead API Monitor (DRY-RUN ONLY)
> [!IMPORTANT]
> **CRITICAL RULE**: NEVER synthetic-POST the live `/api/lead` endpoint without `dryRun=1`.
> Hitting the live endpoint without `dryRun` triggers false-positive webhook deliveries to sales CRM and notification channels.

- **URL**: `https://www.quiktalkai.com/api/lead?dryRun=1`
- **Method**: `POST`
- **Interval**: `5 minutes`
- **Headers**:
  ```http
  Content-Type: application/json
  X-Dry-Run: 1
  User-Agent: SyntheticMonitor-UptimeBot/1.0
  ```
- **Request Body**:
  ```json
  {
    "name": "Synthetic Uptime Probe",
    "businessName": "Quiktalk System Monitor",
    "phone": "+64210000000",
    "email": "monitor@quiktalkai.com",
    "message": "Automated synthetic availability ping. Do not process as real lead.",
    "marketingConsent": false
  }
  ```
- **Expected Status**: `200 OK`
- **JSON Response Assertion**: `"dryRun": true` and `"success": true`
- **Action on Failure**: Alert immediately via SMS / PagerDuty / Slack.
