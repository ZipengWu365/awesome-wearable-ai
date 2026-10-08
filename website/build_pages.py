#!/usr/bin/env python3
"""Build focused static pages from retained editorial sections, without editing research data."""
from html import escape
from html.parser import HTMLParser
import json
import hashlib
from pathlib import Path
import re
from datetime import date
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
THEMES = {"prediction": "prediction.html", "intervention": "intervention.html", "twin": "digital-twins.html", "interface": "mixed-reality.html"}
THEME_LABELS = {"prediction": "Predicting health changes", "intervention": "Health actions and their effects", "twin": "Personal health models", "interface": "Wearable devices and mixed reality"}
NAV = [("index.html", "Home"), ("columns.html", "Research columns"), ("guide.html", "Research guide"), ("evidence.html", "Evidence"), ("library.html", "Library")]


def validate_editorial(editorial, payload):
    """Validate presentation-only briefs against actual repository IDs."""
    edited = date.fromisoformat(editorial['edited_on'])
    assert re.fullmatch(r'[0-9a-f]{40}', editorial['repository_commit']), 'Missing source revision'
    assert editorial['scope'].strip(), 'Missing scope'
    assert set(editorial['columns']) == set(THEMES), 'Exactly four columns required'
    known = {r['id'] for r in payload['records']} | {'signal-' + s['id'] for s in payload['radar']['signals']}
    for brief in editorial['columns'].values():
        for field in ('headline', 'summary', 'status', 'use', 'takeaway'):
            assert brief[field].strip(), f'Missing {field}'
        assert len(set(brief['ids'])) >= 2, 'A trend needs more than one supporting work'
        assert set(brief['ids']) <= known, 'Unknown trend source'
        assert len(brief['evolution']) >= 2, 'Research history needs comparisons'
        prior_end = 0
        source_years = {r['id']: r['year'] for r in payload['records']}
        source_years.update({'signal-' + s['id']: int(s['event_date'][:4]) for s in payload['radar']['signals']})
        for stage in brief['evolution']:
            assert prior_end < stage['start'] <= stage['end'] <= edited.year, 'Overlapping or invalid research periods'
            prior_end = stage['end']
            for field in ('headline', 'change', 'meaning', 'limit'):
                assert stage[field].strip(), f'Missing history {field}'
            assert stage['ids'] and set(stage['ids']) <= known, 'Unknown history source'
            assert all(stage['start'] <= source_years[id] <= stage['end'] for id in stage['ids']), 'History source outside stated period'
        assert len(brief['dimensions']) == 6
        assert {d['kind'] for d in brief['dimensions']} == {'Methods','Data','Hardware','Functions','Performance','New directions'}
        for dimension in brief['dimensions']:
            assert dimension['text'].strip()
            assert set(dimension['ids']) <= known, 'Unknown comparison source'
        assert len(brief['stories']) == 3
        assert len({s['id'] for s in brief['stories']}) == 3, 'Duplicate featured work'
        for story in brief['stories']:
            assert story['id'] in known, 'Unknown featured work'
            for field in ('name','date','headline','change','result','before','benefit','condition','locator'):
                assert story[field].strip(), f'Missing study {field}'
            source = urlsplit(story['source'])
            assert source.scheme == 'https' and source.netloc and not source.username and not source.password, 'Invalid source link'
            assert date.fromisoformat(story['checked_on']) <= edited, 'Source check after editorial date'
    return editorial


class Fragments(HTMLParser):
    """Find exact source spans without normalizing SVG, text or attributes."""
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer("\n", text))
        self.stack, self.parts = [], {}
        self.feed(text)

    def source_offset(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, self.source_offset(), attrs.get("id"), attrs.get("class", "")))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1][0] != tag:
            raise ValueError(f"Unbalanced source HTML: {tag} at {self.getpos()}")
        _, start, key, classes = self.stack.pop()
        source = self.text[start:self.text.index(">", self.source_offset()) + 1]
        if key:
            self.parts[key] = source
        for cls in classes.split():
            self.parts.setdefault("." + cls, source)


def header():
    links = "".join(f'<a href="{url}">{label}</a>' for url, label in NAV)
    return f'''<header class="site-header">
<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Awesome Wearable AI</span></a>
<nav id="primary-navigation" aria-label="Primary navigation">{links}<a class="nav-github" href="https://github.com/ZipengWu365/awesome-wearable-ai" target="_blank" rel="noreferrer">GitHub ↗</a></nav>
<button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Open navigation">Menu</button></header>'''


def banner(title, text, parent="Home", parent_url="index.html"):
    return f'<div class="page-intro"><nav aria-label="Breadcrumb"><a href="{parent_url}">{parent}</a><span aria-hidden="true"> / </span><span>{title}</span></nav><h1>{title}</h1><p>{text}</p></div>'


def version_assets(html):
    for name in ('styles.css', 'navigation.css', 'navigation.js', 'app.js'):
        digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:12]
        html = html.replace(f'"{name}"', f'"{name}?v={digest}"')
    return html


def theme_cards(payload, editorial):
    cards = []
    for r in payload["routes"]:
        accepted = payload["route_counts"]["accepted"][r["id"]]["total"]
        watchlist = payload["route_counts"]["watchlist"][r["id"]]["total"]
        brief = editorial['columns'][r['id']]
        cards.append(f'<a class="directory-card" href="{THEMES[r["id"]]}" style="--theme:{r["color"]}"><span>COLUMN {r["number"]}</span><h3>{escape(THEME_LABELS[r["id"]])}</h3><p class="directory-trend">{escape(brief["headline"])}</p><p>{escape(brief["takeaway"])}</p><small>{accepted} resources in the collection. {watchlist} more awaiting review.</small><b>Read this research brief and all papers</b></a>')
    return '<div class="page-directory">' + "".join(cards) + '</div>'


def build():
    source = (ROOT / "templates/editorial.html").read_text()
    fragments = Fragments(source).parts
    research = (ROOT / "research-map.html").read_text()
    data_match = re.search(r'<script id="research-data" type="application/json">(.*?)</script>', research, re.S)
    payload = json.loads(data_match.group(1))
    editorial = validate_editorial(json.loads((ROOT / 'editorial-briefs.json').read_text()), payload)
    head = source[source.index("<head>"):source.index("</head>") + len("</head>")]
    footer = fragments[".site-footer"]
    shelf = fragments["detail-shelf"] + '<div class="shelf-backdrop" hidden></div>'
    cards = theme_cards(payload, editorial)
    resource_panels = [("lifecycle", "Lifecycle matrix", ".matrix-card"), ("families", "Research families", ".family-browser-card"), ("datasets", "Datasets", ".dataset-table-card"), ("evidence", "Evidence crosswalk", ".evidence-crosswalk-card"), ("watchlist", "Watchlist", ".watchlist-card"), ("downloads", "Downloads", ".resource-hub-card")]
    resource_tabs = '<nav class="page-shortcuts resource-tabs" aria-label="Comparison pages">' + ''.join(f'<a href="compare.html?panel={key}">{label}</a>' for key,label,_ in resource_panels) + '</nav>'
    comparisons = '<section class="comparison-section"><div class="comparison-grid">' + ''.join(fragments[cls].replace('<article ', f'<article data-comparison-panel="{key}" ' + ('' if key=='lifecycle' else 'hidden '), 1) for key,_,cls in resource_panels) + '</div></section>'
    landing = '<section class="home-directory" aria-labelledby="home-columns"><p class="eyebrow">CHOOSE A RESEARCH COLUMN</p><h2 id="home-columns">Explore wearable AI research in four topics</h2><p>Find out what researchers are working on and browse every paper by year. The collection contains 396 resources, with 45 more awaiting review. Resources include papers, datasets and research tools.</p>' + cards + '</section>'
    guide_links = '<nav class="page-shortcuts" aria-label="Research guide pages"><a href="guide.html">Lifecycle &amp; taxonomy</a><a href="story.html">Animated explanation</a><a href="models.html">Sensor &amp; model families</a><a href="history.html">Research through time</a></nav>'
    scene_links = '<nav class="page-shortcuts story-chapters" aria-label="Jump to a story chapter">' + ''.join(f'<a href="#{key}">{label}</a>' for key,label in [('signals','01 Signals'),('representations','02 Learned features'),('lifecycle-story','03 Lifecycle'),('resource-types-story','04 Resource types'),('evidence','05 Evidence'),('review-depth-story','06 Review depth')]) + '</nav>'
    pages = {
        "index.html": ("Wearable AI research & technology updates", fragments["overview"] + landing),
        "columns.html": ("Four research columns", banner("Four research columns", "Start with a short research brief: what is changing, which work supports it and why it matters for people building wearable technology. Then explore every paper by year.") + '<section class="directory-section">' + cards + '<p class="directory-note">Briefs edited 8 Oct 2026 using the current repository. Each study shows its own date and source-check date. These briefs summarise collected work, not every paper published this week. Resources include papers, datasets and tools; each has one main topic, without counting related links twice.</p></section>'),
        "guide.html": ("Research guide", banner("How wearable-AI research fits together", "Understand the lifecycle and technical roles before comparing individual studies.") + guide_links + fragments["reading-terms"] + fragments["taxonomy"]),
        "story.html": ("Animated research guide", banner("From body signals to decisions", "An optional visual explanation. Scroll through six scenes, or use the chapter links to go directly to a concept.", "Research guide", "guide.html") + guide_links + scene_links + fragments["story"]),
        "models.html": ("Sensor & model families", banner("Sensor & model families", "Browse the model landscape by signal and research family.", "Research guide", "guide.html") + guide_links + fragments["model-landscape"]),
        "history.html": ("Research through time", banner("Research through time", "A visual overview of the repository. For the full paper-by-paper history, open a research column.", "Research guide", "guide.html") + guide_links + fragments["research-map"]),
        "evidence.html": ("Evidence & study claims", banner("What does the evidence support?", "Compare study designs, claim types and the depth of the repository’s review.") + fragments["evidence-map"]),
        "library.html": ("Research library", banner("Search the research library", "Explore 396 accepted records in the interactive map or list. Use the columns for chronological reading and all 45 watchlist candidates.") + '<nav class="page-shortcuts" aria-label="Resource views"><a href="library.html">Interactive library</a><a href="compare.html">Comparison tables &amp; watchlist</a><a href="columns.html">Papers by research theme</a></nav>' + fragments["explore"]),
        "compare.html": ("Compare research resources", banner("Compare datasets, models and evidence", "Choose one focused table. The other views remain available from the navigation below.", "Library", "library.html") + resource_tabs + comparisons),
    }
    owners = {}
    for filename, (_, content) in pages.items():
        for key in re.findall(r'\bid="([^"]+)"', content):
            owners.setdefault(key, filename)
    owners.update({"intelligence": "columns.html", "trend-prediction": "prediction.html", "trend-intervention": "intervention.html", "trend-twin": "digital-twins.html", "trend-interface": "mixed-reality.html", "comparison-lab": "compare.html", "community": "columns.html"})

    def links(text, current):
        def anchor(m):
            key = m.group(1)
            if key == "top": return 'href="index.html"'
            target = owners.get(key)
            if not target or target == current: return m.group(0)
            fragment = "" if key in {"intelligence", "comparison-lab", "community"} or key.startswith("trend-") else "#" + key
            return f'href="{target}{fragment}"'
        text = re.sub(r'href="#([^\"]+)"', anchor, text)
        for theme, target in THEMES.items():
            text = text.replace('research-map.html?theme=' + theme, target)
            text = text.replace('research-map.html#assessment-' + theme, target)
        return text.replace('href="research-map.html"', 'href="columns.html"')

    for filename, (title, content) in pages.items():
        page_head = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' · Awesome Wearable AI</title>', head)
        url = 'https://zipengwu365.github.io/awesome-wearable-ai/' + ('' if filename == 'index.html' else filename)
        page_head = re.sub(r'(<link rel="canonical" href=")[^"]+', r'\g<1>' + url, page_head)
        page_head = re.sub(r'(<meta property="og:url" content=")[^"]+', r'\g<1>' + url, page_head)
        page_head = re.sub(r'(<meta property="og:title" content=")[^"]+', r'\g<1>' + escape(title), page_head)
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="navigation.css">\n</head>')
        intro_class = 'page-home' if filename == 'index.html' else 'page-interior'
        progress = '<div class="story-progress" aria-hidden="true"><span></span></div>' if filename == 'story.html' else ''
        old = '<script>window.ATLAS_ANCHOR_PAGES=' + json.dumps(owners) + ';</script>' if filename == 'index.html' else ''
        rendered = '<!doctype html>\n<html lang="en">\n' + page_head + f'\n<body class="{intro_class}" data-scene="0"><a class="skip-link" href="#page-content">Skip to page content</a>' + header() + progress + '<main id="page-content">' + links(content, filename) + '</main>' + links(footer, filename) + shelf + old + '<script src="navigation.js"></script><script src="app.js"></script></body></html>\n'
        (ROOT / filename).write_text(version_assets(rendered))

    # Dedicated routes, not one long page or a hash-based tab pretending to be a page.
    for theme, filename in THEMES.items():
        column = research.replace('<body>', f'<body data-column-page="{theme}">')
        column = re.sub(r'<header class="columns-header">.*?</header>', header(), column, count=1, flags=re.S)
        column = column.replace('<style>/* Full-page', '<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="navigation.css"><style>/* Full-page')
        column = column.replace('</body>', '<script src="navigation.js"></script></body>')
        title = THEME_LABELS[theme]
        column = re.sub(r'<div class="columns-intro">.*?</div>', '<div class="columns-intro"><p class="columns-kicker"><a href="columns.html">RESEARCH COLUMNS</a> / ' + escape(title.upper()) + '</p><p id="columns-coverage" class="columns-coverage"></p></div>', column, count=1, flags=re.S)
        column = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' · Awesome Wearable AI</title>', column, count=1)
        column = column.replace('</head>', f'<link rel="canonical" href="https://zipengwu365.github.io/awesome-wearable-ai/{filename}"></head>', 1)
        (ROOT / filename).write_text(version_assets(column))
    print(f"Built {len(pages) + len(THEMES)} focused pages; all original research data unchanged")


if __name__ == '__main__':
    build()
