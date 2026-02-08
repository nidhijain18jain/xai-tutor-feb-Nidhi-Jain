from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    product_id: int
    quantity: int

class InvoiceCreate(BaseModel):
    invoice_no: str
    issue_date: str
    due_date: str
    client_id: int
    tax: float
    items: List[InvoiceItem]