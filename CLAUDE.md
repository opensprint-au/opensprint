# OpenSprint website

Marketing site for OpenSprint, a managed IT services company in Sydney. Live at https://www.opensprint.com.au.

## Principles

- Keep it lean: plain HTML and CSS with no build step, no framework and no npm dependencies. The owner chose this over a static site generator.
- Write Australian English (en-AU), in plain language.
- Branding isn't finished yet. Keep colours in the CSS variables in `public/css/style.css` so they can be swapped in one place.

## Layout

- `public/`: everything that gets published. Cloudflare Pages serves this folder as the site.
- `public/_headers`: security headers, including the CSP. When adding a third-party script, frame or image, update the CSP or it will be blocked.
- `functions/api/contact.js`: the contact form handler (a Cloudflare Pages Function). It must stay outside `public/`.

## Adding a page

1. Copy `public/privacy.html` as a starting point.
2. Keep the `<!-- header -->…<!-- /header -->` and `<!-- footer -->…<!-- /footer -->` blocks identical on every page. Change them across all pages together; the markers exist to make that easy.
3. Set `<title>` (format: "Page name | OpenSprint"), the description, the canonical URL and the `og:` tags.
4. Use extensionless links (`/about`, not `/about.html`). Pages serves `about.html` at `/about`.
5. Add the URL to `public/sitemap.xml`, and add it to the header nav if it belongs there.
6. Inline `<script>` and `style=""` attributes are blocked by the CSP. Use `public/js/site.js` and `public/css/style.css` instead.

## Hosting and deploy

- Cloudflare Pages project `opensprint`, deployed from the `main` branch of github.com/natewhi/opensprint. Build command: none. Output directory: `public`.
- Pushing to `main` deploys to production. Pushing any other branch creates a preview URL.
- Environment variables (set in Cloudflare): `TURNSTILE_SECRET`, `RESEND_API_KEY`, `MAIL_TO`, `MAIL_FROM`. Changes to them only take effect after a redeploy.
- Preview locally with `python -m http.server 8000 -d public`. The form doesn't work locally.

## DNS (managed at Namecheap, not Cloudflare)

- `www` is a CNAME to `opensprint.pages.dev`. The bare domain uses a Namecheap URL redirect to www, which works over HTTP only.
- The MX, SPF, `MS=` TXT and `autodiscover` records are Microsoft 365 email. Never change them.
- `send.opensprint.com.au` is the Resend sending domain used by the contact form.
