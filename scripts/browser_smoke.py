"""Chromium regression checks served from a project subpath, as on GitHub Pages."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
import json
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/site/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            context=browser.new_context(viewport={'width':1280,'height':900},accept_downloads=True)
            page=context.new_page();errors=[]
            page.on('pageerror',lambda error: errors.append(str(error)))
            page.goto(url)
            expect(page.locator('#count')).to_contain_text('408 matching records')
            page.get_by_role('button',name='Explore digital twins',exact=True).click()
            expect(page.locator('#count')).to_contain_text('14 matching records')
            page.get_by_label('Include watchlist (not accepted)',exact=True).check()
            expect(page.locator('#count')).to_contain_text('22 matching records')
            share=page.url
            page.reload()
            expect(page.locator('#count')).to_contain_text('22 matching records')
            assert page.url==share
            with page.expect_download() as event:
                page.get_by_role('button',name='Export JSON',exact=True).click()
            downloaded=json.loads(Path(event.value.path()).read_text(encoding='utf-8'))
            assert len(downloaded)==22
            assert sum(r['pool']=='watchlist' for r in downloaded)==8
            page.get_by_role('button',name='Details & sources',exact=True).first.click()
            expect(page.get_by_role('dialog')).to_be_visible()
            assert 'record=' in page.url
            expect(page.get_by_role('dialog').get_by_role('heading',name='Digital twin profile',exact=True)).to_be_visible()
            page.get_by_role('button',name='Close details').click()
            expect(page.get_by_role('dialog')).not_to_be_visible()
            assert 'record=' not in page.url
            page.get_by_role('button',name='Reset filters',exact=True).click()
            page.get_by_label('Search',exact=True).fill('WESAD')
            page.get_by_label('Resource type',exact=True).select_option('dataset')
            expect(page.locator('#count')).to_contain_text('1 matching records')
            page.get_by_text('Dataset release filters',exact=True).click()
            page.get_by_label('Raw signals',exact=True).select_option('true')
            page.get_by_label('Labels available',exact=True).select_option('true')
            expect(page.locator('#count')).to_contain_text('1 matching records')
            page.get_by_label('Minimum participants',exact=True).fill('1000000')
            expect(page.locator('#count')).to_contain_text('0 matching records')
            expect(page.get_by_role('button',name='Export CSV',exact=True)).to_be_disabled()
            page.get_by_role('button',name='Reset filters',exact=True).click()
            page.get_by_role('button',name='Next',exact=True).click()
            expect(page.locator('#page')).to_contain_text('Page 2')
            page.get_by_role('button',name='Explore digital twins',exact=True).click()
            page.screenshot(path=str(ROOT/'portal-desktop.png'))
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.screenshot(path=str(ROOT/'portal-mobile.png'))
            assert not errors,errors
            browser.close()
        print('PASS: browser load, twin/watchlist filters, query reload, JSON download, details, release filters, empty results, pagination and mobile layout')
    finally:
        server.shutdown();server.server_close()

if __name__=='__main__':main()
