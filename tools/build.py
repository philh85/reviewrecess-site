#!/usr/bin/env python3
"""Builds the static Review Recess site into ../site/ (pages, sitemap, robots).
Shared header/footer live here so every page stays consistent. Links are NOT here: they live
in assets/js/config.js so Phil can change them without rebuilding."""
import os, html, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from games import GAMES
from game_pages import GAME_PAGES, OLD_SLUGS, NEED, FREE_TEXT, FULL_TEXT, BUNDLE_TEXT
LASTMOD = '2026-10-23'
GP = {g['slug']: g for g in GAME_PAGES}
assert [g[0] for g in GAMES if g[0] not in GP] == [] and len(GAMES) == len(GAME_PAGES) == 13
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://reviewrecess.com'
E = html.escape

MARK = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="14" fill="#13294b"/>'
 + ''.join(f'<rect x="{11+c*15}" y="{11+r*15}" width="12" height="12" rx="2.5" fill="{"#d4af37" if r+c==2 else "#2b4a7a"}"/>' for r in range(3) for c in range(3))
 + '</svg>')

NAV = [('/', 'Home'), ('/games/', 'Games'), ('/help/', 'Help & Support'), ('/about/', 'About')]

def btn(key, label, cls='btn-gold', extra=''):
    return f'<a class="btn {cls}{extra}" data-link="{key}" aria-disabled="true">{label}<span class="soon">Coming soon</span></a>'

def header(path):
    items = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="Review Recess home">{MARK}<span><span class="brand-name">Review Recess</span><span class="brand-sub">Classroom review games</span></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav class="nav" id="site-nav" aria-label="Main"><ul>{items}<li>{btn("TPT_STORE_URL", "TpT store", "btn-navy btn-sm")}</li></ul></nav>
</div></header>'''

FOOT_GAMES = ''.join(f'<li><a href="/games/{g[0]}/">{E(g[1])}</a></li>' for g in GAMES)
FOOTER = f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/">{MARK}<span><span class="brand-name">Review Recess</span><span class="brand-sub">Classroom review games</span></span></a>
<p class="small" style="margin-top:14px;max-width:30em">Whole-class review games for the classroom screen. They run in your own Google account, and your questions stay in your own Google Drive.</p></div>
<div><h2>Games</h2><ul class="foot-games">{FOOT_GAMES}</ul></div>
<div><h2>Explore</h2><ul><li><a href="/games/">All games</a></li><li><a href="/help/">Help &amp; Support</a></li><li><a href="/about/">About</a></li><li>{btn("TPT_STORE_URL","TpT store","btn-sm btn-ghost-foot")}</li></ul></div>
<div><h2>Policies</h2><ul><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms &amp; licence</a></li><li><a data-link="YOUTUBE_URL" aria-disabled="true">YouTube<span class="soon"> (coming soon)</span></a></li></ul></div>
</div>
<div class="legal">
<p>© 2026 Review Recess. All rights reserved.</p>
<p>AP® is a trademark registered by the College Board, which is not affiliated with, and does not endorse, this product.</p>
<p>Review Recess is an independent seller and is not affiliated with Teachers Pay Teachers. Google, Google Drive and Google Apps Script are trademarks of Google LLC.</p>
</div></div></footer>'''

def page(path, title, desc, body, out, noindex=False, og_image='/assets/img/og-image.png', og_alt='Review Recess: classroom review games for the whole class', og_type='website', jsonld=None):
    full = title if 'Review Recess' in title else f'{title} | Review Recess'
    canon = DOMAIN + path
    ld = ''.join('\n<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>' for j in (jsonld or []))
    doc = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">'}
<meta name="theme-color" content="#13294b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Review Recess">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(og_alt)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(full)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{DOMAIN}{og_image}">
<meta name="twitter:image:alt" content="{E(og_alt)}">{ld}
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/config.js" defer></script>
<script src="/assets/js/site.js" defer></script>
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    p = os.path.join(OUT, out); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(doc)

def img(gid, alt, eager=False, sizes='(max-width:620px) 100vw, (max-width:900px) 50vw, 360px'):
    return (f'<img src="/assets/img/games/{gid}-640.webp" srcset="/assets/img/games/{gid}-640.webp 640w, /assets/img/games/{gid}-1200.webp 1200w" '
            f'sizes="{sizes}" width="640" height="360" alt="{E(alt)}"{"" if eager else " loading=\"lazy\""} decoding="async">')

PACKS = '''<ul class="pill-list">
<li>AP® World History: Modern</li><li>AP® United States Government and Politics</li><li>Grade 8 U.S. History &amp; Civics</li><li>ELA skills: grammar, vocabulary and more</li></ul>'''

CTA = f'''<section class="cta on-navy"><div class="wrap">
<p class="eyebrow">Ready for your next review lesson?</p>
<h2>Find Review Recess on Teachers Pay Teachers</h2>
<p class="lead" style="margin:0 auto 26px">Every game, bundle and question pack is sold through our TpT store.</p>
<div class="btn-row">{btn("TPT_STORE_URL","Visit our TpT store")}<a class="btn btn-ghost" href="/help/">Installation help</a></div>
</div></section>'''

# ---------------- Home ----------------
feature = [g for g in GAMES if g[0] in ('brain-board-blitz','million-point-climb','forbidden-words','answer-armada','word-magnets','sentence-snap')]
def game_card(g, h='h3'):
    return (f'''<article class="card game-card"><a class="card-img" href="/games/{g[0]}/" tabindex="-1" aria-hidden="true">{img(g[0], g[7])}</a><div class="body"><span class="tag">{E(g[2])}</span>'''
            f'''<{h}><a class="card-link" href="/games/{g[0]}/">{E(g[1])}</a></{h}><p class="muted" style="margin:0">{E(g[5])}</p><p class="more"><a href="/games/{g[0]}/">How to play →<span class="sr"> {E(g[1])}</span></a></p></div></article>''')
cards = ''.join(game_card(g) for g in feature)
home = f'''<section class="hero"><div class="wrap hero-grid">
<div>
<p class="eyebrow">Classroom review games for U.S. teachers</p>
<h1>Whole-class review games, ready for your classroom screen.</h1>
<p class="lead">Team games that run on your smart TV or projector, filled with your own questions or a ready-made pack, and saved in your own Google Drive.</p>
<ul class="hero-points"><li>A growing collection, from quiz boards to drag-and-drop word games</li><li>Pick exactly which questions to use each lesson</li><li>No student accounts or devices needed</li></ul>
<div class="btn-row">{btn("TPT_STORE_URL","Visit our TpT store")}<a class="btn btn-ghost" href="/games/">See the games</a></div>
</div>
<figure class="shot" style="margin:0">{img("brain-board-blitz", GAMES[0][7], eager=True, sizes="(max-width:900px) 100vw, 540px")}<figcaption>Brain Board Blitz: a 5 × 5 team quiz board with live scores.</figcaption></figure>
</div></section>

<section><div class="wrap">
<p class="eyebrow">How it works</p><h2>From purchase to playing in three steps</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><span class="step-num">1</span><h3>Open your game link</h3><p class="muted">Your TpT download includes the game link. Open it while signed in to Google and allow access once.</p></div>
<div class="card"><span class="step-num">2</span><h3>Choose your questions</h3><p class="muted">Use the sample bank, paste in your own questions, or load a question pack. Untick anything you don't want today.</p></div>
<div class="card"><span class="step-num">3</span><h3>Put it on the big screen</h3><p class="muted">Split the class into teams, go full screen and play. Scores, timers and turns are handled for you.</p></div>
</div></div></section>

<section class="alt"><div class="wrap">
<div style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:26px">
<div><p class="eyebrow">The games</p><h2 style="margin:0">Built for the front of the room</h2></div>
<a class="btn btn-navy" href="/games/">See all the games</a></div>
<div class="grid g3">{cards}</div>
</div></section>

<section><div class="wrap">
<p class="eyebrow">Why it works in class</p><h2>Designed around how teachers actually review</h2>
<div class="grid g3" style="margin-top:26px">
<div class="feature"><h3>Your questions, your choice</h3><p class="muted">A tick-box question picker lets you select all, or read through and untick anything that doesn't fit today's lesson.</p></div>
<div class="feature"><h3>Reusable question banks</h3><p class="muted">Save a bank once per unit and load it again next lesson, next term or next year.</p></div>
<div class="feature"><h3>Questions never run out</h3><p class="muted">Nothing repeats until every question has been used, then the bank reshuffles on its own.</p></div>
<div class="feature"><h3>Whole-class and team play</h3><p class="muted">Team rosters, fair student pickers and rotating turns keep every student involved, not just the fastest hands.</p></div>
<div class="feature"><h3>Readable from the back row</h3><p class="muted">Light, dark and high-contrast themes, plus big-text and large-button options for projectors.</p></div>
<div class="feature"><h3>Private by design</h3><p class="muted">Games run in your own Google account and only use files they create. Student data never comes to us.</p></div>
</div></div></section>

<section class="alt"><div class="wrap grid g2" style="align-items:center;gap:40px">
<div><p class="eyebrow">Question packs</p><h2>Curriculum-aligned packs for the whole year</h2>
<p class="muted">We're writing review packs that follow the units teachers already teach, so you can use them after every unit, not just before exams. Every question is written by a teacher. First packs in development:</p>
{PACKS}
<p class="small muted" style="margin-top:16px">Packs will appear in the TpT store as each one is finished.</p></div>
<figure class="shot" style="margin:0;box-shadow:var(--shadow);border-color:var(--line)">{img("question-picker","The question picker: a numbered list of questions with tick boxes, grouped by category, with Select all and Clear all buttons.", sizes="(max-width:620px) 100vw, 520px")}<figcaption>The question picker: tick or untick any question before you play.</figcaption></figure>
</div></section>

<section><div class="wrap grid g2" style="align-items:center;gap:40px">
<div><p class="eyebrow">Coming soon</p><h2>Live mode</h2>
<p class="muted">An optional live mode is in development. Students will join from their own devices by scanning a QR code, with no login. Nothing is stored after the session ends.</p></div>
<div class="notice"><strong>Live mode is not available yet.</strong> Today, every game runs on one teacher screen, which needs no student devices at all.</div>
</div></section>
{CTA}'''
page('/', 'Review Recess | Classroom review games for the whole class',
     'Whole-class review games for your smart TV or projector. Team games that run in your own Google account, with reusable question banks and a tick-box question picker.',
     home, 'index.html')

# ---------------- Games ----------------
# Old anchors that must keep working after a rename (links like /games/#old-id land on the renamed game).
OLD_ANCHORS = OLD_SLUGS   # in game_pages.py
def anchors(gid):
    return ''.join(f'<span id="{a}" aria-hidden="true"></span>' for a in OLD_ANCHORS.get(gid, []))
rows = ''.join(f'''<article class="game-row" id="{g[0]}">{anchors(g[0])}
<figure class="game-media shot" style="margin:0;box-shadow:var(--shadow);border-color:var(--line)">{img(g[0], g[7], eager=i<2, sizes="(max-width:820px) 100vw, 560px")}</figure>
<div><span class="tag">{E(g[2])}</span><h2 style="font-size:1.7rem"><a class="card-link" href="/games/{g[0]}/">{E(g[1])}</a></h2><p><strong>{E(g[5])}</strong></p><p class="muted">{E(g[6])}</p>
<dl><dt>Best for</dt><dd>{E(g[3])}</dd><dt>Players</dt><dd>{E(g[4])}</dd></dl>
<p style="margin:18px 0 0"><a class="btn btn-navy btn-sm" href="/games/{g[0]}/">How to play {E(g[1])}</a></p></div>
</article>''' for i, g in enumerate(GAMES))
jump = ''.join(f'<li><a href="/games/{g[0]}/">{E(g[1])}</a></li>' for g in GAMES)
games = f'''<div class="page-head"><div class="wrap">
<p class="eyebrow">The collection</p><h1>All the games</h1>
<p class="lead">Every game is built for one classroom screen and the whole class. Each one includes saved question banks, team rosters, a tick-box question picker and automatic reshuffling. Open any game for a step-by-step guide to playing it.</p>
<ul class="toc">{jump}</ul></div></div>
<section style="padding-top:20px"><div class="wrap">{rows}</div></section>
<section class="alt"><div class="wrap"><h2>Included in every game</h2>
<div class="grid g3" style="margin-top:20px">
<div class="feature"><h3>Saved question banks</h3><p class="muted">Load, edit, save and reuse banks, or paste rows straight from a spreadsheet.</p></div>
<div class="feature"><h3>Question picker</h3><p class="muted">Select all, or untick individual questions or whole categories before you start.</p></div>
<div class="feature"><h3>Team rosters</h3><p class="muted">Save each class once and use a fair student picker during play.</p></div>
<div class="feature"><h3>Automatic reshuffle</h3><p class="muted">No question repeats until all have been used.</p></div>
<div class="feature"><h3>Display options</h3><p class="muted">Light, dark and high-contrast themes, big text, large buttons and full screen.</p></div>
<div class="feature"><h3>Your Drive, your data</h3><p class="muted">Questions and rosters are saved in a spreadsheet in your own Google Drive.</p></div>
</div></div></section>
{CTA}'''
page('/games/', 'The games', 'Whole-class review games for the classroom screen: Brain Board Blitz, Million Point Climb, Forbidden Words, Review Recess Word Magnets, Word Scramble and more.', games, 'games/index.html')
# ---------------- Game pages (/games/<slug>/) ----------------
# All wording lives in tools/game_pages.py. Links (TpT, free version) live in assets/js/config.js.
def crumbs(items):
    lis = ''.join((f'<li><a href="{h}">{E(t)}</a></li>' if h else f'<li aria-current="page">{E(t)}</li>') for h, t in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>'

def shot_img(key, alt, eager=False, sizes='(max-width:620px) 100vw, (max-width:900px) 50vw, 360px'):
    return img(key, alt, eager=eager, sizes=sizes)

def ol(items, start):
    return f'<ol class="steps" start="{start}">' + ''.join(f'<li data-n="{start + i}">{E(x)}</li>' for i, x in enumerate(items)) + '</ol>'

def game_page(g):
    slug, name, short = g['slug'], g['name'], g['short']
    path = f'/games/{slug}/'
    url = DOMAIN + path
    main_key, main_src, main_alt, main_cap = g['shots'][0]
    tpt = (f'<a class="btn btn-gold" data-link="TPT_GAME_URLS.{slug}" data-fallback="TPT_STORE_URL" aria-disabled="true">'
           f'Get it on TpT<span class="soon">Coming soon</span></a>')
    free = (f'<a class="btn btn-ghost" data-link="FREE_VERSION_URLS.{slug}" data-optional hidden aria-disabled="true">'
            f'Try the free version<span class="soon">Coming soon</span></a>')
    glance = (f'<dl class="glance"><dt>Grades</dt><dd>{E(g["grades"])}</dd><dt>Subjects</dt><dd>{E(g["subjects"])}</dd>'
              f'<dt>Group size</dt><dd>{E(g["players"])}</dd><dt>Time</dt><dd>{E(g["time"])}</dd></dl>')
    intro = ''.join(f'<p class="lead">{E(p)}</p>' if i == 0 else f'<p class="muted">{E(p)}</p>' for i, p in enumerate(g['intro']))
    n1, n2 = len(g['setup']), len(g['setup']) + len(g['round'])
    how = (f'<h3>Set up the game</h3>{ol(g["setup"], 1)}<h3>Play a round</h3>{ol(g["round"], n1 + 1)}'
           f'<h3>Scoring and winning</h3>{ol(g["scoring"], n2 + 1)}')
    gallery = ''.join(f'<figure class="shot shot-light">{shot_img(k, a)}<figcaption>{E(c)}</figcaption></figure>' for k, s, a, c in g['shots'][1:])
    badge = '<span class="badge-full">Full version</span>'
    feat = lambda items: ''.join(f'<div class="feature{" feature-full" if x[2:] else ""}"><h3>{E(x[0])}{badge if x[2:] else ""}</h3>'
                                 f'<p class="muted">{E(x[1])}</p></div>' for x in items)
    tips = ''.join(f'<li>{E(t)}</li>' for t in g['tips'])
    ideas = ''.join(f'<div class="card idea"><h3>{E(k)}</h3><p class="muted" style="margin:0">{E(v)}</p></div>' for k, v in g['subject_ideas'].items())
    need = ''.join(f'<div class="card"><h3>{E(t)}</h3><p class="muted" style="margin:0">{E(d)}</p></div>' for t, d in NEED)
    full_extra = f' {E(g["full_extra"])}' if g.get('full_extra') else ''
    free_extra = f' {E(g["free_extra"])}' if g.get('free_extra') else ''
    faq = ''.join(f'<details><summary>{E(q_)}</summary><div class="a"><p>{E(a)}</p></div></details>' for q_, a in g['faq'])
    rel = ''.join(game_card(next(x for x in GAMES if x[0] == r), h='h3') for r in g['related'])
    toc = [('how-to-play', 'How to play'), ('modes', 'Modes & settings'), ('tips', 'Teacher tips'),
           ('what-you-need', 'What you need'), ('versions', 'Free & full version'), ('faq', 'FAQ'), ('related', 'Related games')]
    toc_html = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc)
    body = f'''{crumbs([('/', 'Home'), ('/games/', 'Games'), (None, name)])}
<div class="page-head game-head"><div class="wrap game-hero">
<div>
<p class="eyebrow">{E(g["tag"])}</p>
<h1>{E(g["h1"])}</h1>
{intro}
<div class="btn-row" style="margin-top:22px">{tpt}{free}<a class="btn btn-ghost" href="#how-to-play">How to play</a></div>
</div>
<div><figure class="shot shot-light" style="margin:0">{shot_img(main_key, main_alt, eager=True, sizes="(max-width:900px) 100vw, 520px")}<figcaption>{E(main_cap)}</figcaption></figure>
{glance}</div>
</div>
<div class="wrap"><ul class="toc" aria-label="On this page">{toc_html}</ul></div></div>

<section id="how-to-play"><div class="wrap grid g2 how">
<div class="prose"><p class="eyebrow">Step by step</p><h2>How to play {E(short)}</h2>{how}</div>
<div class="gallery">{gallery}</div>
</div></section>

<section class="alt" id="modes"><div class="wrap">
<p class="eyebrow">Make it fit your class</p><h2>{E(short)} modes, settings and options</h2>
<div class="grid g3" style="margin-top:22px">{feat(g["modes"])}{feat(g["settings"])}</div>
<p class="small muted" style="margin:22px 0 0">Every Review Recess game also has light, dark and high-contrast themes, big text, large buttons and full screen, plus a tick-box question picker and an automatic reshuffle so no question repeats until all have been used.</p>
</div></section>

<section id="tips"><div class="wrap grid g2" style="gap:40px">
<div class="prose"><p class="eyebrow">From the classroom</p><h2>Tips for teachers</h2><ul class="ticks">{tips}</ul></div>
<div><p class="eyebrow">Ideas by subject</p><h2>Ways to use it across the curriculum</h2><div class="grid g2 ideas" style="margin-top:18px">{ideas}</div></div>
</div></section>

<section class="alt" id="what-you-need"><div class="wrap">
<p class="eyebrow">Before you start</p><h2>What you need</h2>
<div class="grid g3" style="margin-top:22px">{need}</div>
<div class="grid g2" id="versions" style="margin-top:40px">
<div class="card"><h3>Free version</h3><p class="muted">{E(FREE_TEXT)}{free_extra}</p><div class="btn-row">{free.replace('btn-ghost', 'btn-navy')}<span class="small muted" data-free-note>The free version for this game is coming soon.</span></div></div>
<div class="card version-full"><h3>Full version</h3><p class="muted">{E(FULL_TEXT)}{full_extra}</p><p class="muted">{E(BUNDLE_TEXT)}</p><div class="btn-row">{tpt}</div></div>
</div>
</div></section>

<section id="faq"><div class="wrap prose faq">
<p class="eyebrow">Questions</p><h2>{E(short)} FAQ</h2>{faq}
<div class="card" style="margin-top:26px"><h3>Need help getting started?</h3><p class="muted">Opening your game link, Google permissions and school accounts are all covered on our help page.</p><div class="btn-row"><a class="btn btn-navy" href="/help/">Help &amp; Support</a></div></div>
</div></section>

<section class="alt" id="related"><div class="wrap">
<p class="eyebrow">Keep exploring</p><h2>Related games</h2>
<div class="grid g3" style="margin-top:22px">{rel}</div>
<p style="margin:26px 0 0"><a href="/games/">See all the games →</a></p>
</div></section>
<section class="cta on-navy"><div class="wrap">
<p class="eyebrow">Ready to play {E(short)}?</p>
<h2>Get {E(short)} on Teachers Pay Teachers</h2>
<p class="lead" style="margin:0 auto 26px">Every game, bundle and question pack is sold through our TpT store.</p>
<div class="btn-row">{tpt}<a class="btn btn-ghost" href="/help/">Installation help</a></div>
</div></section>'''
    img_abs = f'{DOMAIN}/assets/img/games/{main_key}-1200.webp'
    jsonld = [{
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': g['title'], 'description': g['description'],
             'inLanguage': 'en-US', 'isPartOf': {'@type': 'WebSite', 'name': 'Review Recess', 'url': DOMAIN + '/'},
             'primaryImageOfPage': {'@type': 'ImageObject', 'url': img_abs, 'width': 1200, 'height': 675},
             'breadcrumb': {'@id': url + '#breadcrumb'}, 'about': {'@id': url + '#game'}},
            {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Games', 'item': DOMAIN + '/games/'},
                {'@type': 'ListItem', 'position': 3, 'name': name, 'item': url}]},
            {'@type': 'SoftwareApplication', '@id': url + '#game', 'name': name, 'description': g['description'],
             'applicationCategory': 'EducationalApplication', 'applicationSubCategory': 'Classroom review game',
             'operatingSystem': 'Web browser', 'image': img_abs, 'url': url, 'inLanguage': 'en-US',
             'audience': {'@type': 'EducationalAudience', 'educationalRole': 'teacher'},
             'educationalLevel': g['grades'], 'publisher': {'@type': 'Organization', 'name': 'Review Recess', 'url': DOMAIN + '/'}},
            {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
                {'@type': 'Question', 'name': q_, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q_, a in g['faq']]},
        ]}]
    page(path, g['title'], g['description'], body, f'games/{slug}/index.html',
         og_image=f'/assets/img/og/{slug}.jpg', og_alt=main_alt, og_type='article', jsonld=jsonld)

for _g in GAME_PAGES:
    game_page(_g)


# ---------------- game-pages-copy.md (all game-page wording in one file for review) ----------------
def write_copy_md():
    L = ['# Review Recess game pages: all copy for review', '',
         f'Generated by tools/build.py from tools/game_pages.py on {LASTMOD}. Edit the wording in tools/game_pages.py, then rebuild.', '',
         '## Shared sections (on every game page)', '', '### What you need']
    L += [f'- **{t}.** {d}' for t, d in NEED]
    L += ['', '### Free version', FREE_TEXT, '', '### Full version', FULL_TEXT, '', BUNDLE_TEXT, '',
          '### Buttons', '- "Get it on TpT": TPT_GAME_URLS[slug] in config.js, else TPT_STORE_URL, else a grey Coming soon badge.',
          '- "Try the free version": FREE_VERSION_URLS[slug] in config.js. Hidden while blank.', '- "Help & Support" (/help/) and 3 related games.', '']
    for g in GAME_PAGES:
        L += ['---', '', f'## {g["name"]}', '', f'**URL:** {DOMAIN}/games/{g["slug"]}/  ',
              f'**Title tag:** {g["title"]}  ', f'**Meta description ({len(g["description"])} characters):** {g["description"]}  ',
              f'**H1:** {g["h1"]}  ', f'**Tag:** {g["tag"]}', '', '### Intro'] + [p + '\n' for p in g['intro']]
        L += ['### At a glance', f'- Grades: {g["grades"]}', f'- Subjects: {g["subjects"]}', f'- Group size: {g["players"]}', f'- Time: {g["time"]}', '']
        n = 1
        L += [f'### How to play {g["short"]}']
        for head, key in (('Set up the game', 'setup'), ('Play a round', 'round'), ('Scoring and winning', 'scoring')):
            L += ['', f'**{head}**']
            for x in g[key]: L.append(f'{n}. {x}'); n += 1
        L += ['', '### Modes, settings and options'] + [f'- **{x[0]}:**{" *(Full version badge)*" if x[2:] else ""} {x[1]}' for x in g['modes'] + g['settings']]
        L += ['', '### Tips for teachers'] + [f'- {t}' for t in g['tips']]
        L += ['', '### Ideas by subject'] + [f'- **{k}:** {v}' for k, v in g['subject_ideas'].items()]
        if g.get('free_extra'): L += ['', f'**Free version, extra line:** {g["free_extra"]}']
        if g.get('full_extra'): L += ['', f'**Full version, extra line:** {g["full_extra"]}']
        L += ['', '### FAQ']
        for q_, a in g['faq']: L += [f'**Q: {q_}**  ', f'A: {a}', '']
        L += ['### Screenshots (alt text, then caption)'] + [f'- `{k}`: {a} *Caption:* {c}' for k, s_, a, c in g['shots']]
        L += ['', '### Related games: ' + ', '.join(GP[r]['name'] for r in g['related']), '']
    open(os.path.join(OUT, '..', 'game-pages-copy.md'), 'w', encoding='utf-8').write('\n'.join(L))
write_copy_md()

# ---------------- Help ----------------
def q(qid, question, answer):
    return f'<details id="{qid}"><summary>{question}</summary><div class="a">{answer}</div></details>'
EMAIL_TXT = '<span data-text="CONTACT_EMAIL">our support email (coming soon)</span>'
faq_start = ''.join([
 q('what-you-need','What do I need to run a game?','<ul><li>A Google account you already have. A personal one works if your school blocks the games.</li><li>A computer connected to your smart TV or projector.</li><li>An up-to-date browser. Chrome works best.</li></ul><p>Students don\'t need accounts or devices. The whole game runs on your screen.</p>'),
 q('open-link','How do I open my game?','<ol><li>Open the PDF in your TpT download.</li><li>Click the game link while you are signed in to Google.</li><li>The first time, Google asks you to allow access (see below). After that, the game opens straight away.</li><li>Bookmark the page so it\'s one click next lesson.</li></ol><p>The first time a game opens, it creates its own spreadsheet in your Google Drive with sample questions and a sample class, so you can try it immediately.</p>'),
 q('copy','Do I need to make a copy of anything?','<p>No. The game runs from the link, in your own Google account. You don\'t need to copy a file, install anything, or open a script editor. Your questions are kept in the spreadsheet the game creates in <em>your</em> Drive, and you can open that spreadsheet from inside the game to edit questions in bulk.</p>'),
 q('several-accounts','The link shows an error or a blank page. What should I try?','<p>The most common cause is being signed in to more than one Google account in the same browser. Google can get confused about which account is opening the game.</p><ul><li>Open the link in a private or incognito window and sign in with just one account, <strong>or</strong></li><li>Create a separate Chrome profile for the account you use for games.</li></ul><p>Also check that you\'re signed in at all, and try reloading the page once.</p>'),
])
faq_perm = ''.join([
 q('permissions','What permission does the game ask for, and why?','<p>Each game asks for one Google Drive permission. Google describes it as access to <em>only the specific Google Drive files you use with this app</em>. In practice that means the game can only reach the spreadsheet it creates for your questions and rosters.</p><p>It <strong>can\'t</strong> see, read or change any of your other Drive files, your email or your contacts. (In technical terms, this is the <code>drive.file</code> scope.)</p>'),
 q('warning-screen','Google shows a warning screen before I can continue. Is that normal?','<p>Google can show an extra screen the first time you allow a small independent app. If you see one, check that it names the game you bought, click <strong>Advanced</strong>, then the option to go to the game, and then <strong>Allow</strong>. If anything on the screen asks for more than access to the files the app creates, stop and contact us.</p>'),
 q('school-blocked','My school account says the app is blocked. What can I do?','<p>Some school districts block apps like these on school Google accounts. You have two options:</p><ol><li><strong>Use a personal Google account you already have.</strong> If your school allows it, sign in with that account and open the link there. Your question banks will be saved in that account\'s Drive. Students still need nothing.</li><li><strong>Ask your IT team</strong> whether they can allow the app for your account.</li></ol><p>If you use a personal account, follow your school\'s rules about what can be stored in it. Team names and first names are usually all a game needs.</p>'),
 q('where-data','Where are my questions and rosters saved?','<p>In a spreadsheet in your own Google Drive, for example <em>"Letter Lifeline – Word Banks"</em>, with tabs for questions and rosters. Each teacher gets their own private copy. We never see it, and other teachers can\'t see it either.</p><p>If you delete that spreadsheet, the game builds a fresh one with the samples the next time you open it.</p>'),
])
faq_play = ''.join([
 q('picker','How do I choose which questions are used?','<p>On the setup screen, click <strong>Choose…</strong> next to the question count. Every question is ticked by default. Use <strong>Select all</strong> or <strong>Clear all</strong>, filter by a word, or untick single questions or whole categories, then click <strong>Done</strong>.</p><p>Your selection is remembered in that browser on that computer, so the classroom PC remembers it for next lesson. If a selection is too small to play well, the game warns you before you start.</p>'),
 q('own-questions','How do I add my own questions?','<p>Open <strong>Questions &amp; Teams</strong> in the game. You can type questions in, or copy rows from Google Sheets or Excel and paste them in. Each game\'s PDF shows the exact format, and you can save as many banks as you like.</p>'),
 q('projector','How do I make the game easier to read on a projector?','<p>Open <strong>Display</strong> (bottom left) and try the <strong>High contrast</strong> theme, <strong>Big text</strong> and <strong>Large buttons</strong>. Use <strong>Full screen</strong>, or press <kbd>F11</kbd> if your browser blocks it.</p>'),
 q('run-out','What happens when we run out of questions?','<p>Nothing breaks. The game reshuffles the bank and keeps going, and it never starts a new cycle with the question you just asked.</p>'),
])
help_ = f'''<div class="page-head"><div class="wrap">
<p class="eyebrow">Help &amp; Support</p><h1>Installation help and answers</h1>
<p class="lead">Most questions are answered below. For step-by-step help getting a game running, use the installation assistant.</p>
<div class="btn-row" style="margin-top:22px">{btn("SUPPORT_CHATBOT_URL","Open the installation assistant","btn-navy")}<a class="btn btn-ghost" data-link="CONTACT_EMAIL" aria-disabled="true">Email support<span class="soon">Coming soon</span></a></div>
<ul class="toc" aria-label="Help topics"><li><a href="#getting-started">Getting started</a></li><li><a href="#permissions-accounts">Permissions &amp; school accounts</a></li><li><a href="#in-class">Using the games in class</a></li><li><a href="#contact">Still stuck?</a></li></ul>
</div></div>
<section style="padding-top:44px"><div class="wrap prose faq">
<h2 id="getting-started" style="margin-top:0">Getting started</h2>{faq_start}
<h2 id="permissions-accounts">Permissions &amp; school accounts</h2>{faq_perm}
<h2 id="in-class">Using the games in class</h2>{faq_play}
<h2 id="contact">Still stuck?</h2>
<div class="card"><p>Try the installation assistant first. It walks you through the most common fixes. If that doesn't solve it, email us at {EMAIL_TXT} with the game name, the browser you're using and a screenshot of any error message.</p>
<div class="btn-row">{btn("SUPPORT_CHATBOT_URL","Open the installation assistant","btn-navy")}</div>
<p class="small muted" style="margin:14px 0 0">Bought on TpT? You can also message us through the Q&amp;A tab on the product page.</p></div>
</div></section>'''
page('/help/', 'Help & Support', 'Installation help for Review Recess games: opening your game link, Google permissions explained, what to do if your school account blocks the app, and classroom tips.', help_, 'help/index.html')

# ---------------- About ----------------
about = f'''<div class="page-head"><div class="wrap"><p class="eyebrow">About</p><h1>Made by a teacher, for the classroom screen</h1>
<p class="lead">Review Recess makes whole-class review games that are quick to set up, easy to read from the back of the room, and built around your own questions.</p></div></div>
<section><div class="wrap prose">
<!-- PHIL: personalise this paragraph (who you are, what you teach) if you'd like. Keep it true. -->
<p>Review Recess started in a real classroom. Each game was built by a working teacher who wanted review time to involve the whole class, not just the few students who answer first, and who was tired of rebuilding slide decks for every unit.</p>
<h2>What we care about</h2>
<ul>
<li><strong>Teacher control.</strong> You decide which questions are used, how teams are formed and when to move on.</li>
<li><strong>Reuse.</strong> A question bank you build once should keep working, term after term.</li>
<li><strong>Privacy.</strong> The games run in your own Google account. Your questions and class lists stay in your Drive, not ours.</li>
<li><strong>Human-written content.</strong> Our question packs are written by a teacher and follow the units teachers already teach.</li>
</ul>
<h2>Where to find us</h2>
<p>Our games and question packs are sold through Teachers Pay Teachers. For help, visit <a href="/help/">Help &amp; Support</a> or email {EMAIL_TXT}.</p>
<div class="btn-row">{btn("TPT_STORE_URL","Visit our TpT store")}<a class="btn btn-ghost" data-link="YOUTUBE_URL" aria-disabled="true">Watch on YouTube<span class="soon">Coming soon</span></a></div>
</div></section>'''
page('/about/', 'About', 'Review Recess makes whole-class review games for U.S. classrooms, built by a teacher around your own questions and your own Google Drive.', about, 'about/index.html')

# ---------------- Privacy ----------------
privacy = f'''<div class="page-head"><div class="wrap"><p class="eyebrow">Policies</p><h1>Privacy</h1><p class="lead">The short version: this website doesn't track you, and our games don't send us your students' information.</p><p class="small muted">Last updated: October 20, 2026</p></div></div>
<section><div class="wrap prose">
<h2 style="margin-top:0">This website</h2>
<ul>
<li>We don't use analytics, advertising or tracking cookies, and we don't set any cookies.</li>
<li>We don't load fonts, scripts or trackers from other companies.</li>
<li>There are no forms or accounts on this site, so we don't collect personal information here.</li>
<li>Like any website host, our hosting provider may keep standard technical logs (such as IP address and pages requested) to keep the site secure and running.</li>
<li>If you email us, we use your email only to reply to you.</li>
</ul>
<h2>The games</h2>
<ul>
<li>Each game is a Google Apps Script web app that runs in <strong>your own Google account</strong>.</li>
<li>Your question banks and class rosters are saved in a spreadsheet in <strong>your own Google Drive</strong>. They are not sent to us, and we can't see them.</li>
<li>The games ask for only one Google permission: access to the files the game itself creates. They can't read your other Drive files, your email or your contacts.</li>
<li>Some preferences (such as display theme and which questions you have unticked) are saved in your browser's local storage on that computer. They never leave your device.</li>
<li>Google's own terms and privacy policy apply to your Google account.</li>
</ul>
<p><strong>Tip for teachers:</strong> games only need team names or first names. Please follow your school's rules about student information.</p>
<h2>Live mode (coming soon)</h2>
<p>Live mode is not available yet. When it launches, students will join by scanning a QR code with no login, and nothing will be stored after the session ends. We'll update this page with the full details before live mode goes live.</p>
<h2>Teachers Pay Teachers</h2>
<p>Purchases are handled by Teachers Pay Teachers under its own privacy policy. We receive the order information TpT shares with sellers, not your payment details.</p>
<h2>Questions</h2>
<p>Email {EMAIL_TXT}.</p>
</div></section>'''
page('/privacy/', 'Privacy', 'Review Recess privacy: no tracking cookies on this website, and games that run in your own Google account so student data never comes to us.', privacy, 'privacy/index.html')

# ---------------- Terms ----------------
terms = f'''<div class="page-head"><div class="wrap"><p class="eyebrow">Policies</p><h1>Terms &amp; licence</h1><p class="lead">A plain-language summary of how you can use Review Recess products.</p><p class="small muted">Last updated: October 20, 2026</p></div></div>
<section><div class="wrap prose">
<h2 style="margin-top:0">Your licence</h2>
<ul>
<li>Each purchase is for <strong>one teacher</strong> to use with their own classes, year after year.</li>
<li>Colleagues need their own licence. Additional licences can be bought on TpT, usually at a discount.</li>
<li>Please don't share game links, download files or question packs outside your licence, or post them on public websites.</li>
<li>You may not resell, redistribute or copy the games or packs, in whole or in part.</li>
</ul>
<h2>Your content</h2>
<p>Questions and rosters you create are yours. They are stored in your own Google Drive.</p>
<h2>Updates and availability</h2>
<p>We improve the games over time and may change features. The games depend on Google services, which are outside our control. If something stops working, contact us and we'll help.</p>
<h2>No warranty</h2>
<p>The games are provided as they are. Always preview a game before using it with a class.</p>
<h2>Purchases and refunds</h2>
<p>Purchases are made on Teachers Pay Teachers and are covered by TpT's terms, including its refund policy.</p>
<h2>Trademarks</h2>
<p>AP® is a trademark registered by the College Board, which is not affiliated with, and does not endorse, this product. Other names are trademarks of their owners.</p>
<h2>Contact</h2>
<p>Email {EMAIL_TXT}.</p>
</div></section>'''
page('/terms/', 'Terms & licence', 'Terms of use and licence summary for Review Recess classroom games and question packs.', terms, 'terms/index.html')

# ---------------- 404 ----------------
nf = '''<section class="nf"><div class="wrap"><p class="eyebrow">Error 404</p><h1>We can't find that page</h1>
<p class="lead" style="margin:0 auto 26px">It may have moved. Try one of these instead.</p>
<div class="btn-row"><a class="btn btn-navy" href="/">Home</a><a class="btn btn-ghost" href="/games/">Games</a><a class="btn btn-ghost" href="/help/">Help &amp; Support</a></div></div></section>'''
page('/404', 'Page not found', 'This page could not be found.', nf, '404.html', noindex=True)

# ---------------- sitemap / robots ----------------
urls = ['/', '/games/'] + [f'/games/{g[0]}/' for g in GAMES] + ['/help/', '/about/', '/privacy/', '/terms/']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  ''.join(f'  <url><loc>{DOMAIN}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'favicon.svg'), 'w').write(MARK.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true" focusable="false"', ''))
print('built', OUT)
