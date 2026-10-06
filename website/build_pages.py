#!/usr/bin/env python3
"""Build focused static pages from retained editorial sections, without editing research data."""
from html import escape
from html.parser import HTMLParser
import json
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
THEMES = {"prediction": "prediction.html", "intervention": "intervention.html", "twin": "digital-twins.html", "interface": "mixed-reality.html"}
NAV = [("index.html", "Home"), ("columns.html", "Research columns"), ("guide.html", "Research guide"), ("evidence.html", "Evidence"), ("library.html", "Library")]


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


def theme_cards(payload):
    takeaways = {
        "prediction": "New models, biosignals and longer health histories. Compare what they can predict and how they are evaluated.",
        "intervention": "Causal methods, alternative actions and intervention trials. See what changed outcomes—and what did not.",
        "twin": "Individual simulations, repeated updates and personalized feedback. Distinguish working components from proposed frameworks.",
        "interface": "First-person data, muscle-signal input and wearable products. Separate research capabilities from product announcements.",
    }
    cards = []
    for r in payload["routes"]:
        accepted = payload["route_counts"]["accepted"][r["id"]]["total"]
        watchlist = payload["route_counts"]["watchlist"][r["id"]]["total"]
        cards.append(f'<a class="directory-card" href="{THEMES[r["id"]]}" style="--theme:{r["color"]}"><span>COLUMN {r["number"]}</span><h3>{escape(r["label"])}</h3><p>{takeaways[r["id"]]}</p><small>{accepted} accepted · {watchlist} watchlist · related work labelled separately</small><b>Read trends &amp; paper timeline →</b></a>')
    return '<div class="page-directory">' + "".join(cards) + '</div>'


def build():
    source = (ROOT / "templates/editorial.html").read_text()
    fragments = Fragments(source).parts
    research = (ROOT / "research-map.html").read_text()
    data_match = re.search(r'<script id="research-data" type="application/json">(.*?)</script>', research, re.S)
    payload = json.loads(data_match.group(1))
    head = source[source.index("<head>"):source.index("</head>") + len("</head>")]
    footer = fragments[".site-footer"]
    shelf = fragments["detail-shelf"] + '<div class="shelf-backdrop" hidden></div>'
    cards = theme_cards(payload)
    resource_panels = [("lifecycle", "Lifecycle matrix", ".matrix-card"), ("families", "Research families", ".family-browser-card"), ("datasets", "Datasets", ".dataset-table-card"), ("evidence", "Evidence crosswalk", ".evidence-crosswalk-card"), ("watchlist", "Watchlist", ".watchlist-card"), ("downloads", "Downloads", ".resource-hub-card")]
    resource_tabs = '<nav class="page-shortcuts resource-tabs" aria-label="Comparison pages">' + ''.join(f'<a href="compare.html?panel={key}">{label}</a>' for key,label,_ in resource_panels) + '</nav>'
    comparisons = '<section class="comparison-section"><div class="comparison-grid">' + ''.join(fragments[cls].replace('<article ', f'<article data-comparison-panel="{key}" ' + ('' if key=='lifecycle' else 'hidden '), 1) for key,_,cls in resource_panels) + '</div></section>'
    landing = '<section class="home-directory" aria-labelledby="home-columns"><p class="eyebrow">CHOOSE A RESEARCH COLUMN</p><h2 id="home-columns">Four topics. Clear updates. Every catalog record.</h2><p>Read the direction of research, then browse papers by year. The four columns cover all 396 accepted and 45 watchlist records.</p>' + cards + '</section>'
    guide_links = '<nav class="page-shortcuts" aria-label="Research guide pages"><a href="guide.html">Lifecycle &amp; taxonomy</a><a href="story.html">Animated explanation</a><a href="models.html">Sensor &amp; model families</a><a href="history.html">Research through time</a></nav>'
    scene_links = '<nav class="page-shortcuts story-chapters" aria-label="Jump to a story chapter">' + ''.join(f'<a href="#{key}">{label}</a>' for key,label in [('signals','01 Signals'),('representations','02 Learned features'),('lifecycle-story','03 Lifecycle'),('resource-types-story','04 Resource types'),('evidence','05 Evidence'),('review-depth-story','06 Review depth')]) + '</nav>'
    pages = {
        "index.html": ("Wearable AI research & technology updates", fragments["overview"] + landing),
        "columns.html": ("Four research columns", banner("Four research columns", "Choose your topic. Each column has its own page, a research summary and a searchable paper timeline.") + '<section class="directory-section">' + cards + '<p class="directory-note">Source updates reviewed 4 Oct 2026. Accepted papers, watchlist candidates and product announcements remain clearly separated.</p></section>'),
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
        title = next(r['label'] for r in payload['routes'] if r['id'] == theme)
        column = re.sub(r'<div class="columns-intro">.*?</div>', '<div class="columns-intro"><p class="columns-kicker"><a href="columns.html">RESEARCH COLUMNS</a> / ' + escape(title.upper()) + '</p><p id="columns-coverage" class="columns-coverage"></p></div>', column, count=1, flags=re.S)
        column = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' · Awesome Wearable AI</title>', column, count=1)
        column = column.replace('</head>', f'<link rel="canonical" href="https://zipengwu365.github.io/awesome-wearable-ai/{filename}"></head>', 1)
        (ROOT / filename).write_text(version_assets(column))
    print(f"Built {len(pages) + len(THEMES)} focused pages; all original research data unchanged")


if __name__ == '__main__':
    build()
