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

# Create the folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# TESSERACT CONFIGURATION
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# EXTRACT INFORMATION FROM OCR TEXT
# ==========================================

def extract_invoice_data(ocr_text):

    data = {
        "date": "-",
        "ice_client": "-",
        "ice_fournisseur": "-",
        "montant_ht": "-",
        "tva": "-",
        "montant_ttc": "-"
    }

    # --------------------------------------
    # DATE
    # --------------------------------------

    date_match = re.search(
        r"Date\s*:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        ocr_text,
        re.IGNORECASE
    )

    if date_match:
        data["date"] = date_match.group(1)


    # --------------------------------------
    # ICE
    # --------------------------------------

    ice_matches = re.findall(
        r"ICE\s*[:\-]?\s*(\d{10,20})",
        ocr_text,
        re.IGNORECASE
    )

    if len(ice_matches) >= 1:
        data["ice_fournisseur"] = ice_matches[0]

    if len(ice_matches) >= 2:
        data["ice_client"] = ice_matches[1]


    # --------------------------------------
    # TOTAL HT
    # --------------------------------------

    ht_match = re.search(
        r"TOTAL\s*HT\s*[:\-]?\s*([\d\s.,]+)",
        ocr_text,
        re.IGNORECASE
    )

    if ht_match:
        data["montant_ht"] = ht_match.group(1).strip()


    # --------------------------------------
    # TVA
    # --------------------------------------

    tva_match = re.search(
        r"TVA(?:\s*\([^)]*\))?\s*[:\-]?\s*([\d\s.,]+)",
        ocr_text,
        re.IGNORECASE
    )

    if tva_match:
        data["tva"] = tva_match.group(1).strip()


    # --------------------------------------
    # TOTAL TTC
    # --------------------------------------

    ttc_match = re.search(
        r"TOTAL\s*TTC\s*[:\-]?\s*([\d\s.,]+)",
        ocr_text,
        re.IGNORECASE
    )

    if ttc_match:
        data["montant_ttc"] = ttc_match.group(1).strip()


    return data


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    print("HOME ROUTE WORKS")

    return render_template("index.html")


# ==========================================
# UPLOAD + OCR + EXTRACTION
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    print("\n================================")
    print("UPLOAD ROUTE CALLED")
    print("================================")


    # --------------------------------------
    # CHECK FILE
    # --------------------------------------

    if "invoice" not in request.files:

        print("ERROR: No invoice file received.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier reçu."
        })


    file = request.files["invoice"]


    # --------------------------------------
    # CHECK FILENAME
    # --------------------------------------

    if file.filename == "":

        print("ERROR: Empty filename.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier sélectionné."
        })


    # --------------------------------------
    # SAVE FILE
    # --------------------------------------

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    print("Fichier sauvegardé :")
    print(filepath)


    # ======================================
    # OCR
    # ======================================

    try:

        print("\n================================")
        print("STARTING OCR")
        print("================================")


        # Open image
        image = Image.open(filepath)

        print("Image ouverte avec succès.")
        print("Format :", image.format)
        print("Taille :", image.size)


        # ----------------------------------
        # OCR
        # ----------------------------------

        ocr_text = pytesseract.image_to_string(
            image,
            lang="fra+eng"
        )


        # ----------------------------------
        # DISPLAY OCR TEXT
        # ----------------------------------

        print("\n================================")
        print("OCR TEXT")
        print("================================")

        print(ocr_text)

        print("================================")
        print("END OCR TEXT")
        print("================================")


        # ==================================
        # EXTRACT INVOICE INFORMATION
        # ==================================

        invoice_data = extract_invoice_data(ocr_text)


        print("\n================================")
        print("EXTRACTED INVOICE DATA")
        print("================================")

        print(invoice_data)

        print("================================")


        # ==================================
        # SEND RESULT TO JAVASCRIPT
        # ==================================

        return jsonify({

            "success": True,

            "message": "Facture analysée avec succès.",

            "ocr_text": ocr_text,

            "data": invoice_data

        })


    # ======================================
    # ERROR HANDLING
    # ======================================

    except Exception as e:

        print("\n================================")
        print("OCR ERROR")
        print("================================")

        print(str(e))

        return jsonify({

            "success": False,

            "message": f"Erreur OCR : {str(e)}"

        })


# ==========================================
# START FLASK
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)