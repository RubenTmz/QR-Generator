"""Interfaz Streamlit para crear y descargar QRs estáticos."""

import streamlit as st

from qrstudio import contact_vcard, generate_png, generate_svg, plain_text, website_url

st.set_page_config(page_title="QR Studio", page_icon="🔳", layout="centered")
st.title("🔳 QR Studio")
st.caption("Códigos QR estáticos, sin caducidad propia, sin marca de agua. Se generan localmente.")

qr_type = st.selectbox("Tipo de QR", ["Contacto (vCard)", "Sitio web", "Texto"])
payload = None

if qr_type == "Contacto (vCard)":
    contact_mode = st.radio("Tipo de contacto", ["Básico", "Completo"], horizontal=True)
    name = st.text_input("Nombre completo *", placeholder="Ej. Ana García")
    phone = st.text_input(
        "Celular *" if contact_mode == "Básico" else "Celular",
        placeholder="Ej. +52 81 1234 5678",
    )

    work_phone = email = company = title = website = ""
    if contact_mode == "Completo":
        st.caption("Puedes registrar celular, teléfono fijo o ambos. Los demás campos son opcionales.")
        work_phone = st.text_input("Teléfono fijo", placeholder="Ej. +52 81 2345 6789")
        email = st.text_input("Correo electrónico")
        company = st.text_input("Empresa")
        title = st.text_input("Puesto")
        website = st.text_input("Sitio web", placeholder="https://ejemplo.com")
    else:
        st.caption("El QR básico incluye únicamente nombre y celular, sin puesto ni empresa.")

    if name.strip() and (phone.strip() or work_phone.strip()):
        try:
            payload = contact_vcard(
                name=name,
                phone=phone,
                work_phone=work_phone,
                email=email,
                company=company,
                title=title,
                website=website,
            )
        except ValueError as exc:
            st.warning(str(exc))
elif qr_type == "Sitio web":
    url = st.text_input("Enlace *", placeholder="https://ejemplo.com")
    if url.strip():
        try:
            payload = website_url(url)
        except ValueError as exc:
            st.warning(str(exc))
else:
    raw_text = st.text_area("Contenido *", placeholder="Escribe el texto")
    if raw_text.strip():
        payload = plain_text(raw_text)

col1, col2 = st.columns(2)
with col1:
    pixels = st.selectbox("Resolución PNG", [1024, 2000, 4000, 6000, 10000], index=2, format_func=lambda x: f"{x:,} × {x:,} px")
with col2:
    ecc = st.selectbox("Corrección de errores", ["M", "Q", "H", "L"], index=0)

st.caption("Para máxima compatibilidad, se utilizan módulos negros, fondo blanco y margen de seguridad.")
if payload:
    try:
        png = generate_png(payload, pixels=pixels, error_correction=ecc)
        svg = generate_svg(payload, error_correction=ecc)
    except (ValueError, OverflowError) as exc:
        st.error(f"No se pudo generar el QR: {exc}")
    else:
        st.image(png, caption="Vista previa de tu QR", width=320)
        left, right = st.columns(2)
        with left:
            st.download_button("⬇️ Descargar PNG", data=png, file_name="qr-studio.png", mime="image/png", use_container_width=True)
        with right:
            st.download_button("⬇️ Descargar SVG", data=svg, file_name="qr-studio.svg", mime="image/svg+xml", use_container_width=True)
        if qr_type == "Contacto (vCard)":
            st.info("Al escanear, el teléfono puede ofrecer guardar el contacto. El guardado requiere confirmación del usuario y depende de la app de cámara/contactos.")
        st.caption("Prueba el QR con al menos dos celulares antes de imprimir. Los códigos URL dependen de que el sitio siga disponible.")
else:
    st.info("Completa los campos obligatorios para generar el código QR.")
