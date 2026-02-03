from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TaxRequest(BaseModel):
    taxable_income: float
    tax_withheld: float
    deductions: float
    offsets: float

def calculate_tax(income):
    # 2024-25 resident rates (simplified, no medicare)
    if income <= 18200:
        return 0
    elif income <= 45000:
        return (income - 18200) * 0.16
    elif income <= 135000:
        return 4288 + (income - 45000) * 0.30
    elif income <= 190000:
        return 31288 + (income - 135000) * 0.37
    else:
        return 51638 + (income - 190000) * 0.45

@app.post("/calc")
def calc(req: TaxRequest):
    adjusted_income = req.taxable_income - req.deductions
    tax = calculate_tax(adjusted_income) - req.offsets
    refund = req.tax_withheld - tax
    return {
        "adjusted_income": adjusted_income,
        "tax_payable": round(tax, 2),
        "refund_or_owing": round(refund, 2)
    }
