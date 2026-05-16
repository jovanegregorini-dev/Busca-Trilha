import streamlit as st
import pandas as pd

# Configuração da página padrão MRGLabs Studio
st.set_page_config(page_title="Buscador de Trilhas MRGLabs", page_icon="🎵", layout="wide")

# Estilo Dark Mode profissional para o estúdio
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stButton>button { background-color: #00ffcc; color: #0e1117; font-weight: bold; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #00cc99; color: white; }
    div[data-testid="stBlock"] {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #2d313f;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 Buscador de Trilhas - MRGLabs")
st.write("Filtre e encontre suas trilhas brancas favoritas do Artlist e Envato Elements instantaneamente.")

# --- BANCO DE DADOS DAS SUAS TRILHAS ---
# Dica: Você pode ir adicionando mais linhas aqui dentro desse padrão sempre que quiser!
@st.cache_data
def carregar_banco_trilhas():
    dados = [
        {
            "Nome da Trilha": "Corporate Uplifting & Inspiring",
            "Plataforma": "Envato Elements",
            "Estilo / Clima": "Corporativo / Motivado",
            "Ritmo": "Médio",
            "Tags": "tecnologia, inovação, empresa, manifesto",
            "Link": "https://elements.envato.com/"
        },
        {
            "Nome da Trilha": "Epic Cinematic Drums & Thunder",
            "Plataforma": "Artlist",
            "Estilo / Clima": "Varejo Épico / Impacto",
            "Ritmo": "Rápido",
            "Tags": "bateria, comercial, forte, impacto, varejo",
            "Link": "https://artlist.io/"
        },
        {
            "Nome da Trilha": "Emotional Piano Background",
            "Plataforma": "Envato Elements",
            "Estilo / Clima": "Emocional / Suave",
            "Ritmo": "Lento",
            "Tags": "piano, sensível, drama, locução mansa",
            "Link": "https://elements.envato.com/"
        },
        {
            "Nome da Trilha": "Modern Tech Groove",
            "Plataforma": "Artlist",
            "Estilo / Clima": "Corporativo / Dinâmico",
            "Ritmo": "Rápido",
            "Tags": "eletrônica, batida, jovem, agronegócio, agro",
            "Link": "https://artlist.io/"
        }
    ]
    return pd.DataFrame(dados)

df_trilhas = carregar_banco_trilhas()

# --- FILTROS LATERAIS (IGUAL AO SEU CODEPEN) ---
st.sidebar.header("🔍 Filtros de Busca")

busca_texto = st.sidebar.text_input("Buscar por Nome ou Tag (ex: agro, piano)").strip().lower()

plataformas = ["Todas"] + list(df_trilhas["Plataforma"].unique())
filtro_plat = st.sidebar.selectbox("Plataforma", plataformas)

estilos = ["Todos"] + list(df_trilhas["Estilo / Clima"].unique())
filtro_estilo = st.sidebar.selectbox("Estilo / Clima", estilos)

ritmos = ["Todos"] + list(df_trilhas["Ritmo"].unique())
filtro_ritmo = st.sidebar.selectbox("Ritmo", ritmos)

# --- PROCESSAMENTO DOS FILTROS ---
df_filtrado = df_trilhas.copy()

if filtro_plat != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Plataforma"] == filtro_plat]

if filtro_estilo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Estilo / Clima"] == filtro_estilo]

if filtro_ritmo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Ritmo"] == filtro_ritmo]

if busca_texto:
    df_filtrado = df_filtrado[
        df_filtrado["Nome da Trilha"].str.lower().str.contains(busca_texto) | 
        df_filtrado["Tags"].str.lower().str.contains(busca_texto)
    ]

# --- RESULTADOS COM DESIGN EM CARDS ---
st.subheader(f"📋 Trilhas Disponíveis ({len(df_filtrado)})")

if df_filtrado.empty:
    st.warning("Nenhuma trilha bate com os filtros aplicados.")
else:
    for idx, row in df_filtrado.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {row['Nome da Trilha']}")
                st.markdown(f"📍 **Plataforma:** `{row['Plataforma']}` | ⚡ **Ritmo:** {row['Ritmo']} | 🎭 **Estilo:** {row['Estilo / Clima']}")
                st.markdown(f"🏷️ *Tags:* {row['Tags']}")
            with col2:
                st.write("")
                st.write("")
                st.link_button("🚀 Abrir Link", row["Link"])
