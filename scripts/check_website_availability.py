"""Verify the public HTTPS deployment from the GitHub-hosted deploy runner.

This is an independent availability check, not a proxy or a firewall bypass.
It checks only this site's published pages and first-party static assets.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import time
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / 'website'


class Assets(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.targets = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'img') and attrs.get('src'):
            self.targets.append(attrs['src'])
        elif tag == 'link' and attrs.get('href') and any(
                rel in attrs.get('rel', '').split() for rel in ('stylesheet', 'icon', 'preload')):
            self.targets.append(attrs['href'])


def first_party(base, document, target):
    url = urljoin(document, target)
    original, resolved = urlsplit(base), urlsplit(url)
    if resolved.scheme != 'https' or resolved.netloc != original.netloc:
        return None
    if not unquote(resolved.path).startswith(original.path):
        return None
    return url


def fetch(base, url, method='GET'):
    request = Request(url, method=method, headers={
        'User-Agent': 'Awesome-Wearable-AI-Pages-Availability-Check',
        'Cache-Control': 'no-cache',
    })
    # Default TLS validation remains enabled. Never hide certificate failures.
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f'{method} {url}: HTTP {response.status}')
        if not first_party(base, url, response.url):
            raise RuntimeError(f'{url}: unexpected redirect to {response.url}')
        return response.read() if method == 'GET' else b''


def check(base, version):
    pages = sorted(ROOT.glob('*.html'))
    assets = set()

    def page(path):
        url = urljoin(base, path.name) + '?availability=' + version
        body = fetch(base, url)
        if hashlib.sha256(body).digest() != hashlib.sha256(path.read_bytes()).digest():
            raise RuntimeError(f'{path.name}: online content differs from this deployment')
        text = body.decode('utf-8')
        targets = Assets(text).targets
        return {u for target in targets if (u := first_party(base, url, target))}

    with ThreadPoolExecutor(max_workers=4) as pool:
        for targets in pool.map(page, pages):
            assets.update(targets)
        for url in sorted(assets):
            if urlsplit(url).path.endswith('.css'):
                css = fetch(base, url).decode('utf-8')
                for target in re.findall(r'url\(\s*[\'"]?([^\)\'"\s]+)', css):
                    nested = first_party(base, url, target)
                    if nested:
                        assets.add(nested)
        list(pool.map(lambda url: fetch(base, url, 'HEAD'), sorted(assets)))
    return len(pages), len(assets)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--attempts', type=int, default=4)
    args = parser.parse_args()
    base = args.base_url.rstrip('/') + '/'
    if urlsplit(base).scheme != 'https' or not urlsplit(base).netloc:
        parser.error('An HTTPS deployment URL is required')
    version = os.environ.get('GITHUB_SHA', 'manual-check')
    for attempt in range(args.attempts):
        try:
            pages, assets = check(base, version)
            message = f'PASS: {base} — {pages} pages match this deployment; {assets} assets respond over verified HTTPS.'
            print(message)
            if os.environ.get('GITHUB_STEP_SUMMARY'):
                with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as summary:
                    summary.write(message + '\n')
            return
        except Exception as error:
            print(f'Attempt {attempt + 1}/{args.attempts}: {type(error).__name__}: {error}', flush=True)
            if attempt + 1 == args.attempts:
                raise
            time.sleep(12)


if __name__ == '__main__':
    main()
