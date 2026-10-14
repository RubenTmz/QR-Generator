"""Codificadores de contenido para QR. Añade otros tipos aquí."""

from urllib.parse import urlsplit


def _vcard_escape(value: str) -> str:
    """Escapa caracteres reservados por vCard 3.0."""
    return (
        value.replace("\\", "\\\\")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def contact_vcard(
    name: str,
    phone: str = "",
    email: str = "",
    company: str = "",
    title: str = "",
    website: str = "",
    work_phone: str = "",
) -> str:
    """Construye una vCard 3.0 con celular y/o teléfono fijo.

    Compatibilidad: `phone` sigue siendo el celular. Los otros datos son
    opcionales y solo se incluyen cuando se proporcionan.
    """
    name = name.strip()
    phone = phone.strip()
    work_phone = work_phone.strip()
    if not name:
        raise ValueError("El nombre es obligatorio.")
    if not (phone or work_phone):
        raise ValueError("Ingresa al menos un teléfono: celular o fijo.")
    if any(number and not any(c.isdigit() for c in number) for number in (phone, work_phone)):
        raise ValueError("Los teléfonos deben contener dígitos.")

    lines = ["BEGIN:VCARD", "VERSION:3.0", "N:;;;;", f"FN:{_vcard_escape(name)}"]
    if phone:
        lines.append(f"TEL;TYPE=CELL:{_vcard_escape(phone)}")
    if work_phone:
        lines.append(f"TEL;TYPE=WORK,VOICE:{_vcard_escape(work_phone)}")

    optional = (
        ("EMAIL;TYPE=INTERNET", email),
        ("ORG", company),
        ("TITLE", title),
        ("URL", website),
    )
    for key, value in optional:
        if value.strip():
            lines.append(f"{key}:{_vcard_escape(value.strip())}")
    lines.append("END:VCARD")
    return "
".join(lines) + "
"


def website_url(url: str) -> str:
    url = url.strip()
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.netloc or " " in url:
        raise ValueError("Ingresa una URL válida que comience con https:// o http://")
    return url


def plain_text(value: str) -> str:
    if not value.strip():
        raise ValueError("El texto no puede estar vacío.")
    return value
