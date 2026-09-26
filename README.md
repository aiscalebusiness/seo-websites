# SEO Websites — site rebuild

Static rebuild of 8 pages of [seowebsites.co.nz](https://seowebsites.co.nz) in the new dark / neon design.

| Page | Path |
|---|---|
| Home | `/` |
| SEO Auckland | `/seo-auckland/` |
| SEO Services Auckland | `/seo-services-auckland/` |
| Local SEO Services | `/local-seo-services/` |
| Instagram SEO | `/instagram-seo/` |
| TikTok SEO | `/tiktok-seo/` |
| About Us | `/about-us/` |
| Contact | `/contact/` |

## Structure

- `site/` — the built website, ready to deploy (upload this folder's contents to the web root).
- `build.py` — generates every page from shared header, footer and section templates. Edit copy here.
- `assets/` — stylesheet, JavaScript and images (copied into `site/assets` on build).

## Build and preview

```bash
python3 build.py
python3 -m http.server 4410 -d site
```

Then open http://localhost:4410.

## Before going live

- Hero dashboard figures on the homepage (+286%, 12.4K, $48K) are illustrative — replace with real case-study numbers or remove.
- The contact form posts to [FormSubmit](https://formsubmit.co), which forwards submissions to seowebsitesnz@gmail.com. The first submission triggers a one-time activation email to that inbox. Click the link in it, or later submissions won't be delivered. The destination is set by `EMAIL` / `FORM_ACTION` in `build.py`.
- `/testimonials/`, `/seo-audit/`, `/blog/` and `/seo-pricing-nz/` are linked but not part of this rebuild.
