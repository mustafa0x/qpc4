# /// script
# dependencies = [
#   "html_sanitizer",
#   "beautifulsoup4",
#   "regex"
# ]
# ///
import sys
from html_sanitizer import Sanitizer
from pathlib import Path
from bs4 import BeautifulSoup
import regex as re

DEFAULT_SETTINGS = {
    "tags": {
        "a", "h1", "h2", "h3", "strong", "em", "p", "ul", "ol",
        "li", "br", "sub", "sup", "hr", "span", "style"
    },
    "attributes": {"a": ("href", "name", "target", "title", "id", "rel"), "span": ("style",)},
    "empty": {"hr", "a", "br"},
    "separate": {"a", "p", "li", "span"},
    "whitespace": {"br"},
    "keep_typographic_whitespace": False,
    "add_nofollow": False,
    "autolink": False,
    "element_postprocessors": [],
    "is_mergeable": lambda e1, e2: True,
}

def clean_html(file_path):
    # Create Path object
    path = Path(file_path)
    # Read input file
    html_content = path.read_text()
    # Configure sanitizer to allow only span and style tags
    sanitizer = Sanitizer(DEFAULT_SETTINGS)
    clean_content = sanitizer.sanitize(html_content)

    # Use BeautifulSoup to prettify the HTML
    soup = BeautifulSoup(clean_content, 'html.parser')
    formatted_html = soup.prettify()

    output_path = path.with_stem(f"{path.stem}-clean")
    output_path.write_text(formatted_html)
    return output_path

output_file = clean_html(sys.argv[1])
print(f"Cleaned HTML saved to: {output_file}")

