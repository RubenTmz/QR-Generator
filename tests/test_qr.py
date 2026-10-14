from io import BytesIO

import pytest
from PIL import Image

from qrstudio import contact_vcard, generate_png, generate_svg, plain_text, website_url


def test_vcard_required_fields_and_escaping():
    card = contact_vcard("Ana; García", "+52 81 1234 5678", company="Ejemplo, S.A.")
    assert card.startswith("BEGIN:VCARD\r\nVERSION:3.0\r\n")
    assert "FN:Ana\\; García\r\n" in card
    assert "TEL;TYPE=CELL:+52 81 1234 5678" in card
    assert "ORG:Ejemplo\\, S.A." in card
    assert card.endswith("END:VCARD\r\n")


def test_vcard_rejects_incomplete_contact():
    with pytest.raises(ValueError):
        contact_vcard("", "123")
    with pytest.raises(ValueError):
        contact_vcard("Ana", "teléfono")


def test_url_validation():
    assert website_url(" https://ejemplo.com ") == "https://ejemplo.com"
    with pytest.raises(ValueError):
        website_url("javascript:alert(1)")


def test_text_validation():
    with pytest.raises(ValueError):
        plain_text("  ")
    assert plain_text("Hola") == "Hola"


def test_png_exact_size():
    raw = generate_png(contact_vcard("Ana García", "+52 81 1234 5678"), pixels=1200)
    with Image.open(BytesIO(raw)) as image:
        assert image.size == (1200, 1200)
        assert image.format == "PNG"


def test_svg_is_valid_xml():
    from xml.etree import ElementTree

    raw = generate_svg("https://ejemplo.com")
    assert ElementTree.fromstring(raw).tag.endswith("svg")


def test_invalid_resolution():
    with pytest.raises(ValueError):
        generate_png("Hola", pixels=20)
