"""Render de QR PNG y SVG, sin red, cuentas ni servicios externos."""

from io import BytesIO
from xml.etree import ElementTree as ET

import qrcode
from PIL import Image, ImageColor
from qrcode.image.svg import SvgPathImage


def _make_qr(payload: str, error_correction: str = "M") -> qrcode.QRCode:
    if not payload:
        raise ValueError("El contenido QR no puede estar vacío.")
    levels = {"L": qrcode.constants.ERROR_CORRECT_L, "M": qrcode.constants.ERROR_CORRECT_M,
              "Q": qrcode.constants.ERROR_CORRECT_Q, "H": qrcode.constants.ERROR_CORRECT_H}
    if error_correction not in levels:
        raise ValueError("Corrección de errores inválida.")
    qr = qrcode.QRCode(version=None, error_correction=levels[error_correction], box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    return qr


def _colors(foreground: str, background: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    front = ImageColor.getrgb(foreground)
    back = ImageColor.getrgb(background)
    if len(front) != 3 or len(back) != 3:
        raise ValueError("Utiliza colores RGB opacos.")
    if front == back:
        raise ValueError("Los colores de fondo y módulos deben ser distintos.")
    return front, back


def _luminance(rgb: tuple[int, int, int]) -> float:
    def linear(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(channel) for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def color_contrast(foreground: str, background: str) -> tuple[float, bool]:
    """Devuelve contraste (WCAG) y si los módulos son más oscuros que el fondo."""
    fg, bg = _colors(foreground, background)
    fg_lightness, bg_lightness = _luminance(fg), _luminance(bg)
    ratio = (max(fg_lightness, bg_lightness) + 0.05) / (min(fg_lightness, bg_lightness) + 0.05)
    return ratio, fg_lightness < bg_lightness


def generate_png(payload: str, pixels: int = 4000, foreground: str = "#000000", background: str = "#FFFFFF", error_correction: str = "M") -> bytes:
    """Genera PNG cuadrado con borde blanco suficiente y resolución exacta."""
    if not 256 <= pixels <= 10000:
        raise ValueError("La resolución debe estar entre 256 y 10000 píxeles.")
    fg, bg = _colors(foreground, background)
    qr = _make_qr(payload, error_correction)
    result = qr.make_image(fill_color=fg, back_color=bg).convert("RGB")
    result = result.resize((pixels, pixels), resample=Image.Resampling.NEAREST)
    out = BytesIO()
    result.save(out, format="PNG", dpi=(300, 300), optimize=True)
    return out.getvalue()


def generate_svg(payload: str, error_correction: str = "M", foreground: str = "#000000", background: str = "#FFFFFF") -> bytes:
    """Genera un SVG vectorial con módulos y fondo del color solicitado."""
    fg, bg = _colors(foreground, background)
    qr = _make_qr(payload, error_correction)
    svg = qr.make_image(image_factory=SvgPathImage)
    root = ET.fromstring(svg.to_string(encoding="utf-8"))
    namespace = "{http://www.w3.org/2000/svg}"
    path = root.find(f"{namespace}path")
    if path is None:
        raise RuntimeError("No se encontraron los módulos QR en el SVG.")
    path.set("fill", "#{:02X}{:02X}{:02X}".format(*fg))
    root.insert(0, ET.Element(f"{namespace}rect", {
        "x": "0", "y": "0", "width": "100%", "height": "100%",
        "fill": "#{:02X}{:02X}{:02X}".format(*bg),
    }))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)
