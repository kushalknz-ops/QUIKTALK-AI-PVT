/**
 * functions/api/lead.js
 * Cloudflare Pages Function Adapter for Quiktalk AI Lead Processing (~30 lines)
 * Thin adapter: Delegates 100% of validation and logic to lib/leadHandler.js.
 */

import { handleLead } from '../../lib/leadHandler.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const clientIp = request.headers.get('CF-Connecting-IP') || request.headers.get('x-forwarded-for') || '';
  let payload = {};

  try {
    const contentType = request.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      payload = await request.json();
    } else if (contentType.includes('application/x-www-form-urlencoded') || contentType.includes('multipart/form-data')) {
      const formData = await request.formData();
      payload = Object.fromEntries(formData.entries());
    } else {
      payload = await request.json().catch(() => ({}));
    }
  } catch (err) {
    return new Response(JSON.stringify({ success: false, message: 'Malformed request payload.' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const url = new URL(request.url);
  const isDryRun = url.searchParams.get('dryRun') === '1' || request.headers.get('x-dry-run') === '1';

  // Delegate directly to shared single source of truth
  const result = await handleLead(payload, env, clientIp, { dryRun: isDryRun });

  return new Response(JSON.stringify(result.body), {
    status: result.status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store'
    }
  });
}
