# OpenSprint website

The site is plain HTML and CSS in `public/`, hosted on Cloudflare Pages. The contact form handler lives in `functions/api/contact.js`.

Preview locally (the contact form doesn't work in this preview):

```sh
python -m http.server 8000 -d public
```

See [CLAUDE.md](CLAUDE.md) for conventions, the checklist for adding a page, and hosting and DNS details.
