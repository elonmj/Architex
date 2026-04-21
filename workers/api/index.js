/**
 * Architex API — Cloudflare Worker
 *
 * Routes:
 *   GET  /health          → status check
 *   ANY  /api/*           → proxy to HF Space (set HF_SPACE_URL in wrangler.toml [vars])
 *   POST /api/ifc/mesh    → (future) trigger mesh job on HF Space
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // Health check
    if (url.pathname === "/health") {
      return json({ status: "ok", service: "architex-api", version: "0.1" });
    }

    // Proxy to HF Space
    if (url.pathname.startsWith("/api/") && env.HF_SPACE_URL) {
      const targetPath = url.pathname.replace("/api", "");
      const target = new URL(targetPath + url.search, env.HF_SPACE_URL);

      const proxyReq = new Request(target.toString(), {
        method: request.method,
        headers: request.headers,
        body: ["GET", "HEAD"].includes(request.method) ? undefined : request.body,
      });

      try {
        const res = await fetch(proxyReq);
        const newRes = new Response(res.body, res);
        Object.entries(CORS_HEADERS).forEach(([k, v]) => newRes.headers.set(k, v));
        return newRes;
      } catch (err) {
        return json({ error: "Upstream HF Space unreachable", detail: String(err) }, 502);
      }
    }

    // Default
    return json({ service: "Architex API", endpoints: ["/health", "/api/*"] });
  },
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS },
  });
}
