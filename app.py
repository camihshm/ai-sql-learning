import streamlit as st
import sqlite3
import pandas as pd
from typing import Dict, Any, List

# -------------------------------
# CONFIGURAÇÃO INICIAL DA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Curso Interativo de SQL",
    layout="wide",
    page_icon="🧠"
)

# -------------------------------
# FUNÇÕES DE BANCO DE DADOS
# -------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Cria (ou reaproveita) uma conexão SQLite.
    Para demo, usaremos um arquivo local.
    """
    conn = sqlite3.connect("marketing_bebidas.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Cria as tabelas e insere dados caso ainda não existam.
    """
    cursor = conn.cursor()

    # Cria tabelas
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS dim_produto (
        id_produto INTEGER PRIMARY KEY,
        nome_produto TEXT,
        categoria TEXT,
        preco REAL
    );

    CREATE TABLE IF NOT EXISTS dim_campanha (
        id_campanha INTEGER PRIMARY KEY,
        canal TEXT,
        objetivo TEXT
    );

    CREATE TABLE IF NOT EXISTS fato_marketing (
        id_fato INTEGER PRIMARY KEY,
        id_produto INTEGER,
        id_campanha INTEGER,
        data TEXT,
        impressoes INTEGER,
        cliques INTEGER,
        gastos REAL,
        vendas INTEGER,
        FOREIGN KEY (id_produto) REFERENCES dim_produto(id_produto),
        FOREIGN KEY (id_campanha) REFERENCES dim_campanha(id_campanha)
    );
    """)

    # Verifica se já tem dados
    cursor.execute("SELECT COUNT(*) FROM dim_produto;")
    qtd_produtos = cursor.fetchone()[0]

    if qtd_produtos == 0:
        # Insere dados de exemplo
        cursor.executescript("""
        INSERT INTO dim_produto (id_produto, nome_produto, categoria, preco) VALUES
        (1, 'Refrigerante Cola', 'Refrigerante', 6.50),
        (2, 'Água Mineral 500ml', 'Água', 2.50),
        (3, 'Suco Tropical', 'Suco', 7.90);

        INSERT INTO dim_campanha (id_campanha, canal, objetivo) VALUES
        (101, 'Instagram', 'Alcance'),
        (102, 'Facebook', 'Conversão'),
        (103, 'Google Ads', 'Cliques');

        INSERT INTO fato_marketing (id_fato, id_produto, id_campanha, data,
                                    impressoes, cliques, gastos, vendas) VALUES
        (1, 1, 101, '2025-01-10', 50000, 1200, 800.00, 150),
        (2, 1, 102, '2025-01-11', 30000, 800, 600.00, 90),
        (3, 2, 103, '2025-01-12', 45000, 2000, 1500.00, 300),
        (4, 3, 101, '2025-01-10', 20000, 400, 300.00, 45),
        (5, 3, 102, '2025-01-11', 26000, 610, 500.00, 70);
        """)
        conn.commit()


def run_query(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Executa uma query SQL e retorna um DataFrame.
    Lança exceção se a query for inválida.
    """
    df = pd.read_sql_query(query, conn)
    return df


# -------------------------------
# DESAFIOS / GAMIFICAÇÃO
# -------------------------------

def get_challenges() -> List[Dict[str, Any]]:
    """
    Retorna a lista de desafios com a query esperada.
    A validação será feita comparando o resultado
    do aluno com o resultado da query esperada.
    """
    challenges = [
        {
            "id": 1,
            "titulo": "Vendas por produto",
            "descricao": "Liste o total de vendas (vendas) por produto.",
            "dica": "Use SUM(vendas) e GROUP BY nome_produto.",
            "expected_query": """
                SELECT p.nome_produto, SUM(f.vendas) AS total_vendas
                FROM fato_marketing f
                JOIN dim_produto p ON f.id_produto = p.id_produto
                GROUP BY p.nome_produto
            """
        },
        {
            "id": 2,
            "titulo": "Gasto total por canal",
            "descricao": "Calcule quanto foi gasto em cada canal de campanha.",
            "dica": "Use SUM(gastos) e agrupe por canal.",
            "expected_query": """
                SELECT c.canal, SUM(f.gastos) AS total_gasto
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY c.canal
            """
        },
        {
            "id": 3,
            "titulo": "Campanha com mais cliques por canal",
            "descricao": "Mostre o maior número de cliques registrado por canal.",
            "dica": "Use MAX(cliques) e GROUP BY canal.",
            "expected_query": """
                SELECT c.canal, MAX(f.cliques) AS max_cliques
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY c.canal
            """
        },
        {
            "id": 4,
            "titulo": "CPC por fato",
            "descricao": "Calcule o custo por clique (CPC) de cada linha da fato_marketing.",
            "dica": "Divida gastos por cliques. Use 1.0 * cliques para forçar número real.",
            "expected_query": """
                SELECT id_fato, gastos / cliques AS cpc
                FROM fato_marketing
            """
        },
        {
            "id": 5,
            "titulo": "Produto com menor CPC médio",
            "descricao": "Descubra qual produto tem o menor CPC médio.",
            "dica": "Use AVG(gastos / cliques), GROUP BY produto e ORDER BY ASC LIMIT 1.",
            "expected_query": """
                SELECT p.nome_produto, AVG(f.gastos * 1.0 / f.cliques) AS cpc_medio
                FROM fato_marketing f
                JOIN dim_produto p ON f.id_produto = p.id_produto
                GROUP BY p.nome_produto
                ORDER BY cpc_medio ASC
                LIMIT 1
            """
        },
        {
            "id": 6,
            "titulo": "Impressões por data",
            "descricao": "Some as impressões por data.",
            "dica": "Use SUM(impressoes) e GROUP BY data.",
            "expected_query": """
                SELECT data, SUM(impressoes) AS total_impressoes
                FROM fato_marketing
                GROUP BY data
            """
        },
        {
            "id": 7,
            "titulo": "Vendas por canal",
            "descricao": "Mostre quanto cada canal vendeu no total.",
            "dica": "Use SUM(vendas) e agrupe por canal.",
            "expected_query": """
                SELECT c.canal, SUM(f.vendas) AS total_vendas
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY c.canal
                ORDER BY total_vendas DESC
            """
        },
        {
            "id": 8,
            "titulo": "CTR por fato",
            "descricao": "Calcule o CTR (cliques / impressões) de cada linha.",
            "dica": "Use 1.0 * cliques / impressoes.",
            "expected_query": """
                SELECT id_fato, 1.0 * cliques / impressoes AS ctr
                FROM fato_marketing
            """
        },
        {
            "id": 9,
            "titulo": "Campanhas do Instagram",
            "descricao": "Liste todas as linhas da fato_marketing apenas para canal = 'Instagram'.",
            "dica": "Filtre pelo canal na dim_campanha.",
            "expected_query": """
                SELECT f.*
                FROM fato_marketing f
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                WHERE c.canal = 'Instagram'
            """
        },
        {
            "id": 10,
            "titulo": "Vendas por produto e canal",
            "descricao": "Mostre quanto cada combinação produto + canal vendeu.",
            "dica": "Junte fato + produto + campanha e use GROUP BY.",
            "expected_query": """
                SELECT p.nome_produto, c.canal, SUM(f.vendas) AS total_vendas
                FROM fato_marketing f
                JOIN dim_produto p ON f.id_produto = p.id_produto
                JOIN dim_campanha c ON f.id_campanha = c.id_campanha
                GROUP BY p.nome_produto, c.canal
            """
        },
    ]
    return challenges


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena colunas e linhas para comparar resultados
    independentemente da ordem.
    """
    if df is None or df.empty:
        return df
    df_norm = df.copy()
    df_norm = df_norm.reindex(sorted(df_norm.columns), axis=1)
    df_norm = df_norm.sort_values(by=list(df_norm.columns)).reset_index(drop=True)
    return df_norm


def validate_answer(conn: sqlite3.Connection, challenge: Dict[str, Any], user_query: str) -> Dict[str, Any]:
    """
    Compara o resultado da query do aluno com o resultado da query esperada.
    Retorna dict com status e mensagens.
    """
    result = {
        "ok": False,
        "error": None,
        "df_user": None,
        "df_expected": None
    }

    try:
        df_expected = run_query(conn, challenge["expected_query"])
        df_user = run_query(conn, user_query)

        df_expected_norm = normalize_df(df_expected)
        df_user_norm = normalize_df(df_user)

        result["df_user"] = df_user
        result["df_expected"] = df_expected

        if df_expected_norm.equals(df_user_norm):
            result["ok"] = True
        else:
            result["ok"] = False

    except Exception as e:
        result["error"] = str(e)

    return result


# -------------------------------
# ESTADO DA SESSÃO (XP, PROGRESSO)
# -------------------------------

if "xp" not in st.session_state:
    st.session_state["xp"] = 0

if "completed_challenges" not in st.session_state:
    st.session_state["completed_challenges"] = set()


def add_xp(challenge_id: int, xp_gain: int = 20):
    """
    Marca desafio como concluído e soma XP apenas uma vez.
    """
    completed = st.session_state["completed_challenges"]
    if challenge_id not in completed:
        completed.add(challenge_id)
        st.session_state["completed_challenges"] = completed
        st.session_state["xp"] += xp_gain


def get_level(xp: int) -> str:
    """
    Retorna o nível do aluno baseado em XP.
    """
    if xp < 60:
        return "Estagiário SQL"
    elif xp < 120:
        return "Analista Júnior SQL"
    elif xp < 180:
        return "Analista Pleno SQL"
    elif xp < 220:
        return "Especialista SQL em Marketing"
    else:
        return "Consultor SQL Marketing Jedi"


# -------------------------------
# CONEXÃO E INICIALIZAÇÃO DO BANCO
# -------------------------------

conn = get_connection()
init_db(conn)

# -------------------------------
# LAYOUT PRINCIPAL
# -------------------------------

st.title("🎓 Curso Interativo de SQL para Marketing")
st.caption("Construa consultas SQL praticando em um cenário real de campanhas de marketing para uma empresa de bebidas.")

tab_curso, tab_sandbox, tab_desafios, tab_progresso = st.tabs(
    ["📘 Curso", "🧪 Sandbox SQL", "🎮 Desafios Gamificados", "🏅 Progresso"]
)

# -------------------------------
# ABA: CURSO (TEORIA)
# -------------------------------

with tab_curso:
    st.header("📘 Módulos Teóricos")

    # -------------------
    # MÓDULO 1
    # -------------------
    with st.expander("Módulo 1 - O que é um banco de dados?"):
        st.write("""
Um **banco de dados** é um lugar organizado onde guardamos informações
para consultá-las e analisá-las depois.

No marketing digital, bancos de dados são essenciais para armazenar:

- Informações de campanhas (Instagram, Facebook, Google Ads)
- Leads e clientes
- Métricas como CPC, CTR, ROAS
- Vendas e conversões

Sem banco de dados, nenhuma análise seria confiável.
""")

    # -------------------
    # MÓDULO 2
    # -------------------
    with st.expander("Módulo 2 - Tipos de bancos: estruturados vs. não estruturados"):
        st.subheader("📌 Dados Estruturados")
        st.write("""
Dados organizados em colunas, linhas e formatos previsíveis.

**Exemplos:**
- Tabela de leads (nome, email, telefone)
- Base de produtos (nome, categoria, preço)
- Métricas de campanha (data, cliques, gastos)
""")

        st.subheader("📌 Dados Semiestruturados")
        st.write("""
Dados que têm estrutura, mas não obrigatoriamente tabular.

**Exemplos:**
- JSON retornado por API do Instagram
- XML de integrações
- Logs de servidores
""")

        st.subheader("📌 Dados Não Estruturados")
        st.write("""
Dados sem formato padrão.

**Exemplos:**
- Fotos e vídeos de campanhas
- Comentários do Instagram
- Áudios de WhatsApp
- PDFs variados
""")

        st.write("""
**Bancos Relacionais (SQL)** lidam com dados estruturados.

**Bancos Não Relacionais (NoSQL)** lidam melhor com semiestruturados e não estruturados.
""")

    # -------------------
    # MÓDULO 3
    # -------------------
    with st.expander("Módulo 3 - Tipos de linguagens SQL"):

        st.write("### 📌 DDL — Data Definition Language")
        st.code("CREATE TABLE produtos (...);\nALTER TABLE produtos ADD COLUMN preco DECIMAL;")

        st.write("### 📌 DML — Data Manipulation Language")
        st.code("INSERT INTO produtos VALUES (...);\nUPDATE produtos SET preco = 10.0 WHERE id = 1;")

        st.write("### 📌 DQL — Data Query Language")
        st.code("SELECT * FROM produtos;")

        st.write("### 📌 DCL — Data Control Language")
        st.code("GRANT SELECT ON tabela TO usuario;\nREVOKE INSERT ON tabela FROM usuario;")

        st.write("### 📌 TCL — Transaction Control Language")
        st.code(
"BEGIN TRANSACTION;\n"
"UPDATE contas SET saldo = saldo - 50 WHERE id = 1;\n"
"UPDATE contas SET saldo = saldo + 50 WHERE id = 2;\n"
"COMMIT;\n"
"-- ou ROLLBACK para desfazer"
        )

    # -------------------
    # NOVO MÓDULO 4
    # -------------------
    with st.expander("Módulo 4 - Arquitetura Medalhão, Star Schema e Modelagem Dimensional"):
        st.subheader("🏅 Arquitetura Medalhão")
        st.write("""
        A **Arquitetura Medalhão** é um modelo moderno de organização de dados dividido em camadas 
        (Bronze, Prata e Ouro), onde cada etapa representa um nível de qualidade e transformação. 
        Os dados chegam brutos na camada Bronze, são limpos e padronizados na camada Prata, 
        e se tornam modelos analíticos prontos para decisão na camada Ouro.
        """)

        st.write("### 🥉 Camada Bronze — Dados Crus")
        st.write("""
Dados exatamente como chegam das fontes:
- CSVs
- APIs brutas
- Logs crus
""")

        st.write("### 🥈 Camada Prata — Dados Tratados")
        st.write("""
Dados limpos e padronizados:
- Tipos corrigidos
- Datas ajustadas
- Remoção de duplicados
""")

        st.write("### 🥇 Camada Ouro — Dados Prontos para Negócio")
        st.write("""
Dados agregados e organizados para tomada de decisão:
- Indicadores calculados (CTR, CPC, ROAS)
- Tabelas otimizadas para dashboards
""")

        st.subheader("⭐ Star Schema")
        st.write("""
No star schema:

- **Fatos** guardam métricas (números)
- **Dimensões** guardam contexto (descrições)

O nome vem do formato de estrela ao redor da tabela fato.
""")

        st.subheader("📘 Tabela Dimensão")
        st.write("""
Responde **quem, o quê, onde**.

Exemplos:
- Produto
- Canal
- Cliente
""")

        st.subheader("📗 Tabela Fato")
        st.write("""
Responde **quanto e quando**.

Exemplos de métricas:
- impressões  
- cliques  
- gastos  
- vendas  
""")

    # -------------------
    # MÓDULO 5
    # -------------------
    with st.expander("Módulo 5 - Tabelas fato e dimensões (explicação didática)"):

        st.write("""
Imagine que você é o analista da empresa **Bebidas Tropicais™**.

Para analisar campanhas, criamos dimensões e fatos.
""")

        st.subheader("📗 Dimensão Produto — O cardápio da empresa")
        st.write("""
Aqui ficam informações que mudam pouco:
- nome do produto
- categoria
- preço

Ela responde:
➡ **O que estamos anunciando?**
""")

        st.subheader("📣 Dimensão Campanha — Os canais de marketing")
        st.write("""
Aqui ficam informações sobre o canal:
- Instagram, Facebook, Google Ads
- Objetivo (Alcance, Cliques, Conversão)

Ela responde:
➡ **Onde estamos anunciando?**
""")

        st.subheader("🎯 Tabela Fato — O resultado das campanhas")
        st.write("""
Aqui ficam os números reais:
- impressões
- cliques
- gastos
- vendas

Ela responde:
➡ **O que aconteceu?**

Se as dimensões são o *contexto*,
A fato é a **história acontecendo**.
""")


# -------------------------------
# ABA: SANDBOX SQL
# -------------------------------
with tab_sandbox:
    st.header("🧪 Sandbox SQL")
    st.write("Digite qualquer comando `SELECT` para explorar o banco de dados.")

    col1, col2 = st.columns([2, 1])

    with col1:
        default_query = "SELECT * FROM dim_produto;"
        user_query = st.text_area(
            "Sua query SQL:",
            value=default_query,
            height=150,
            key="sandbox_query"
        )

        if st.button("Executar consulta", type="primary"):
            try:
                df_result = run_query(conn, user_query)
                st.success(f"Consulta executada com sucesso! {len(df_result)} linha(s) retornadas.")
                st.dataframe(df_result, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao executar a query:\n\n{e}")

    with col2:
        st.markdown("### 🧮 Dicas rápidas")
        st.markdown("- `SELECT * FROM dim_produto;`")
        st.markdown("- `SELECT * FROM dim_campanha;`")
        st.markdown("- `SELECT * FROM fato_marketing;`")
        st.markdown("- Use `WHERE` para filtrar.")
        st.markdown("- Use `GROUP BY` para agrupar.")

# -------------------------------
# ABA: DESAFIOS GAMIFICADOS
# -------------------------------
with tab_desafios:
    st.header("🎮 Desafios Gamificados")
    st.write("Responda aos desafios escrevendo queries SQL. Se o resultado bater com o esperado, você ganha XP!")

    challenges = get_challenges()
    challenge_options = {f"{c['id']} - {c['titulo']}": c for c in challenges}

    selected_label = st.selectbox(
        "Escolha um desafio:",
        options=list(challenge_options.keys())
    )

    challenge = challenge_options[selected_label]

    st.subheader(f"Desafio {challenge['id']} – {challenge['titulo']}")
    st.write(challenge["descricao"])
    with st.expander("💡 Dica", expanded=False):
        st.write(challenge["dica"])

    default_user_sql = ""
    user_sql = st.text_area(
        "Digite sua query de resposta:",
        value=default_user_sql,
        height=150,
        key=f"challenge_sql_{challenge['id']}"
    )

    if st.button("Validar resposta", type="primary", key=f"validate_{challenge['id']}"):
        if not user_sql.strip():
            st.warning("Digite uma query antes de validar.")
        else:
            result = validate_answer(conn, challenge, user_sql)

            if result["error"]:
                st.error(f"Erro na execução da sua query:\n\n{result['error']}")
            else:
                if result["ok"]:
                    st.success("🎉 Correto! Sua resposta gera o mesmo resultado que a solução esperada. +20 XP")
                    add_xp(challenge["id"])
                else:
                    st.warning("A query executou, mas o resultado é diferente do esperado. Compare abaixo e ajuste sua resposta.")
                    st.markdown("#### 🔎 Seu resultado")
                    st.dataframe(result["df_user"], use_container_width=True)
                    st.markdown("#### ✅ Resultado esperado")
                    st.dataframe(result["df_expected"], use_container_width=True)

# -------------------------------
# ABA: PROGRESSO
# -------------------------------
with tab_progresso:
    st.header("🏅 Progresso do Aluno")

    xp = st.session_state["xp"]
    completed = st.session_state["completed_challenges"]
    nivel = get_level(xp)

    st.metric("XP total", xp)
    st.metric("Desafios concluídos", f"{len(completed)} / 10")
    st.metric("Nível atual", nivel)

    st.markdown("### ✅ Desafios concluídos")
    if completed:
        for cid in sorted(list(completed)):
            ch = next((c for c in get_challenges() if c["id"] == cid), None)
            if ch:
                st.write(f"- Desafio {cid} – {ch['titulo']}")
    else:
        st.write("Você ainda não concluiu nenhum desafio. Vá na aba **Desafios Gamificados** e comece!")

    st.markdown("---")
    st.markdown("### 🏁 Sugestão de próxima etapa")
    st.write("""
    - Finalizar todos os 10 desafios
    - Repetir consultas mudando filtros (`WHERE`) para explorar os dados
    - Criar suas próprias perguntas de negócio e escrever as queries para respondê-las
    """)

