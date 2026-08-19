from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

ocr_text = """
FACTURE N° FAC-2026-001
Date : 15/08/2026

SOCIETE EXEMPLE SARL
ICE : 001234567890123

Client :
SOCIETE CLIENTE SARL
ICE : 009876543210987

TOTAL HT : 1 000 DH
TVA 20% : 200 DH
TOTAL TTC : 1 200 DH

Mode de paiement : Virement bancaire
RIB : 123456789012345678901234
Banque : Exemple Bank
"""

response = client.responses.create(
    model="gpt-5-mini",
input=f"""
You are an invoice data extraction assistant.

Your job is to extract information from the invoice text.

Rules:
1. Return ONLY valid JSON.
2. Do not invent or guess information.
3. If a field is not present, return null.
4. Keep names and invoice numbers exactly as they appear.
5. Amounts must be numbers when they can be converted to numbers.
6. The JSON must contain exactly these fields:

- invoice_number
- supplier_name
- client_name
- supplier_ice
- client_ice
- invoice_date
- amount_ht
- tva
- amount_ttc
- payment_method
- rib
- bank
- swift

Invoice text:

{ocr_text}
"""
)

print(response.output_text)