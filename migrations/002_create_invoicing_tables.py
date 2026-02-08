from app.database import get_db


def upgrade():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            registration_no TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            client_id INTEGER NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )
        """)


def downgrade():
    with get_db() as conn:
        conn.execute("DROP TABLE IF EXISTS invoice_items")
        conn.execute("DROP TABLE IF EXISTS invoices")
        conn.execute("DROP TABLE IF EXISTS products")
        conn.execute("DROP TABLE IF EXISTS clients")