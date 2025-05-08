import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos desde el archivo Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("gasto_medio.xlsx")
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

    total_nac = num_nac * gasto_nac
    total_int = num_int * gasto_int
    total = total_nac + total_int

    return total, total_nac, total_int, num_nac, num_int

# Función para crear gráficos
def crear_graficos(total_nac, total_int, num_nac, num_int):
    # Gráfico de barras de recaudación
    recaudacion = [total_nac, total_int]
    categorias = ['Nacionales', 'Internacionales']
    
    fig, ax = plt.subplots()
    ax.bar(categorias, recaudacion, color=["blue", "orange"])
    ax.set_title('Recaudación por Tipo de Asistentes')
    ax.set_ylabel('Recaudación (€)')
    st.pyplot(fig)

    # Gráfico de pie de distribución de asistentes
    asistentes = [num_nac, num_int]
    labels = ['Nacionales', 'Internacionales']
    
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(asistentes, labels=labels, autopct='%1.1f%%', colors=["lightblue", "lightcoral"], startangle=90)
    ax_pie.set_title('Distribución de Participantes')
    st.pyplot(fig_pie)

# Interfaz Streamlit
st.title("Calculadora de Impacto Económico de Eventos")

df_datos = cargar_datos()

eventos = df_datos.columns.tolist()
evento_sel = st.selectbox("Selecciona el tipo de evento", eventos)
participantes = st.number_input("Número de participantes estimados", min_value=0, step=1)

if st.button("Calcular"):
    total, total_nac, total_int, num_nac, num_int = calcular_recaudacion(df_datos, evento_sel, participantes)
    st.success(f"Recaudación estimada total: {total:,.2f} €")
    st.info(f"👉 Nacionales: {total_nac:,.2f} €\n👉 Internacionales: {total_int:,.2f} €")

    # Mostrar gráficos
    crear_graficos(total_nac, total_int, num_nac, num_int)

