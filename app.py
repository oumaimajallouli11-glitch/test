from flask import Flask, render_template, request, jsonify
import os
import re
import pytesseract
from PIL import Image


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# TESSERACT CONFIGURATION
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# EXTRACT INVOICE INFORMATION
# ==========================================

def extract_invoice_data(ocr_text):

    data = {

        "client_name": "-",

        "supplier_name": "-",

        "date": "-",

        "ice_client": "-",

        "ice_fournisseur": "-",

        "montant_ht": "-",

        "tva": "-",

        "montant_ttc": "-",

        "mode_paiement": "-"

    }


    # ======================================
    # CLEAN OCR TEXT
    # ======================================

    text = ocr_text.replace("\r", "")

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]


    # ======================================
    # SUPPLIER NAME
    # ======================================

    # Example:
    #
    # SOCIÉTÉ EXEMPLE SARL
    # Fournisseur

    for i, line in enumerate(lines):

        normalized = line.upper()

        if (
            "FOURNISSEUR" in normalized
            and i > 0
        ):

            previous_line = lines[i - 1].strip()

            if previous_line:

                data["supplier_name"] = previous_line

                break


    # ======================================
    # CLIENT NAME
    # ======================================

    # Example:
    #
    # Client
    # SOCIÉTÉ CLIENTE SARL

    for i, line in enumerate(lines):

        normalized = line.upper()

        if normalized == "CLIENT":

            if i + 1 < len(lines):

                next_line = lines[i + 1].strip()

                if next_line:

                    data["client_name"] = next_line

                    break


    # ======================================
    # DATE
    # ======================================

    date_match = re.search(
        r"Date\s*:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        text,
        re.IGNORECASE
    )

    if date_match:

        data["date"] = date_match.group(1)


    # ======================================
    # ICE
    # ======================================

    ice_matches = re.findall(
        r"ICE\s*[:\-]?\s*(\d{10,20})",
        text,
        re.IGNORECASE
    )


    if len(ice_matches) >= 1:

        data["ice_fournisseur"] = ice_matches[0]


    if len(ice_matches) >= 2:

        data["ice_client"] = ice_matches[1]


    # ======================================
    # TOTAL HT
    # ======================================

    ht_match = re.search(
        r"TOTAL\s*HT\s*[:\-]?\s*([\d\s.,]+)",
        text,
        re.IGNORECASE
    )


    if ht_match:

        data["montant_ht"] = (
            ht_match.group(1)
            .strip()
        )


    # ======================================
    # TVA
    # ======================================

    tva_match = re.search(
        r"TVA(?:\s*\([^)]*\))?\s*[:\-]?\s*([\d\s.,]+)",
        text,
        re.IGNORECASE
    )


    if tva_match:

        data["tva"] = (
            tva_match.group(1)
            .strip()
        )


    # ======================================
    # TOTAL TTC
    # ======================================

    # Sometimes OCR gives:
    #
    # TOTAL TTC
    #
    # 19 560,00 DH
    #
    # so we allow spaces/new lines between
    # TOTAL TTC and the amount.

    ttc_match = re.search(
        r"TOTAL\s*TTC[\s:\-]*([\d\s.,]+)",
        text,
        re.IGNORECASE
    )


    if ttc_match:

        amount = ttc_match.group(1).strip()

        # Remove unnecessary spaces at the beginning/end
        amount = amount.strip()

        if amount:

            data["montant_ttc"] = amount


    # ======================================
    # SECOND TTC METHOD
    # ======================================

    # If the first method doesn't work,
    # search for "TOTAL TTC" and look at
    # the following lines.

    if data["montant_ttc"] == "-":

        for i, line in enumerate(lines):

            normalized = line.upper()

            if "TOTAL TTC" in normalized:

                # Check next few lines

                for j in range(
                    i + 1,
                    min(i + 4, len(lines))
                ):

                    possible_amount = lines[j]

                    amount_match = re.search(
                        r"([\d\s.,]{3,})",
                        possible_amount
                    )

                    if amount_match:

                        amount = (
                            amount_match.group(1)
                            .strip()
                        )

                        if amount:

                            data["montant_ttc"] = amount

                            break


    # ======================================
    # MODE DE PAIEMENT
    # ======================================

    # Example:
    #
    # Mode de paiement: Virement bancaire

    payment_match = re.search(
        r"Mode\s*de\s*paiement\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )


    if payment_match:

        payment = payment_match.group(1).strip()

        if payment:

            data["mode_paiement"] = payment


    # ======================================
    # PRINT EXTRACTED DATA
    # ======================================

    print("\n================================")
    print("EXTRACTED INVOICE DATA")
    print("================================")

    print("Client :", data["client_name"])

    print("Fournisseur :", data["supplier_name"])

    print("Date :", data["date"])

    print("ICE Client :", data["ice_client"])

    print("ICE Fournisseur :", data["ice_fournisseur"])

    print("Montant HT :", data["montant_ht"])

    print("TVA :", data["tva"])

    print("Montant TTC :", data["montant_ttc"])

    print("Mode de paiement :", data["mode_paiement"])

    print("================================")


    return data


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    print("HOME ROUTE WORKS")

    return render_template("index.html")


# ==========================================
# UPLOAD + OCR
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    print("\n================================")
    print("UPLOAD ROUTE CALLED")
    print("================================")


    # ======================================
    # CHECK FILE
    # ======================================

    if "invoice" not in request.files:

        print("ERROR: No invoice file received.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier reçu."
        })


    file = request.files["invoice"]


    # ======================================
    # CHECK FILENAME
    # ======================================

    if file.filename == "":

        print("ERROR: Empty filename.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier sélectionné."
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

    try:

        print("\n================================")
        print("STARTING OCR")
        print("================================")


        image = Image.open(filepath)


        print("Image ouverte avec succès.")

        print("Format :", image.format)

        print("Taille :", image.size)


        # ==================================
        # OCR
        # ==================================

        ocr_text = pytesseract.image_to_string(
            image,
            lang="fra+eng"
        )


        # ==================================
        # DISPLAY OCR TEXT
        # ==================================

        print("\n================================")
        print("OCR TEXT")
        print("================================")

        print(ocr_text)

        print("================================")
        print("END OCR TEXT")
        print("================================")


        # ==================================
        # EXTRACT DATA
        # ==================================

        invoice_data = extract_invoice_data(
            ocr_text
        )


        # ==================================
        # RETURN JSON
        # ==================================

        return jsonify({

            "success": True,

            "message":
                "Facture analysée avec succès.",

            "ocr_text":
                ocr_text,

            "data":
                invoice_data

        })


    except Exception as e:

        print("\n================================")
        print("OCR ERROR")
        print("================================")

        print(str(e))


        return jsonify({

            "success": False,

            "message":
                f"Erreur OCR : {str(e)}"

        })


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)