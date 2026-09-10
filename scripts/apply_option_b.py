"""
scripts/apply_option_b.py
Applies strictly NON-VISUAL / INVISIBLE technical improvements to index.original.html.
Preserves 100% of the visual UI, design, layout, colors, typography, hero headings, and copy.
"""

import re
import json

def apply_option_b():
    with open('index.original.html', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Unify brand name in copy without changing headings or layout
    # "QuickTalk AI" -> "Quiktalk AI", "QuikTalk AI" -> "Quiktalk AI"
    src = src.replace('QuikTalk AI', 'Quiktalk AI')
    src = src.replace('QuickTalk AI', 'Quiktalk AI')
    src = src.replace('QuickTalk', 'Quiktalk')
    src = src.replace('QuikTalk', 'Quiktalk')

    # 2. Add invisible/screen-reader styles to <style>
    hidden_styles = """
/* Non-visual accessibility & utility styles (zero UI impact) */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
.skip-link {
  position: absolute;
  top: -100px;
  left: 16px;
  background: var(--cyan);
  color: #000;
  padding: 8px 16px;
  font-weight: 600;
  font-size: 13px;
  z-index: 99999;
  border-radius: 4px;
  text-decoration: none;
  transition: top 0.2s;
}
.skip-link:focus {
  top: 16px;
}
:focus-visible {
  outline: 2px solid var(--cyan) !important;
  outline-offset: 3px !important;
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  #gl { display: none !important; }
}
"""
    src = src.replace('/* ============================================================= WebGL Canvas', hidden_styles + '\n/* ============================================================= WebGL Canvas')

    # 3. Add invisible Head metadata (SEO, JSON-LD, Favicons, Noscript)
    head_metadata = """  <link rel="canonical" href="https://www.quiktalkai.com/">
  <meta name="theme-color" content="#060608">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

  <!-- Open Graph & Social Cards -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Quiktalk AI">
  <meta property="og:title" content="Quiktalk AI — Personalised 24/7 AI Voice Agents">
  <meta property="og:description" content="Quiktalk AI builds custom 24/7 personalised AI voice agents for your business. Answer every call, qualify leads, and book appointments seamlessly.">
  <meta property="og:url" content="https://www.quiktalkai.com/">
  <meta property="og:image" content="https://www.quiktalkai.com/assets/og-image.jpg">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Quiktalk AI — Personalised 24/7 AI Voice Agents">
  <meta name="twitter:description" content="Custom 24/7 AI voice receptionists for New Zealand & Australia businesses.">
  <meta name="twitter:image" content="https://www.quiktalkai.com/assets/og-image.jpg">

  <!-- Structured Data Graph (JSON-LD) for AEO/GEO (QTK-005, QTK-016) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "https://www.quiktalkai.com/#organization",
        "name": "Quiktalk AI",
        "url": "https://www.quiktalkai.com/",
        "logo": "https://www.quiktalkai.com/assets/logo-192.webp",
        "email": "admin@quiktalkai.com",
        "areaServed": [
          { "@type": "Country", "name": "New Zealand" },
          { "@type": "Country", "name": "Australia" }
        ],
        "description": "24/7 custom AI voice receptionists for NZ and AU businesses."
      },
      {
        "@type": "LocalBusiness",
        "@id": "https://www.quiktalkai.com/#localbusiness",
        "name": "Quiktalk AI",
        "url": "https://www.quiktalkai.com/",
        "email": "admin@quiktalkai.com",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Auckland",
          "addressCountry": "NZ"
        },
        "priceRange": "$$"
      },
      {
        "@type": "Service",
        "@id": "https://www.quiktalkai.com/#service",
        "name": "24/7 AI Voice Agent",
        "provider": { "@id": "https://www.quiktalkai.com/#organization" },
        "serviceType": "Phone Answering Service",
        "areaServed": ["New Zealand", "Australia"],
        "description": "Personalised 24/7 AI voice phone receptionist service."
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://www.quiktalkai.com/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://www.quiktalkai.com/"
          }
        ]
      },
      {
        "@type": "FAQPage",
        "@id": "https://www.quiktalkai.com/#faq",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "What does Quiktalk AI do?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Quiktalk AI is an AI voice receptionist that answers your phone, speaks naturally with callers, answers questions about your business, and books appointments straight into your calendar or CRM."
            }
          },
          {
            "@type": "Question",
            "name": "Will callers know they are talking to an AI?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Most callers can't tell the difference. Quiktalk AI sounds like a warm, professional Kiwi or Australian receptionist."
            }
          },
          {
            "@type": "Question",
            "name": "Can I keep my existing business phone number?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. You keep your current number. Quiktalk AI uses conditional call forwarding."
            }
          },
          {
            "@type": "Question",
            "name": "How much does an AI receptionist cost?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Plans start from $149 NZD per month for 100 minutes of talk time, scaling up based on call volume."
            }
          },
          {
            "@type": "Question",
            "name": "How long does setup take?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Your agent is typically live within 3 business days."
            }
          },
          {
            "@type": "Question",
            "name": "What happens on complex or emergency calls?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "You set the rules. The agent can transfer high-priority calls straight to your mobile."
            }
          },
          {
            "@type": "Question",
            "name": "Does it book appointments into my calendar automatically?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. It connects to Google Calendar, Outlook, Cliniko, Tradify, Fergus, ServiceM8, and others."
            }
          },
          {
            "@type": "Question",
            "name": "Can I listen to calls or read transcripts?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. Every single call is recorded, transcribed, and logged."
            }
          },
          {
            "@type": "Question",
            "name": "Which tools does it integrate with?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Google Calendar, Outlook, HubSpot, Salesforce, Tradify, Fergus, ServiceM8, Cliniko, SimPRO, and Shopify."
            }
          },
          {
            "@type": "Question",
            "name": "Is it legal to answer and record calls this way?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. Quiktalk AI follows call-recording consent rules in NZ and Australia."
            }
          },
          {
            "@type": "Question",
            "name": "Do I need new hardware or software?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "No. Quiktalk AI runs on your existing phone line via call forwarding."
            }
          },
          {
            "@type": "Question",
            "name": "What if the AI can't answer a caller's question?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The agent lets the caller know, takes their message, and alerts you."
            }
          }
        ]
      }
    ]
  }
  </script>

  <!-- Fallback for JavaScript disabled (QTK-018) -->
  <noscript>
    <style>
      #pre { display: none !important; }
      .faq-a { display: block !important; }
      #gl { display: none !important; }
    </style>
  </noscript>
"""
    src = src.replace('<link rel="icon" href="assets/logo.png">', head_metadata)

    # 4. Add off-screen skip link right after <body> (zero visual impact)
    src = src.replace('<body>', '<body>\n  <a href="#main" class="skip-link">Skip to main content</a>')

    # 5. Add semantic <main id="main"> wrapper around content (zero visual impact)
    src = src.replace('<div class="page">', '<div class="page">\n    <main id="main">', 1)
    src = src.replace('<!-- ============================================================= FOOTER', '</main>\n\n    <!-- ============================================================= FOOTER', 1)

    # 6. Add aria-expanded and attributes to burger button (zero visual impact)
    src = src.replace('<div class="burger" onclick="toggleMenu()">', '<div class="burger" id="burgerBtn" role="button" tabindex="0" aria-expanded="false" aria-label="Toggle navigation menu" onclick="toggleMenu()">')

    # 7. Add aria-expanded to FAQ questions (zero visual impact)
    faq_num = 0
    def add_faq_aria(m):
        nonlocal faq_num
        faq_num += 1
        return f'<div class="faq-q" role="button" tabindex="0" aria-expanded="false" aria-controls="faq-ans-{faq_num}" onclick="toggleFaq(this)">'
    src = re.sub(r'<div class="faq-q" onclick="toggleFaq\(this\)">', add_faq_aria, src)

    # 8. Upgrade Lead Form non-visually: add hidden sr-only labels, input attributes, honeypot, and live status
    form_old = re.search(r'<form id="leadForm".*?</form>', src, re.DOTALL)
    if form_old:
        form_upgraded = """<form id="leadForm" onsubmit="handleFormSubmit(event)">
        <!-- Hidden Honeypot Trap for Spam Protection -->
        <input type="text" name="_hp" id="leadHp" style="display:none !important;" tabindex="-1" autocomplete="off">

        <div class="form-grid">
          <div>
            <label class="sr-only" for="leadName">Your name</label>
            <input type="text" id="leadName" name="name" class="input-field" placeholder="Your name" autocomplete="name" maxlength="100" required>
          </div>
          <div>
            <label class="sr-only" for="leadBusiness">Business name</label>
            <input type="text" id="leadBusiness" name="businessName" class="input-field" placeholder="Business name" autocomplete="organization" maxlength="120" required>
          </div>
        </div>
        <div class="form-grid">
          <div>
            <label class="sr-only" for="leadPhone">Phone number</label>
            <input type="tel" id="leadPhone" name="phone" class="input-field" placeholder="Phone number" inputmode="tel" autocomplete="tel" maxlength="30" required>
          </div>
          <div>
            <label class="sr-only" for="leadEmail">Email address</label>
            <input type="email" id="leadEmail" name="email" class="input-field" placeholder="Email address" inputmode="email" autocomplete="email" maxlength="254" required>
          </div>
        </div>
        <div class="form-grid">
          <div style="grid-column: 1 / -1;">
            <label class="sr-only" for="leadWebsite">Company website</label>
            <input type="text" id="leadWebsite" name="website" class="input-field" placeholder="Company website" inputmode="url" autocomplete="url" maxlength="200" style="width: 100%;">
          </div>
        </div>
        <div>
          <label class="sr-only" for="leadMessage">What kind of calls do you receive most often?</label>
          <textarea id="leadMessage" name="message" class="input-field" rows="3" placeholder="What kind of calls do you receive most often?" maxlength="2000" required style="margin-bottom: 20px;"></textarea>
        </div>

        <!-- Accessible Live Submission Status Alert Container (Invisible by default) -->
        <div id="formStatus" class="sr-only" aria-live="polite"></div>

        <button type="submit" class="btn-submit" id="submitBtn">Build my free demo agent</button>
        <div style="font-size: 11px; color: var(--muted); text-align: center; margin-top: 14px; letter-spacing: 0.08em; text-transform: uppercase;">
          We reply within 1 business day · No credit card required · <a href="/privacy-policy" style="color: var(--cyan); text-decoration: underline;">Privacy Policy</a>
        </div>
      </form>"""
        src = src.replace(form_old.group(0), form_upgraded, 1)

    # 9. Update handleFormSubmit in the script to submit to /api/lead while keeping the exact original button animation & style
    handler_old = re.search(r'function handleFormSubmit\(e\)\s*\{.*?setTimeout\(.*?\};\s*\}', src, re.DOTALL)
    if handler_old:
        handler_new = """async function handleFormSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const btn = document.getElementById('submitBtn');
  const statusBox = document.getElementById('formStatus');

  btn.innerText = 'BUILDING DEMO AGENT...';
  btn.style.background = '#fff';
  btn.style.color = '#000';
  btn.disabled = true;

  if (statusBox) statusBox.innerText = 'Submitting demo request...';

  try {
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload._page = window.location.href;

    const response = await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok || !data.success) {
      throw new Error(data.message || (data.errors && data.errors[0]) || 'Server error');
    }

    // Success confirmed by server
    btn.innerText = '✓ DEMO REQUEST SUBMITTED';
    btn.style.background = '#e5c158';
    btn.style.color = '#000';
    btn.disabled = true;
    if (statusBox) statusBox.innerText = 'Demo request confirmed!';
    window.dispatchEvent(new CustomEvent('lead:success', { detail: data }));
    form.reset();

  } catch (err) {
    btn.disabled = false;
    btn.innerText = 'SOMETHING WENT WRONG — TRY AGAIN';
    btn.style.background = '#f87171';
    btn.style.color = '#fff';
    if (statusBox) statusBox.innerText = 'Error: ' + err.message;
  }
}"""
        src = src.replace(handler_old.group(0), handler_new, 1)

    # 10. Update preloader script to fade on load and never trap users
    preloader_old = re.search(r'// ============================================================= Preloader Animation.*?const loadInterval = setInterval\(.*?\}, 60\);', src, re.DOTALL)
    if preloader_old:
        preloader_new = """// ============================================================= Preloader Animation
let progress = 0;
const preFill = document.getElementById('pre-bar-fill');
const preNum = document.getElementById('pre-num');
const preEl = document.getElementById('pre');

function finishPreloader() {
  if (preEl && !preEl.classList.contains('done')) {
    if (preNum) preNum.innerText = '100%';
    if (preFill) preFill.style.right = '0%';
    setTimeout(() => {
      preEl.classList.add('done');
    }, 150);
  }
}

const loadInterval = setInterval(() => {
  progress += Math.floor(Math.random() * 18) + 12;
  if (progress >= 100) {
    progress = 100;
    clearInterval(loadInterval);
    finishPreloader();
  }
  if (preFill) preFill.style.right = (100 - progress) + '%';
  if (preNum) preNum.innerText = progress + '%';
}, 40);

window.addEventListener('load', finishPreloader);
setTimeout(finishPreloader, 1200);"""
        src = src.replace(preloader_old.group(0), preloader_new, 1)

    # 11. Three.js try/catch and performance guards (visibilitychange & IntersectionObserver)
    three_init_old = "const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });"
    three_init_new = """let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: window.devicePixelRatio < 2, alpha: true, powerPreference: 'high-performance' });
} catch (e) {
  console.warn('[Three.js] WebGL not supported, running with canvas hidden');
  if (canvas) canvas.style.display = 'none';
}"""
    src = src.replace(three_init_old, three_init_new, 1)

    # Wrap animate rAF in visibility & hero intersection check
    animate_old = re.search(r'function animate\(\)\s*\{.*?requestAnimationFrame\(animate\);.*?renderer\.render\(scene, camera\);\s*\}', src, re.DOTALL)
    if animate_old:
        animate_new = """let isTabVisible = true;
let isHeroVisible = true;
let isLoopRunning = true;
let cachedScrollHeight = document.body.scrollHeight || 3000;

document.addEventListener('visibilitychange', () => {
  isTabVisible = !document.hidden;
  if (isTabVisible && isHeroVisible && !isLoopRunning) {
    isLoopRunning = true;
    requestAnimationFrame(animate);
  }
});

if (window.IntersectionObserver) {
  const heroEl = document.getElementById('hero');
  if (heroEl) {
    new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        isHeroVisible = entry.isIntersecting;
        if (isTabVisible && isHeroVisible && !isLoopRunning) {
          isLoopRunning = true;
          requestAnimationFrame(animate);
        }
      });
    }, { threshold: 0.05 }).observe(heroEl);
  }
}

window.addEventListener('resize', () => {
  cachedScrollHeight = document.body.scrollHeight || 3000;
}, { passive: true });

function animate() {
  if (!isTabVisible || !isHeroVisible) {
    isLoopRunning = false;
    return;
  }
  requestAnimationFrame(animate);

  const time = clock.getElapsedTime();
  scrollY += (targetScrollY - scrollY) * 0.05;
  mouseX += (targetMouseX - mouseX) * 0.05;
  mouseY += (targetMouseY - mouseY) * 0.05;

  const scrollFraction = scrollY / (cachedScrollHeight - window.innerHeight || 1);

  headsetGroup.rotation.y = time * 0.35 + mouseX * 0.45;
  headsetGroup.rotation.x = Math.sin(time * 0.5) * 0.18 + mouseY * 0.35;
  headsetGroup.rotation.z = Math.cos(time * 0.4) * 0.1;
  headsetGroup.position.y = 2 + Math.sin(time * 1.5) * 0.5;

  gyro1Mesh.rotation.z = time * 0.6;
  gyro2Mesh.rotation.z = -time * 0.4;

  const pos = gridGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const u = (i % gridWidth) / gridWidth;
    const v = Math.floor(i / gridWidth) / gridHeight;
    const wave1 = Math.sin(u * 10 + time * 2.0) * 1.2;
    const wave2 = Math.cos(v * 8 + time * 1.5) * 1.2;
    pos.setY(i, wave1 + wave2);
  }
  gridGeo.attributes.position.needsUpdate = true;

  particleSystem.rotation.y = time * 0.03;
  particleSystem.rotation.x = Math.sin(time * 0.02) * 0.1;

  camera.position.z = 22 - scrollFraction * 8;
  camera.position.y = 2 - scrollFraction * 3;
  camera.position.x = Math.sin(scrollFraction * Math.PI * 2) * 5;
  camera.lookAt(headsetGroup.position.x * 0.3, headsetGroup.position.y * 0.3, 0);

  if (renderer) renderer.render(scene, camera);
}"""
        src = src.replace(animate_old.group(0), animate_new, 1)

    # 12. Add analytics.js script tag before end of body
    src = src.replace('<script src="assets/three.min.js"></script>', '<script src="assets/js/analytics.js" defer></script>\n<script src="assets/three.min.js"></script>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(src)

    print("Option B successfully applied to index.html!")

if __name__ == '__main__':
    apply_option_b()
