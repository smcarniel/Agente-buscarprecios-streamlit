import streamlit as st
import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
import io

def buscar_precios_mercadolibre(producto, intentos=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1"
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

            items = soup.select(".ui-search-layout__item")[:12]
            for item in items:
                try:
                    titulo_tag = item.select_one(".ui-search-item__title")
                    if not titulo_tag:
                        continue

                    titulo = titulo_tag.text.lower()
                    if any(palabra in titulo for palabra in palabras_excluir):
                        continue

                    precio_tag = item.select_one(".andes-money-amount__fraction")
                    if not precio_tag:
                        continue

                    precio_texto = precio_tag.text.replace(".", "")
                    precio = int(precio_texto)

                    link_tag = item.select_one("a")
                    if not link_tag or not link_tag.get('href'):
                        continue

                    link = link_tag['href']
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
            time.sleep(random.uniform(2.5, 6))  # Pausas un poquito más largas

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
