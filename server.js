/**
 * server.js
 * Quiktalk AI Local Development Server & Parity Environment
 * Thin adapter: Serves static files, enforces _headers rules locally, routes /api/lead to lib/leadHandler.js.
 * Zero external npm dependencies required.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { handleLead } = require('./lib/leadHandler.js');

const PORT = process.env.PORT || 3000;
const ROOT_DIR = __dirname;

// MIME types dictionary
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.mp3': 'audio/mpeg'
};

/**
 * Parses _headers file and returns an array of { pattern, regex, headers }
 */
function parseHeadersFile() {
  const headersPath = path.join(ROOT_DIR, '_headers');
  if (!fs.existsSync(headersPath)) {
    console.warn('[Header-Parity] Warning: _headers file not found. Running without custom headers.');
    return [];
  }

  const content = fs.readFileSync(headersPath, 'utf8');
  const lines = content.split(/\r?\n/);
  const rules = [];
  let currentRule = null;

  for (let line of lines) {
    line = line.trim();
    if (!line || line.startsWith('#')) continue;

    // Check if line is a route pattern (e.g. /*, /*.html, /assets/*)
    if (line.startsWith('/') || line.startsWith('/*')) {
      if (currentRule) {
        rules.push(currentRule);
      }
      // Convert glob pattern to RegExp
      const regexPattern = '^' + line
        .replace(/\./g, '\\.')
        .replace(/\*/g, '.*') + '$';
      currentRule = {
        pattern: line,
        regex: new RegExp(regexPattern),
        headers: {}
      };
    } else if (currentRule && line.includes(':')) {
      const colonIdx = line.indexOf(':');
      const key = line.slice(0, colonIdx).trim();
      const val = line.slice(colonIdx + 1).trim();
      currentRule.headers[key] = val;
    }
  }

  if (currentRule) {
    rules.push(currentRule);
  }

  return rules;
}

const headerRules = parseHeadersFile();

console.log('\n======================================================');
console.log(' Quiktalk AI Local Server Parity & Security Engine');
console.log('======================================================');
console.log('[Header-Parity] Loaded rules from _headers:');
headerRules.forEach(r => {
  console.log(`  Pattern: ${r.pattern}`);
  Object.entries(r.headers).forEach(([k, v]) => {
    console.log(`    ${k}: ${v.length > 70 ? v.slice(0, 67) + '...' : v}`);
  });
});
console.log('======================================================\n');

/**
 * Applies matched headers to ServerResponse
 */
function applyHeaders(reqPath, res) {
  for (const rule of headerRules) {
    if (rule.regex.test(reqPath)) {
      for (const [key, val] of Object.entries(rule.headers)) {
        res.setHeader(key, val);
      }
    }
  }
}

/**
 * Collects stream body from IncomingMessage
 */
function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1e6) { // 1MB limit
        req.destroy();
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => resolve(body));
    req.on('error', err => reject(err));
  });
}

const server = http.createServer(async (req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = parsedUrl.pathname;

  // Apply security & parity headers to all responses
  applyHeaders(pathname, res);

  // 1. API: /api/lead
  if (pathname === '/api/lead' && req.method === 'POST') {
    try {
      const rawBody = await readRequestBody(req);
      let payload = {};
      const contentType = req.headers['content-type'] || '';

      if (contentType.includes('application/json')) {
        payload = JSON.parse(rawBody || '{}');
      } else if (contentType.includes('application/x-www-form-urlencoded')) {
        const params = new URLSearchParams(rawBody);
        payload = Object.fromEntries(params.entries());
      } else {
        try {
          payload = JSON.parse(rawBody || '{}');
        } catch {
          const params = new URLSearchParams(rawBody);
          payload = Object.fromEntries(params.entries());
        }
      }

      const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '';
      const isDryRun = parsedUrl.searchParams.get('dryRun') === '1' || req.headers['x-dry-run'] === '1';
      const result = await handleLead(payload, process.env, clientIp, { dryRun: isDryRun });

      res.writeHead(result.status, {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      });
      res.end(JSON.stringify(result.body));
      return;
    } catch (err) {
      console.error('[API /api/lead] Error:', err);
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Invalid request body.' }));
      return;
    }
  }

  // 2. API: /api/csp-report
  if (pathname === '/api/csp-report' && req.method === 'POST') {
    const rawBody = await readRequestBody(req);
    try {
      const report = JSON.parse(rawBody);
      console.log('[CSP-REPORT Violation]:', JSON.stringify(report['csp-report'] || report, null, 2));
    } catch {
      console.log('[CSP-REPORT Violation]:', rawBody);
    }
    res.writeHead(204);
    res.end();
    return;
  }

  // 3. API: /api/health
  if (pathname === '/api/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
    res.end(JSON.stringify({
      status: 'ok',
      service: 'quiktalkai-local',
      timestamp: new Date().toISOString(),
      uptimeSeconds: Math.floor(process.uptime())
    }));
    return;
  }

  // 4. Static file resolution
  // Handle root
  if (pathname === '/') {
    pathname = '/index.html';
  }

  let filePath = path.join(ROOT_DIR, pathname);

  // Clean URL resolution: /privacy-policy -> /privacy-policy.html
  if (!fs.existsSync(filePath)) {
    const htmlCandidate = filePath + '.html';
    if (fs.existsSync(htmlCandidate)) {
      filePath = htmlCandidate;
      pathname = pathname + '.html';
    }
  }

  // Check if target exists and is a file
  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // 404 handler
      const notFoundPath = path.join(ROOT_DIR, '404.html');
      if (fs.existsSync(notFoundPath)) {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        fs.createReadStream(notFoundPath).pipe(res);
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('404 Not Found - Quiktalk AI');
      }
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Stream the file
    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`[Server] Quiktalk AI running at http://localhost:${PORT}/`);
    console.log(`[Server] Press Ctrl+C to stop.\n`);
  });
}

module.exports = { server, parseHeadersFile };
