# OpenSprint website

Static site (plain HTML/CSS) hosted on Cloudflare Pages. The only server code is the contact form handler in `functions/api/contact.js`.

## Preview locally

```sh
python -m http.server 8000
```

Then open http://localhost:8000. This preview doesn't run the contact form; that only works once the site is deployed to Cloudflare Pages, or locally through `npx wrangler pages dev .` if Node is installed.

## Deploy (Cloudflare Pages)

1. Push this folder to a GitHub repository.
2. In Cloudflare, go to Workers & Pages, create a Pages project and connect the repository. Set the build command to none and the output directory to `/`.
3. Add these environment variables to the project (mark the keys as secrets):
   - `TURNSTILE_SECRET`: the Turnstile widget's secret key
   - `RESEND_API_KEY`: a Resend API key
   - `MAIL_TO`: the inbox that receives enquiries
   - `MAIL_FROM`: for example `OpenSprint Website <website@send.opensprint.com.au>`
4. Add the custom domain `opensprint.com.au` (and `www`) to the project.

## Contact form

- Spam protection comes from Cloudflare Turnstile plus a hidden honeypot field. Replace the test site key in `index.html` with the real one.
- Email is sent through Resend. Verify a sending subdomain (for example `send.opensprint.com.au`) so that the website's mail doesn't affect the main domain's SPF/DMARC.
