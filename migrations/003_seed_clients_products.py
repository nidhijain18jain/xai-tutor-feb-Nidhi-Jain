from app.database import get_db


def upgrade():
    with get_db() as conn:
        conn.executemany(
            """
            INSERT INTO clients (name, address, registration_no)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM clients WHERE registration_no = ?
            )
            """,
            [
                ("Acme Corp", "New York", "AC123", "AC123"),
                ("Globex", "San Francisco", "GB456", "GB456"),
            ],
        )

        conn.executemany(
            """
            INSERT INTO products (name, price)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM products WHERE name = ?
            )
            """,
            [
                ("Laptop", 1000, "Laptop"),
                ("Mouse", 50, "Mouse"),
            ],
        )


def downgrade():
    with get_db() as conn:
        conn.execute(
            "DELETE FROM clients WHERE registration_no IN ('AC123','GB456')"
        )
        conn.execute(
            "DELETE FROM products WHERE name IN ('Laptop','Mouse')"
        )