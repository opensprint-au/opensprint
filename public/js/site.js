// Site-wide script, loaded with defer on every page

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Highlight the current page in the main nav
const here = location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
document.querySelectorAll('.nav-links a').forEach((a) => {
  if (a.getAttribute('href') === here) a.setAttribute('aria-current', 'page');
});

// Price calculator (pricing page)
const calc = document.querySelector('[data-calc]');
if (calc) {
  const range = calc.querySelector('[data-users-range]');
  const number = calc.querySelector('[data-users-number]');
  const total = calc.querySelector('[data-total]');
  const detail = calc.querySelector('[data-detail]');
  const quote = calc.querySelector('[data-quote]');
  const aud = new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 });

  const update = () => {
    const plan = calc.querySelector('input[name="plan"]:checked');
    const users = Math.max(1, Math.min(500, parseInt(number.value, 10) || 1));
    const price = Number(plan.dataset.price);
    const monthly = users * price;
    total.textContent = aud.format(monthly);
    detail.textContent = `${users} ${users === 1 ? 'user' : 'users'} × ${aud.format(price)} on ${plan.dataset.name}. ${aud.format(monthly * 1.1)} a month including GST.`;
    quote.href = `/contact?plan=${plan.value}&users=${users}`;
  };

  range.addEventListener('input', () => { number.value = range.value; update(); });
  number.addEventListener('input', () => {
    const n = parseInt(number.value, 10);
    if (n) range.value = Math.min(n, Number(range.max));
    update();
  });
  calc.addEventListener('change', update);
  update();
}

// Prefill the quote form from ?plan=&users= (links from the pricing page)
const quoteForm = document.querySelector('[data-quote-form]');
if (quoteForm) {
  const params = new URLSearchParams(location.search);
  const plan = params.get('plan');
  const users = parseInt(params.get('users'), 10);
  if (plan && quoteForm.plan.querySelector(`option[value="${CSS.escape(plan)}"]`)) quoteForm.plan.value = plan;
  if (users > 0 && users <= 10000) quoteForm.users.value = users;
}
