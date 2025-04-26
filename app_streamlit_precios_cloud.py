import streamlit as st
import pandas as pd
import time
import random
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def buscar_precios_mercadolibre(producto, driver):
    try:
        url = f"https://listado.mercadolibre.com.ar/{producto.replace(' ', '-')}_OrderId_PRICE"
        driver.get(url)
        time.sleep(random.uniform(4, 6))

        items = driver.find_elements(By.CSS_SELECTOR, ".ui-search-layout__item")[:10]
        precios = []

        for item in items:
            try:
                precio_element = item.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction")
                link_element = item.find_element(By.TAG_NAME, "a")
                
                precio_texto = precio_element.text.replace(".", "").replace(",", "")
                precio = int(precio_texto)
                link = link_element.get_attribute('href')

                precios.append((precio, link))
            except Exception:
                continue

        precios_ordenados = sorted(precios, key=lambda x: x[0])
        return precios_ordenados[:3]
    except Exception as e:
        return []

def inicializar_driver_cloud():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--single-process")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def main():
    st.title("🔎 Buscador de Precios - Librería NEA (Cloud)")
    st.write("Subí un archivo Excel con los productos en la columna B y buscá los mejores precios en MercadoLibre.")

    archivo = st.file_uploader("📂 Subí tu archivo Excel", type=["xlsx"])

    if archivo is not None:
        df = pd.read_excel(archivo)
        st.success(f"✅ Archivo cargado. Productos encontrados: {df.shape[0]}")

        if st.button("🚀 Buscar precios"):
            driver = inicializar_driver_cloud()

            resultados = []
            productos = df.iloc[:, 1].dropna().tolist()
            total_productos = len(productos)

            with st.spinner("🔍 Buscando precios, por favor esperá..."):
                for idx, producto in enumerate(productos, start=1):
                    precios = buscar_precios_mercadolibre(producto, driver)
                    if precios:
                        fila = {
                            "Producto": producto,
                            "Precio 1": precios[0][0], "Fuente 1": precios[0][1],
                            "Precio 2": precios[1][0] if len(precios) > 1 else None, "Fuente 2": precios[1][1] if len(precios) > 1 else None,
                            "Precio 3": precios[2][0] if len(precios) > 2 else None, "Fuente 3": precios[2][1] if len(precios) > 2 else None,
                        }
                    else:
                        fila = {
                            "Producto": producto,
                            "Precio 1": None, "Fuente 1": None,
                            "Precio 2": None, "Fuente 2": None,
                            "Precio 3": None, "Fuente 3": None,
                        }
                    resultados.append(fila)

                    time.sleep(random.uniform(6, 10))

            driver.quit()

            df_resultados = pd.DataFrame(resultados)
            st.success("🎯 Búsqueda completada!")

            st.dataframe(df_resultados)

            output = io.BytesIO()
            df_resultados.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="💾 Descargar Excel de Resultados",
                data=output,
                file_name="precios_buscados_resultados_cloud.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
