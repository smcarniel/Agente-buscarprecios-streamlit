import streamlit as st
import pandas as pd
import time
import random
import io
import requests
from bs4 import BeautifulSoup

def buscar_precios_mercadolibre_bs4(producto, cantidad):
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

def buscar_precios_multisitio_bs4(producto, cantidad):
    # Por ahora incluye MercadoLibre. Luego podríamos expandir.
    return buscar_precios_mercadolibre_bs4(producto, cantidad)

def main():
    st.title("🔎 Buscador de Precios - Librería NEA (Final Mejorado)")
    st.write("Subí un archivo Excel con los productos en la columna B y buscá los mejores precios en MercadoLibre o en múltiples sitios.")

    archivo = st.file_uploader("📂 Subí tu archivo Excel", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        st.success(f"✅ Archivo cargado. Productos encontrados: {df.shape[0]}")

        cantidad_precios = st.selectbox("📊 ¿Cuántos precios querés buscar por producto?", [1, 3, 5, 10, 15], index=2)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Buscar precios MercadoLibre"):
                procesar_busqueda(df, cantidad_precios, modo="ML")

        with col2:
            if st.button("🔎 Buscar en múltiples sitios"):
                procesar_busqueda(df, cantidad_precios, modo="MS")

def procesar_busqueda(df, cantidad_precios, modo="ML"):
    resultados = []
    productos = df.iloc[:, 1].dropna().tolist()
    total_productos = len(productos)

    barra_progreso = st.progress(0)
    progreso = 0

    with st.spinner("🔍 Buscando precios, por favor esperá..."):
        for idx, producto in enumerate(productos, start=1):
            if modo == "ML":
                precios = buscar_precios_mercadolibre_bs4(producto, cantidad_precios)
            else:
                precios = buscar_precios_multisitio_bs4(producto, cantidad_precios)

            if precios:
                fila = {"Producto": producto}
                for i in range(cantidad_precios):
                    if i < len(precios):
                        fila[f"Precio {i+1}"] = precios[i][0]
                        fila[f"Fuente {i+1}"] = precios[i][1]
                    else:
                        fila[f"Precio {i+1}"] = None
                        fila[f"Fuente {i+1}"] = None
            else:
                fila = {"Producto": producto}
                for i in range(cantidad_precios):
                    fila[f"Precio {i+1}"] = None
                    fila[f"Fuente {i+1}"] = None

            resultados.append(fila)

            progreso = int((idx / total_productos) * 100)
            barra_progreso.progress(progreso)

            time.sleep(random.uniform(4, 7))

    df_resultados = pd.DataFrame(resultados)
    st.success("🎯 Búsqueda completada!")

    st.dataframe(df_resultados)

    output = io.BytesIO()
    nombre_archivo = "precios_buscados_bs4_mejorado_MS.xlsx" if modo == "MS" else "precios_buscados_bs4_mejorado.xlsx"
    df_resultados.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    st.download_button(
        label="💾 Descargar Excel de Resultados",
        data=output,
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()
