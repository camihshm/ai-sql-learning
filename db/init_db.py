import sqlite3


def initialize_db(conn: sqlite3.Connection) -> None:
    """
    Create tables if they do not exist and insert seed data on first run.
    """
    cursor = conn.cursor()

    cursor.executescript(
        """
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
        """
    )

    cursor.execute("SELECT COUNT(*) FROM dim_produto;")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        cursor.executescript(
            """
            INSERT INTO dim_produto (id_produto, nome_produto, categoria, preco) VALUES
            (1, 'Refrigerante Cola', 'Refrigerante', 6.50),
            (2, 'Água Mineral 500ml', 'Água', 2.50),
            (3, 'Suco Tropical', 'Suco', 7.90);

            INSERT INTO dim_campanha (id_campanha, canal, objetivo) VALUES
            (101, 'Instagram', 'Alcance'),
            (102, 'Facebook', 'Conversão'),
            (103, 'Google Ads', 'Cliques');

            INSERT INTO fato_marketing (
                id_fato, id_produto, id_campanha, data,
                impressoes, cliques, gastos, vendas
            ) VALUES
            (1, 1, 101, '2025-01-10', 50000, 1200, 800.00, 150),
            (2, 1, 102, '2025-01-11', 30000, 800, 600.00, 90),
            (3, 2, 103, '2025-01-12', 45000, 2000, 1500.00, 300),
            (4, 3, 101, '2025-01-10', 20000, 400, 300.00, 45),
            (5, 3, 102, '2025-01-11', 26000, 610, 500.00, 70);
            """
        )
        conn.commit()
