# -*- coding: utf-8 -*-
"""Gera o site estático ninaroseartstudio.com (EN / ES / PT). Uso: python3 build.py"""
import json, os, html, random
from content import T, STORY, REVIEWS, LANGS, HTML_LANG, SHOP, IG, THREADS

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://ninaroseartstudio.com"
D = {d["n"]: d for d in json.load(open(os.path.join(ROOT, "_data.json")))}
DETAIL = {37, 43, 46, 69, 76, 101, 117, 128}
FIX = {"Simba the Little Lion Lion": "Simba the Little Lion", "Baby": "Baby Flor", "Fall Collection Carolina": "Carolina"}
for n, d in D.items():
    if d.get("name") in FIX: d["name"] = FIX[d["name"]]
    if n in DETAIL: d["cat"], d["name"] = "detail", None

PAGES = {"home": "", "dolls": "dolls/", "story": "story/", "paintings": "paintings/"}
NAVKEY = {"home": "nav_home", "dolls": "nav_dolls", "story": "nav_story", "paintings": "nav_paint"}
CATS = ["doll", "baby", "animal", "frog", "season", "detail"]

def img(n, big=False): return f"/img/g/{n:03d}{'' if big else '-s'}.webp"
def url(lang, page): return "/" + LANGS[lang] + PAGES[page]
def e(s): return html.escape(s or "", quote=True)
def ok(ns): return [n for n in ns if n in D]


def head(lang, page, t):
    title, desc = t[f"meta_{'paint' if page=='paintings' else page}_t"], t[f"meta_{'paint' if page=='paintings' else page}_d"]
    alts = "\n".join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{DOMAIN}{url(l,page)}">' for l in LANGS)
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Nina Rose Art Studio", "url": DOMAIN + "/",
          "founder": {"@type": "Person", "name": "Alessandra Lavieri de Abreu"}, "sameAs": [SHOP, IG, THREADS],
          "description": t["meta_home_d"]}
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{DOMAIN}{url(lang,page)}">
{alts}
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url('en',page)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Nina Rose Art Studio">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{DOMAIN}{url(lang,page)}"><meta property="og:image" content="{DOMAIN}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#B5626A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Nunito:wght@400;600;700&family=Caveat:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=2">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="p-{page}">"""

def nav(lang, page, t):
    links = "".join(f'<a href="{url(lang,p)}"{" aria-current=page" if p==page else ""}>{t[NAVKEY[p]]}</a>' for p in ["dolls","story","paintings"])
    langs = "".join(f'<a href="{url(l,page)}" hreflang="{HTML_LANG[l]}" class="{"on" if l==lang else ""}">{l.upper()}</a>' for l in LANGS)
    return f"""<nav id="nav" class="{'solid' if page!='home' else ''}"><div class="wrap">
<a class="logo" href="{url(lang,'home')}"><span class="rose">🌹</span><span>Nina Rose <b>Art Studio</b></span></a>
<button class="burger" aria-label="Menu" onclick="document.body.classList.toggle('menu-open')"><i></i><i></i><i></i></button>
<div class="menu">{links}<div class="lang">{langs}</div>
<a class="btn primary sm" href="{SHOP}" target="_blank" rel="noopener">{t['nav_shop']}</a></div>
</div></nav>"""

def footer(lang, t):
    return f"""<footer><div class="wrap">
<div class="f-logo">🌹 Nina Rose <b>Art Studio</b></div>
<p class="hand big">{t['foot']}</p>
<p class="f-links"><a href="{SHOP}" target="_blank" rel="noopener">Etsy</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{THREADS}" target="_blank" rel="noopener">Threads</a></p>
<p class="small">{t['foot_made']}<br>© 2026 Nina Rose Art Studio</p>
</div></footer>
<div id="lb" role="dialog" aria-modal="true"><button class="lb-x" aria-label="{t['lb_close']}">×</button><button class="lb-p" aria-label="{t['lb_prev']}">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" aria-label="{t['lb_next']}">›</button></div>
<script src="/assets/site.js?v=2" defer></script>
</body></html>"""

def fig(n, t, big_attr=True, cls="rv"):
    d = D[n]; cap = d["name"] or t["c_"+d["cat"]]
    return (f'<figure class="{cls}" data-k="{d["cat"]}"><a href="{img(n,True)}" data-lb data-cap="{e(cap)}">'
            f'<img loading="lazy" decoding="async" src="{img(n)}" width="{round(d["w"]*640/max(d["w"],d["h"]))}" height="{round(d["h"]*640/max(d["w"],d["h"]))}" alt="{e(cap)} — Nina Rose Art Studio"></a>'
            f'<figcaption>{e(cap)}</figcaption></figure>')

def cta(lang, t):
    fl = "".join(f'<img src="{img(n)}" alt="" style="left:{l};top:{tp};animation-delay:{-i*1.3}s" loading="lazy">' for i,(n,l,tp) in enumerate([(96,'5%','12%'),(121,'85%','18%'),(59,'10%','68%'),(94,'82%','66%'),(26,'47%','82%')]) if n in D)
    return f"""<section id="adopt"><div class="floaters">{fl}</div><div class="wrap">
<span class="kicker rv">{t['a_k']}</span><h2 class="rv">{t['a_h']}</h2>
<p class="rv lead">{t['a_p']}</p>
<div class="ctas rv center"><a class="btn primary" href="{SHOP}" target="_blank" rel="noopener">{t['cta_shop']}</a>
<a class="btn ghost" href="{IG}" target="_blank" rel="noopener">Instagram</a>
<a class="btn ghost" href="{SHOP}" target="_blank" rel="noopener">{t['a_custom']}</a></div></div></section>"""

def home(lang):
    t = T[lang]; out = [head(lang,"home",t), nav(lang,"home",t)]
    slides = "".join(f'<img src="{img(n,True)}" alt="" {"class=on fetchpriority=high" if i==0 else "loading=lazy"}>' for i,n in enumerate(ok([5,23,36,18,8,49,60,31])))
    out.append(f"""<header id="hero"><div class="hero-text">
<div class="blob b1"></div><div class="blob b2"></div>
<div class="ht"><span class="kicker">{t['hero_k']}</span><h1>{t['hero_h']}</h1>
<svg class="stitch" viewBox="0 0 240 18" aria-hidden="true"><path d="M2 12 C 40 2, 80 18, 120 9 S 200 2, 238 10"/></svg>
<p class="lead">{t['hero_p']}</p>
<div class="ctas"><a class="btn primary" href="{url(lang,'dolls')}">{t['cta_meet']}</a><a class="btn ghost" href="{SHOP}" target="_blank" rel="noopener">{t['cta_shop']}</a></div></div></div>
<div class="slides" id="slides">{slides}<div class="badge">{t['badge']}</div></div></header>""")
    mq = ok([42,47,59,12,26,28,31,40,55,96,94,121,60,19,113,35,62,75,98,134])
    trk = "".join(f'<img src="{img(n)}" alt="" loading="lazy">' for n in mq*2)
    out.append(f'<div class="marquee" aria-hidden="true"><div class="track">{trk}</div></div>')
    cards = ""
    for i,n in enumerate(ok([1,3,7,12,13,19,18,99,95,121,62,96])):
        d = D[n]; nm = d["name"] or t["c_"+d["cat"]]
        cards += f'<div class="card rv" style="transition-delay:{(i%4)*.08:.2f}s" tabindex="0"><div class="in"><div class="f"><img loading="lazy" src="{img(n)}" alt="{e(nm)}"><span>{e(nm)}</span></div><div class="b"><h3>{e(nm)}</h3><p>{t["c_"+d["cat"]]}</p><small>{t["card_back"]}</small></div></div></div>'
    out.append(f"""<section id="names"><div class="wrap"><span class="kicker rv">{t['names_k']}</span><h2 class="rv">{t['names_h']}</h2>
<p class="rv lead">{t['names_p']}</p><div class="names-grid">{cards}</div></div></section>""")
    nr = next((n for n,d in D.items() if d.get("name")=="Baby Nina Rose"), None)
    out.append(f"""<section id="nina"><div class="wrap nina"><div class="polaroids rv">
<figure><img src="/img/p/ig02.webp" alt="{e(t['nina_cap3'])}" loading="lazy"><figcaption>{t['nina_cap3']}</figcaption></figure>
<figure><img src="/img/p/ig01.webp" alt="{e(t['nina_cap1'])}" loading="lazy"><figcaption>{t['nina_cap1']}</figcaption></figure>
{f'<figure><img src="{img(nr)}" alt="Baby Nina Rose" loading="lazy"><figcaption>{t["nina_cap2"]}</figcaption></figure>' if nr else ''}
</div><div class="rv"><span class="kicker">{t['nina_k']}</span><h2>{t['nina_h']}</h2><p class="lead">{t['nina_p']}</p>
<a class="btn ghost" href="{url(lang,'story')}">{t['jr_more']}</a></div></div></section>""")
    stops = "".join(f'<div class="stop rv" style="transition-delay:{i*.08:.2f}s"><div class="flag">{f}</div><h3>{t[f"s{i+1}h"]}</h3><p>{t[f"s{i+1}p"]}</p></div>' for i,f in enumerate(["🇧🇷","🇲🇽","🇳🇱","🇺🇸","🧵","🌹"]))
    out.append(f"""<section id="journey"><div class="wrap"><span class="kicker rv">{t['jr_k']}</span><h2 class="rv">{t['jr_h']}</h2><p class="rv lead">{t['jr_p']}</p>
<div class="map"><svg viewBox="0 0 1000 120" aria-hidden="true"><path id="jpath" d="M30 80 C 150 10, 250 110, 360 60 S 560 10, 640 70 S 860 110, 970 40"/></svg><div class="stops">{stops}</div></div>
<p class="center"><a class="btn ghost" href="{url(lang,'story')}">{t['jr_more']}</a></p></div></section>""")
    prev = ok([28,62,96,121,13,75,94,40,118,99,19,134,58,113,31,66,98,55])
    out.append(f"""<section id="gallery"><div class="wrap"><span class="kicker rv">{t['gal_k']}</span><h2 class="rv">{t['gal_h']}</h2>
<div class="masonry">{''.join(fig(n,t) for n in prev)}</div>
<p class="center"><a class="btn primary" href="{url(lang,'dolls')}">{t['gal_more']} ({len(D)}) →</a></p></div></section>""")
    mats = "".join(f'<div class="mat rv" style="transition-delay:{i*.1:.1f}s"><div class="ring"><img loading="lazy" src="{img(n)}" alt=""></div><h3>{t[f"mt{i+1}h"]}</h3><p>{t[f"mt{i+1}p"]}</p></div>' for i,n in enumerate(ok([42,46,117,5,64])))
    out.append(f'<section id="materials"><div class="wrap"><span class="kicker rv">{t["mat_k"]}</span><h2 class="rv">{t["mat_h"]}</h2><div class="mats">{mats}</div></div></section>')
    out.append(f"""<section id="villages"><div class="wrap vill"><div class="rv"><span class="kicker">{t['v_k']}</span><h2>{t['v_h']}</h2><p>{t['v_p1']}</p><p>{t['v_p2']}</p>
<div class="ctas"><a class="btn primary" href="{url(lang,'paintings')}">{t['v_cta']}</a><a class="btn ghost" href="{IG}" target="_blank" rel="noopener">{t['v_ig']}</a></div></div>
<div class="paint-stack" id="pstack"><img src="/img/p/ig12.webp" alt="" loading="lazy"><img src="/img/p/ig11.webp" alt="" loading="lazy"><img src="/img/p/ig08.webp" alt="" loading="lazy"></div></div></section>""")
    qs = "".join(f'<blockquote class="{"on" if i==0 else ""}">“{q}”<cite>{w} · {it}</cite></blockquote>' for i,(q,w,it) in enumerate(REVIEWS))
    out.append(f"""<section id="reviews"><div class="wrap center"><span class="kicker rv">{t['r_k']}</span><h2 class="rv">{t['r_h']}</h2>
<div class="stats rv"><div><b data-count="277">277</b><span>{t['st1']}</span></div><div><b data-count="157">157</b><span>{t['st2']}</span></div><div><b>5.0★</b><span>{t['st3']}</span></div></div>
<div class="quotes" id="quotes">{qs}</div><p class="small">{t['st_note']}</p></div></section>""")
    out.append(cta(lang,t)); out.append(footer(lang,t)); return "\n".join(out)

def dolls(lang):
    t = T[lang]; out=[head(lang,"dolls",t), nav(lang,"dolls",t)]
    cnt = {c: sum(1 for d in D.values() if d["cat"]==c) for c in CATS}
    btn = f'<button class="on" data-f="all">{t["f_all"]} <small>{len(D)}</small></button>' + "".join(f'<button data-f="{c}">{t["f_"+c]} <small>{cnt[c]}</small></button>' for c in CATS if cnt[c])
    order = sorted(D, reverse=True)  # mais recentes primeiro
    out.append(f"""<header class="page-head"><div class="wrap"><span class="kicker">{t['gal_k']}</span><h1>{t['gal_h']}</h1><p class="lead">{t['dolls_intro']}</p>
<div class="filters" id="filters">{btn}</div></div></header>
<section class="tight"><div class="wrap"><div class="masonry" id="masonry">{''.join(fig(n,t) for n in order)}</div></div></section>""")
    out.append(cta(lang,t)); out.append(footer(lang,t)); return "\n".join(out)

def story(lang):
    t = T[lang]; out=[head(lang,"story",t), nav(lang,"story",t)]
    pics = [ok([12,59]), ok([47,121]), ok([28,96]), ok([62,99]), []]
    body = ""
    for i,(h,ps) in enumerate(STORY[lang]):
        ims = "".join(f'<img src="{img(n)}" alt="" loading="lazy">' for n in pics[i])
        if i==4: ims = '<img src="/img/p/ig12.webp" alt="" loading="lazy"><img src="/img/p/ig11.webp" alt="" loading="lazy">'
        body += f'<article class="chapter {"alt" if i%2 else ""}"><div class="ch-text rv"><span class="num">0{i+1}</span><h2>{h}</h2>{"".join(f"<p>{p}</p>" for p in ps)}</div><div class="ch-pics rv">{ims}</div></article>'
    out.append(f"""<header class="page-head"><div class="wrap"><span class="kicker">{t['story_k']}</span><h1>{t['story_h']}</h1></div></header>
<section class="tight"><div class="wrap">{body}</div></section>""")
    out.append(cta(lang,t)); out.append(footer(lang,t)); return "\n".join(out)

def paintings(lang):
    t = T[lang]; out=[head(lang,"paintings",t), nav(lang,"paintings",t)]
    figs = "".join(f'<figure class="rv"><a href="/img/p/{k}.webp" data-lb data-cap="{e(t["v_h"])}"><img src="/img/p/{k}.webp" alt="{e(t["v_h"])}" loading="lazy"></a></figure>' for k in ["ig12","ig11","ig08","ig04","ig10","ig06","ig02","ig03","ig01"])
    out.append(f"""<header class="page-head green"><div class="wrap"><span class="kicker">{t['v_k']}</span><h1>{t['v_h']}</h1><p class="lead">{t['v_p1']}</p><p>{t['v_p2']}</p></div></header>
<section class="tight"><div class="wrap"><div class="masonry paint">{figs}</div><p class="center"><a class="btn ghost" href="{IG}" target="_blank" rel="noopener">{t['v_ig']}</a></p></div></section>""")
    out.append(cta(lang,t)); out.append(footer(lang,t)); return "\n".join(out)

GEN = {"home": home, "dolls": dolls, "story": story, "paintings": paintings}
urls = []
for lang in LANGS:
    for page, fn in GEN.items():
        p = os.path.join(ROOT, LANGS[lang], PAGES[page], "index.html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(fn(lang)); urls.append(url(lang, page))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for page in PAGES:
    for lang in LANGS:
        sm += f'<url><loc>{DOMAIN}{url(lang,page)}</loc>' + "".join(f'<xhtml:link rel="alternate" hreflang="{HTML_LANG[l]}" href="{DOMAIN}{url(l,page)}"/>' for l in LANGS) + '</url>\n'
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print(len(urls), "páginas;", len(D), "fotos")
