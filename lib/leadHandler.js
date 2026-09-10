/**
 * lib/leadHandler.js
 * SHARED SINGLE SOURCE OF TRUTH for Quiktalk AI Lead Processing
 * Framework-free module: works in Node.js, Cloudflare Pages Functions, and test runners.
 */

// In-memory rate limiting cache (per-process)
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const RATE_LIMIT_MAX_REQUESTS = 5;

/**
 * Validates email format according to standard RFC-like pattern
 */
function isValidEmail(email) {
  if (typeof email !== 'string') return false;
  const re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
  return re.test(email.trim()) && email.length <= 254;
}

/**
 * Validates phone numbers with support for New Zealand and Australian formats,
 * as well as general international E.164.
 */
function isValidPhone(phone) {
  if (typeof phone !== 'string') return false;
  const clean = phone.replace(/[\s\-\(\)\.]/g, '');
  if (clean.length < 7 || clean.length > 20) return false;
  // Allows +64, 02X, 0800, 09, +61, 04, and standard digits
  return /^\+?[0-9]{7,18}$/.test(clean);
}

/**
 * Validates website URL if provided
 */
function isValidWebsite(url) {
  if (!url || typeof url !== 'string' || url.trim() === '') return true;
  const clean = url.trim();
  if (clean.length > 200) return false;
  return /^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/.*)?$/i.test(clean);
}

/**
 * Validates the complete lead payload.
 * Returns { valid: boolean, errors: string[], sanitized: object }
 */
function validateLead(payload) {
  const errors = [];
  const sanitized = {};

  if (!payload || typeof payload !== 'object') {
    return { valid: false, errors: ['Invalid request payload. Expected a JSON object.'], sanitized: {} };
  }

  // Honeypot check: _hp MUST be empty
  if (payload._hp && String(payload._hp).trim().length > 0) {
    // Spam detected
    return { valid: false, errors: ['Spam detection triggered.'], isSpam: true, sanitized: {} };
  }

  // Name (required, 1-100 chars)
  const name = typeof payload.name === 'string' ? payload.name.trim() : '';
  if (!name) {
    errors.push('Full name is required.');
  } else if (name.length > 100) {
    errors.push('Name must not exceed 100 characters.');
  } else {
    sanitized.name = name;
  }

  // Business Name (required, 1-120 chars)
  const businessName = typeof payload.businessName === 'string' 
    ? payload.businessName.trim() 
    : (typeof payload.business === 'string' ? payload.business.trim() : '');
  if (!businessName) {
    errors.push('Business name is required.');
  } else if (businessName.length > 120) {
    errors.push('Business name must not exceed 120 characters.');
  } else {
    sanitized.businessName = businessName;
  }

  // Phone (required, NZ/AU/international valid)
  const phone = typeof payload.phone === 'string' ? payload.phone.trim() : '';
  if (!phone) {
    errors.push('Phone number is required.');
  } else if (!isValidPhone(phone)) {
    errors.push('Please enter a valid phone number (e.g., NZ +64 21 000 0000 or AU +61 400 000 000).');
  } else {
    sanitized.phone = phone;
  }

  // Email (required, RFC valid)
  const email = typeof payload.email === 'string' ? payload.email.trim().toLowerCase() : '';
  if (!email) {
    errors.push('Email address is required.');
  } else if (!isValidEmail(email)) {
    errors.push('Please enter a valid email address.');
  } else {
    sanitized.email = email;
  }

  // Website (optional, max 200 chars)
  const website = typeof payload.website === 'string' ? payload.website.trim() : '';
  if (website && !isValidWebsite(website)) {
    errors.push('Please enter a valid company website URL (e.g. https://yourbusiness.co.nz).');
  } else {
    sanitized.website = website;
  }

  // Message / Primary Call Types (required, 1-2000 chars)
  const message = typeof payload.message === 'string' ? payload.message.trim() : '';
  if (!message) {
    errors.push('Please describe the kind of calls you receive most often.');
  } else if (message.length > 2000) {
    errors.push('Message must not exceed 2,000 characters.');
  } else {
    sanitized.message = message;
  }

  // Marketing consent (optional boolean)
  sanitized.marketingConsent = payload.marketingConsent === true || payload.marketingConsent === 'true' || payload.marketingConsent === 'on';

  // Metadata
  sanitized.submittedAt = new Date().toISOString();
  sanitized.userAgent = typeof payload.userAgent === 'string' ? payload.userAgent.slice(0, 300) : '';
  sanitized.sourcePage = typeof payload._page === 'string' ? payload._page.slice(0, 200) : '/';

  return {
    valid: errors.length === 0,
    errors,
    sanitized
  };
}

/**
 * Checks in-memory rate limiting for a client key (IP or identifier)
 */
function checkRateLimit(clientIp) {
  if (!clientIp) return true;
  const now = Date.now();
  const history = rateLimitMap.get(clientIp) || [];
  const validHistory = history.filter(ts => now - ts < RATE_LIMIT_WINDOW_MS);
  
  if (validHistory.length >= RATE_LIMIT_MAX_REQUESTS) {
    return false;
  }
  
  validHistory.push(now);
  rateLimitMap.set(clientIp, validHistory);
  return true;
}

/**
 * Handles a lead submission from any runtime adapter.
 * 
 * @param {object} payload Parsed request body
 * @param {object} env Environment variables (LEAD_WEBHOOK_URL, ADMIN_EMAIL, etc.)
 * @param {string} [clientIp] Client IP address for rate limiting
 * @param {object} [options] Options object { dryRun: boolean }
 * @returns {Promise<{ status: number, body: object }>}
 */
async function handleLead(payload, env = {}, clientIp = '', options = {}) {
  // 1. Rate limiting check
  if (clientIp && !checkRateLimit(clientIp)) {
    return {
      status: 429,
      body: {
        success: false,
        message: 'Too many demo requests submitted from this connection. Please wait 10 minutes or email us directly at admin@quiktalkai.com.',
        code: 'RATE_LIMITED'
      }
    };
  }

  // 2. Validate payload
  const validation = validateLead(payload);

  if (validation.isSpam) {
    // For bots hitting the honeypot, return 400 without revealing internal details
    return {
      status: 400,
      body: {
        success: false,
        message: 'Submission could not be processed.',
        code: 'SPAM_REJECTED'
      }
    };
  }

  if (!validation.valid) {
    return {
      status: 400,
      body: {
        success: false,
        message: 'Please review and correct the errors below.',
        errors: validation.errors,
        code: 'VALIDATION_FAILED'
      }
    };
  }

  const lead = validation.sanitized;

  // Check dry-run mode (?dryRun=1 or header X-Dry-Run: 1 or payload.dryRun)
  const isDryRun = options.dryRun === true || options.dryRun === '1' || payload.dryRun === true || payload.dryRun === '1';
  if (isDryRun) {
    console.log(`[LeadHandler] DRY-RUN lead validation passed: ${lead.businessName} (${lead.name} <${lead.email}>, ${lead.phone}). Skipping webhook/email.`);
    return {
      status: 200,
      body: {
        success: true,
        dryRun: true,
        message: '[DRY RUN] Lead payload validated successfully. Webhook dispatch skipped.',
        leadId: 'dry_run_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
      }
    };
  }

  // 3. Webhook dispatch (if configured)
  const webhookUrl = env.LEAD_WEBHOOK_URL || (typeof process !== 'undefined' && process.env ? process.env.LEAD_WEBHOOK_URL : null);
  if (webhookUrl && webhookUrl.trim() !== '') {
    try {
      if (typeof fetch !== 'undefined') {
        const response = await fetch(webhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event: 'lead.created',
            source: 'quiktalkai-website',
            lead: lead
          })
        });
        if (!response.ok) {
          console.warn(`[LeadHandler] Webhook responded with status ${response.status}`);
        }
      }
    } catch (err) {
      console.error('[LeadHandler] Webhook dispatch error:', err.message);
      // We do not fail the user submission if external webhook fails
    }
  } else {
    // In local development or when webhook is unconfigured, log lead capture safely
    console.log(`[LeadHandler] Lead received locally: ${lead.businessName} (${lead.name} <${lead.email}>, ${lead.phone})`);
  }

  // 4. Return successful structured response
  return {
    status: 200,
    body: {
      success: true,
      message: 'Demo request received! Our Auckland team will configure your custom voice agent and email you within 1 business day.',
      leadId: 'lead_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
    }
  };
}

// ES Module exports (Node ESM + Cloudflare Pages Functions)
export { validateLead, handleLead, isValidEmail, isValidPhone, isValidWebsite };
