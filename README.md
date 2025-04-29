# 🔎 Buscador de Precios de Referencia

Sistema automático para la **búsqueda de precios de artículos de librería** en MercadoLibre, desarrollado en Python y desplegado en Streamlit Cloud.

Este agente permite subir una lista de productos, buscar los mejores precios en tiempo real, visualizar resultados en pantalla y descargar un informe final en Excel.

---

## ✨ Características Principales

- Subí un archivo `.xlsx` con los productos.
- Elegí cuántos precios querés buscar (1, 3, 5, 10 o 15).
- Búsqueda automática en MercadoLibre usando `requests` + `BeautifulSoup`.
- Barra de progreso en vivo.
- Resultados visibles en pantalla.
- Descarga directa del informe final en Excel.

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
streamlit run buscador_precios_referencia.py
```

---

## 🌐 Uso en Streamlit Cloud

1. Subí tu repositorio a GitHub.
2. Andá a [Streamlit Cloud](https://streamlit.io/cloud).
3. Creá una nueva aplicación:
   - Repositorio: tu repo de GitHub.
   - Rama: main (o la que uses).
   - Archivo principal: `buscador_precios_referencia.py`
4. Deployá y usá tu agente online.

---

## 📊 Ejemplo de uso

1. Subí tu archivo `productos.xlsx` (columna B con los nombres de productos).
2. Seleccioná la cantidad de precios a buscar.
3. Click en **"Buscar precios MercadoLibre"**.
4. Visualizá los resultados directamente en la página.
5. Descargá el Excel final correspondiente:
   - `precios_buscados_mercadolibre.xlsx`

---

## ✨ Autor

**Desarrollado por:** Santi Carniel

**Proyecto de automatización de búsqueda de precios para la región NEA - Argentina.**

---

# 🚀 Estado del Proyecto

☑️ Finalizado y funcional en Streamlit Cloud.
☑️ Versión estable 2024:
- Búsqueda automática en MercadoLibre.
- Visualización de resultados en pantalla.
- Barra de progreso en vivo.
- Descarga de resultados en Excel.

☑️ Mejoras futuras posibles: agregar más filtros de precios, nuevas integraciones de sitios.

---

