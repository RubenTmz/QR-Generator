"""Render de QR PNG y SVG, sin red, cuentas ni servicios externos."""

from io import BytesIO

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


def generate_svg(payload: str, error_correction: str = "M") -> bytes:
    """Genera SVG escalable con módulos negros y fondo blanco."""
    qr = _make_qr(payload, error_correction)
    svg = qr.make_image(image_factory=SvgPathImage)
    return svg.to_string(encoding="utf-8")
