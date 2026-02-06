import streamlit as st
import math
import re
import pyodbc

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Calculadora de Custo: Açúcar", 
    page_icon="☕", 
    layout="centered"
)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 2. DESIGN MODERNO E MINIMALISTA (FOCO NO BOTÃO COM TEXTO BRANCO)
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp { background-color: #F5F5DC; }
    
    /* Títulos, Rótulos e Textos em Preto */
    h1, h2, h3, p, label, span, .stMarkdown {
        color: #000000 !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Formulário Minimalista (Removendo fundos escuros/cinzas) */
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

    input::placeholder {
        color: #888888 !important;
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
    
    /* Hover do Botão: Mantém texto branco */
    .stButton>button:hover {
        background-color: #333333 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] { background-color: #1A1A1A; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---

def salvar_no_sql(nome, email, celular):
    """Insere dados na tabela Contatos preservando os existentes."""
    try:
        # Nota: Trusted_Connection só funciona localmente. 
        # No Cloud, use UID e PWD na string.
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=RODRIGOAIOSA\SQLEXPRESS;"
            "Database=BD_APP;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "INSERT INTO Contatos (aplicativo, nome_completo, email, celular) VALUES (?, ?, ?, ?)"
        cursor.execute(query, ("Gestão de Custos: Açúcar", nome, email, celular))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro no Banco de Dados: {e}")
        return False

def validar_dados(nome, email, celular):
    regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if len(nome) < 10:
        st.error("Nome deve ter 10+ letras.")
        return False
    if not re.search(regex_email, email):
        st.error("E-mail inválido.")
        return False
    if not celular.isdigit() or len(celular) != 11:
        st.error("Celular deve ter 11 dígitos.")
        return False
    return True

# --- FLUXO DE TELAS ---

if not st.session_state.autenticado:
    st.markdown("# 🎬 Cadastro de Acesso")
    st.write("Preencha os dados para continuar.")
    
    with st.form("form_cadastro"):
        nome_input = st.text_input("Nome Completo")
        email_input = st.text_input("E-mail")
        celular_input = st.text_input("Celular (apenas números)", max_chars=11, placeholder="11977019335")
        
        # Botão agora com texto branco garantido pelo CSS
        if st.form_submit_button("Acessar Aplicativo"):
            if validar_dados(nome_input, email_input, celular_input):
                if salvar_no_sql(nome_input, email_input, celular_input):
                    st.session_state.dados_usuario = {"nome": nome_input}
                    st.session_state.autenticado = True
                    st.rerun()

else:
    # TELA PRINCIPAL
    st.title("☕ Gestão de Custos: Açúcar")
    st.markdown(f"### Bem-vindo, {st.session_state.dados_usuario['nome']}")
    
    with st.sidebar:
        st.header("📋 Parâmetros")
        funcionarios = st.number_input("Funcionários", min_value=1, value=50)
        xicaras_dia = st.number_input("Xícaras/dia", min_value=1, value=2)
        dias_ano = st.number_input("Dias úteis/ano", min_value=1, value=250)
        st.divider()
        peso_sache_g = st.number_input("Peso sachê (g)", value=5.0)
        preco_kg_granel = st.number_input("Preço kg (R$)", value=4.50)
        preco_caixa = st.number_input("Preço caixa (R$)", value=35.00)
        sache_por_caixa = st.number_input("Sachês/caixa", value=400)

    # Cálculos
    total_xicaras = funcionarios * xicaras_dia * dias_ano
    total_kg = (total_xicaras * peso_sache_g) / 1000
    peso_caixa_kg = (sache_por_caixa * peso_sache_g) / 1000
    caixas = math.ceil(total_kg / peso_caixa_kg) if peso_caixa_kg > 0 else 0
    custo_granel = total_kg * preco_kg_granel
    custo_sache = caixas * preco_caixa
    economia = custo_sache - custo_granel

    # Display de Resultados
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Consumo Anual", f"{total_kg:.1f} kg")
    c2.metric("Xícaras", f"{total_xicaras:,.0f}")
    c3.metric("Caixas", int(caixas))

    st.info(f"Custo Granel: R$ {custo_granel:,.2f}")
    st.warning(f"Custo Sachê: R$ {custo_sache:,.2f}")
    
    if economia > 0:
        st.success(f"Economia Anual: R$ {economia:,.2f}")

    if st.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
