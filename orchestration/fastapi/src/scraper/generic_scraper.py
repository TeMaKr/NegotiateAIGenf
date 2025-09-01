"""
Scraper for UNEP-style “accordion” pages.
Captures for each PDF link:

    href,
    a_text,
    surrounding_p,
    accordion_name,
    section,        # nearest <h1-h6>
    subsection      # nearest <p><strong>…</strong></p>

Usage:
    pip install requests bs4 lxml
    python scraper.py
"""

from __future__ import annotations

import json
import logging
import re
import urllib.parse

from bs4 import BeautifulSoup, Tag
from scraper.helper import fetch_html

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# ---------------------------------------------------------------------------#
# Config                                                                     #
# ---------------------------------------------------------------------------#
PDF_RE = re.compile(r"\.pdf($|#.*$|\?)", re.I)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PDFScraper/1.0)"}


# ---------------------------------------------------------------------------#
# Helper: locate section & subsection                                        #
# ---------------------------------------------------------------------------#
def heading_context(link_tag, root) -> tuple[str | None, str | None]:
    """
    Walk backwards from `link_tag` and return (section, subsection).

    section     = nearest real heading  <h1-h6>
    subsection  = nearest pseudo heading <p><strong>…</strong></p> that
                  appears *after* that heading but *before* the link.

    Either can be None if absent.
    """

    # Accept any BeautifulSoup element type for tag
    def is_real_h(tag) -> bool:
        # Ensure the return value is always a boolean
        return bool(
            tag
            and tag.name
            and tag.name.lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}
        )

    def is_pseudo_h(tag) -> bool:
        return bool(
            tag and tag.name == "p" and tag.find("strong") and not tag.find("a")
        )

    section = subsection = None

    # first scan siblings on the current level
    for sib in link_tag.find_previous_siblings():
        if subsection is None and is_pseudo_h(sib):
            subsection = sib.get_text(" ", strip=True)
            continue
        if section is None and is_real_h(sib):
            section = sib.get_text(" ", strip=True)
            if subsection:  # already have both → stop early
                break

    # if missing, climb up and repeat
    parent = link_tag.parent
    while (section is None or subsection is None) and parent and parent is not root:
        for sib in parent.find_previous_siblings():
            if subsection is None and is_pseudo_h(sib):
                subsection = sib.get_text(" ", strip=True)
            if section is None and is_real_h(sib):
                section = sib.get_text(" ", strip=True)
            if section and subsection:
                break
        parent = parent.parent

    return section, subsection


# ---------------------------------------------------------------------------#
# Core                                                                       #
# ---------------------------------------------------------------------------#
def scrape_page(
    url: str,
    include_accordions: list[str] = [],
    prevent_duplicate_accordions: bool = False,
) -> list[dict]:
    """
    Return a list of dictionaries – one per PDF link on the page.
    """
    html = fetch_html(url)
    if not html:
        logger.error(f"Failed to fetch HTML from {url}")
        return []
    soup = BeautifulSoup(html, "html.parser")
    base = urllib.parse.urlsplit(url)

    results: list[dict] = []
    seen_accordions = set()
    for li in soup.select("li.accordion-item"):
        acc_title = li.select_one(".accordion-title")
        accordion_nm = acc_title.get_text(" ", strip=True) if acc_title else None

        # Check if accordion name has been seen before
        if (
            accordion_nm
            and prevent_duplicate_accordions
            and accordion_nm in seen_accordions
        ):
            logger.debug(
                f"Skipping duplicate accordion '{accordion_nm}' "
                "as prevent_duplicate_accordions is enabled."
            )
            continue
        # If prevent_duplicate_accordions is enabled, add the accordion name to seen_accordions
        if accordion_nm and prevent_duplicate_accordions:
            seen_accordions.add(accordion_nm)

        # Filter by accordion name if specified
        if include_accordions and accordion_nm not in include_accordions:
            logger.debug(
                f"Skipping accordion '{accordion_nm}' as it is not in the filter list."
            )
            continue

        content = li.select_one(".accordion-content")
        if not content:
            continue

        a_list = content.find_all("a", href=True)
        for a in a_list:
            if not PDF_RE.search(str(a["href"])):  # type: ignore
                continue

            previous_elems = a.find_all_previous()
            surrounding_p = None
            if previous_elems:
                # Check if first element is a Tag and has name attribute li
                first_elem = previous_elems[0]
                if (
                    isinstance(first_elem, Tag)
                    and hasattr(first_elem, "name")
                    and first_elem.name == "li"
                ):
                    # get text inside previous p
                    p_tag = a.find_previous("p")
                    if p_tag and p_tag.get_text(strip=True):
                        surrounding_p = p_tag.get_text(strip=True)

            href = urllib.parse.urljoin(base.geturl(), a["href"])  # type: ignore
            a_text = a.get_text(" ", strip=True)

            if not surrounding_p:
                p_tag = a.find_parent("p")
                surrounding_p = p_tag.get_text(" ", strip=True) if p_tag else None

            section, subsection = heading_context(a, content)

            results.append(
                dict(
                    href=href,
                    a_text=a_text,
                    surrounding_p=surrounding_p,
                    accordion_name=accordion_nm,
                    section=section,
                    subsection=subsection,
                )
            )

    return results


# ---------------------------------------------------------------------------#
# Demo driver                                                                #
# ---------------------------------------------------------------------------#
if __name__ == "__main__":
    URL = "https://www.unep.org/inc-plastic-pollution/session-3/documents/in-session"  # sample page
    data = scrape_page(URL)

    # pretty-print to stdout
    logger.debug(json.dumps(data, indent=2, ensure_ascii=False))

    # uncomment to write JSON file
    # with open("documents.json", "w", encoding="utf-8") as fp:
    #     json.dump(data, fp, ensure_ascii=False, indent=2)
