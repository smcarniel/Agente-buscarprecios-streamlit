import streamlit as st
import pandas as pd
import time
import random
import io
import requests
from bs4 import BeautifulSoup

# Funciones para cada sitio

def buscar_precios_mercadolibre(producto, cantidad):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://listado.mercadolibre.com.ar/{producto.replace(' ', '-')}_OrderId_PRICE"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".ui-search-layout__item")[:cantidad * 2]
        precios = []

        for item in items:
            try:
                precio_tag = item.select_one(".andes-money-amount__fraction")
                link_tag = item.select_one("a")
                if not (precio_tag and link_tag):
                    continue
                precio_texto = precio_tag.text.replace(".", "").replace(",", "")
                precio = int(precio_texto)
                link = link_tag['href']
                precios.append((precio, link))
            except Exception:
                continue

        precios_ordenados = sorted(precios, key=lambda x: x[0])
        return precios_ordenados[:cantidad]
    except Exception:
        return []

def buscar_precios_cetrogar(producto, cantidad):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.cetrogar.com.ar/catalogsearch/result/?q={producto.replace(' ', '%20')}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".product-item-info")[:cantidad * 2]
        precios = []

        for item in items:
            try:
                precio_tag = item.select_one(".price-final_price .price")
                link_tag = item.select_one(".product-item-link")
                if not (precio_tag and link_tag):
                    continue
                precio_texto = precio_tag.text.strip().replace("$", "").replace(".", "").replace(",", "")
                precio = int(precio_texto)
                link = link_tag['href']
                precios.append((precio, link))
            except Exception:
                continue

        precios_ordenados = sorted(precios, key=lambda x: x[0])
        return precios_ordenados[:cantidad]
    except Exception:
        return []

def buscar_precios_musimundo(producto, cantidad):
    return []

def buscar_precios_fravega(producto, cantidad):
    return []

def buscar_precios_garbarino(producto, cantidad):
    return []

def buscar_precios_multisitio(producto, cantidad, sitios_seleccionados):
    resultados = []

    if "MercadoLibre" in sitios_seleccionados:
        resultados.extend(buscar_precios_mercadolibre(producto, cantidad))

    if "Cetrogar" in sitios_seleccionados:
        resultados.extend(buscar_precios_cetrogar(producto, cantidad))

    if "Musimundo" in sitios_seleccionados:
        resultados.extend(buscar_precios_musimundo(producto, cantidad))

    if "Frávega" in sitios_seleccionados:
        resultados.extend(buscar_precios_fravega(producto, cantidad))

    if "Garbarino" in sitios_seleccionados:
        resultados.extend(buscar_precios_garbarino(producto, cantidad))

    precios_ordenados = sorted(resultados, key=lambda x: x[0])
    return precios_ordenados[:cantidad]

def main():
    st.title("🔎 Buscador de Precios Multisitio - Librería NEA")
    st.write("Subí un archivo Excel con los productos en la columna B y buscá los mejores precios en múltiples sitios.")

    archivo = st.file_uploader("📂 Subí tu archivo Excel", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        st.success(f"✅ Archivo cargado. Productos encontrados: {df.shape[0]}")

        cantidad_precios = st.selectbox("📊 ¿Cuántos precios querés buscar por producto?", [1, 3, 5, 10, 15], index=2)

        sitios = st.multiselect(
            "🌐 Seleccioná los sitios donde buscar precios:",
            ["MercadoLibre", "Cetrogar", "Musimundo", "Frávega", "Garbarino"],
            default=["MercadoLibre", "Cetrogar"]
        )

        if st.button("🚀 Buscar precios en sitios seleccionados"):
            resultados = []
            productos = df.iloc[:, 1].dropna().tolist()
            total_productos = len(productos)

            barra_progreso = st.progress(0)

            with st.spinner("🔍 Buscando precios, por favor esperá..."):
                for idx, producto in enumerate(productos, start=1):
                    precios = buscar_precios_multisitio(producto, cantidad_precios, sitios)
                    if precios:
                        fila = {"Producto": producto}
                        for i in range(cantidad_precios):
                            if i < len(precios):
                                fila[f"Precio {i+1}"] = precios[i][0]
                                fila[f"Fuente {i+1}"] = precios[i][1]
                            else:
                                fila[f"Precio {i+1}"] = None
                                fila[f"Fuente {i+1}"] = None
                        resultados.append(fila)

                    barra_progreso.progress(int((idx / total_productos) * 100))
                    time.sleep(random.uniform(4, 7))

            df_resultados = pd.DataFrame(resultados)
            st.success("🎯 Búsqueda completada!")

            output = io.BytesIO()
            df_resultados.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="💾 Descargar Excel de Resultados",
                data=output,
                file_name="precios_buscados_multisitio_final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
