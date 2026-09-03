.PHONY: validate export coverage families readme site build test audit clean

validate:
	python scripts/validate_registry.py
export:
	python scripts/export_registry.py
coverage:
	python scripts/coverage_report.py
families:
	python scripts/render_family_pages.py
readme:
	python scripts/render_readme.py
site:
	python scripts/build_site.py
build: validate export coverage families readme site
test: build
	python -m unittest discover -s tests -v
	python scripts/internal_link_check.py
audit: test
	python scripts/release_audit.py
clean:
	rm -f generated/catalog.csv generated/watchlist.csv generated/relations.csv generated/registry.json generated/statistics.json generated/coverage.json generated/coverage.md
	rm -rf generated/families
	rm -f site/registry.json site/index.html
