# 🔳 QR Studio — QR Generator

Generador gratuito y de código abierto de **QR estáticos**, con interfaz web en Streamlit y salida **PNG de alta resolución** o **SVG vectorial**. Diseñado para añadir más tipos en futuras versiones.

## Funciones v0.3.0

- **Contacto básico (vCard 3.0)**: solo nombre completo y celular, sin puesto ni empresa.
- **Contacto completo (vCard 3.0)**: nombre, celular, teléfono fijo, correo electrónico, empresa, puesto y sitio web. Se admite celular, fijo o ambos. Los campos vacíos no se incluyen.
- **URL**: código QR que abre sitios web.
- **Texto**: contenido libre.
- **PNG**: resoluciones de 1,024 a 10,000 píxeles, con metadatos 300 DPI.
- **SVG**: vector escalable para diseño e impresión, con los mismos colores personalizados que el PNG.
- **🎨 Coloreador**: negro clásico, preset azul corporativo `#234388` y dos selectores de color (módulos y fondo).
- **Contraste**: advertencia cuando una combinación puede dificultar el escaneo; se conserva el margen blanco/de fondo de seguridad.
- Generación local, sin marcas de agua y sin límites artificiales de uso.

## 🚀 Ejecución local

Requiere Python 3.10 o superior.

```bash
git clone https://github.com/RubenTmz/QR-Generator.git
cd QR-Generator
python -m venv .venv
```

Activa el entorno virtual (Windows PowerShell: `.venv\Scripts\Activate.ps1`; Linux/macOS: `source .venv/bin/activate`).

```bash
pip install -r requirements.txt
streamlit run app.py
```

Entra a `http://localhost:8501` o a la dirección que indique Streamlit.

## Usar desde Python

```python
from pathlib import Path
from qrstudio import contact_vcard, generate_png, generate_svg

# Solo nombre y celular
basic = contact_vcard('Ana García', '+52 81 1234 5678')
Path('contacto_basico.png').write_bytes(generate_png(basic, pixels=4000))

# Contacto completo: además de celular, puede llevar teléfono fijo y más datos
full = contact_vcard(
    name='Ana García',
    phone='+52 81 1234 5678',
    work_phone='+52 81 8765 4321',
    email='ana@example.com',
    company='Mi empresa',
    title='Gerente',
    website='https://example.com',
)
Path('contacto_completo.svg').write_bytes(generate_svg(full))

# QR azul corporativo para impresión (también exporta SVG con los mismos colores)
Path('contacto_azul.png').write_bytes(generate_png(basic, pixels=4000, foreground='#234388', background='#FFFFFF'))
Path('contacto_azul.svg').write_bytes(generate_svg(basic, foreground='#234388', background='#FFFFFF'))
```

## Colores desde la interfaz

En la interfaz Streamlit, elige **Clásico**, **Azul corporativo 2L (#234388)** o **Personalizado**. En este último modo aparecen los selectores para el color del código y del fondo. El PNG y el SVG incorporan ambos colores. Para mejorar la lectura, utiliza módulos oscuros sobre un fondo claro y procura un contraste de al menos **4.5:1**. La interfaz avisa cuando puede haber problemas; comprueba el QR con varios teléfonos antes de imprimir.

## Pruebas

```bash
pip install pytest
python -m pytest -q
```

GitHub Actions ejecuta las pruebas en cada push y pull request.

## Organización

```text
app.py                         interfaz Streamlit
qrstudio/core.py               motor PNG/SVG
qrstudio/payloads.py           codificadores vCard, URL y texto
tests/test_qr.py               pruebas automáticas
.github/workflows/tests.yml    pruebas en GitHub Actions
```

## Próximas versiones

- [ ] Wi-Fi, WhatsApp y llamada telefónica
- [ ] Correo electrónico y eventos de calendario
- [x] Colores personalizables con advertencia de contraste
- [ ] Logotipos (asegurando legibilidad)
- [ ] Generación masiva desde CSV y Excel
- [ ] Publicar la interfaz web para uso desde navegador

## Notas importantes

Los QR estáticos no caducan por sí mismos, pero un enlace externo puede dejar de existir. La importación de contactos requiere una acción del usuario y depende del teléfono y la app de cámara. Haz siempre una prueba de escaneo antes de imprimir. No publiques datos personales reales de clientes en este repositorio.

**Licencia:** MIT.
