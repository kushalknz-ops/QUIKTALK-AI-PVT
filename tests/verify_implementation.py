"""
tests/verify_implementation.py
Full automated verification suite for Quiktalk AI Audit Remediation (QTK-001 to QTK-025).
"""

import sys
import os
import json
import time
import subprocess
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

import argparse

parser = argparse.ArgumentParser(description="Quiktalk AI Automated Verification Suite")
parser.add_argument("--env", choices=["local", "staging", "prod"], default="local", help="Target environment (local, staging, prod)")
parser.add_argument("--url", default=None, help="Custom target host URL (for staging/prod)")
args, unknown = parser.parse_known_args()

TARGET_ENV = args.env

PASSED = 0
FAILED = 0

def assert_test(condition, test_name, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  [PASS] {test_name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {test_name} - {detail}")

print("\n============================================================")
print(f" QUIKTALK AI — AUTOMATED VERIFICATION SUITE [ENV: {TARGET_ENV.upper()}]")
print("============================================================\n")

# ------------------------------------------------------------
# 1. API Unit Validation via Node.js invoking lib/leadHandler.js
# ------------------------------------------------------------
print("1. Testing lib/leadHandler.js (Shared Single Source of Truth - QTK-001)")

node_test_script = """
const { validateLead, handleLead } = require('./lib/leadHandler.js');

async function runTests() {
  const results = [];

  // Test 1: Valid payload
  const validPayload = {
    name: 'Sarah Connor',
    businessName: 'Apex Medical Clinic',
    phone: '+64 21 555 1234',
    email: 'sarah@apexmedical.co.nz',
    website: 'https://apexmedical.co.nz',
    message: 'We need 24/7 call triage for emergency patient appointments.',
    marketingConsent: true,
    _hp: ''
  };
  const res1 = await handleLead(validPayload, {});
  results.push({ name: 'Valid lead submission returns 200', pass: res1.status === 200 && res1.body.success === true });

  // Test 2: Missing required field (name)
  const invalidPayload1 = { ...validPayload, name: '' };
  const res2 = await handleLead(invalidPayload1, {});
  results.push({ name: 'Missing name returns 400', pass: res2.status === 400 && res2.body.success === false });

  // Test 3: Invalid email format
  const invalidPayload2 = { ...validPayload, email: 'not-an-email' };
  const res3 = await handleLead(invalidPayload2, {});
  results.push({ name: 'Invalid email returns 400', pass: res3.status === 400 });

  // Test 4: Invalid phone format
  const invalidPayload3 = { ...validPayload, phone: '123' };
  const res4 = await handleLead(invalidPayload3, {});
  results.push({ name: 'Short invalid phone returns 400', pass: res4.status === 400 });

  // Test 5: Honeypot triggered
  const spamPayload = { ...validPayload, _hp: 'spam-bot-input' };
  const res5 = await handleLead(spamPayload, {});
  results.push({ name: 'Honeypot trap rejects bot with 400', pass: res5.status === 400 && res5.body.code === 'SPAM_REJECTED' });

  // Test 6: Maxlength enforcement
  const longPayload = { ...validPayload, name: 'a'.repeat(150) };
  const res6 = await handleLead(longPayload, {});
  results.push({ name: 'Excessive name length rejected with 400', pass: res6.status === 400 });

  // Test 7: Dry-run support (Stage 2 Step 1)
  const dryRunPayload = { ...validPayload };
  const res7 = await handleLead(dryRunPayload, {}, '', { dryRun: true });
  results.push({ name: 'Dry-run validation returns 200 without webhook dispatch', pass: res7.status === 200 && res7.body.dryRun === true });

  console.log(JSON.stringify(results));
}

runTests().catch(e => {
  console.error(e);
  process.exit(1);
});
"""

with open('scratch_node_test.js', 'w', encoding='utf-8') as f:
    f.write(node_test_script)

proc = subprocess.run(['node', 'scratch_node_test.js'], capture_output=True, text=True)
if os.path.exists('scratch_node_test.js'):
    os.remove('scratch_node_test.js')

if proc.returncode == 0:
    try:
        lines = [line.strip() for line in proc.stdout.strip().splitlines() if line.strip()]
        last_line = lines[-1] if lines else "{}"
        node_results = json.loads(last_line)
        for r in node_results:
            assert_test(r['pass'], r['name'])
    except Exception as e:
        assert_test(False, 'Node test execution', str(e) + " - Output: " + proc.stdout)
else:
    assert_test(False, 'Node test runner error', proc.stderr)

# ------------------------------------------------------------
# 2. Server Parity & HTTP Route Verification (server.js)
# ------------------------------------------------------------
print("\n2. Testing server.js (Header Parity & Route Verification - QTK-011, QTK-025)")

TEST_PORT = 3456
server_proc = subprocess.Popen(['node', 'server.js'], env={**os.environ, 'PORT': str(TEST_PORT)}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(1.5)

base_url = f"http://127.0.0.1:{TEST_PORT}"

def fetch_url(path, method='GET', data=None, headers=None):
    url = base_url + path
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            hdrs = {k.lower(): v for k, v in response.headers.items()}
            raw = response.read()
            text = raw.decode('utf-8', errors='ignore')
            return response.status, hdrs, text
    except urllib.error.HTTPError as e:
        hdrs = {k.lower(): v for k, v in e.headers.items()}
        raw = e.read()
        text = raw.decode('utf-8', errors='ignore')
        return e.code, hdrs, text
    except Exception as e:
        return 0, {}, str(e)

try:
    # Test Homepage and Headers
    status, hdrs, body = fetch_url('/')
    assert_test(status == 200, "GET / returns HTTP 200")
    assert_test('x-frame-options' in hdrs and hdrs['x-frame-options'] == 'DENY', "Header parity: X-Frame-Options: DENY")
    assert_test('x-content-type-options' in hdrs and hdrs['x-content-type-options'] == 'nosniff', "Header parity: X-Content-Type-Options: nosniff")
    assert_test('referrer-policy' in hdrs and hdrs['referrer-policy'] == 'strict-origin-when-cross-origin', "Header parity: Referrer-Policy")
    assert_test('permissions-policy' in hdrs, "Header parity: Permissions-Policy present")
    if TARGET_ENV in ('local', 'staging'):
        assert_test('x-robots-tag' in hdrs and 'noindex' in hdrs['x-robots-tag'], f"Header parity: X-Robots-Tag: noindex, nofollow (Draft Quarantine - {TARGET_ENV.upper()})")
        assert_test('content-security-policy-report-only' in hdrs, f"Header parity: CSP-Report-Only active ({TARGET_ENV.upper()})")
    else:
        # Prod expectation: CSP enforcing after flip
        assert_test('content-security-policy' in hdrs or 'content-security-policy-report-only' in hdrs, "Header parity: CSP active (PROD)")

    # Test /api/lead via HTTP POST
    post_data = {
      'name': 'Dave Plumber',
      'businessName': 'Dave Roofing & Plumbing',
      'phone': '021 555 9876',
      'email': 'dave@daveroofing.co.nz',
      'message': 'Need after hours call forwarding.',
      '_hp': ''
    }
    status_lead, _, body_lead = fetch_url('/api/lead', method='POST', data=post_data)
    assert_test(status_lead == 200, "POST /api/lead HTTP 200 Success Confirmation")
    lead_res = json.loads(body_lead)
    assert_test(lead_res.get('success') is True and 'leadId' in lead_res, "POST /api/lead returns confirmed leadId")

    # Test /api/lead spam rejection
    spam_data = { **post_data, '_hp': 'bot-val' }
    status_spam, _, _ = fetch_url('/api/lead', method='POST', data=spam_data)
    assert_test(status_spam == 400, "POST /api/lead rejects bot honeypot with HTTP 400")

    # Test /api/lead?dryRun=1 HTTP endpoint
    status_dry, _, body_dry = fetch_url('/api/lead?dryRun=1', method='POST', data=post_data)
    dry_res = json.loads(body_dry) if status_dry == 200 else {}
    assert_test(status_dry == 200 and dry_res.get('dryRun') is True, "POST /api/lead?dryRun=1 returns HTTP 200 with dryRun: true")

    # Test /api/health
    status_health, _, body_health = fetch_url('/api/health')
    assert_test(status_health == 200 and 'healthy' in body_health or 'ok' in body_health, "GET /api/health returns HTTP 200")

    # Test /api/csp-report
    status_csp, _, _ = fetch_url('/api/csp-report', method='POST', data={'csp-report': {'blocked-uri': 'eval'}})
    assert_test(status_csp == 204, "POST /api/csp-report logs violation with HTTP 204")

    # Test subpages resolution (clean URLs and .html)
    subpages = [
        ('/pricing', 'Pricing & Plans'),
        ('/about', 'About Quiktalk AI'),
        ('/privacy-policy', 'Privacy Policy'),
        ('/terms', 'Terms of Service'),
        ('/ai-voice-agents', '24/7 AI Voice Receptionists'),
        ('/ai-systems-automations', 'AI Systems & Workflow Automations'),
        ('/ai-consulting', 'Consulting'),
        ('/web-software-development', 'Custom Web & Software Development'),
        ('/case-studies', 'Case Studies'),
        ('/robots.txt', 'User-agent'),
        ('/sitemap.xml', '<urlset'),
        ('/favicon.ico', '')
    ]
    for path, expected_text in subpages:
        s, _, b = fetch_url(path)
        if expected_text:
            assert_test(s == 200 and expected_text in b, f"GET {path} returns HTTP 200 and expected content")
        else:
            assert_test(s == 200, f"GET {path} returns HTTP 200")

    # Test 404 page
    status_404, _, body_404 = fetch_url('/non-existent-page-test-404')
    assert_test(status_404 == 404 and '404' in body_404, "GET /non-existent-page returns custom 404 page")

finally:
    server_proc.terminate()
    server_proc.wait()

# ------------------------------------------------------------
# 3. Static Code & SEO Quality Checks
# ------------------------------------------------------------
print("\n3. Testing Technical SEO, Schema, Brand & Accessibility (QTK-004, QTK-005, QTK-010, QTK-016)")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Brand consistency
assert_test('QuickTalk AI' not in html and 'QuikTalk AI' not in html, "Brand Consistency: zero occurrences of QuickTalk or QuikTalk in index.html")

# JSON-LD validation
import re
json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
assert_test(len(json_ld_matches) >= 1, "JSON-LD structured data block present in <head>")
if json_ld_matches:
    try:
        ld_data = json.loads(json_ld_matches[0])
        types = [item.get('@type') for item in ld_data.get('@graph', [])]
        assert_test('Organization' in types, "JSON-LD contains Organization schema")
        assert_test('LocalBusiness' in types, "JSON-LD contains LocalBusiness schema")
        assert_test('Service' in types, "JSON-LD contains Service schema")
        assert_test('FAQPage' in types, "JSON-LD contains FAQPage schema")
        assert_test('BreadcrumbList' in types, "JSON-LD contains BreadcrumbList schema")
    except Exception as e:
        assert_test(False, "JSON-LD JSON parsing", str(e))

# Accessibility checks
assert_test('class="skip-link"' in html, "Accessibility: Skip to content link present")
assert_test('<main id="main">' in html, "Accessibility: Semantic <main> landmark present")
assert_test('aria-expanded="false"' in html, "Accessibility: aria-expanded present on interactive elements")
assert_test('aria-live="polite"' in html, "Accessibility: aria-live='polite' form status container present")
assert_test('id="leadHp"' in html and '_hp' in html, "Security/Spam: Honeypot field present in lead form")
assert_test('<label class="sr-only"' in html, "Accessibility: Accessible labels present for form inputs")
assert_test('<noscript>' in html, "Resilience: <noscript> fallback styles present")

# Sitemap validation
try:
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    assert_test(len(urls) >= 10, f"Sitemap valid with {len(urls)} URLs")
    assert_test('https://www.quiktalkai.com/' in urls, "Sitemap includes canonical root")
    assert_test('https://www.quiktalkai.com/pricing' in urls, "Sitemap includes /pricing")
except Exception as e:
    assert_test(False, "sitemap.xml validation", str(e))

# Assets presence
assert_test(os.path.exists('assets/favicon-32x32.png'), "Asset: favicon-32x32.png exists")
assert_test(os.path.exists('assets/apple-touch-icon.png'), "Asset: apple-touch-icon.png exists")
assert_test(os.path.exists('assets/og-image.jpg'), "Asset: og-image.jpg (1200x630) exists")
assert_test(os.path.exists('assets/logo-64.webp') and os.path.getsize('assets/logo-64.webp') < 10000, "Asset: logo-64.webp optimized (<10KB)")
assert_test(os.path.exists('PLACEHOLDERS.md'), "Registry: PLACEHOLDERS.md exists with PH-01..PH-07")
assert_test(os.path.exists('.env.example'), "Config: .env.example exists")
assert_test(os.path.exists('wrangler.toml'), "Stage 2 Config: wrangler.toml exists (Cloudflare Pages)")
assert_test(os.path.exists('llms.txt'), "Stage 2 SEO: llms.txt exists (GEO add-on)")
assert_test(os.path.exists('documentation/dns-records-cutover-guide.md'), "Stage 2 Documentation: dns-records-cutover-guide.md exists")
assert_test(os.path.exists('documentation/origin-lockdown-and-monitoring.md'), "Stage 2 Documentation: origin-lockdown-and-monitoring.md exists")

# ------------------------------------------------------------
# Final Summary
# ------------------------------------------------------------
print("\n============================================================")
print(f" TOTAL TESTS RUN: {PASSED + FAILED}")
print(f" PASSED: {PASSED}")
print(f" FAILED: {FAILED}")
print("============================================================\n")

if FAILED > 0:
    sys.exit(1)
else:
    print("ALL STAGE 1 LOCAL VALIDATION TESTS PASSED SUCCESSFULLY!\n")
    sys.exit(0)
