/**
 * functions/api/csp-report.js
 * Receives CSP violation reports (report-uri target in _headers). Logs and returns 204.
 */

export async function onRequestPost(context) {
  try {
    const report = await context.request.json().catch(() => null);
    if (report) {
      console.log('[CSP-REPORT]', JSON.stringify(report['csp-report'] || report).slice(0, 2000));
    }
  } catch {
    // ignore malformed reports
  }
  return new Response(null, { status: 204 });
}
