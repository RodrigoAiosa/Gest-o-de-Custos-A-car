import streamlit as st
import math

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Custo: Açúcar", 
    page_icon="☕", 
    layout="centered"
)

# 2. DESIGN MODERNO E MINIMALISTA (PRETO NO BEGE)
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp { background-color: #F5F5DC; }
    
    /* Todos os textos, títulos e rótulos em PRETO */
    h1, h2, h3, p, label, span, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #000000 !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Campos de Entrada Brancos com Borda Preta */
    input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #000000 !important;
        border-radius: 5px !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* BOTÃO: FUNDO PRETO E TEXTO BRANCO */
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 5px;
        border: none;
        width: 100%;
        font-weight: bold;
        height: 3.5em;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #333333 !important;
        color: #FFFFFF !important;
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] { background-color: #1A1A1A; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    
    /* Ajuste de métricas para ficarem pretas */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TELA ÚNICA (CALCULADORA DIRETA) ---

st.title("☕ Gestão de Custos: Açúcar")
st.write("Ajuste os parâmetros na barra lateral para calcular a economia.")

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

# Lógica de Cálculo
total_xic = func * xic * dias
total_kg = (total_xic * p_sache) / 1000
peso_caixa_kg = (s_caixa * p_sache) / 1000
caixas = math.ceil(total_kg / peso_caixa_kg) if peso_caixa_kg > 0 else 0
c_granel = total_kg * p_granel
c_sache = caixas * p_caixa
economia = c_sache - c_granel

# Resultados
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Consumo Anual", f"{total_kg:.1f} kg")
col2.metric("Total Xícaras", f"{total_xic:,}".replace(",", "."))
col3.metric("Caixas (Sachê)", int(caixas))

st.markdown("---")
st.subheader("📊 Comparativo Financeiro")
st.info(f"**Custo A Granel:** R$ {c_granel:,.2f}")
st.warning(f"**Custo Em Sachês:** R$ {c_sache:,.2f}")

if economia > 0:
    st.success(f"### 🚀 Economia Anual: R$ {economia:,.2f}")
else:
    st.error("### O sachê é mais vantajoso!")
