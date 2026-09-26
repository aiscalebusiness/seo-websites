#!/usr/bin/env python3
"""Builds the static site into ./site. Run: python3 build.py"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"
DOMAIN = "https://seowebsites.co.nz"
PHONE, PHONE_TEL = "020 4059 1357", "+64204059 1357".replace(" ", "")
EMAIL = "seowebsitesnz@gmail.com"
FORM_ACTION = f"https://formsubmit.co/{EMAIL}"  # FormSubmit forwards submissions to EMAIL

# ---------------------------------------------------------------- icons
def ico(name, cls=""):
    p = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "chev": '<path d="M6 9l6 6 6-6"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
        "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
        "ads": '<path d="M10.5 4.5l-7 12a2.5 2.5 0 004.3 2.5l7-12a2.5 2.5 0 00-4.3-2.5z"/><path d="M13.5 7l6.8 11.8a2.5 2.5 0 01-4.3 2.5L11 12.5"/>',
        "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19a5.5 5.5 0 0111 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A4.5 4.5 0 0121 18.5"/>',
        "doc": '<path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
        "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>',
        "trophy": '<path d="M8 4h8v5a4 4 0 01-8 0z"/><path d="M8 6H5a3 3 0 003 4M16 6h3a3 3 0 01-3 4M12 13v4M8 21h8M9 17h6"/>',
        "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
        "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.8-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1.1-1.5 1.7 1.7 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.8 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1.1 1.7 1.7 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.8.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.8V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/>',
        "bars": '<path d="M5 20v-6M10 20V9M15 20v-9M20 20V4"/>',
        "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
        "bag": '<path d="M6 7h12l-1 13H7z"/><path d="M9 7a3 3 0 016 0"/>',
        "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
        "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
        "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
        "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "pin": '<path d="M12 21s-7-6-7-12a7 7 0 0114 0c0 6-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
        "link": '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
        "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "funnel": '<path d="M3 4h18l-7 8v7l-4 2v-9z"/>',
        "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        "hash": '<path d="M5 9h14M5 15h14M10 3L8 21M16 3l-2 18"/>',
        "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/>',
        "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
        "music": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
        "play": '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M10 9l5 3-5 3z"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
        "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
        "report": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 17v-3M12 17v-6M16 17V8"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
        "chat": '<path d="M21 12a8 8 0 01-11.6 7.1L4 20l1-4.6A8 8 0 1121 12z"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "badge": '<path d="M12 2l2.4 2.1 3.1-.4.9 3 2.7 1.6-1 3 1 3-2.7 1.6-.9 3-3.1-.4L12 22l-2.4-2.1-3.1.4-.9-3-2.7-1.6 1-3-1-3 2.7-1.6.9-3 3.1.4z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    }[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def gico(name):
    """Gradient-stroked large icon (service cards)."""
    return ico(name).replace('stroke="currentColor"', 'stroke="url(#g1)"').replace('stroke-width="1.8"', 'stroke-width="1.9"')

GOOGLE_G = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9 3.5l6.7-6.7C35.6 2.4 30.2 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.8 6C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.4-4.6 7l7.4 5.8c4.3-4 6.9-9.9 6.9-17.3z"/><path fill="#FBBC05" d="M10.5 28.7c-.5-1.4-.8-3-.8-4.7s.3-3.2.8-4.7l-7.8-6C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.8c-2.1 1.4-4.8 2.3-8.5 2.3-6.3 0-11.6-4.1-13.5-9.8l-7.8 6C6.6 42.6 14.6 48 24 48z"/></svg>'

SVG_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset=".55" stop-color="#3b82f6"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
<linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b82f6" stop-opacity=".55"/><stop offset="1" stop-color="#3b82f6" stop-opacity="0"/></linearGradient>
<linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2d6b"/><stop offset="1" stop-color="#050b20"/></linearGradient>
</defs></svg>'''

AC = ' aria-current="page"'
# ---------------------------------------------------------------- navigation
SERVICES = [
    ("/seo-services-auckland/", "SEO Services Auckland"),
    ("/local-seo-services/", "Local SEO"),
    ("/instagram-seo/", "Instagram SEO"),
    ("/tiktok-seo/", "TikTok SEO"),
]
NAV = [("/", "Home"), ("/seo-auckland/", "SEO Auckland"), ("SERVICES", "Services"),
       ("/local-seo-services/", "Local SEO"), ("/about-us/", "About Us"), ("/contact/", "Contact")]

def header(cur):
    items = []
    for href, label in NAV:
        if href == "SERVICES":
            sub = "".join(f'<li><a href="{h}"{AC if h == cur else ""}>{l}</a></li>' for h, l in SERVICES)
            active = " has-current" if any(h == cur for h, _ in SERVICES) and cur not in [n[0] for n in NAV] else ""
            items.append(f'<li class="has-drop{active}"><button type="button" aria-expanded="false" aria-haspopup="true">Services {ico("chev")}</button><ul class="dropdown">{sub}</ul></li>')
        else:
            ac = ' aria-current="page"' if href == cur else ""
            items.append(f'<li><a href="{href}"{ac}>{label}</a></li>')
    items.append(f'<li class="mobile-cta"><a class="btn btn-primary" href="/contact/">Contact Us {ico("arrow")}</a></li>')
    return f'''<header class="site-header"><div class="wrap nav">
  <a class="logo" href="/" aria-label="SEO Websites home"><b><span>SEO</span> Websites</b><small>GROW · RANK · CONVERT</small></a>
  <ul class="menu" id="menu">{"".join(items)}</ul>
  <a class="btn btn-primary btn-sm" href="/contact/">Contact Us {ico("arrow")}</a>
  <button class="burger" type="button" aria-controls="menu" aria-expanded="false" aria-label="Open menu">{ico("menu")}</button>
</div></header>'''

FOOTER = f'''<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div><a class="logo" href="/"><b><span>SEO</span> Websites</b><small>GROW · RANK · CONVERT</small></a>
      <p>A boutique Auckland-based SEO and digital marketing agency. We eat, sleep and breathe online marketing, and we monitor our clients' marketing progress every day.</p></div>
    <div><h4>Quick Links</h4><ul class="foot-links">
      <li><a href="/">Home</a></li><li><a href="/seo-auckland/">SEO Auckland</a></li>
      <li><a href="/about-us/">About Us</a></li><li><a href="/seo-services-auckland/">SEO Services</a></li>
      <li><a href="/contact/">Contact</a></li><li><a href="/local-seo-services/">Local SEO</a></li>
      <li><a href="/testimonials/">Testimonials</a></li><li><a href="/instagram-seo/">Instagram SEO</a></li>
      <li><a href="/seo-audit/">Website Audits</a></li><li><a href="/tiktok-seo/">TikTok SEO</a></li>
      <li><a href="/blog/">Blog</a></li><li><a href="/seo-pricing-nz/">SEO Pricing NZ</a></li>
    </ul></div>
    <div><h4>Contact Us</h4><ul class="foot-contact">
      <li>{ico("phone")}<a href="tel:{PHONE_TEL}">{PHONE}</a></li>
      <li>{ico("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>{ico("pin")}Auckland, New Zealand</li>
    </ul></div>
  </div>
  <div class="foot-bar"><span>© 2026 SEO Websites. All rights reserved.</span><span>Auckland's SEO &amp; AI Digital Marketing Agency</span></div>
</div></footer>'''

SKYLINE = '''<svg class="skyline" viewBox="0 0 760 300" preserveAspectRatio="xMaxYMax meet" aria-hidden="true">
<path fill="#0b1740" d="M0 300V230l40-12 50 6 60-20 70 10 60-28 80 18 70-14 90 12 80-8 70 10 90-6v132z" opacity=".8"/>
<g fill="url(#gSky)" stroke="rgba(99,145,255,.35)" stroke-width="1">
<rect x="250" y="170" width="38" height="130"/><rect x="292" y="140" width="30" height="160"/><rect x="326" y="186" width="44" height="114"/>
<rect x="380" y="120" width="34" height="180"/><rect x="418" y="150" width="46" height="150"/><rect x="530" y="160" width="40" height="140"/>
<rect x="574" y="132" width="32" height="168"/><rect x="610" y="178" width="50" height="122"/><rect x="664" y="150" width="36" height="150"/><rect x="704" y="190" width="56" height="110"/>
<rect x="190" y="200" width="54" height="100"/><rect x="140" y="222" width="46" height="78"/>
<path d="M494 300V96h-6l4-10h-3l3-8h8l3 8h-3l4 10h-6v204z"/><path d="M491 86h14l-7-66z"/>
</g>
<circle cx="498" cy="88" r="10" fill="#1d3a8a" stroke="#60a5fa"/><path d="M498 20V2" stroke="#e2e8f0" stroke-width="2"/>
<g fill="#fde68a" opacity=".55"><rect x="258" y="182" width="3" height="4"/><rect x="270" y="200" width="3" height="4"/><rect x="300" y="160" width="3" height="4"/><rect x="310" y="190" width="3" height="4"/><rect x="390" y="140" width="3" height="4"/><rect x="400" y="170" width="3" height="4"/><rect x="430" y="170" width="3" height="4"/><rect x="448" y="200" width="3" height="4"/><rect x="540" y="180" width="3" height="4"/><rect x="584" y="150" width="3" height="4"/><rect x="620" y="200" width="3" height="4"/><rect x="676" y="170" width="3" height="4"/><rect x="716" y="210" width="3" height="4"/></g>
<g fill="#60a5fa" opacity=".6"><rect x="340" y="200" width="3" height="4"/><rect x="590" y="190" width="3" height="4"/><rect x="200" y="215" width="3" height="4"/><rect x="646" y="220" width="3" height="4"/></g>
</svg>'''

def cta(title="Ready to Grow Your Business?", text="Let's discuss how SEO, web design, Google Ads and AI-driven marketing can help you get more visibility, more traffic and more customers."):
    return f'''<section class="cta"><div class="wrap">
  <h2 class="reveal">{title}</h2><p class="reveal">{text}</p>
  <div class="btn-row reveal"><a class="btn btn-primary" href="/contact/">Book a Strategy Call {ico("arrow")}</a><a class="btn btn-ghost" href="/seo-audit/">{ico("bars")} Get a Website Audit</a></div>
</div><span class="dash-note">Auckland based<br>Results focused</span>{SKYLINE}</section>'''

# ---------------------------------------------------------------- shared blocks
SERVICE_CARDS = [
    ("search", "SEO", "While SEO may not be a quick fix for sales and leads, it is a long-term, cost-effective marketing strategy that requires ongoing optimisation.", "/seo-services-auckland/"),
    ("monitor", "Web Design", "Our websites get you off to a flying start. We build websites designed to rank higher in the Google search results.", "/contact/"),
    ("ads", "Google Ads", "Google Ads (Pay Per Click) is your instant solution for driving traffic, often used alongside a Search Engine Optimisation plan.", "/contact/"),
    ("users", "Social Media", "Cost-effective social media advertising. We specialise in Facebook, Instagram, LinkedIn and YouTube advertising.", "/instagram-seo/"),
    ("doc", "Audits", "Has the number of visitors to your website dropped? Our audits identify and remedy your loss of traffic.", "/seo-audit/"),
    ("cap", "Training", "Online training sessions over Zoom and Skype for all our services, including SEO, Google Ads and social media marketing.", "/contact/"),
]

def services_grid():
    cards = "".join(f'''<article class="card svc reveal"><div class="svc-ico">{gico(i)}</div><h3>{t}</h3><p>{d}</p><a class="link-arrow" href="{h}">Learn More {ico("arrow")}</a></article>''' for i, t, d, h in SERVICE_CARDS)
    return f'<div class="grid g-6">{cards}</div>'

WHY = [
    ("trophy", "First-Page Google Results", "All our clients are on the first page of Google."),
    ("users", "Boutique Agency Attention", "More focused attention on each client's industry and niche."),
    ("doc", "No Long-Term Contracts", "We're confident in delivering measurable results, so we don't lock you in."),
    ("heart", "100% Client Retention", "Our 100% client retention speaks volumes."),
    ("gear", "Technical SEO Expertise", "Site speed, crawlability, indexation and architecture handled properly."),
    ("bars", "Data-Driven Reporting", "Ongoing analytics and reporting so you can see your growth."),
]

def why_grid(items=WHY):
    return '<div class="grid g-6 why-grid">' + "".join(
        f'<div class="why reveal"><div class="ring-ico">{ico(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items) + "</div>"

CLIENTS = [("pacific-fuel.png", "Pacific Fuel Solutions"), ("marina-specialists.png", "Marina Specialists"),
           ("frontier-pools.png", "Frontier Pools"), ("extreme-global.png", "Extreme Global"),
           ("equal-exes.png", "Equal Exes"), ("joint-sup.png", "Joint Supplements NZ"),
           ("katarzyna-mackenzie.png", "Katarzyna Mackenzie"), ("gf-flow.jpeg", "Guaranteed Flow Systems"),
           ("one-day-video.png", "One Day Video"), ("auckland-plastic-surgical.png", "Auckland Plastic Surgical Centre"),
           ("shafer-design.jpeg", "Shafer Design"), ("operation-restore-hope.png", "Operation Restore Hope"),
           ("humphries-associates.png", "Humphries Associates")]

def logos(title="Trusted by Businesses Across New Zealand", sub="We work with ambitious businesses of all sizes, from local companies to growing national brands."):
    imgs = "".join(f'<span><img src="/assets/img/clients/{f}" alt="{a}" loading="lazy"></span>' for f, a in CLIENTS)
    return f'''<section class="sec-tight"><div class="wrap"><div class="sec-head reveal"><h2>{title}</h2><p>{sub}</p></div><div class="logos reveal">{imgs}</div></div></section>'''

TESTI_TEXT = "Clinton has completely transformed our online presence. Our website is now experiencing unprecedented levels of traffic resulting in a huge increase in the number of viable leads. We have no hesitation in recommending SEO Websites!"

def testimonial(eyebrow="Client Testimonial", title="What Our Clients Say", text=TESTI_TEXT):
    return f'''<section class="sec testi-band"><div class="wrap testi-grid">
  <div class="reveal"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p class="muted">We're proud to build long-term relationships with businesses who trust us to grow their online presence.</p><a class="link-arrow" href="/testimonials/">Read more testimonials {ico("arrow")}</a></div>
  <figure class="testi reveal" style="margin:0">
    <div class="testi-who"><img src="/assets/img/clare.jpeg" alt="Clare Chambers" width="110" height="110" loading="lazy"><b>Clare Chambers</b><small>Project Manager</small></div>
    <div><blockquote><p>{text}</p></blockquote>
      <div class="testi-foot"><span class="stars" aria-label="5 out of 5 stars">★★★★★</span><span class="badge">{ico("shield")} Client Review</span></div></div>
  </figure>
</div></section>'''

CERTS = [("c1.png", "Semrush"), ("c2.png", "Google Ads"), ("c3.png", "Google Data Studio"), ("c4.png", "Google Analytics"), ("c5.png", "Google Shopping")]

def certs(title="Our Certifications"):
    c = "".join(f'<span><img src="/assets/img/certs/{f}" alt="{a}" loading="lazy"></span>' for f, a in CERTS)
    return f'<section class="sec-tight"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Tools &amp; Platforms</span><h2>{title}</h2></div><div class="certs reveal">{c}</div></div></section>'

def page_hero(crumb, eyebrow, h1, lead, side, ctas=None):
    ctas = ctas or f'<a class="btn btn-primary" href="/contact/">Book a Strategy Call {ico("arrow")}</a><a class="btn btn-ghost" href="/seo-audit/">{ico("bars")} Get a Free SEO Audit</a>'
    return f'''<section class="hero page-hero"><div class="wrap hero-grid">
  <div><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>{crumb}</span></nav>
    <span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p><div class="btn-row">{ctas}</div></div>
  <div class="reveal">{side}</div>
</div></section>'''

def orb(icon, title, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="orb-card"><div class="big-ico">{ico(icon)}</div><h4>{title}</h4><ul class="check">{lis}</ul></div>'

def feature_cards(items, cols="g-4", numbered=False):
    out = []
    for n, (i, t, d) in enumerate(items, 1):
        head = f'<span class="num">{n:02d}</span>' if numbered else f'<div class="card-ico">{ico(i)}</div>'
        out.append(f'<article class="card reveal">{head}<h3>{t}</h3><p>{d}</p></article>')
    return f'<div class="grid {cols}">{"".join(out)}</div>'

# ---------------------------------------------------------------- pages
def home():
    chart = '''<svg viewBox="0 0 300 180" preserveAspectRatio="none" aria-hidden="true">
<g stroke="rgba(99,145,255,.15)"><path d="M0 30h300M0 70h300M0 110h300M0 150h300"/></g>
<g fill="rgba(59,130,246,.35)"><rect x="12" y="140" width="10" height="40"/><rect x="40" y="132" width="10" height="48"/><rect x="68" y="136" width="10" height="44"/><rect x="96" y="120" width="10" height="60"/><rect x="124" y="112" width="10" height="68"/><rect x="152" y="100" width="10" height="80"/><rect x="180" y="84" width="10" height="96"/><rect x="208" y="70" width="10" height="110"/><rect x="236" y="52" width="10" height="128"/><rect x="264" y="34" width="10" height="146"/></g>
<path d="M0 150L30 138 60 142 90 118 120 124 150 96 180 102 210 70 240 54 270 26 300 14V180H0z" fill="url(#gArea)"/>
<path d="M0 150L30 138 60 142 90 118 120 124 150 96 180 102 210 70 240 54 270 26 300 14" fill="none" stroke="#38bdf8" stroke-width="3" style="filter:drop-shadow(0 0 6px #38bdf8)"/>
<circle cx="270" cy="26" r="5" fill="#fff" stroke="#38bdf8" stroke-width="3"/></svg>'''
    dash = f'''<div class="dash" aria-label="Illustration of a search rankings dashboard">
  <div class="dash-main">
    <div class="dash-card"><h4>Search Rankings</h4><div class="dash-chart">{chart}<div class="dash-bubble"><b>+286%</b><small>Organic Traffic</small></div></div></div>
    <div class="dash-card side"><h4>AI Insights</h4><ul class="insights">
      <li>{ico("up")}Higher rankings</li><li>{ico("bars")}More traffic</li><li>{ico("users")}More leads</li><li>{ico("spark")}More revenue</li></ul></div>
  </div>
  <div class="dash-stats">
    <div class="stat-tile g">{GOOGLE_G}</div>
    <div class="stat-tile"><b>12.4K</b><small>Website Visitors</small><em>↑ +236%</em></div>
    <div class="stat-tile"><b>387</b><small>Leads</small><em>↑ +178%</em></div>
    <div class="stat-tile"><b>$48K</b><small>Sales Value</small><em>↑ +312%</em></div>
  </div>
  <span class="dash-note">Auckland<br>New Zealand</span>
</div>'''
    hero = f'''<section class="hero"><div class="wrap hero-grid">
  <div><span class="eyebrow">Auckland's AI SEO &amp; Digital Marketing Agency</span>
    <h1>Grow Your Business with <span class="grad-text">SEO, Web Design, Google Ads &amp; AI</span></h1>
    <p class="lead">SEO Websites is a boutique Auckland-based AI SEO agency helping businesses get found, generate targeted traffic and achieve long-term growth through SEO, web design, Google Ads and AI-driven digital marketing.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/contact/">Book a Strategy Call {ico("arrow")}</a><a class="btn btn-ghost" href="/seo-audit/">{ico("bars")} Get a Website Audit</a></div>
    <div class="hero-feats">
      <div class="hero-feat"><span class="ring-ico">{ico("search")}</span><div><b>More Visibility</b><small>Get found online</small></div></div>
      <div class="hero-feat"><span class="ring-ico">{ico("target")}</span><div><b>Targeted Traffic</b><small>Attract the right customers</small></div></div>
      <div class="hero-feat"><span class="ring-ico">{ico("bag")}</span><div><b>More Conversions</b><small>Turn clicks into clients</small></div></div>
    </div></div>
  {dash}
</div></section>'''
    approach = [
        ("pen", "On-Page Optimisation", "We fine-tune meta tags, headings, content structure, keyword placement and internal linking so each page is more relevant, more visible and a better experience for users."),
        ("link", "Off-Page Optimisation", "We build your website's authority through ethical link building, earning high-quality backlinks from reputable sites while keeping a natural, diverse link profile."),
        ("gear", "Technical SEO", "A comprehensive audit of your site architecture, speed and mobile-friendliness, so search engines can crawl and index your content effectively."),
        ("report", "Analytics & Reporting", "We track rankings, organic traffic and user behaviour, then make data-driven adjustments to maximise the effectiveness of your campaign."),
    ]
    body = f'''{hero}
<section class="sec sec-alt" id="services"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Our Services</span><h2>What We Do as an SEO Web Services Agency</h2><p>Everything your business needs to grow online, all in one place.</p></div>
  {services_grid()}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><h2>Why Work With SEO Web Marketing Experts</h2><p>A boutique AI SEO Auckland agency focused on real results, not empty promises.</p></div>
  {why_grid()}
</div></section>
{logos()}
{testimonial()}
<section class="sec"><div class="wrap split top">
  <div class="reveal"><span class="eyebrow">How We Work</span><h2>A Customised Strategy That Connects You With Customers</h2>
    <div class="prose"><p>Our AI SEO agency specialises in effective digital marketing campaigns that target specific search terms and enhance your website's visibility in search results. Our team of <a href="/local-seo-services/">local SEO services</a> experts conducts thorough keyword research, allowing us to create a customised strategy that connects you with potential customers through organic search engine rankings.</p>
    <p>Ultimately, our primary goal is to enhance your website's organic rankings, drive targeted traffic and increase conversions for your business. With our dedicated team of digital marketing specialists, we deliver strategies tailored to your unique needs.</p></div>
    <a class="btn btn-ghost" href="/seo-auckland/">Explore SEO Auckland {ico("arrow")}</a></div>
  {feature_cards(approach, "g-2")}
</div></section>
<section class="sec sec-alt" id="pricing"><div class="wrap">
  <div class="price-head reveal"><div><span class="eyebrow">SEO Pricing NZ</span><h2>How Much Does SEO Cost?</h2><p class="muted" style="margin:0">Flexible options to suit different business needs. All pricing in NZD.</p></div>
    <a class="link-arrow" href="/contact/">Talk to us about your goals {ico("arrow")}</a></div>
  <div class="grid g-2">
    <div class="price reveal"><span class="card-ico">{ico("bars")}</span><div><h3>Monthly SEO</h3><p class="muted">Ongoing SEO campaigns to grow your visibility, traffic and leads over time.</p>
      <div class="amt">$1,000 – $3,000 <small>/month</small></div>
      <ul class="check"><li>Keyword research &amp; strategy</li><li>On-page and technical SEO</li><li>Quality content &amp; link building</li><li>Detailed monthly reporting</li></ul></div></div>
    <div class="price reveal"><span class="card-ico">{ico("doc")}</span><div><h3>SEO Projects</h3><p class="muted">One-off projects for specific SEO needs such as audits, migrations or content.</p>
      <div class="amt">$5,000 – $20,000</div>
      <ul class="check"><li>In-depth website audit</li><li>Technical SEO improvements</li><li>Content optimisation</li><li>Custom project scope</li></ul></div></div>
  </div>
  <p class="price-note reveal">Typical SEO pricing in NZ is between $1,000 and $3,000 per month. Individual projects range from $5,000 to $20,000 depending on scope. For small businesses, hourly SEO rates usually fall between $150 and $250. <a href="/seo-pricing-nz/">See SEO pricing in detail</a>.</p>
</div></section>
{cta()}'''
    return dict(slug="", title="SEO Web Services, AI SEO Agency, SEO Websites",
                desc="Boost your presence with SEO Web Services, the leading AI SEO Agency in Auckland. Specialising in tailored SEO services for businesses.",
                body=body, crumb=None)

def seo_auckland():
    faqs = [
        ("Why is SEO a long-term investment?", "Because strong rankings take time to build, but once they're established, they deliver sustained traffic without ad spend."),
        ("How can SEO improve my online visibility?", "By optimising your website to match searcher intent and ensuring search engines can index and trust your content."),
        ("What makes a good SEO strategy in Auckland?", "A combination of local insights, technical precision, content relevance and ethical link building that suits the Auckland market."),
        ("Is SEO better than Google Ads?", "For long-term ROI, yes. SEO builds a foundation that Google Ads simply can't replicate over time."),
    ]
    includes = [
        ("key", "Keyword Research", "Uncover what your customers are really searching for."),
        ("pen", "On-Page SEO", "Optimise titles, content and structure for maximum relevancy."),
        ("gear", "Technical SEO", "Enhance site speed, crawlability and indexation."),
        ("link", "Link Building", "Earn high-quality backlinks that improve your search engine rankings."),
        ("doc", "Content Strategy", "Create helpful content that aligns with user intent and ranking signals."),
        ("pin", "Local SEO", "Boost your visibility for local searches and Google Maps results."),
    ]
    faq_html = "".join(f"<details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    side = orb("trend", "Full-service SEO for Auckland businesses", ["Keyword research &amp; on-page SEO", "Technical SEO &amp; site speed", "High-quality link building", "Local SEO &amp; Google Maps visibility"])
    body = f'''{page_hero("SEO Auckland", "SEO Auckland", 'SEO Auckland: <span class="grad-text">Get Found</span>',
        "Struggling to stand out online? Our expert SEO Auckland solutions help local businesses increase visibility, attract organic traffic and convert potential customers, cost-effectively.", side,
        f'<a class="btn btn-primary" href="/seo-audit/">Get a Free SEO Audit {ico("arrow")}</a><a class="btn btn-ghost" href="/contact/">{ico("phone")} Talk to Us</a>')}
<section class="sec sec-alt"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Why Invest</span><h2>Why Invest in SEO in Auckland?</h2>
    <div class="prose"><p>With over 90% of Kiwis using search engines to discover local products and services, your business needs more than just a website. It needs visibility. As a leading name among Auckland SEO companies, we focus on long-term growth, not quick fixes.</p></div></div>
  <div class="panel reveal"><ul class="check"><li>Boost your online presence</li><li>Rank higher for local search terms</li><li>Drive more qualified leads</li><li>Compete with top brands without breaking the bank</li></ul>
    <div class="callout" style="margin-top:20px"><p>We also have an <strong>AI Marketing Agency</strong> that specialises in all things AI.</p><a class="link-arrow" href="/contact/">Ask about AI marketing {ico("arrow")}</a></div></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">What's Included</span><h2>What Our SEO Services Include</h2><p>Full-service SEO tailored to your business goals.</p></div>
  {feature_cards(includes, "g-3")}
</div></section>
<section class="sec sec-alt"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Your Strategy</span><h2>Your Custom SEO Strategy</h2>
    <div class="prose"><p>No cookie-cutter tactics here. Your business is unique, and so is your SEO strategy. We take the time to understand your industry, target audience and goals.</p><p>Then we craft a marketing strategy that builds trust, drives traffic and adapts to algorithm updates, delivering high-quality, sustainable results.</p></div>
    <a class="btn btn-primary" href="/contact/">Plan My Strategy {ico("arrow")}</a></div>
  {feature_cards([("search","Understand","Your industry, audience and goals."),("target","Plan","A strategy built around real search demand."),("bolt","Execute","On-page, technical, content and links."),("report","Adapt","Measure, report and adjust to algorithm updates.")], "g-2", numbered=True)}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Compare</span><h2>What's Better? SEO vs Google Ads</h2><p>Google Ads offer immediate visibility but stop delivering once the budget is gone. SEO is a long-term investment that compounds over time.</p></div>
  <div class="compare">
    <div class="card reveal"><span class="tag dim">Google Ads</span><h3>Paid visibility</h3><ul class="check cross"><li>Ads stop when the budget runs out</li><li>You pay for every click</li><li>No lasting asset once campaigns end</li></ul></div>
    <div class="card win reveal"><span class="tag">SEO</span><h3>Compounding growth</h3><ul class="check"><li>SEO builds lasting value in your website</li><li>Organic traffic earns more trust from users</li><li>SEO scales more cost-effectively over months and years</li></ul></div>
  </div>
</div></section>
{testimonial("Trusted by Auckland Businesses", "What Our Clients Say", "Clinton and the team at SEO WEBSITES has completely transformed our online presence. Our website is now experiencing unprecedented levels of traffic resulting in a huge increase in the number of viable leads. When it comes to SEO in Auckland, look no further.")}
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">FAQ</span><h2>Frequently Asked Questions</h2></div>
  <div class="faq">{faq_html}</div>
</div></section>
{cta("Ready to Boost Your Rankings?", "Let's take your business to the top of the search results. Contact us today for a free SEO audit and discover how we can grow your traffic organically and cost-effectively.")}'''
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    return dict(slug="seo-auckland/", title="SEO Auckland | First Page Google Specialists | SEO WEBSITES",
                desc="Want to rank on Page 1 of Google? At SEO Websites, our local and international SEO Auckland services are tailored to suit your business.",
                body=body, crumb="SEO Auckland", extra_ld=[faq_ld])

def seo_services():
    benefits = [
        ("trend", "Increased Organic Traffic", "SEO makes your content customer-centric and hyper-targeted, so it appears when users search. That traffic is high quality because the user intent is fully met, and visitors stay longer."),
        ("bars", "An Impressive Return on Investment", "SEO takes time, but the right strategy delivers impressive ROI. Ranking on the first page brings more leads, and search leads close at 14.6%, well above traditional marketing methods."),
        ("shield", "Develops Trust and Credibility", "Google weighs many on-page and off-page factors before ranking a site, and users trust that algorithm. 75% of searchers never scroll past the first page."),
        ("clock", "24/7 Promotion", "SEO doesn't stop after work hours or when a budget runs out. Organic rankings let you take advantage of over 60,000 Google searches every second."),
        ("funnel", "Targets the Entire Marketing Funnel", "Top- and middle-of-funnel content builds brand identity, which eventually leads people to your services and, ultimately, to conversion."),
        ("users", "Reaches Your Whole Audience", "One website can have different service pages for different audiences. A pool installer, for example, can target both homeowners and commercial clients."),
        ("eye", "Optimises User Experience", "When users get the content they're looking for and have questions answered in seconds, they stay on your website longer."),
        ("ads", "Enhances PPC Success", "SEO and Pay Per Click work together to strengthen your website's overall online presence."),
        ("globe", "A Long-Term Marketing Strategy", "On-page, off-page and content work take time, but once done correctly they yield results for years, and brand recognition for longer."),
        ("search", "The Key to Search Visibility", "When you're visible on the first pages of search engines, your brand identity grows. Optimised correctly, your site stays there longer."),
    ]
    stats = [("14.6%", "Close rate on leads from search"), ("75%", "Of users never go past page one"), ("60,000", "Google searches every second"), ("24/7", "Promotion that never switches off")]
    side = orb("badge", "10 benefits of SEO for your business", ["More organic traffic", "Stronger ROI than traditional marketing", "Trust and credibility", "Round-the-clock promotion"])
    body = f'''{page_hero("SEO Services Auckland", "SEO Services Auckland", 'SEO Services <span class="grad-text">Auckland</span>',
        "There's no one-size-fits-all in marketing. Our SEO Services Auckland strategies are tailored to your business, so your website earns an organic audience that keeps growing.", side)}
<section class="sec sec-alt"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Is SEO Necessary?</span><h2>Why SEO Still Matters More Than Ever</h2></div>
  <div class="prose reveal"><p>SEO is an essential part of being found online, and rightfully so. The practice of AI SEO lets you rank your website in search engines like Google, provided it has been correctly optimised.</p>
    <p>Still, website owners ask: Is SEO really necessary? Should I invest my time and money with <strong>SEO Websites</strong>? Does it affect business growth? The truth is, organic search visibility is more important than all other digital marketing strategies combined. Search Engine Optimisation ensures your website is earning an organic audience.</p>
    <p>Here are ten benefits SEO delivers for website owners.</p></div>
</div></section>
<section class="sec-tight"><div class="wrap"><div class="stats">{"".join(f'<div class="stat reveal"><b class="grad-text">{a}</b><span>{b}</span></div>' for a, b in stats)}</div></div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">The Benefits</span><h2>10 Benefits of Search Engine Optimisation</h2><p>How SEO delivers value to your target audience and increases your visibility in search engines.</p></div>
  {feature_cards(benefits, "g-2", numbered=True)}
</div></section>
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Our Services</span><h2>Complete Digital Marketing Solutions</h2></div>
  {services_grid()}
</div></section>
{certs()}
{cta()}'''
    return dict(slug="seo-services-auckland/", title="SEO Services Auckland | Google Page 1 Specialists | SEO Websites",
                desc="There is no one shoe size fits all when it comes to marketing. Our SEO Services Auckland marketing strategies are tailored to suit you.",
                body=body, crumb="SEO Services Auckland")

def local_seo():
    deliver = [
        ("map", "Google Business Profile", "We enhance your Google Business Profile so it ranks highly in your Local Pack listings."),
        ("pin", "Every Location Covered", "Our approach expands across every physical location your company operates."),
        ("link", "Local Link Building", "Earn relevant local links that build authority in your market."),
        ("pen", "Content Marketing", "Content that answers what local customers are searching for."),
        ("key", "Keyword Research", "Research-led strategies built by our dedicated marketing specialists."),
        ("report", "Location-Specific Reports", "Mobile rankings, maps, NAP and citation tracking, all presented visually."),
    ]
    side = orb("pin", "Local SEO that gets you found", ["Google Business Profile optimisation", "Local Pack rankings", "NAP & local citation tracking", "Location-specific reporting"])
    body = f'''{page_hero("Local SEO Services", "Local SEO Services", 'Local SEO <span class="grad-text">Services</span>',
        "Need to be on Page 1 of Google New Zealand? Our local SEO services are tailored to your business, making sure you get the traffic you deserve from prospective clients.", side,
        f'<a class="btn btn-primary" href="/contact/">Let’s Talk {ico("arrow")}</a><a class="btn btn-ghost" href="/seo-audit/">{ico("bars")} Try Our Free Website Auditor</a>')}
<section class="sec sec-alt"><div class="wrap split top">
  <div class="reveal"><span class="eyebrow">Effective Marketing</span><h2>Effective Marketing for Businesses Using Our Local SEO Services</h2>
    <div class="prose"><p>Planning an efficient, growth-orientated SEO strategy isn't easy, but it becomes a smooth process with an Auckland-based <a href="/seo-auckland/">SEO agency</a> like us. Our approach isn't limited to one location; it expands across every physical location your company owns.</p>
    <p>We cater to every business in New Zealand looking to promote their brand and gain new clients. Our strategies are detail-orientated and specific to your business model, which is why we can increase your digital presence and brand visibility.</p></div></div>
  <div class="prose reveal"><p><strong>Research drives everything we do.</strong> Our strategies are based on research by our dedicated marketing specialists, who find the data needed to build the most efficient plan for your business. With that analysis and an SEO blueprint in hand, the strategy is implemented, producing measurable results.</p>
    <p>Your digital footprint becomes our responsibility the moment you choose us. We analyse the SEO strategies of every New Zealand business that is your direct online competition, so your presence in Google eventually surpasses theirs.</p>
    <p>We also provide location-specific performance reports: mobile search rankings, maps for your service locations, and NAP and local citation tracking that shows your strongest locations and the ones not yet at the top of Google.</p></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">What You Get</span><h2>What Our Local SEO Includes</h2></div>
  {feature_cards(deliver, "g-3")}
</div></section>
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Why Us</span><h2>Why Work With Us?</h2></div>
  {why_grid()}
</div></section>
{testimonial("This Month's Client Review")}
{certs()}
{cta("Try Our Free Website Auditor", "See how your website is performing in local search, then let's talk about getting you into the Local Pack.")}'''
    return dict(slug="local-seo-services/", title="Local SEO Services | Page #1 Google Specialists | SEO WEBSITES",
                desc="Need to be on Page 1 of Google New Zealand? At SEO Websites our local SEO services is tailored to suit your business.",
                body=body, crumb="Local SEO Services")

WHY_SHORT = [
    ("trophy", "Page 1 of Google", "All our clients are on Page 1 of Google."),
    ("users", "Boutique Focus", "More focused attention on each client's industry and niche."),
    ("doc", "No Lock-In Contracts", "We're confident in delivering measurable results."),
    ("heart", "100% Retention", "Our client retention speaks volumes."),
]

def social_page(kind):
    if kind == "instagram":
        d = dict(slug="instagram-seo/", crumb="Instagram SEO", title="Instagram SEO | SEO Websites | Page 1 Google Specialists",
                 desc="At SEO Websites, we specialise in Instagram SEO, helping brands like yours increase visibility, attract the right audience, and drive engagement.",
                 h1='Boost Your Instagram Reach with <span class="grad-text">Powerful SEO Strategies</span>',
                 lead="Instagram is more than a visual platform. It's a search engine in its own right. We help brands increase visibility, attract the right audience and drive engagement.",
                 icon="image", why_t="Why Instagram SEO Matters",
                 why_p="With millions of daily active users, standing out on Instagram takes more than great photos. Optimising your profile and content ensures your brand appears in search results, trending hashtags and user recommendations.",
                 why=[("user", "Optimised Profiles", "From your bio to your handle, we refine your profile to make it searchable and engaging."), ("hash", "Strategic Hashtags", "Data-backed hashtags that amplify your reach and connect with your target audience."), ("pen", "Keyword-Rich Captions", "Captions that tell your story while boosting discoverability."), ("image", "Alt Text Optimisation", "Descriptive, keyword-focused alt text makes your content accessible and searchable.")],
                 svc_t="Our Instagram SEO Services",
                 svc=[("user", "Profile Optimisation", "A bio and profile layout that captures attention and ranks for relevant searches."), ("hash", "Hashtag Strategy", "Trending and niche hashtags to maximise your post reach."), ("doc", "Content Optimisation", "From captions to alt text, every element of your post works towards visibility."), ("report", "Analytics & Growth", "Monitor performance and adapt your strategy for consistent growth.")],
                 ben_t="The Benefits of Instagram SEO",
                 ben=[("eye", "Increase Your Discoverability", "Be found by the audience that matters most."), ("heart", "Engage Your Ideal Followers", "Attract users who align with your brand values and goals."), ("trophy", "Stay Ahead of the Competition", "Optimisation gives you the edge in a crowded marketplace."), ("trend", "Drive Real Results", "Turn visibility into follows, engagement and conversions.")],
                 cta_t="Let's Elevate Your Instagram Presence",
                 cta_p="Instagram success isn't just about posting. It's about being found. With our Instagram SEO strategies, you'll attract more followers, boost engagement and achieve measurable results.")
    else:
        d = dict(slug="tiktok-seo/", crumb="TikTok SEO", title="TikTok SEO | SEO Websites | Page 1 Google Specialists",
                 desc="Unlock the power of TikTok SEO with SEO Websites. Discover how to optimise your profile, captions, and hashtags to increase visibility, reach your target audience, and grow your engagement.",
                 h1='Unlock Viral Success with Expert <span class="grad-text">TikTok SEO</span>',
                 lead="Want to dominate TikTok and Google? TikTok is a discovery engine with billions of users searching for the next big trend. We help creators and brands maximise visibility, grow followers and achieve measurable results.",
                 icon="music", why_t="What Is TikTok SEO?",
                 why_p="TikTok SEO is about making your content discoverable to the right audience. From hashtags to captions and trending audio strategies, we make sure your videos get seen, liked and shared.",
                 why=[("hash", "Hashtag Optimisation", "Targeted hashtags that boost visibility and engagement."), ("key", "Keyword Integration", "Captions and video descriptions that align with audience searches."), ("bolt", "Trending Insights", "Up-to-date knowledge of TikTok trends and algorithm shifts."), ("report", "Performance Analytics", "Data-driven improvements that refine your strategy and extend your reach.")],
                 svc_t="Our TikTok SEO Services",
                 svc=[("user", "Profile Optimisation", "Your TikTok bio, links and content aligned with your brand."), ("play", "Content Strategy", "Creative ideas and videos optimised for maximum discoverability."), ("search", "SEO Implementation", "The right keywords, hashtags and metadata to make your content rank."), ("music", "Trend Monitoring", "Leverage trending audio and challenges to keep content relevant.")],
                 ben_t="Why TikTok SEO Matters",
                 ben=[("eye", "Boost Visibility", "Appear in searches and on more For You Pages (FYP)."), ("users", "Engage Your Audience", "Reach users genuinely interested in your niche."), ("trophy", "Stay Competitive", "Stand out on one of the most dynamic social platforms."), ("trend", "Drive Conversions", "Turn your TikTok presence into measurable growth.")],
                 cta_t="Let's Make Your TikTok Shine",
                 cta_p="Whether you're an influencer, a brand or a content creator, we have the expertise to elevate your TikTok presence. Start your TikTok transformation today.")
    side = orb(d["icon"], "Why brands choose our boutique agency", [w[2] for w in WHY_SHORT])
    body = f'''{page_hero(d["crumb"], d["crumb"], d["h1"], d["lead"], side,
        f'<a class="btn btn-primary" href="/contact/">Get Started {ico("arrow")}</a><a class="btn btn-ghost" href="/contact/">{ico("chat")} Book a Free Consultation</a>')}
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">The Opportunity</span><h2>{d["why_t"]}</h2><p>{d["why_p"]}</p></div>
  {feature_cards(d["why"], "g-4")}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">What We Do</span><h2>{d["svc_t"]}</h2></div>
  {feature_cards(d["svc"], "g-4", numbered=True)}
</div></section>
<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">The Results</span><h2>{d["ben_t"]}</h2></div>
  {feature_cards(d["ben"], "g-4")}
</div></section>
<section class="sec-tight"><div class="wrap">
  <div class="sec-head reveal"><h2>Why Work With SEO Websites</h2></div>
  <div class="grid g-4">{"".join(f'<div class="why reveal"><div class="ring-ico">{ico(i)}</div><h3>{t}</h3><p>{x}</p></div>' for i, t, x in WHY_SHORT)}</div>
</div></section>
{cta(d["cta_t"], d["cta_p"])}'''
    return dict(slug=d["slug"], title=d["title"], desc=d["desc"], body=body, crumb=d["crumb"])

def about():
    side = f'<div class="orb-card"><div class="big-ico">{ico("heart")}</div><h4>We eat, sleep and breathe online marketing.</h4><p class="muted" style="margin:0">Going the extra mile is a way of life for us because we\'re passionate about what we do. We monitor our clients\' marketing progress every day.</p></div>'
    body = f'''{page_hero("About Us", "About Us", 'A Boutique Auckland Agency That <span class="grad-text">Goes the Extra Mile</span>',
        "As an SEO Auckland based agency, we're dedicated to providing exceptional online marketing services, with a hands-on approach and individual attention every day.", side)}
<section class="sec sec-alt"><div class="wrap split">
  <div class="reveal"><span class="eyebrow">Who We Are</span><h2>Hands-On, Measurable, Personal</h2>
    <div class="prose"><p>As an <a href="/seo-auckland/">SEO Auckland</a> based agency, we are dedicated to providing exceptional online marketing services. As a boutique agency, we take a hands-on approach and give our clients individualised attention on a daily basis, resulting in measurable success.</p>
    <p>Our passion for digital marketing is evident in the results we deliver. Trust us to go the extra mile for your business.</p></div></div>
  <div class="panel founder reveal"><img src="/assets/img/clinton.jpeg" alt="Clinton, Head of Digital at SEO Websites" width="260" height="325" loading="lazy">
    <div><blockquote>“Results speak louder than glossy reports.”</blockquote><b>Clinton</b><p class="muted" style="margin:0">Head of Digital, SEO Websites</p></div></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Our Values</span><h2>Why Clients Stay With Us</h2></div>
  {why_grid()}
</div></section>
{certs()}
{logos()}
{cta()}'''
    return dict(slug="about-us/", title="About Us - SEO Websites",
                desc="At SEO WEBSITES we eat, sleep and breathe online marketing. Going the extra mile is a way of life for us as we’re passionate about what we do.",
                body=body, crumb="About Us")

def contact():
    body = f'''<section class="hero page-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Contact</span></nav>
  <span class="eyebrow">Contact</span><h1>Get <span class="grad-text">In Touch</span></h1>
  <p class="lead">Tell us about your business and goals. We'll come back to you with honest advice on how SEO, web design, Google Ads and AI marketing can help you grow.</p>
</div></section>
<section class="sec" style="padding-top:10px"><div class="wrap contact-grid">
  <div class="contact-items">
    <a class="contact-item reveal" href="tel:{PHONE_TEL}"><span class="ring-ico">{ico("phone")}</span><span><small>Call Us</small><b>{PHONE}</b></span></a>
    <a class="contact-item reveal" href="mailto:{EMAIL}"><span class="ring-ico">{ico("mail")}</span><span><small>Email Us</small><b>{EMAIL}</b></span></a>
    <div class="contact-item reveal"><span class="ring-ico">{ico("pin")}</span><span><small>Location</small><b>Auckland, New Zealand</b></span></div>
    <div class="panel reveal"><h3>What happens next?</h3><ul class="check"><li>We review your website and goals</li><li>A strategy call to talk through your options</li><li>A clear plan, with no long-term contracts</li></ul></div>
  </div>
  <form class="panel reveal" id="contact-form" method="post" action="{FORM_ACTION}">
    <input type="hidden" name="_subject" value="New enquiry from seowebsites.co.nz">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_next" value="{DOMAIN}/contact/?sent=1#contact-form">
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
    <h2 style="font-size:1.6rem">Send Us a Message</h2>
    <div class="f-row"><label><span>First name <span class="req">*</span></span><input name="first" autocomplete="given-name" required></label>
      <label><span>Last name</span><input name="last" autocomplete="family-name"></label></div>
    <label><span>Email <span class="req">*</span></span><input type="email" name="email" autocomplete="email" required></label>
    <label><span>Website</span><input name="website" type="url" placeholder="https://" autocomplete="url"></label>
    <label><span>Comment or message <span class="req">*</span></span><textarea name="message" required></textarea></label>
    <button class="btn btn-primary" type="submit" style="justify-self:start">Submit {ico("arrow")}</button>
    <p class="form-msg" role="status"></p>
  </form>
</div></section>
{cta()}'''
    return dict(slug="contact/", title="Contact - SEO Websites",
                desc="Contact SEO Websites, a boutique Auckland SEO and AI digital marketing agency. Call 020 4059 1357 or email seowebsitesnz@gmail.com.",
                body=body, crumb="Contact")

# ---------------------------------------------------------------- render
ORG_LD = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "SEO Websites", "url": DOMAIN + "/",
          "telephone": "+64 20 4059 1357", "email": EMAIL, "priceRange": "$$",
          "address": {"@type": "PostalAddress", "addressLocality": "Auckland", "postalCode": "2018", "addressCountry": "NZ"},
          "areaServed": "New Zealand"}

def render(p):
    url = DOMAIN + "/" + p["slug"]
    lds = [ORG_LD] + p.get("extra_ld", [])
    if p["crumb"]:
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]})
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{p["title"]}"><meta property="og:description" content="{p["desc"]}"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_NZ">
<meta name="theme-color" content="#040a1c">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat&family=Inter:wght@400;500;600&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{SVG_DEFS}
{header("/" + p["slug"])}
<main id="main">
{p["body"]}
</main>
{FOOTER}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

PAGES = [home, seo_auckland, seo_services, local_seo, lambda: social_page("instagram"), lambda: social_page("tiktok"), about, contact]

if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    urls = []
    for fn in PAGES:
        p = fn()
        dest = OUT / p["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(p), encoding="utf-8")
        urls.append(DOMAIN + "/" + p["slug"])
        print("built", dest.relative_to(ROOT))
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
