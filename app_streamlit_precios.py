import streamlit as st
import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
import io

def buscar_precios_mercadolibre(producto, intentos=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://listado.mercadolibre.com.ar/{producto.replace(' ', '-')}_OrderId_PRICE"

    palabras_excluir = ["broches", "pack", "insumos", "repuesto"]

    for intento in range(intentos):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                time.sleep(2)
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            resultados = []
            for item in soup.select(".ui-search-layout__item")[:8]:
                try:
                    titulo = item.select_one(".ui-search-item__title").text.lower()
                    if any(palabra in titulo for palabra in palabras_excluir):
                        continue
                    precio_texto = item.select_one(".andes-money-amount__fraction").text.replace(".", "")
                    precio = int(precio_texto)
                    link = item.select_one("a")['href']
                    tienda = "MercadoLibre"
                    resultados.append((precio, tienda, link))
                except Exception:
                    continue
            resultados_ordenados = sorted(resultados, key=lambda x: x[0])
            return resultados_ordenados[:3]
        except Exception as e:
            time.sleep(2)
    return []

def procesar_productos(df):
    productos = df.iloc[:, 1].dropna().tolist()
    resultados = []
    total_productos = len(productos)

    for idx, producto in enumerate(productos, start=1):
        with st.spinner(f"Buscando precios para ({idx}/{total_productos}): {producto}"):
            precios = buscar_precios_mercadolibre(producto)
            if precios:
                fila = {
                    "Producto": producto,
                    "Precio 1": precios[0][0], "Fuente 1": precios[0][2],
                    "Precio 2": precios[1][0] if len(precios) > 1 else None, "Fuente 2": precios[1][2] if len(precios) > 1 else None,
                    "Precio 3": precios[2][0] if len(precios) > 2 else None, "Fuente 3": precios[2][2] if len(precios) > 2 else None,
                }
            else:
                fila = {
                    "Producto": producto,
                    "Precio 1": None, "Fuente 1": None,
                    "Precio 2": None, "Fuente 2": None,
                    "Precio 3": None, "Fuente 3": None,
                }
            resultados.append(fila)
            time.sleep(random.uniform(2, 5))
    return pd.DataFrame(resultados)

def main():
    st.title("Agente de Búsqueda de Precios - Librería NEA")
    st.write("Subí tu archivo Excel con la lista de productos en la columna B.")

    archivo = st.file_uploader("Subí tu Excel", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        st.success(f"Archivo cargado correctamente. Total de filas: {df.shape[0]}")

        if st.button("🔍 Buscar precios"):
            resultados = procesar_productos(df)
            st.success("🎉 Búsqueda terminada!")

            st.dataframe(resultados)

            output = io.BytesIO()
            resultados.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="💾 Descargar Excel de Resultados",
                data=output,
                file_name="Precios_Buscados_Resultados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
