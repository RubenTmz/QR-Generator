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


def contact_vcard(name: str, phone: str, email: str = "", company: str = "", title: str = "", website: str = "") -> str:
    """Devuelve una vCard 3.0 para importar a contactos Android/iOS.

    La app de contactos del teléfono puede pedir confirmación antes de guardar.
    """
    name, phone = name.strip(), phone.strip()
    if not name or not phone:
        raise ValueError("Nombre y teléfono son obligatorios.")
    if not any(ch.isdigit() for ch in phone):
        raise ValueError("El teléfono debe incluir números.")

    # No inventamos la separación de apellidos: FN conserva el nombre completo.
    lines = ["BEGIN:VCARD", "VERSION:3.0", "N:;;;;", f"FN:{_vcard_escape(name)}", f"TEL;TYPE=CELL:{_vcard_escape(phone)}"]
    optional = (("EMAIL;TYPE=INTERNET", email), ("ORG", company), ("TITLE", title), ("URL", website))
    for key, value in optional:
        if value.strip():
            lines.append(f"{key}:{_vcard_escape(value.strip())}")
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


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
