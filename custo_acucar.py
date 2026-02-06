import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import math
import re

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Custo: Açúcar", 
    page_icon="☕", 
    layout="centered"
)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

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

    /* Remove o fundo e bordas do formulário (Design Clean) */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background-color: transparent !important;
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

# 3. CONEXÃO COM GOOGLE SHEETS
# Certifique-se de configurar o link da planilha nos Secrets do Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

def salvar_no_sheets(nome, email, celular):
    """Salva dados na planilha preservando os existentes [cite: 2026-01-18]."""
    try:
        # Lê os dados atuais
        df_atual = conn.read()
        
        # Cria a nova linha
        novo_registro = pd.DataFrame([{
            "aplicativo": "Gestão de Custos: Açúcar",
            "nome_completo": nome,
            "email": email,
            "celular": celular
        }])
        
        # Concatena preservando o histórico
        df_final = pd.concat([df_atual, novo_registro], ignore_index=True)
        
        # Atualiza a planilha
        conn.update(data=df_final)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar na Planilha: {e}")
        return False

def validar_dados(nome, email, celular):
    regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if len(nome) < 10:
        st.error("O nome deve ter pelo menos 10 letras.")
        return False
    if not re.search(regex_email, email):
        st.error("E-mail inválido.")
        return False
    if not celular.isdigit() or len(celular) != 11:
        st.error("Celular deve ter 11 dígitos (apenas números).")
        return False
    return True

# --- FLUXO DE TELAS ---

if not st.session_state.autenticado:
    st.markdown("# 🎬 Cadastro de Acesso")
    st.write("Identifique-se para acessar a calculadora.")
    
    with st.form("form_cadastro"):
        nome_input = st.text_input("Nome Completo")
        email_input = st.text_input("E-mail")
        celular_input = st.text_input("Celular", max_chars=11, placeholder="11977019335")
        
        if st.form_submit_button("Acessar Aplicativo"):
            if validar_dados(nome_input, email_input, celular_input):
                if salvar_no_sheets(nome_input, email_input, celular_input):
                    st.session_state.dados_usuario = {"nome": nome_input}
                    st.session_state.autenticado = True
                    st.rerun()

else:
    # TELA PRINCIPAL (CALCULADORA)
    st.title("☕ Gestão de Custos: Açúcar")
    st.markdown(f"### Bem-vindo, {st.session_state.dados_usuario['nome']}!")
    
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

    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()