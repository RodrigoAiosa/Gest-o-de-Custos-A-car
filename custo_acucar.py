import streamlit as st
import math

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(
    page_title="Calculadora de Custos Corporativos",
    layout="centered"
)

# =====================================================
# CSS (mantendo seu padrão visual)
# =====================================================
st.markdown("""
<style>
.stApp { background-color: #F5F5DC; }
[data-testid="stSidebar"] { background-color: #1A1A1A; }

h1 { color: #000000 !important; }

label [data-testid="stWidgetLabel"] p {
    color: #000000 !important;
    font-weight: bold !important;
}

[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
}

input {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stAlert"] {
    color: #000000 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÃO GENÉRICA DE CÁLCULO
# =====================================================
def calcular_consumo(funcionarios, consumo_dia, dias_ano, peso_unitario):
    return (funcionarios * consumo_dia * dias_ano * peso_unitario) / 1000


def calcular_custos(total_kg, preco_granel, preco_caixa, unidades_caixa, peso_unitario):
    peso_caixa_kg = (unidades_caixa * peso_unitario) / 1000
    caixas = math.ceil(total_kg / peso_caixa_kg) if peso_caixa_kg > 0 else 0
    custo_granel = total_kg * preco_granel
    custo_caixa = caixas * preco_caixa
    economia = custo_caixa - custo_granel
    return caixas, custo_granel, custo_caixa, economia


# =====================================================
# INTERFACE
# =====================================================
st.title("📊 Calculadora de Custos Corporativos")

tipo = st.selectbox(
    "Selecione o insumo",
    ["Açúcar", "Café", "Copos descartáveis", "Papel"]
)

with st.sidebar:
    st.header("📋 Parâmetros Gerais")

    func = st.number_input("Número de funcionários", min_value=1, value=50)
    consumo = st.number_input("Consumo médio por dia", min_value=1.0, value=2.0)
    dias = st.number_input("Dias úteis no ano", min_value=1, value=250)

    st.divider()
    st.header("💰 Custos")

    peso_unit = st.number_input("Peso por unidade (g)", value=5.0)
    preco_granel = st.number_input("Preço kg a granel (R$)", value=4.50)
    preco_caixa = st.number_input("Preço da caixa (R$)", value=35.00)
    unidades_caixa = st.number_input("Unidades por caixa", value=400)

# =====================================================
# CÁLCULOS
# =====================================================
total_kg = calcular_consumo(func, consumo, dias, peso_unit)

caixas, custo_granel, custo_caixa, economia = calcular_custos(
    total_kg,
    preco_granel,
    preco_caixa,
    unidades_caixa,
    peso_unit
)

# =====================================================
# RESULTADOS
# =====================================================
st.subheader(f"Resultados — {tipo}")

col1, col2, col3 = st.columns(3)
col1.metric("Consumo Anual", f"{total_kg:.1f} kg")
col2.metric("Caixas", int(caixas))
col3.metric("Economia", f"R$ {economia:,.2f}")

if economia > 0:
    st.success(f"### Economia anual estimada: R$ {economia:,.2f}")
else:
    st.warning("Não há economia no cenário atual.")
