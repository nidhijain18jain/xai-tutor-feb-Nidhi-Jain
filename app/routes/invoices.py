from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.schemas import InvoiceCreate


router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/")
def create_invoice(payload: InvoiceCreate):
    try:
        with get_db() as conn:
            total = 0
            for item in payload.items:
                product = conn.execute(
                    "SELECT price FROM products WHERE id = ?",
                    (item.product_id,),
                ).fetchone()

                if not product:
                    raise HTTPException(404, f"Product {item.product_id} not found")

                total += product["price"] * item.quantity

            total += payload.tax

            cursor = conn.execute(
                """
                INSERT INTO invoices (invoice_no, issue_date, due_date, client_id, tax, total)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.invoice_no,
                    payload.issue_date,
                    payload.due_date,
                    payload.client_id,
                    payload.tax,
                    total,
                ),
            )

            invoice_id = cursor.lastrowid

            for item in payload.items:
                conn.execute(
                    """
                    INSERT INTO invoice_items (invoice_id, product_id, quantity)
                    VALUES (?, ?, ?)
                    """,
                    (invoice_id, item.product_id, item.quantity),
                )

            return {"id": invoice_id, "total": total}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/")
def list_invoices():
    with get_db() as conn:
        return conn.execute("SELECT * FROM invoices").fetchall()
        
        
@router.get("/{invoice_id}")
def get_invoice(invoice_id: int):
    with get_db() as conn:
        invoice = conn.execute(
            "SELECT * FROM invoices WHERE id = ?", (invoice_id,)
        ).fetchone()


        if not invoice:
            raise HTTPException(404, "Invoice not found")


        items = conn.execute(
            "SELECT * FROM invoice_items WHERE invoice_id = ?",
             (invoice_id,),
        ).fetchall()


        return {"invoice": invoice, "items": items}




@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
        deleted = conn.execute(
            "DELETE FROM invoices WHERE id = ?", (invoice_id,)
        ).rowcount


        if not deleted:
            raise HTTPException(404, "Invoice not found")


        return {"message": "Invoice deleted"}