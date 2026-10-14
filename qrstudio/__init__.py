"""Generación de códigos QR estáticos, offline y extensibles."""

from .core import generate_png, generate_svg
from .payloads import contact_vcard, plain_text, website_url

__all__ = ["generate_png", "generate_svg", "contact_vcard", "plain_text", "website_url"]
