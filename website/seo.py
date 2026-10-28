"""Deterministic public-page metadata and a readable registry source directory.

This module does not change existing pages or write files when imported.  The
website builder owns its page inventory and calls these helpers explicitly.
"""
from __future__ import annotations

from collections import Counter
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Mapping
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
BASE_URL = "https://zipengwu.me/awesome-wearable-ai/"
SITE_NAME = "Awesome Wearable AI"
SOCIAL_IMAGE = BASE_URL + "assets/images/hero-wearable-researcher-v3.png"
SOURCE_FILENAME = "sources.html"
SOURCE_TITLE = "Wearable AI sources & evidence directory"
THEME_PAGES = {
    "prediction": "prediction.html",
    "intervention": "intervention.html",
    "twin": "digital-twins.html",
    "interface": "mixed-reality.html",
}
ROLE_LABELS = {
    "direct": "Research", "support": "Enabler",
    "framework": "Framework", "adjacent": "Adjacent",
}
EVIDENCE_LABELS = {
    "peer_reviewed": "Peer reviewed", "preprint": "Preprint",
    "vendor_announcement": "Vendor announcement",
}


def canonical_url(filename: str) -> str:
    """Return a project URL, refusing paths, query strings and fragments."""
    if not isinstance(filename, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.html", filename):
        raise ValueError("A canonical page must be a local HTML filename")
    return BASE_URL + ("" if filename == "index.html" else filename)


def json_script(value: dict) -> str:
    """Serialize JSON safely inside an HTML script element."""
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


class _Tag(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.attributes = {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.attributes = {key.lower(): value for key, value in attrs}

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def page_head(head: str, filename: str, title: str, description: str, kind: str = "WebPage") -> str:
    """Replace inherited SEO tags in a complete head without changing its assets.

    Structured data describes the visible page, not a medical certification,
    dataset release or a promise of a Google rich result.
    """
    if not re.search(r"<head\b[^>]*>", head, re.I) or not re.search(r"</head\s*>\s*$", head, re.I):
        raise ValueError("page_head requires a complete head element")
    if not title.strip() or not description.strip():
        raise ValueError("A page needs a nonempty title and description")
    if kind not in {"WebPage", "CollectionPage"}:
        raise ValueError("Only WebPage or CollectionPage metadata is supported")
    url = canonical_url(filename)
    full_title = title.strip()
    if SITE_NAME.lower() not in full_title.lower():
        full_title += " · " + SITE_NAME
    head = re.sub(r"<title\b[^>]*>.*?</title\s*>\s*", "", head, flags=re.I | re.S)
    head = re.sub(r"<script\b(?=[^>]*\btype\s*=\s*['\"]application/ld\+json['\"])[^>]*>.*?</script\s*>\s*", "", head, flags=re.I | re.S)

    def retain_tag(match):
        tag = match.group(0)
        attrs = _Tag(tag).attributes
        name = str(attrs.get("name") or attrs.get("property") or "").lower()
        rel = str(attrs.get("rel") or "").lower().split()
        if name == "description" or name.startswith(("og:", "twitter:")) or "canonical" in rel:
            return ""
        return tag

    head = re.sub(r"<(?:meta|link)\b[^>]*>", retain_tag, head, flags=re.I)
    structured = {
        "@context": "https://schema.org", "@type": kind,
        "@id": url + "#webpage", "url": url,
        "name": full_title, "description": description.strip(), "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "#website", "url": BASE_URL, "name": SITE_NAME},
    }
    metadata = f'''<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description.strip(), quote=True)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{escape(full_title, quote=True)}">
<meta property="og:description" content="{escape(description.strip(), quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SOCIAL_IMAGE}">
<meta property="og:image:alt" content="Wearable AI research illustration">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(full_title, quote=True)}">
<meta name="twitter:description" content="{escape(description.strip(), quote=True)}">
<meta name="twitter:image" content="{SOCIAL_IMAGE}">
<meta name="twitter:image:alt" content="Wearable AI research illustration">
<script type="application/ld+json">{json_script(structured)}</script>
'''
    retained = re.sub(r"</head\s*>\s*$", "", head, flags=re.I).rstrip()
    retained = "\n".join(line.rstrip() for line in retained.splitlines())
    return retained + "\n" + metadata + "</head>"


def _safe_url(value) -> str | None:
    if not isinstance(value, str) or any(char.isspace() or ord(char) < 32 for char in value) or "\\" in value:
        return None
    try:
        parsed = urlsplit(value)
        _ = parsed.port
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            return None
    except ValueError:
        return None
    return value


def _link(url, label: str) -> str:
    checked = _safe_url(url)
    return f'<a href="{escape(checked, quote=True)}" rel="noreferrer">{escape(label)}</a>' if checked else ""


def _text_section(label: str, value) -> str:
    return f'<div><dt>{escape(label)}</dt><dd>{escape(str(value))}</dd></div>' if value not in (None, "", []) else ""


def _record(record: dict) -> str:
    record_id = record["id"]
    accepted = record["catalog_status"] == "accepted"
    status = "Accepted registry record" if accepted else "Watchlist candidate — not accepted"
    meta = " · ".join(str(value) for value in (record.get("year"), record.get("venue") or record.get("status"), record.get("record_type") or "candidate", ROLE_LABELS.get(record.get("route_role"), record.get("route_role")), record.get("subtopic")) if value)
    links = []
    if not record.get("link_withheld") and not record.get("source_issue"):
        links.append(_link(record.get("primary_url"), "Original source"))
    for key, label in (("code_url", "Code"), ("data_url", "Data"), ("project_url", "Project")):
        links.append(_link(record.get(key), label))
    warning = ""
    if record.get("link_withheld") or record.get("source_issue"):
        warning = '<p class="warning">Source link withheld: ' + escape(record.get("source_issue") or "The source identity requires correction.") + '</p>'
    if not accepted:
        warning += '<p class="warning">Watchlist classification does not upgrade publication or evidence status.</p>'
    fields = [
        ("Contribution", record.get("contribution")), ("Why it matters", record.get("why_it_matters")),
        ("Reported outcome", record.get("outcome_status")), ("Limitations", record.get("limitations")),
        ("Evidence boundary", record.get("evidence_boundary")), ("Watchlist reason", record.get("reason")),
        ("Review action", record.get("review_action")), ("Editorial placement", record.get("classification_reason")),
        ("Review note", record.get("review_note")),
    ]
    detail = "".join(_text_section(label, value) for label, value in fields)
    keywords = " · ".join(record.get("topic_keywords", []))
    keyword_line = f'<p class="keywords">{escape(keywords)}</p>' if keywords else ""
    return f'''<article class="record" id="record-{escape(record_id, quote=True)}" data-record-id="{escape(record_id, quote=True)}" data-catalog-status="{record['catalog_status']}">
<p class="status {'accepted' if accepted else 'watchlist'}">{status}</p>
<h3>{escape(record['title'])}</h3><p class="meta">{escape(meta)}</p>{keyword_line}
<p class="source-links">{' · '.join(link for link in links if link)}</p>{warning}
<details><summary>Contribution, evidence boundary &amp; original metadata</summary><dl>{detail}</dl>
<details><summary>Complete retained record</summary><pre>{escape(json.dumps(record, ensure_ascii=False, indent=2))}</pre></details>
</details></article>'''


def _signal(signal: dict, routes: dict, update_types: dict) -> str:
    meta = " · ".join((routes[signal["route"]]["short_label"], EVIDENCE_LABELS[signal["evidence_level"]], "Evidence baseline" if signal["temporal_role"] == "baseline" else "Dated update"))
    fields = [("Before", signal["before"]), ("What changed", signal["after"]), ("Evidence", signal["evidence"]), ("Availability", signal["availability"])]
    if signal.get("comparison"):
        fields += [("Comparison baseline", signal["comparison"]["baseline"]), ("Reported result", signal["comparison"]["result"]), ("Comparison conditions", signal["comparison"]["conditions"])]
    fields += [("Limits", signal["limit"]), ("Why it matters — editorial interpretation", signal["implication"])]
    sources = " · ".join(_link(source["url"], source["title"]) for source in signal["sources"])
    dates = " · ".join(f'{label} <time datetime="{escape(signal[key], quote=True)}">{escape(signal[key])}</time>' for key, label in (("event_date", "Event"), ("publication_date", "Published"), ("verified_on", "Source checked")))
    linked = " · ".join(f'<a href="#record-{escape(quote(record_id, safe=""), quote=True)}">{escape(record_id)}</a>' for record_id in signal["registry_ids"])
    scope = 'Existing registry links: ' + linked if linked else 'Separate intelligence item; not an accepted registry record and not counted in the library.'
    return f'''<article class="signal" id="signal-{escape(signal['id'], quote=True)}" data-signal-id="{escape(signal['id'], quote=True)}">
<p class="meta">{escape(meta)}</p><h3>{escape(signal['title'])}</h3><p class="meta">{dates}</p>
<p class="keywords">{escape(' · '.join(update_types[key] for key in signal['types']))} · {escape(' · '.join(signal['keywords']))}</p>
<dl>{''.join(_text_section(label, value) for label, value in fields)}</dl><p class="source-links">{sources}</p><p class="meta">{scope}</p></article>'''


STYLE = """
:root{color-scheme:light;--ink:#243443;--muted:#5d6d79;--line:#dce4e8;--paper:#fbfcfa}
*{box-sizing:border-box}html{scroll-padding-top:24px}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}a{color:#116675;text-underline-offset:3px}a:hover{color:#184450}a:focus-visible,summary:focus-visible{outline:3px solid #5266c8;outline-offset:4px}.skip{position:absolute;left:12px;top:-100px;background:#fff;padding:10px;z-index:3}.skip:focus{top:12px}.header{max-width:1200px;margin:auto;padding:22px 28px;display:flex;align-items:center;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line)}.brand{font-weight:650;color:var(--ink);text-decoration:none;white-space:nowrap}.header nav,.shortcuts{display:flex;gap:18px;flex-wrap:wrap}.header nav a{font-size:13px;color:var(--muted)}main{max-width:1200px;margin:auto;padding:36px 28px 60px}.intro{max-width:850px;margin-bottom:28px}.eyebrow{text-transform:uppercase;letter-spacing:.1em;font-size:11px;font-weight:650;color:#087f8c;margin:0 0 8px}h1{font-size:clamp(28px,3vw,38px);line-height:1.2;letter-spacing:-.7px;margin:0 0 14px}h2{font-size:24px;letter-spacing:-.4px;line-height:1.3;margin:0 0 12px}h3{font-size:17px;line-height:1.45;margin:0 0 6px;overflow-wrap:anywhere}p{margin:0 0 12px}.intro>p:not(.eyebrow){color:var(--muted)}.scope{padding:14px 18px;border-left:3px solid #b97936;background:#f8f4eb;font-size:13px}.layout{display:grid;grid-template-columns:220px minmax(0,1fr);gap:40px}.contents{position:sticky;top:22px;align-self:start;border-left:1px solid var(--line);padding-left:18px;font-size:13px}.contents a{display:block;margin:10px 0}.contents p{font-size:12px;color:var(--muted)}.theme{margin-bottom:46px;scroll-margin-top:24px}.theme-header{border-top:3px solid var(--theme);padding-top:17px;margin-bottom:10px}.theme-header .meta{margin-bottom:8px}.record{border-bottom:1px solid var(--line);padding:18px 0}.record:first-of-type{border-top:1px solid var(--line)}.status{font-size:10px;letter-spacing:.06em;text-transform:uppercase;font-weight:650;margin:0 0 5px}.accepted{color:#146d66}.watchlist{color:#92661e}.meta,.keywords{font-size:12px;line-height:1.6;color:var(--muted);margin:0 0 8px}.keywords{color:#596779}.source-links{font-size:13px;margin:0 0 8px}.warning{font-size:12px;color:#82591c;margin:8px 0}summary{cursor:pointer;color:#355c67;font-size:13px;width:fit-content}details[open]>summary{margin-bottom:14px}details details{margin-top:15px}dl{margin:0;font-size:13px}dl>div{margin-bottom:12px}dt{font-weight:650;margin-bottom:3px}dd{margin:0;color:#52616c;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f3f3;padding:14px;font-size:11px;line-height:1.6;color:#52616c}.signal,.assessment{padding:22px 0;border-bottom:1px solid var(--line)}.section-start{border-top:1px solid var(--line);padding-top:26px;margin-top:36px}.footnote{max-width:1200px;margin:auto;border-top:1px solid var(--line);padding:20px 28px;font-size:12px;color:var(--muted)}@media(min-width:1500px){main,.header,.footnote{max-width:1280px}.layout{grid-template-columns:240px minmax(0,1fr);gap:52px}}@media(max-width:850px){.header{align-items:flex-start;flex-direction:column;gap:14px}.layout{grid-template-columns:1fr;gap:24px}.contents{position:static;border-left:0;border-bottom:1px solid var(--line);padding:0 0 14px}.contents a{display:inline-block;margin:4px 14px 4px 0}.header nav{gap:14px}main{padding-top:26px}}@media(max-width:480px){main,.header,.footnote{padding-left:18px;padding-right:18px}body{font-size:14px}.header nav{gap:10px}h3{font-size:16px}.scope{padding:12px}.theme{margin-bottom:32px}}
"""


def render_sources(payload: dict) -> str:
    """Render every retained record as useful HTML, without JavaScript."""
    records = payload["records"]
    routes = {route["id"]: route for route in payload["routes"]}
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)) or any(not isinstance(record_id, str) or not record_id for record_id in ids):
        raise ValueError("Directory records need unique nonempty IDs")
    if set(routes) != set(THEME_PAGES) or any(record["primary_route"] not in routes for record in records):
        raise ValueError("Every directory record needs one of the four primary themes")
    status_counts = Counter(record["catalog_status"] for record in records)
    expected = {status: payload["counts"][status] for status in ("accepted", "watchlist")}
    if any(status not in expected for status in status_counts) or any(status_counts[status] != count for status, count in expected.items()):
        raise ValueError("Directory status counts must equal the source payload")
    accepted, watchlist = expected["accepted"], expected["watchlist"]
    description = f"Browse {accepted} accepted wearable AI records and {watchlist} watchlist candidates across disease prediction, interventions, personal digital twins and mixed reality."
    head = page_head('<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>' + STYLE + '</style></head>', SOURCE_FILENAME, SOURCE_TITLE, description, "CollectionPage")
    contents, groups = [], []
    for route in payload["routes"]:
        rows = sorted((record for record in records if record["primary_route"] == route["id"]), key=lambda record: (-record["year"], record["title"].casefold(), record["id"]))
        count = Counter(record["catalog_status"] for record in rows)
        contents.append(f'<a href="#theme-{route["id"]}">{escape(route["short_label"])} <span>({len(rows)})</span></a>')
        groups.append(f'''<section class="theme" id="theme-{route['id']}" style="--theme:{escape(route['color'], quote=True)}">
<div class="theme-header"><p class="eyebrow">{escape(route['number'])} · {'Interaction entry point' if route['id'] == 'interface' else 'Research theme'}</p><h2>{escape(route['label'])}</h2>
<p>{escape(route['summary'])}</p><p class="meta">{count['accepted']} accepted · {count['watchlist']} watchlist · primary assignments only</p><p class="meta">{escape(route['boundary'])}</p><a href="{THEME_PAGES[route['id']]}">Open the research column →</a></div>
{''.join(_record(record) for record in rows)}</section>''')
    radar = payload.get("radar")
    intelligence = ""
    if radar:
        types = {row["id"]: row["label"] for row in radar["update_types"]}
        assessments = []
        for assessment in radar["assessments"]:
            evidence = " · ".join(f'<a href="#signal-{escape(quote(signal_id, safe=""), quote=True)}">{escape(signal_id)}</a>' for signal_id in assessment["signal_ids"])
            assessments.append(f'''<article class="assessment" data-assessment-route="{escape(assessment['route'], quote=True)}"><p class="eyebrow">{escape(routes[assessment['route']]['short_label'])} · {'Emerging pattern — inference' if assessment['kind'] == 'emerging_pattern' else 'Editorial assessment'}</p><h3>{escape(assessment['headline'])}</h3><p>{escape(assessment['summary'])}</p><p class="warning">{escape(assessment['limit'])}</p><p class="source-links">Evidence: {evidence or 'No linked signals'}</p></article>''')
        intelligence = f'''<section id="intelligence" class="section-start"><p class="eyebrow">Dated intelligence snapshot</p><h2>Assessments &amp; technical signals</h2>
<p class="meta">Reviewed {escape(radar['reviewed_on'])} · Review window {escape(radar['window']['start'])} to {escape(radar['window']['end'])} · {len(radar['signals'])} selected signals</p><p class="scope">{escape(radar['coverage_note'])} Publication dates, event dates and source-check dates are different. These signals are separate from the accepted scientific registry.</p>
{''.join(assessments)}{''.join(_signal(signal, routes, types) for signal in sorted(radar['signals'], key=lambda signal: (signal['event_date'], signal['id']), reverse=True))}</section>'''
        contents.append('<a href="#intelligence">Dated intelligence snapshot</a>')
    return f'''<!doctype html>
<html lang="en">{head}<body><a class="skip" href="#content">Skip to source directory</a>
<header class="header"><a class="brand" href="index.html">{SITE_NAME}</a><nav aria-label="Primary navigation"><a href="index.html">Home</a><a href="columns.html">Research columns</a><a href="library.html">Interactive library</a><a href="research-map.html">Research overview</a><a href="sources.html" aria-current="page">Sources</a><a href="https://github.com/ZipengWu365/awesome-wearable-ai" rel="noreferrer">GitHub</a></nav></header>
<main id="content"><div class="intro"><p class="eyebrow">Readable research directory</p><h1>Wearable AI sources &amp; evidence</h1><p>{accepted} accepted records + {watchlist} watchlist candidates. All {len(records)} repository records, grouped by their primary research theme. Use your browser’s Find command to locate a title or keyword.</p><p class="scope">Catalog cutoff: {escape(payload['cutoff'])}. Complete repository coverage does not mean a complete frontier survey. Enablers, frameworks and adjacent work are not claims that a clinical or digital-twin stage has been achieved. Open a record to inspect its retained contribution, limitations and source metadata.</p></div>
<div class="layout"><aside class="contents"><p>ON THIS PAGE</p><nav aria-label="Directory themes">{''.join(contents)}</nav><p>Primary counts are unique. Keywords and cross-theme links can overlap. Smart-glasses coverage includes adjacent enabling work.</p></aside><div>{''.join(groups)}{intelligence}</div></div></main>
<footer class="footnote">Registry v{escape(str(payload['version']))} · Catalog cutoff {escape(payload['cutoff'])} · <a href="library.html">Interactive library</a> · <a href="columns.html">Research columns</a> · <a href="https://github.com/ZipengWu365/awesome-wearable-ai">Source repository</a></footer></body></html>
'''


def render_sitemap(filenames) -> str:
    """List only real canonical pages; no synthetic freshness timestamps."""
    names = set(filenames)
    if "index.html" not in names:
        raise ValueError("The sitemap must include the project homepage")
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    root = ET.Element(f"{{{namespace}}}urlset")
    for filename in sorted(names, key=lambda name: (name != "index.html", name)):
        item = ET.SubElement(root, f"{{{namespace}}}url")
        ET.SubElement(item, f"{{{namespace}}}loc").text = canonical_url(filename)
    return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def write_discovery_pages(payload: dict, pages: Mapping[str, Mapping[str, str]], output_dir: Path | None = None) -> None:
    """Write only sources.html and sitemap.xml after all normal pages exist.

    ``pages`` is the builder's canonical inventory, keyed by HTML filename;
    values hold its title/description.  The source directory is added here.
    An explicit output_dir is useful for isolated build tests.
    """
    target = Path(output_dir) if output_dir is not None else ROOT
    names = set(pages) | {SOURCE_FILENAME}
    for filename in names:
        canonical_url(filename)
        if filename != SOURCE_FILENAME and not (target / filename).is_file():
            raise ValueError(f"Sitemap target does not exist: {filename}")
    directory = render_sources(payload)
    sitemap = render_sitemap(names)
    (target / SOURCE_FILENAME).write_text(directory, encoding="utf-8")
    (target / "sitemap.xml").write_text(sitemap, encoding="utf-8")
