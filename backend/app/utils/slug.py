import re
from slugify import slugify as _slugify


def make_slug(text: str) -> str:
    return _slugify(text, max_length=200, word_boundary=True)


def ensure_unique_slug(base: str, existing_slugs: set[str]) -> str:
    slug = base
    counter = 1
    while slug in existing_slugs:
        slug = f"{base}-{counter}"
        counter += 1
    return slug
