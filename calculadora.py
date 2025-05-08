import streamlit as st
import pandas as pd
import plotly.express as px

# --- Cargar datos desde Excel ---
@st.cache_data
def cargar_datos():
    df = pd.read_excel("gasto_medio.xlsx", index_col=[0, 1])
    return df

df = cargar_datos()

# --- Interfaz de usuario ---
st.title("🧮 Calculadora de impacto económico de reuniones")
st.markdown("Selecciona el tipo de reunión y el número estimado de asistentes para predecir la recaudación.")

evento_sel = st.selectbox("Tipo de evento", df.columns)
participantes = st.number_input("Número total de participantes", min_value=1, value=100)

# --- Valores por defecto desde Excel ---
dias_nac_def = df.loc[("Nacional", "DIAS MEDIOS"), evento_sel]
dias_int_def = df.loc[("Internacional", "DIAS MEDIOS"), evento_sel]

fee_nac_def = df.loc[("Nacional", "GASTO MEDIO"), evento_sel]
fee_int_def = df.loc[("Internacional", "GASTO MEDIO"), evento_sel]

porc_nac_def = df.loc[("Nacional", "%PARTICIPACION"), evento_sel]
porc_int_def = df.loc[("Internacional", "%PARTICIPACION"), evento_sel]

# --- Ajustes opcionales ---
st.markdown("### 🔧 Ajustes opcionales (puedes modificarlos si conoces los datos reales)")

dias_nac = st.number_input("Días de estancia (Nacionales)", value=int(dias_nac_def), step=1)
dias_int = st.number_input("Días de estancia (Internacionales)", value=int(dias_int_def), step=1)

fee_nac = st.number_input("Gasto medio total por persona (Nacionales)", value=float(fee_nac_def), step=10.0)
fee_int = st.number_input("Gasto medio total por persona (Internacionales)", value=float(fee_int_def), step=10.0)

porc_nac = st.slider("Porcentaje de asistentes Nacionales (%)", 0, 100, int(porc_nac_def))
porc_int = 100 - porc_nac
st.markdown(f"👉 Porcentaje de asistentes Internacionales: **{porc_int}%**")

# --- Cálculo de resultados ---
if st.button("Calcular"):
    num_nac = participantes * (porc_nac / 100)
    num_int = participantes * (porc_int / 100)

    total_nac = num_nac * fee_nac
    total_int = num_int * fee_int
    total = total_nac + total_int

    # Resultados
    st.success(f"💰 Recaudación estimada total: {total:,.2f} €")
    st.info(f"👉 Nacionales: {total_nac:,.2f} €\n👉 Internacionales: {total_int:,.2f} €")

    # Párrafo destacado
    st.markdown(
        f"""
        <div style="background-color:#fff8b3; padding:10px; border-radius:10px; margin-top:10px;">
            <b>Porcentaje de participación:</b> Nacionales: {porc_nac}% &nbsp;&nbsp; Internacionales: {porc_int}%
        </div>
        """,
        unsafe_allow_html=True
    )


    # Gráfico 2: Recaudación por origen
    df_gasto = pd.DataFrame({
        'Origen': ['Nacionales', 'Internacionales'],
        'Recaudación (€)': [total_nac, total_int]
    })
    fig2 = px.bar(df_gasto, x='Origen', y='Recaudación (€)',
                  title='Recaudación por origen de asistentes',
                  text='Recaudación (€)',
                  color='Origen',
                  color_discrete_map={'Nacionales': '#f4a582', 'Internacionales': '#92c5de'})
    fig2.update_layout(yaxis_tickformat=",.0f")
    st.plotly_chart(fig2)

    # Gráfico 3: Gasto diario por asistente
    df_dia = pd.DataFrame({
        'Origen': ['Nacionales', 'Internacionales'],
        'Gasto diario (€)': [fee_nac / dias_nac, fee_int / dias_int]
    })
    fig3 = px.bar(df_dia, x='Origen', y='Gasto diario (€)',
                  title='Gasto medio diario por asistente',
                  text='Gasto diario (€)',
                  color='Origen',
                  color_discrete_map={'Nacionales': '#d95f02', 'Internacionales': '#1b9e77'})
    fig3.update_layout(yaxis_tickformat=",.0f")
    st.plotly_chart(fig3)


