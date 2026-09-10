/**
 * functions/api/health.js
 * Cloudflare Pages Function health check endpoint (QTK-025)
 */

export async function onRequestGet() {
  return new Response(JSON.stringify({
    status: 'healthy',
    service: 'quiktalkai',
    timestamp: new Date().toISOString()
  }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store'
    }
  });
}
