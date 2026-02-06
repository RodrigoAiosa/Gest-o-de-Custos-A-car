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

# --- INICIALIZAÇÃO DO ESTADO DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 2. ESTILIZAÇÃO CSS (TEXTOS PRETOS E BOTÃO ROXO)
st.markdown("""
    <style>
    .stApp { background-color: #F5F5DC; }
    
    /* Forçar preto em textos, labels e alertas */
    .main .stMarkdown p, .main h1, .main h2, .main h3, .main span, .main label,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    .stAlert p, .stAlert div { 
        color: #000000 !important; 
    }
    
    [data-testid="stSidebar"] { background-color: #3E2723; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #FFFFFF !important; 
    }

    .stButton>button {
        background-color: #7D3CFF;
        color: white !important;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    .stButton>button:hover { background-color: #5A27C6; color: white !important; }
    .stTextInput>div>div>input { border: 1px solid #7D3CFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---

def salvar_no_sql(nome, email, celular):
    """Insere dados na tabela Contatos preservando os existentes [cite: 2026-01-18]."""
    try:
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=RODRIGOAIOSA\SQLEXPRESS;"
            "Database=BD_APP;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        query = """
            INSERT INTO Contatos (aplicativo, nome_completo, email, celular) 
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, ("Gestão de Custos: Açúcar", nome, email, celular))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no Banco de Dados: {e}")
        return False

def validar_dados(nome, email, celular):
    """Validações estritas para Nome e Celular (apenas 11 números)."""
    regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    if len(nome) < 10:
        st.error("O nome deve conter pelo menos 10 letras.")
        return False
    if not re.search(regex_email, email):
        st.error("E-mail inválido.")
        return False
    
    # Validação do Celular: apenas dígitos e exatamente 11 caracteres
    if not celular.isdigit():
        st.error("O celular deve conter apenas números.")
        return False
    if len(celular) != 11:
        st.error("O celular deve ter exatamente 11 dígitos (DDD + Número).")
        return False
        
    return True

# --- FLUXO DE TELAS ---

if not st.session_state.autenticado:
    st.title("🎬 Cadastro de Acesso")
    st.write("Identifique-se para acessar a calculadora.")
    
    with st.form("form_cadastro"):
        nome_input = st.text_input("Nome Completo")
        email_input = st.text_input("E-mail")
        # max_chars ajuda visualmente, mas a função validar_dados garante a regra
        celular_input = st.text_input("Celular (apenas números)", max_chars=11, placeholder="11977019335")
        
        btn_acessar = st.form_submit_button("Acessar Aplicativo")
        
        if btn_acessar:
            if validar_dados(nome_input, email_input, celular_input):
                if salvar_no_sql(nome_input, email_input, celular_input):
                    st.session_state.dados_usuario = {"nome": nome_input}
                    st.session_state.autenticado = True
                    st.rerun()

else:
    # TELA PRINCIPAL (CALCULADORA)
    st.title("☕ Gestão de Custos: Açúcar")
    st.markdown(f"Olá, **{st.session_state.dados_usuario['nome']}**!")
    
    st.sidebar.header("📋 Parâmetros")
    with st.sidebar:
        funcionarios = st.number_input("Número de funcionários", min_value=1, value=50)
        xicaras_dia = st.number_input("Média de xícaras/dia", min_value=1, value=2)
        dias_ano = st.number_input("Dias úteis no ano", min_value=1, value=250)
        
        st.divider()
        st.header("💰 Custos e Pesos")
        peso_sache_g = st.number_input("Peso do sachê (g)", value=5.0)
        preco_kg_granel = st.number_input("Preço kg a granel (R$)", value=4.50)
        preco_caixa = st.number_input("Preço da caixa (R$)", value=35.00)
        sache_por_caixa = st.number_input("Sachês por caixa", value=400)

    # Lógica de Cálculo
    total_xicaras = funcionarios * xicaras_dia * dias_ano
    total_acucar_kg = (total_xicaras * peso_sache_g) / 1000
    peso_caixa_kg = (sache_por_caixa * peso_sache_g) / 1000
    caixas_necessarias = math.ceil(total_acucar_kg / peso_caixa_kg) if peso_caixa_kg > 0 else 0
    custo_granel = total_acucar_kg * preco_kg_granel
    custo_sache = caixas_necessarias * preco_caixa
    economia = custo_sache - custo_granel
    percentual = (economia / custo_sache) * 100 if custo_sache > 0 else 0

    # Resultados
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Consumo Anual", f"{total_acucar_kg:.1f} kg")
    col2.metric("Total de Xícaras", f"{total_xicaras:,.0f}".replace(",", "."))
    col3.metric("Caixas (Sachê)", f"{int(caixas_necessarias)}")

    st.markdown("---")
    st.subheader("📊 Comparativo Financeiro")
    c1, c2 = st.columns(2)
    with c1: st.info(f"**Custo A Granel:**\nR$ {custo_granel:,.2f}")
    with c2: st.warning(f"**Custo Em Sachês:**\nR$ {custo_sache:,.2f}")

    if economia > 0:
        st.success(f"### 🚀 Economia Anual: R$ {economia:,.2f}")
    else:
        st.error(f"### O sachê é mais vantajoso!")

    if st.button("Sair / Novo Cadastro"):
        st.session_state.autenticado = False
        st.rerun()