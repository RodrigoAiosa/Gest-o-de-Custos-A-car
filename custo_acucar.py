import streamlit as st
import math

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Custo: Açúcar", 
    page_icon="☕", 
    layout="centered"
)

# 2. DESIGN CORRIGIDO: RÓTULOS DA SIDEBAR EM BRANCO, RESTO LEGÍVEL
st.markdown("""
    <style>
    /* FUNDO GERAL BEGE */
    .stApp { background-color: #F5F5DC; }
    
    /* ÁREA PRINCIPAL: TUDO EM PRETO */
    .main h1, .main h2, .main h3, .main p, .main span, .main label {
        color: #000000 !important;
    }

    /* BARRA LATERAL: FUNDO ESCURO */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
    }

    /* AQUI ESTÁ O QUE VOCÊ QUER: SOMENTE OS RÓTULOS DOS PARÂMETROS EM BRANCO */
    /* Mirando especificamente no parágrafo do label dentro da sidebar */
    [data-testid="stSidebar"] label [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-size: 1rem !important;
    }

    /* TÍTULOS DA SIDEBAR EM BRANCO */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    /* INPUTS: FUNDO BRANCO E TEXTO PRETO (PARA NÃO LER COM O CU) */
    [data-testid="stSidebar"] input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* BOTÕES DE MAIS E MENOS DO INPUT EM BRANCO PARA ENXERGAR NO FUNDO ESCURO */
    [data-testid="stSidebar"] button[data-testid="stNumberInputStepUp"], 
    [data-testid="stSidebar"] button[data-testid="stNumberInputStepDown"] {
        background-color: #333333 !important;
        color: #FFFFFF !important;
    }

    /* BOTÃO PRINCIPAL PRETO COM TEXTO BRANCO */
    .stButton>button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TELA DA CALCULADORA ---

st.title("☕ Gestão de Custos: Açúcar")

with st.sidebar:
    st.header("📋 Parâmetros")
    # Estes rótulos agora aparecem em BRANCO
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

# Resultados na Área Principal
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
