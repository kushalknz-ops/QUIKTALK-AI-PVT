"""
scripts/build_index.py
Constructs the upgraded, fully-audited index.html for Quiktalk AI (QTK-001 to QTK-025).
"""

import re
import json

def build_index():
    with open('index.live.html', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update Title & Meta
    head_insert = """  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>AI Receptionist NZ & AU | Quiktalk AI — 24/7 AI Voice Agents</title>
  <meta name="description" content="Custom 24/7 AI voice receptionists for NZ and AU businesses. Answers every call in natural speech, qualifies leads, and books appointments seamlessly. Live in 3 days.">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#060608">
  <link rel="canonical" href="https://www.quiktalkai.com/">

  <!-- Optimized Favicons & Touch Icons (QTK-014, QTK-022) -->
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

  <!-- Open Graph & Social Cards (QTK-016) -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Quiktalk AI">
  <meta property="og:title" content="AI Receptionist NZ & AU | Quiktalk AI — 24/7 AI Voice Agents">
  <meta property="og:description" content="Custom 24/7 AI voice receptionists for NZ and AU businesses. Answers every call, qualifies leads, and books appointments seamlessly.">
  <meta property="og:url" content="https://www.quiktalkai.com/">
  <meta property="og:image" content="https://www.quiktalkai.com/assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="AI Receptionist NZ & AU | Quiktalk AI — 24/7 AI Voice Agents">
  <meta name="twitter:description" content="Custom 24/7 AI voice receptionists for NZ & AU businesses. Never miss another call.">
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
        "description": "Provider of 24/7 conversational AI voice receptionists and automated telephone answering services."
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
        "name": "24/7 AI Voice Receptionist",
        "provider": { "@id": "https://www.quiktalkai.com/#organization" },
        "serviceType": "Telephone Answering & Appointment Booking",
        "areaServed": ["New Zealand", "Australia"],
        "description": "Custom conversational AI phone receptionists that triage inbound calls, qualify leads, and schedule appointments."
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
              "text": "Quiktalk AI builds a personalised AI voice agent that answers your business phone calls 24/7. It sounds completely natural, answers common questions, qualifies callers, takes messages, and books appointments directly into your calendar or CRM."
            }
          },
          {
            "@type": "Question",
            "name": "Will callers know they are talking to an AI?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Most callers can't tell the difference. The agent speaks with natural pauses, realistic intonation, and instant responses (under 0.4 seconds). However, we always recommend transparency — the agent can introduce itself as your AI assistant."
            }
          },
          {
            "@type": "Question",
            "name": "Can I keep my existing business phone number?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes, 100%. You don't need to change numbers or switch carriers. You simply set up conditional call forwarding so that unanswered or busy calls route to your AI agent."
            }
          },
          {
            "@type": "Question",
            "name": "How much does an AI receptionist cost?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Plans start from $149 NZD per month for 100 minutes of talk time, scaling up based on call volume. Compared to a full-time receptionist ($55k–$65k/yr) or traditional answering service ($1.80–$2.50/min), businesses typically save over 70%."
            }
          },
          {
            "@type": "Question",
            "name": "How long does setup take?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Your agent is typically live within 3 business days. We handle everything: voice configuration, prompt engineering, CRM integration, and thorough testing."
            }
          },
          {
            "@type": "Question",
            "name": "What happens on complex or emergency calls?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "You set the rules. The agent can transfer high-priority or emergency calls straight to your mobile or on-call staff immediately, or send an urgent SMS alert."
            }
          },
          {
            "@type": "Question",
            "name": "Does it book appointments into my calendar automatically?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. It connects to Google Calendar, Outlook, Cliniko, Tradify, Fergus, ServiceM8, and others to check real-time availability and confirm bookings on the call."
            }
          },
          {
            "@type": "Question",
            "name": "Can I listen to calls or read transcripts?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. Every single call is recorded, transcribed, and logged in your dashboard. You also receive an instant summary via email or SMS within seconds of the call ending."
            }
          },
          {
            "@type": "Question",
            "name": "Which tools does it integrate with?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "We connect with Google Calendar, Outlook, HubSpot, Salesforce, Tradify, Fergus, ServiceM8, Cliniko, SimPRO, Shopify, and custom webhooks/CRMs."
            }
          },
          {
            "@type": "Question",
            "name": "Is it legal to answer and record calls this way?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. We operate in compliance with New Zealand and Australian telecommunication and privacy laws. We configure your agent with appropriate call recording disclosure greetings."
            }
          },
          {
            "@type": "Question",
            "name": "Do I need new hardware or software?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "None at all. It runs in the cloud and connects to your existing phone line via standard call forwarding. There are zero apps to install."
            }
          },
          {
            "@type": "Question",
            "name": "What if the AI can't answer a caller's question?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The agent gracefully lets the caller know, takes their detailed message and callback number, and flags the item for your team."
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
  </noscript>"""

    # Replace head tag contents up to <style>
    style_idx = src.find('<style>')
    if style_idx != -1:
        new_src = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" + head_insert + "\n" + src[style_idx:]
    else:
        new_src = src

    # 2. Add Accessibility Styles to CSS
    accessibility_css = """
/* Accessibility (WCAG 2.1 AA) & Enhanced Contrast (QTK-010, QTK-023) */
.skip-link {
  position: absolute;
  top: -100px;
  left: 16px;
  background: var(--cyan);
  color: #000;
  padding: 10px 18px;
  font-weight: 600;
  font-size: 13px;
  z-index: 10000;
  border-radius: 6px;
  transition: top 0.2s;
  text-decoration: none;
}
.skip-link:focus { top: 16px; }

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

/* Microcopy contrast enhancement */
.body, .sec-sub, .faq-a, .meta-note {
  color: #a1a1aa !important; /* Passes 4.5:1 AA contrast */
}

/* Touch target minimums */
.burger {
  min-width: 44px;
  min-height: 44px;
  display: none;
  align-items: center;
  justify-content: center;
}
@media (max-width: 900px) {
  .burger { display: flex; }
}

/* Form status box */
.form-status {
  display: none;
  padding: 14px 18px;
  border-radius: 8px;
  font-size: 14px;
  margin-top: 16px;
  text-align: center;
  line-height: 1.5;
}
.form-status.info { background: rgba(229, 193, 88, 0.15); color: #fef08a; border: 1px solid rgba(229, 193, 88, 0.4); }
.form-status.success { background: rgba(52, 211, 153, 0.15); color: #a7f3d0; border: 1px solid #34d399; }
.form-status.error { background: rgba(248, 113, 113, 0.15); color: #fecaca; border: 1px solid #f87171; }

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

.consent-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 14px 0 18px;
  font-size: 13px;
  color: #a1a1aa;
  text-align: left;
}
.consent-row input[type="checkbox"] {
  margin-top: 3px;
  accent-color: var(--cyan);
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* FAQ Accessible Button */
button.faq-q {
  width: 100%;
  text-align: left;
  background: none;
  border: 0;
  cursor: pointer;
  padding: 20px clamp(16px, 2.5vw, 28px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: clamp(14px, 1.2vw, 17px);
  color: #fff;
  font-weight: 400;
}
"""
    new_src = new_src.replace('/* ============================================================= Responsive Breakpoints */', accessibility_css + '\n/* ============================================================= Responsive Breakpoints */')

    # 3. Add Skip Link right after <body>
    new_src = re.sub(r'<body[^>]*>', '<body>\n  <a href="#main" class="skip-link">Skip to main content</a>', new_src)

    # 4. Brand Unification (QTK-004)
    # Replace "QuickTalk AI" and "QuikTalk AI" with "Quiktalk AI"
    new_src = new_src.replace('QuikTalk AI', 'Quiktalk AI')
    new_src = new_src.replace('QuickTalk AI', 'Quiktalk AI')

    # 5. Semantic Landmarks: Add <header id="main-nav"> and <main id="main">
    # Replace nav bar
    nav_old = re.search(r'<div class="nav-track" id="main-nav">.*?</div>\s*</div>', new_src, re.DOTALL)
    if nav_old:
        nav_replacement = """<header class="nav-track" id="main-nav">
      <div class="nav-inner">
        <a href="/" class="brand" aria-label="Quiktalk AI Homepage">
          <img src="assets/logo-64.webp" srcset="assets/logo-64.webp 64w, assets/logo-192.4fc1a254.hash.webp 192w" width="34" height="34" alt="Quiktalk AI Logo" class="brand-img">
          <span>Quiktalk AI</span>
        </a>
        <nav class="nav-links" aria-label="Primary Navigation">
          <a href="#hero" class="nav-link">Home</a>
          <a href="#workflow" class="nav-link">How It Works</a>
          <a href="#industries" class="nav-link">Industries</a>
          <a href="#comparison" class="nav-link">Why Quiktalk AI</a>
          <a href="/pricing" class="nav-link">Pricing</a>
          <a href="#integrations" class="nav-link">Integrations</a>
          <a href="/about" class="nav-link">About</a>
          <a href="#faq" class="nav-link">FAQ</a>
          <a href="#demo" class="nav-cta">Get A Demo</a>
        </nav>
        <button type="button" class="burger" id="burgerBtn" aria-expanded="false" aria-label="Toggle navigation menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </header>"""
        new_src = new_src.replace(nav_old.group(0), nav_replacement, 1)

    # Wrap page content in <main id="main">
    new_src = new_src.replace('<div class="page">', '<div class="page">\n    <main id="main">', 1)
    new_src = new_src.replace('</section>\n\n    <!-- ============================================================= FOOTER', '</section>\n    </main>\n\n    <!-- ============================================================= FOOTER', 1)

    # 6. Hero Heading & AEO Definition Box (QTK-016)
    hero_h1_old = re.search(r'<h1 class="display h-hero">.*?</h1>', new_src, re.DOTALL)
    if hero_h1_old:
        hero_h1_new = """<h1 class="display h-hero">24/7 AI Voice Receptionists for NZ & AU Businesses<br><span style="color: var(--cyan); text-shadow: 0 0 30px rgba(229, 193, 88, 0.35);">Never miss another call — answers 24/7 & books the job.</span></h1>
        <!-- AEO Direct Answer Block (QTK-016) -->
        <div style="background: rgba(229, 193, 88, 0.08); border-left: 3px solid var(--cyan); padding: 14px 18px; margin: 20px 0; border-radius: 0 8px 8px 0; max-width: 680px;">
          <strong style="color: #fff; font-size: 14px; display: block; margin-bottom: 4px;">What is an AI voice receptionist?</strong>
          <p style="margin: 0; font-size: 13px; color: #d4d4d8; line-height: 1.6;">
            An AI voice receptionist is an automated conversational voice assistant that answers inbound business phone calls 24 hours a day. It speaks with a natural accent, answers customer questions, qualifies leads, triages emergencies, and schedules appointments directly into your calendar or CRM—without human intervention.
          </p>
        </div>"""
        new_src = new_src.replace(hero_h1_old.group(0), hero_h1_new, 1)

    # 7. Add Audio Demo Stub into Call Simulator (QTK-017, Change 5)
    sim_old = re.search(r'(<div class="sim-phone">.*?</div>\s*</div>\s*</div>)', new_src, re.DOTALL)
    if sim_old:
        audio_stub_markup = """
          <!-- Audio Demo Stub Component (QTK-017, PH-05) -->
          <div style="border-top: 1px solid var(--line-soft); padding: 14px 18px; background: rgba(0,0,0,0.3); border-radius: 0 0 16px 16px;">
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap;">
              <span style="font-size: 11px; font-weight: 600; color: var(--cyan); letter-spacing: 0.1em; text-transform: uppercase;">Real Call Previews:</span>
              <div style="display: flex; gap: 8px;">
                <button type="button" class="audio-stub-btn" data-slot="emergency-plumbing.mp3" style="font-size: 11px; padding: 5px 10px; border-radius: 4px; border: 1px solid var(--line); color: #fff; background: rgba(229,193,88,0.1);">▶ Plumbing Leak</button>
                <button type="button" class="audio-stub-btn" data-slot="dental-reschedule.mp3" style="font-size: 11px; padding: 5px 10px; border-radius: 4px; border: 1px solid var(--line); color: #fff; background: rgba(229,193,88,0.1);">▶ Dental Booking</button>
              </div>
            </div>
            <div id="audioStubNotice" style="display: none; font-size: 11px; color: #a1a1aa; margin-top: 8px; font-style: italic;"></div>
          </div>"""
        # Insert inside sim-box
        new_src = new_src.replace('</div>\n      </div>\n    </div>\n\n    <!-- Hero Highlights Strip', audio_stub_markup + '\n      </div>\n    </div>\n\n    <!-- Hero Highlights Strip', 1)

    # 8. Comparison Section Claims & Disclosed ROI Calculator (QTK-008)
    new_src = new_src.replace('100% ROI guaranteed within 60 days', 'Satisfaction Commitment: Active appointment capture within 30 days or cancel with zero fee')
    new_src = new_src.replace('$42,000+ / yr', '$55,000 – $65,000 NZD / yr*')
    
    # Expose ROI calculator assumptions visibly
    calc_note = """<div style="font-size: 12px; color: #a1a1aa; margin-top: 16px; line-height: 1.5; border-top: 1px solid var(--line-soft); padding-top: 12px;">
            <strong style="color: #fff;">Calculation Methodology:</strong> Assumes an industry average 30% missed-call rate for unassisted businesses, a 70% live-capture booking rate via instant 24/7 response, and an adjustable average job value (default: $500 NZD).
          </div>"""
    new_src = new_src.replace('</div>\n        </div>\n      </div>\n    </section>\n\n    <!-- ============================================================= INTEGRATIONS', calc_note + '\n        </div>\n      </div>\n    </section>\n\n    <!-- ============================================================= INTEGRATIONS', 1)

    # 9. Accessible FAQ Accordion conversion to <button class="faq-q">
    # Replace <div class="faq-q" onclick="toggleFaq(this)"> with <button type="button" class="faq-q" aria-expanded="false" aria-controls="faq-ans-N">
    faq_idx = 0
    def replace_faq_div(m):
        nonlocal faq_idx
        faq_idx += 1
        return f'<button type="button" class="faq-q" aria-expanded="false" aria-controls="faq-ans-{faq_idx}">'
    
    new_src = re.sub(r'<div class="faq-q"[^>]*>', replace_faq_div, new_src)
    new_src = new_src.replace('</div>\n          <div class="faq-a">', '</button>\n          <div class="faq-a">')
    
    # Add id to faq-a
    faq_a_idx = 0
    def replace_faq_a(m):
        nonlocal faq_a_idx
        faq_a_idx += 1
        return f'<div class="faq-a" id="faq-ans-{faq_a_idx}">'
    new_src = re.sub(r'<div class="faq-a">', replace_faq_a, new_src)

    # 10. Fix Lead Form: Labels, Names, Inputmode, Honeypot, Consent, Status Box (QTK-001)
    form_old = re.search(r'<form id="leadForm".*?</form>', new_src, re.DOTALL)
    if form_old:
        form_new = """<form id="leadForm" novalidate>
        <div class="form-grid">
          <div>
            <label class="sr-only" for="leadName">Your Name</label>
            <input type="text" id="leadName" name="name" class="input-field" placeholder="Your name" autocomplete="name" maxlength="100" required>
          </div>
          <div>
            <label class="sr-only" for="leadBusiness">Business Name</label>
            <input type="text" id="leadBusiness" name="businessName" class="input-field" placeholder="Business name" autocomplete="organization" maxlength="120" required>
          </div>
        </div>
        <div class="form-grid">
          <div>
            <label class="sr-only" for="leadPhone">Phone Number</label>
            <input type="tel" id="leadPhone" name="phone" class="input-field" placeholder="Phone number (NZ / AU)" inputmode="tel" autocomplete="tel" maxlength="30" required>
          </div>
          <div>
            <label class="sr-only" for="leadEmail">Email Address</label>
            <input type="email" id="leadEmail" name="email" class="input-field" placeholder="Email address" inputmode="email" autocomplete="email" maxlength="254" required>
          </div>
        </div>
        <div class="form-grid">
          <div style="grid-column: 1 / -1;">
            <label class="sr-only" for="leadWebsite">Company Website</label>
            <input type="url" id="leadWebsite" name="website" class="input-field" placeholder="Company website (optional)" inputmode="url" autocomplete="url" maxlength="200">
          </div>
        </div>
        <div>
          <label class="sr-only" for="leadMessage">What kind of calls do you receive most often?</label>
          <textarea id="leadMessage" name="message" class="input-field" rows="3" placeholder="What kind of calls do you receive most often?" maxlength="2000" required style="margin-bottom: 8px;"></textarea>
        </div>

        <!-- Honeypot anti-spam field (hidden from real users) -->
        <input type="text" name="_hp" id="leadHp" style="display:none !important;" tabindex="-1" autocomplete="off">

        <!-- Marketing consent checkbox (QTK-002) -->
        <div class="consent-row">
          <input type="checkbox" id="marketingConsent" name="marketingConsent">
          <label for="marketingConsent">Send me occasional NZ/AU voice AI case studies and benchmark research (optional).</label>
        </div>

        <!-- Accessible Live Submission Status Alert Container (QTK-001) -->
        <div id="formStatus" class="form-status" aria-live="polite"></div>

        <button type="submit" class="btn-submit" id="submitBtn">Build my free demo agent</button>
        <div style="font-size: 12px; color: #a1a1aa; text-align: center; margin-top: 14px; letter-spacing: 0.04em;">
          We reply within 1 business day · No credit card required · <a href="/privacy-policy" style="color: var(--cyan); text-decoration: underline;">Privacy Policy</a> · <a href="/terms" style="color: var(--cyan); text-decoration: underline;">Terms of Service</a>
        </div>
      </form>"""
        new_src = new_src.replace(form_old.group(0), form_new, 1)

    # 11. Footer Services and Policy Links (QTK-002, QTK-019)
    new_src = new_src.replace('<li><a href="#demo" style="color: var(--bone-dim); transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'var(--bone-dim)\'">AI Voice Agents</a></li>', '<li><a href="/ai-voice-agents" style="color: var(--bone-dim); transition: color 0.2s;">AI Voice Agents</a></li>')
    new_src = new_src.replace('<li><a href="#demo" style="color: var(--bone-dim); transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'var(--bone-dim)\'">AI Systems & Automations</a></li>', '<li><a href="/ai-systems-automations" style="color: var(--bone-dim); transition: color 0.2s;">AI Systems & Automations</a></li>')
    new_src = new_src.replace('<li><a href="#demo" style="color: var(--bone-dim); transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'var(--bone-dim)\'">AI Consulting & Roadmaps</a></li>', '<li><a href="/ai-consulting" style="color: var(--bone-dim); transition: color 0.2s;">AI Consulting & Roadmaps</a></li>')
    new_src = new_src.replace('<li><a href="#demo" style="color: var(--bone-dim); transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'var(--bone-dim)\'">Web & Software Development</a></li>', '<li><a href="/web-software-development" style="color: var(--bone-dim); transition: color 0.2s;">Web & Software Development</a></li>')
    
    # Footer Policy links
    new_src = new_src.replace('<span><a href="#about" style="color: inherit;">Privacy Policy</a> · <a href="#about" style="color: inherit;">Terms of Service</a></span>', '<span><a href="/privacy-policy" style="color: inherit;">Privacy Policy</a> · <a href="/terms" style="color: inherit;">Terms of Service</a> · <a href="/pricing" style="color: inherit;">Pricing</a> · <a href="/case-studies" style="color: inherit;">Case Studies</a></span>')

    # 12. Replace inline script with external deferred scripts (QTK-011, QTK-013)
    script_old = re.search(r'<script src="assets/three.min.js"></script>\s*<script>.*?</script>', new_src, re.DOTALL)
    if script_old:
        script_replacement = """  <!-- Optimized Scripts (QTK-003, QTK-011, QTK-013) -->
  <script src="assets/js/analytics.js" defer></script>
  <script src="assets/three.min.js" defer></script>
  <script src="assets/js/main.e3f64dd0.hash.js" defer></script>"""
        new_src = new_src.replace(script_old.group(0), script_replacement, 1)

    # 13. Remove remaining inline event handlers
    new_src = re.sub(r'\sonmouseover="[^"]*"', '', new_src)
    new_src = re.sub(r'\sonmouseout="[^"]*"', '', new_src)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_src)

    print("Successfully generated upgraded index.html")

if __name__ == '__main__':
    build_index()
