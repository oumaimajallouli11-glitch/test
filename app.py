from flask import Flask, render_template, request, jsonify
import os
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


app = Flask(__name__)


# ==========================================
# CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================
# POPPLER CONFIGURATION
# ==========================================

POPPLER_PATH = r"C:\Users\mahdi\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text):
    """
    Clean OCR text without destroying useful information.
    """

    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive empty lines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


# ==========================================
# FIND VALUE AFTER A LABEL
# ==========================================

def find_after_label(text, labels):
    """
    Search for text appearing after one of several labels.
    """

    for label in labels:

        pattern = rf"{label}\s*[:\-]?\s*(.+)"

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            # Stop at a line break
            value = value.split("\n")[0].strip()

            if value:
                return value

    return ""


# ==========================================
# EXTRACT INVOICE NUMBER
# ==========================================

def extract_invoice_number(text):

    patterns = [

        r"Facture\s*(?:N[°ºoO]?)?\s*[:\-]?\s*([A-Z0-9\-]+)",

        r"N[°ºoO]?\s*Facture\s*[:\-]?\s*([A-Z0-9\-]+)",

        r"FACT\s*U\s*R\s*E\s*N[°ºoO]?\s*[:\-]?\s*([A-Z0-9\-]+)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return ""


# ==========================================
# EXTRACT DATE
# ==========================================

def extract_invoice_date(text):

    patterns = [

        r"Date\s*[:\-]\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",

        r"Date\s*[:\-]\s*(\d{1,2}\s+[A-Za-zéûîôàèùç]+\s+\d{4})",

        r"Date de la facture\s*[:\-]\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",

        r"Date de la facture\s*[:\-]\s*(\d{1,2}\s+[A-Za-zéûîôàèùç]+\s+\d{4})",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return ""


# ==========================================
# EXTRACT ICE NUMBERS
# ==========================================

def extract_ice_numbers(text):

    # Find every 15-digit number.
    # Moroccan ICE numbers contain 15 digits.

    numbers = re.findall(
        r"\b\d{15}\b",
        text
    )

    if len(numbers) >= 2:

        return {
            "client_ice": numbers[-1],
            "supplier_ice": numbers[0]
        }

    if len(numbers) == 1:

        return {
            "client_ice": numbers[0],
            "supplier_ice": ""
        }

    return {
        "client_ice": "",
        "supplier_ice": ""
    }


# ==========================================
# EXTRACT SUPPLIER NAME
# ==========================================

def extract_supplier_name(text):

    patterns = [

        r"(SOCI[ÉE]T[ÉE]\s+EXEMPLE\s+SARL)",

        r"(SOCIETE\s+EXEMPLE\s+SARL)",

        r"^([A-ZÉÈÀÙÂÊÎÔÛÇ][A-ZÉÈÀÙÂÊÎÔÛÇ\s&\-]+SARL)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.MULTILINE
        )

        if match:

            value = match.group(1).strip()

            if len(value) > 2:

                return value

    # More general fallback

    lines = text.splitlines()

    for line in lines[:10]:

        line = line.strip()

        if "SARL" in line.upper():

            return line

    return ""


# ==========================================
# EXTRACT CLIENT NAME
# ==========================================

def extract_client_name(text):

    patterns = [

        r"(SOCI[ÉE]T[ÉE]\s+CLIENTE\s+SARL)",

        r"(SOCIETE\s+CLIENTE\s+SARL)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    # Fallback: search around "Client"

    match = re.search(
        r"Client\s*\n?\s*([A-ZÉÈÀÙÂÊÎÔÛÇ][A-ZÉÈÀÙÂÊÎÔÛÇ\s]+SARL)",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1).strip()

    return ""


# ==========================================
# EXTRACT AMOUNTS
# ==========================================

def extract_amounts(text):

    result = {

        "amount_ht": "",

        "tva": "",

        "amount_ttc": ""
    }


    # -----------------------------
    # TOTAL HT
    # -----------------------------

    ht_patterns = [

        r"TOTAL\s+HT\s*[:\-]?\s*([\d\s.,]+)",

        r"Total\s+HT\s*[:\-]?\s*([\d\s.,]+)",

    ]

    for pattern in ht_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            result["amount_ht"] = (
                match.group(1).strip()
            )

            break


    # -----------------------------
    # TVA
    # -----------------------------

    tva_patterns = [

        r"TVA\s*\(?\s*20\s*%\s*\)?\s*[:\-]?\s*([\d\s.,]+)",

        r"TVA\s*[:\-]?\s*([\d\s.,]+)",

    ]

    for pattern in tva_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            result["tva"] = (
                match.group(1).strip()
            )

            break


    # -----------------------------
    # TOTAL TTC
    # -----------------------------

    ttc_patterns = [

        r"TOTAL\s+TTC\s*[:\-]?\s*([\d\s.,]+)",

        r"Total\s+TTC\s*[:\-]?\s*([\d\s.,]+)",

    ]

    for pattern in ttc_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            result["amount_ttc"] = (
                match.group(1).strip()
            )

            break


    # -----------------------------
    # FALLBACK TTC
    # -----------------------------

    if not result["amount_ttc"]:

        matches = re.findall(
            r"(\d[\d\s.,]+)\s*DH",
            text,
            re.IGNORECASE
        )

        if matches:

            result["amount_ttc"] = (
                matches[-1].strip()
            )

    return result


# ==========================================
# EXTRACT PAYMENT INFORMATION
# ==========================================

def extract_payment_information(text):

    payment = {

        "payment_method": "",

        "rib": "",

        "bank": "",

        "swift": ""
    }


    # ======================================
    # PAYMENT METHOD
    # ======================================

    payment_patterns = [

        r"Mode\s+de\s+paiement\s*[:\-]\s*(.+)",

        r"Mode\s+paiement\s*[:\-]\s*(.+)",

        r"Paiement\s*[:\-]\s*(.+)",

        r"Modes\s+de\s+règlement\s*[:\-]\s*(.+)",

        r"Modes\s+de\s+reglement\s*[:\-]\s*(.+)",

    ]

    for pattern in payment_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            payment["payment_method"] = (
                match.group(1)
                .split("\n")[0]
                .strip()
            )

            break


    # ======================================
    # RIB
    # ======================================

    rib_patterns = [

        r"RIB\s*[:\-]?\s*([0-9\s]+)",

        r"R\.I\.B\s*[:\-]?\s*([0-9\s]+)"

    ]

    for pattern in rib_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            rib = match.group(1).strip()

            rib = re.sub(
                r"[^0-9\s]",
                "",
                rib
            )

            payment["rib"] = rib.strip()

            break


    # ======================================
    # BANK
    # ======================================

    bank_patterns = [

        r"Banque\s*[:\-]\s*(.+)",

        r"Bank\s*[:\-]\s*(.+)"

    ]

    for pattern in bank_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            payment["bank"] = (
                match.group(1)
                .split("\n")[0]
                .strip()
            )

            break


    # ======================================
    # SWIFT
    # ======================================

    swift_patterns = [

        r"SWIFT\s*[:\-]\s*([A-Z0-9]+)",

        r"BIC\s*[:\-]\s*([A-Z0-9]+)"

    ]

    for pattern in swift_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            payment["swift"] = (
                match.group(1).strip()
            )

            break

    return payment


# ==========================================
# EXTRACT ALL INVOICE INFORMATION
# ==========================================

def extract_invoice_data(text):

    ice = extract_ice_numbers(text)

    amounts = extract_amounts(text)

    payment = extract_payment_information(text)

    data = {

        "invoice_number":
            extract_invoice_number(text),

        "supplier_name":
            extract_supplier_name(text),

        "client_name":
            extract_client_name(text),

        "supplier_ice":
            ice["supplier_ice"],

        "client_ice":
            ice["client_ice"],

        "invoice_date":
            extract_invoice_date(text),

        "amount_ht":
            amounts["amount_ht"],

        "tva":
            amounts["tva"],

        "amount_ttc":
            amounts["amount_ttc"],

        # PAYMENT INFORMATION

        "payment_method":
            payment["payment_method"],

        "rib":
            payment["rib"],

        "bank":
            payment["bank"],

        "swift":
            payment["swift"]
    }

    return data


# ==========================================
# UPLOAD + OCR ROUTE
# ==========================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    print("\n====================================")
    print("UPLOAD ROUTE CALLED")
    print("====================================")


    # ======================================
    # CHECK FILE
    # ======================================

    if "invoice" not in request.files:

        return jsonify({

            "success": False,

            "message":
                "Aucun fichier reçu."
        })


    file = request.files["invoice"]


    if file.filename == "":

        return jsonify({

            "success": False,

            "message":
                "Aucun fichier sélectionné."
        })


    # ======================================
    # SAVE FILE
    # ======================================

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)


    print("Fichier sauvegardé :")
    print(filepath)


    # ======================================
    # START OCR
    # ======================================

    print("\n====================================")
    print("STARTING OCR")
    print("====================================")


    try:

        # ==================================
        # DETECT FILE TYPE
        # ==================================

        file_extension = (
            os.path.splitext(filepath)[1].lower()
        )


        # ==================================
        # PDF
        # ==================================

        if file_extension == ".pdf":

            print("PDF détecté.")

            print(
                "Conversion du PDF en image..."
            )


            pages = convert_from_path(

                filepath,

                dpi=300,

                poppler_path=POPPLER_PATH
            )


            if not pages:

                raise Exception(
                    "Impossible de convertir le PDF."
                )


            print(
                "Nombre de pages :",
                len(pages)
            )


            # Store OCR text from every page

            ocr_parts = []


            for page_number, page in enumerate(
                pages,
                start=1
            ):

                print(
                    f"OCR de la page {page_number}..."
                )


                page_text = (
                    pytesseract.image_to_string(
                        page,
                        lang="fra+eng"
                    )
                )


                ocr_parts.append(
                    page_text
                )


            ocr_text = "\n".join(
                ocr_parts
            )


        # ==================================
        # NORMAL IMAGE
        # ==================================

        else:

            image = Image.open(
                filepath
            )


            print(
                "Image ouverte avec succès."
            )

            print(
                "Format :",
                image.format
            )

            print(
                "Taille :",
                image.size
            )


            ocr_text = (
                pytesseract.image_to_string(
                    image,
                    lang="fra+eng"
                )
            )


        # ==================================
        # CLEAN OCR TEXT
        # ==================================

        ocr_text = clean_text(
            ocr_text
        )


        print("\n====================================")
        print("OCR TEXT")
        print("====================================")

        print(
            ocr_text
        )


        # ==================================
        # EXTRACT INFORMATION
        # ==================================

        print("\n====================================")
        print("EXTRACTED INVOICE DATA")
        print("====================================")


        invoice_data = (
            extract_invoice_data(
                ocr_text
            )
        )


        # ==================================
        # PRINT EXTRACTED DATA
        # ==================================

        for key, value in invoice_data.items():

            print(
                f"{key}: {value}"
            )


        print("\n====================================")
        print("PAYMENT INFORMATION")
        print("====================================")


        print(
            "Mode de paiement:",
            invoice_data[
                "payment_method"
            ]
        )


        print(
            "RIB:",
            invoice_data[
                "rib"
            ]
        )


        print(
            "Banque:",
            invoice_data[
                "bank"
            ]
        )


        print(
            "SWIFT:",
            invoice_data[
                "swift"
            ]
        )


        print(
            "====================================\n"
        )


        # ==================================
        # RETURN DATA TO JAVASCRIPT
        # ==================================

        return jsonify({

            "success": True,

            "message":
                "Facture analysée avec succès.",


            # OCR TEXT

            "ocr_text":
                ocr_text,


            # INVOICE DATA

            "invoice_number":
                invoice_data[
                    "invoice_number"
                ],


            "client_name":
                invoice_data[
                    "client_name"
                ],


            "supplier_name":
                invoice_data[
                    "supplier_name"
                ],


            "client_ice":
                invoice_data[
                    "client_ice"
                ],


            "supplier_ice":
                invoice_data[
                    "supplier_ice"
                ],


            "invoice_date":
                invoice_data[
                    "invoice_date"
                ],


            "amount_ht":
                invoice_data[
                    "amount_ht"
                ],


            "tva":
                invoice_data[
                    "tva"
                ],


            "amount_ttc":
                invoice_data[
                    "amount_ttc"
                ],


            # PAYMENT DATA

            "payment_method":
                invoice_data[
                    "payment_method"
                ],


            "rib":
                invoice_data[
                    "rib"
                ],


            "bank":
                invoice_data[
                    "bank"
                ],


            "swift":
                invoice_data[
                    "swift"
                ]
        })


    # ======================================
    # ERROR
    # ======================================

    except Exception as e:

        print("\n====================================")
        print("ERROR")
        print("====================================")


        print(
            str(e)
        )


        return jsonify({

            "success": False,

            "message":
                str(e)

        })


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )