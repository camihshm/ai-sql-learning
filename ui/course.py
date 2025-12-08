import streamlit as st


def render_course_tab() -> None:
    st.header("📘 Módulos Teóricos")

    # Módulo 1
    with st.expander("Módulo 1 - O que é um banco de dados?"):
        st.write(
            """
Um **banco de dados** é um lugar organizado onde guardamos informações
para consultá-las e analisá-las depois.

No marketing digital, bancos de dados são essenciais para armazenar:

- Informações de campanhas (Instagram, Facebook, Google Ads)
- Leads e clientes
- Métricas como CPC, CTR, ROAS
- Vendas e conversões
"""
        )

    # Módulo 2
    with st.expander("Módulo 2 - Tipos de dados e bancos (estruturados vs. não estruturados)"):
        st.subheader("📌 Dados Estruturados")
        st.write(
            """
Dados organizados em colunas, linhas e formatos previsíveis.

**Exemplos:**

- Tabela de leads (nome, email, telefone)
- Base de produtos (nome, categoria, preço)
- Métricas de campanha (data, cliques, gastos)
"""
        )

        st.subheader("📌 Dados Semiestruturados")
        st.write(
            """
Dados que têm estrutura, mas não necessariamente tabular.

**Exemplos:**

- JSON da API do Instagram
- XML de integrações
- Logs de servidores organizados
"""
        )

        st.subheader("📌 Dados Não Estruturados")
        st.write(
            """
Dados sem formato fixo.

**Exemplos:**

- Fotos e vídeos de campanhas
- Comentários em redes sociais
- Áudios e PDFs diversos
"""
        )

        st.write(
            """
**Bancos relacionais (SQL)** lidam muito bem com dados estruturados.

**Bancos não relacionais (NoSQL)** são mais flexíveis para dados semi ou não estruturados.
"""
        )

    # Módulo 3
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
            "-- ou ROLLBACK para desfazer\n"
        )

    # Módulo 4
    with st.expander("Módulo 4 - Arquitetura Medalhão, Star Schema e Snowflake"):
        st.subheader("🏅 Arquitetura Medalhão")
        st.write(
            """
A **Arquitetura Medalhão** é um modelo moderno de organização de dados em camadas
(Bronze, Prata e Ouro), em que os dados chegam brutos na camada Bronze,
são limpos e padronizados na camada Prata e se tornam modelos analíticos prontos
para decisão na camada Ouro.
"""
        )

        st.write("### 🥉 Camada Bronze — Dados crus")
        st.write(
            """
Dados exatamente como chegam das fontes:

- CSVs
- APIs brutas
- Logs crus
"""
        )

        st.write("### 🥈 Camada Prata — Dados tratados")
        st.write(
            """
Dados limpos e padronizados:

- Tipos corrigidos
- Datas ajustadas
- Remoção de duplicados
"""
        )

        st.write("### 🥇 Camada Ouro — Dados para negócio")
        st.write(
            """
Dados modelados para análise:

- Indicadores calculados (CTR, CPC, ROAS)
- Modelos dimensionais para dashboards
"""
        )

        st.subheader("⭐ Star Schema")
        st.write(
            """
Star Schema é um modelo dimensional com uma tabela fato central ligada
a várias tabelas dimensão ao redor. É simples, intuitivo e muito usado em BI.
"""
        )

        st.subheader("❄ Snowflake Schema")
        st.write(
            """
Snowflake Schema normaliza as dimensões em múltiplas tabelas.
Reduz redundância, mas torna as consultas um pouco mais complexas.
"""
        )

    # Módulo 5
    with st.expander("Módulo 5 - Tabelas fato e dimensão (explicação didática)"):
        st.write(
            """
Imagine que você é o analista da empresa **Bebidas Tropicais™**.

Para analisar campanhas, criamos dimensões e fatos.
"""
        )

        st.subheader("📗 Dimensão Produto — O cardápio da empresa")
        st.write(
            """
Aqui ficam informações que mudam pouco:

- nome do produto
- categoria
- preço

Ela responde:

➡ **O que estamos anunciando?**
"""
        )

        st.subheader("📣 Dimensão Campanha — Os canais de marketing")
        st.write(
            """
Aqui ficam informações sobre o canal:

- Instagram, Facebook, Google Ads
- Objetivo (Alcance, Cliques, Conversão)

Ela responde:

➡ **Onde estamos anunciando?**
"""
        )

        st.subheader("🎯 Tabela Fato — O resultado das campanhas")
        st.write(
            """
Aqui ficam os números reais:

- impressões
- cliques
- gastos
- vendas

Ela responde:

➡ **O que aconteceu?**

Se as dimensões são o *contexto*,
a fato é a **história acontecendo**.
"""
        )
