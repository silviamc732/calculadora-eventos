import streamlit as st
import pandas as pd

# Ruta del archivo (en la misma carpeta)
ARCHIVO_EXCEL = "gasto_medio.xlsx"

# Cargar datos desde archivo local
@st.cache_data
def cargar_datos():
    df = pd.read_excel(ARCHIVO_EXCEL)
    df.set_index(["TIPO", "METRICA"], inplace=True)
    return df

# Función de cálculo
def calcular_recaudacion(df, evento, participantes):
    gasto_nac = df.loc[("Nacional", "GASTO MEDIO"), evento]
    porc_nac = df.loc[("Nacional", "%PARTICIPACION"), evento] / 100

    gasto_int = df.loc[("Internacional", "GASTO MEDIO"), evento]
    porc_int = df.loc[("Internacional", "%PARTICIPACION"), evento] / 100

    num_nac = participantes * porc_nac
    num_int = participantes * porc_int

    total = (num_nac * gasto_nac) + (num_int * gasto_int)
    return round(total, 2), round(num_nac * gasto_nac, 2), round(num_int * gasto_int, 2)

# Interfaz Streamlit
st.title("Calculadora de Impacto Económico de Eventos")

try:
    df_datos = cargar_datos()
    eventos = df_datos.columns.tolist()

    evento_sel = st.selectbox("Selecciona el tipo de evento", eventos)
    participantes = st.number_input("Número de participantes estimados", min_value=0, step=1)

    if st.button("Calcular"):
        total, total_nac, total_int = calcular_recaudacion(df_datos, evento_sel, participantes)
        st.success(f"Recaudación estimada total: {total:,.2f} €")
        st.info(f"👉 Nacionales: {total_nac:,.2f} €\n👉 Internacionales: {total_int:,.2f} €")

except FileNotFoundError:
    st.error(f"No se encontró el archivo '{ARCHIVO_EXCEL}'. Asegúrate de que está en la misma carpeta que este script.")
