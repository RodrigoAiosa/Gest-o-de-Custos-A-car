import streamlit as st
import math

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Custo: Açúcar",
    layout="centered"
)

# 2. CSS
st.markdown("""
    <style>
    /* Fundo Bege */
    .stApp { background-color: #F5F5DC; }
    
    /* Barra Lateral Escura */
    [data-testid="stSidebar"] { background-color: #1A1A1A; }

    /* TÍTULO PRINCIPAL */
    h1 {
        color: #000000 !important;
    }

    /* Labels padrão */
    label [data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Títulos da Sidebar */
    [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
    }

    /* Inputs */
    input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Botão */
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: none;
    }

    /* ===== DESTAQUES ===== */

    /* Valores das métricas */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: bold;
    }

    /* Labels das métricas */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-weight: bold;
    }

    /* Caixa de economia */
    [data-testid="stAlert"] {
        color: #000000 !important;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)

# 3. INTERFACE
st.title("☕ Gestão de Custos: Açúcar")

with st.sidebar:
    st.header("📋 Parâmetros")
    func = st.number_input("Número de funcionários", min_value=1, value=50)
    xic = st.number_input("Média de xícaras/dia", min_value=1, value=2)
    dias = st.number_input("Dias úteis no ano", min_value=1, value=250)

    st.divider()

    st.header("💰 Custos e Pesos")
    p_sache = st.number_input("Peso do sachê (g)", value=5.0)
    p_granel = st.number_input("Preço kg a granel (R$)", value=4.50)
    p_caixa = st.number_input("Preço da caixa (R$)", value=35.00)
    s_caixa = st.number_input("Sachês por caixa", value=400)

# 4. CÁLCULOS
total_kg = (func * xic * dias * p_sache) / 1000
peso_caixa_kg = (s_caixa * p_sache) / 1000
caixas = math.ceil(total_kg / peso_caixa_kg) if peso_caixa_kg > 0 else 0
c_granel = total_kg * p_granel
c_sache = caixas * p_caixa
economia = c_sache - c_granel

# 5. RESULTADOS
st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Consumo Anual", f"{total_kg:.1f} kg")
col2.metric("Caixas (Sachê)", int(caixas))
col3.metric("Economia", f"R$ {economia:,.2f}")

if economia > 0:
    st.success(f"### 🚀 Economia Anual: R$ {economia:,.2f}")

# --- RODAPÉ (FOOTER) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
footer_html = """
<div style='text-align: center; color: gray;'>
    <p style='margin-bottom: 5px;'>Desenvolvido por <b>Rodrigo AIOSA</b></p>
    <div style='display: flex; justify-content: center; gap: 20px; font-size: 24px;'>
        <a href='https://wa.me/5511977019335' target='_blank' style='text-decoration: none;'>
            <img src='https://cdn-icons-png.flaticon.com/512/733/733585.png' width='25' height='25' title='WhatsApp'>
        </a>
        <a href='https://www.linkedin.com/in/rodrigoaiosa/' target='_blank' style='text-decoration: none;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='25' height='25' title='LinkedIn'>
        </a>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
