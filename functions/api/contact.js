// Cloudflare Pages Function: POST /api/contact
// Env vars (set in Cloudflare dashboard): TURNSTILE_SECRET, RESEND_API_KEY, MAIL_TO, MAIL_FROM

export async function onRequestPost({ request, env }) {
  const form = await request.formData();
  const field = (name, max) => String(form.get(name) ?? '').trim().slice(0, max);

  // Honeypot filled in: pretend success so bots learn nothing
  if (field('website', 200)) return redirect(request, '/thanks');

  const turnstile = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({
      secret: env.TURNSTILE_SECRET,
      response: field('cf-turnstile-response', 2048),
      remoteip: request.headers.get('CF-Connecting-IP') ?? '',
    }),
  });
  const check = await turnstile.json();
  if (!check.success) {
    const codes = (check['error-codes'] ?? []).join(', ') || 'unknown';
    console.error('Turnstile failed', codes);
    return fail(`The spam check failed. Please go back and try again. (${codes})`);
  }

  const name = field('name', 100).replace(/[\r\n]+/g, ' ');
  const email = field('email', 200);
  const company = field('company', 100);
  const message = field('message', 5000);
  if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return fail('Please fill in your name, a valid email address and a message.');
  }

  const sent = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.MAIL_FROM,
      to: env.MAIL_TO,
      reply_to: email,
      subject: `Website enquiry from ${name}`,
      text: `Name: ${name}\nEmail: ${email}\nCompany: ${company || '-'}\n\n${message}`,
    }),
  });
  if (!sent.ok) {
    console.error('Resend error', sent.status, await sent.text());
    return fail('Your message could not be sent right now. Please email us directly instead.');
  }

  return redirect(request, '/thanks');
}

function redirect(request, path) {
  return Response.redirect(new URL(path, request.url), 303);
}

function fail(text) {
  return new Response(
    `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Message not sent</title><link rel="stylesheet" href="/css/style.css"><main class="hero"><div class="wrap"><h1>Message not sent.</h1><p class="lede">${text}</p><div class="cta-row"><a class="btn" href="/#contact">Back to the form</a></div></div></main>`,
    { status: 400, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
  );
}
