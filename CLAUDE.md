# OpenSprint website

Marketing site for OpenSprint, a managed IT services company in Sydney. Live at https://www.opensprint.com.au.

## Principles

- Keep it lean: plain HTML and CSS with no build step, no framework and no npm dependencies. The owner chose this over a static site generator.
- Write Australian English (en-AU), in plain language.
- Audience: businesses with 5+ staff that run purely on Microsoft 365, with no on-site servers. The key selling point is devices that arrive registered to the client and set themselves up on first sign-in (Intune, Teams, OneDrive). Don't pitch on-site server support; server-to-cloud moves are a quoted project.
- Fonts are self-hosted in `public/fonts/` (Inter, OFL) because the CSP only allows `'self'`.
- Logo: `public/img/logo.svg` (black) and `logo-white.svg` (footer), plus `public/favicon.svg`. They're drawn from Inter's outlines by `tools/make_logo.py`: "Open" high, "Sprint" stepped down, and the right leg of the "n" extended to the bottom of the S. To regenerate: `pip install fonttools brotli`, then `python tools/make_logo.py public/fonts/inter-latin.woff2 public/img` and move `favicon.svg` up to `public/`.
- Branding isn't finished yet. Keep colours in the CSS variables in `public/css/style.css` so they can be swapped in one place.
- Look: white, corporate and light-only (no dark mode), with black pill buttons and the blue `--brand` colour used sparingly. Graphite (`--graphite`) is for secondary areas (devices band, footer, CTA). Glass effects only on the header and hero card, which sits on a colour wash so the blur shows.

## Layout

- `public/`: everything that gets published. Cloudflare Pages serves this folder as the site.
- `public/_headers`: security headers, including the CSP. When adding a third-party script, frame or image, update the CSP or it will be blocked.
- Plans: Business ($180) and Complete ($240), per user per month ex GST, including Microsoft 365 Business Premium, with a 5-user minimum. Prices appear in several places. When changing them, update all of these: `index.html` (hero line and pricing teaser), `pricing.html` (meta description, plan cards, calculator `data-price` and `data-min-users`, FAQ), `contact.html` (plan dropdown) and the plan list in `functions/api/contact.js`.
- `functions/api/contact.js`: the contact form handler (a Cloudflare Pages Function). It must stay outside `public/`.

## Adding a page

1. Copy `public/privacy.html` as a starting point.
2. Keep the `<!-- header -->…<!-- /header -->` and `<!-- footer -->…<!-- /footer -->` blocks identical on every page. Change them across all pages together; the markers exist to make that easy.
3. Set `<title>` (format: "Page name | OpenSprint"), the description, the canonical URL and the `og:` tags.
4. Use extensionless links (`/about`, not `/about.html`). Pages serves `about.html` at `/about`.
5. Add the URL to `public/sitemap.xml` with a `<lastmod>` date (update that date whenever the page changes), and add it to the header nav if it belongs there.
6. Inline `<script>` and `style=""` attributes are blocked by the CSP. Use `public/js/site.js` and `public/css/style.css` instead.

## Hosting and deploy

- Cloudflare Pages project `opensprint`, deployed from the `main` branch of github.com/opensprint-au/opensprint (GitHub org `opensprint-au`). Build command: none. Output directory: `public`.
- Pushing to `main` deploys to production. Pushing any other branch creates a preview URL.
- Environment variables (set in Cloudflare): `TURNSTILE_SECRET`, `RESEND_API_KEY`, `MAIL_TO`, `MAIL_FROM`. Changes to them only take effect after a redeploy.
- Preview locally with `python -m http.server 8000 -d public`. The form doesn't work locally.

## DNS (managed at Namecheap, not Cloudflare)

- `www` is a CNAME to `opensprint.pages.dev`. The bare domain uses a Namecheap URL redirect to www, which works over HTTP only.
- The MX, SPF, `MS=` TXT and `autodiscover` records are Microsoft 365 email. Never change them.
- `send.opensprint.com.au` is the Resend sending domain used by the contact form.
