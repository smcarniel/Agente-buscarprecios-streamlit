# 🔎 Agente de Búsqueda de Precios - Librería NEA

Sistema automático para la **búsqueda de precios de artículos de librería** en MercadoLibre, desarrollado en Python y desplegado en Streamlit Cloud.

Este agente permite subir una lista de productos, buscar los mejores precios en tiempo real y descargar un informe final en Excel.

---

## ✨ Características Principales

- Subí un archivo `.xlsx` con los productos.
- Elegí cuántos precios querés buscar (1, 3, 5, 10 o 15).
- Búsqueda automática en MercadoLibre usando `requests` + `BeautifulSoup`.
- Búsqueda automática en **múltiples sitios** (MercadoLibre, Cetrogar, Musimundo, etc).
- Barra de progreso en vivo.
- Resultados visibles en pantalla.
- Descarga directa del informe final en Excel.
- Archivos de resultados separados según la opción elegida (MercadoLibre o Múltisitios).

---

## 📈 Tecnologías Utilizadas

- **Python 3.12**
- **Streamlit** (frontend web)
- **Requests** (para scraping)
- **BeautifulSoup4** (procesamiento de HTML)
- **Pandas** (manejo de datos Excel)
- **OpenPyXL** (para exportación de Excel)

---

## 🔧 Instalación Local (Opcional)

1. Cloná este repositorio:

```bash
git clone https://github.com/tu-usuario/tu-repo-agente-precios.git
cd tu-repo-agente-precios
```

2. Instalá las dependencias:

```bash
pip install -r requirements.txt
```

3. Corré la aplicación:

```bash
streamlit run app_streamlit_precios_final_mejorado.py
```

---

## 🌐 Uso en Streamlit Cloud

1. Subí tu repositorio a GitHub.
2. Andá a [Streamlit Cloud](https://streamlit.io/cloud).
3. Creá una nueva aplicación:
   - Repositorio: tu repo de GitHub.
   - Rama: main (o la que uses).
   - Archivo principal: `app_streamlit_precios_final_mejorado.py`
4. Deployá y usá tu agente online.

---

## 📊 Ejemplo de uso

1. Subí tu archivo `productos.xlsx` (columna B con los nombres de productos).
2. Seleccioná la cantidad de precios a buscar.
3. Click en **"Buscar precios MercadoLibre"** o **"Buscar en múltiples sitios"**.
4. Descargá el Excel final correspondiente:
   - `precios_buscados_bs4_mejorado.xlsx` (solo MercadoLibre)
   - `precios_buscados_bs4_mejorado_MS.xlsx` (múltiples sitios)

---

## ✨ Autor

**Desarrollado por:** Santi Carniel

**Proyecto de automatización de búsqueda de precios para la región NEA - Argentina.**

---

# 🚀 Estado del Proyecto

☑️ Finalizado y funcional en Streamlit Cloud.
☑️ Nueva versión 2024:
- Busqueda opcional en múltiples sitios.
- Resultados separados para distintas fuentes.
- Mayor flexibilidad y robustez.
- Integración de barra de progreso en tiempo real.
- Selección de cantidad de precios a buscar.

☑️ Mejoras futuras posibles: agregar filtros de precios, integración de nuevos sitios, búsqueda avanzada.

---

## 📅 Guía para Agregar Nuevos Sitios al Multisitio

Para expandir el sistema de búsqueda a nuevos sitios, seguí estos pasos:

1. **Crear una nueva función**:

```python
def buscar_precios_nuevositio(producto, cantidad):
    # Usar requests y BeautifulSoup para hacer scraping del sitio
    # Devolver una lista de tuplas: (precio, enlace)
    return lista_de_precios
```

2. **Agregar la función al flujo multisitio**:

Dentro de `buscar_precios_multisitio(producto, cantidad)`, agregá:

```python
precios_nuevositio = buscar_precios_nuevositio(producto, cantidad)
resultados.extend(precios_nuevositio)
```

3. **Mantener la estructura**:
- Cada precio debe ser una tupla `(precio, link)`, igual que en MercadoLibre.
- El sistema ordena automáticamente todos los precios encontrados.

4. **Probar y ajustar**:
- Probar si el scraping funciona correctamente.
- Ajustar selectores CSS si la página cambia su estructura.

---

De esta manera, el agente podrá crecer de forma modular y profesional, adaptándose a nuevos sitios de manera sencilla. 🚀
