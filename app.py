from flask import Flask, render_template, request, jsonify
import os
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


# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# TESSERACT CONFIGURATION
# ==========================================

# Windows path to Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# UPLOAD + OCR
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    print("\n================================")
    print("UPLOAD ROUTE CALLED")
    print("================================")


    # --------------------------------------
    # Check if file exists
    # --------------------------------------

    if "invoice" not in request.files:

        print("ERROR: No invoice file received.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier reçu."
        })


    file = request.files["invoice"]


    # --------------------------------------
    # Check filename
    # --------------------------------------

    if file.filename == "":

        print("ERROR: Empty filename.")

        return jsonify({
            "success": False,
            "message": "Aucun fichier sélectionné."
        })


    # --------------------------------------
    # Save file
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
        # Print OCR result
        # ----------------------------------

        print("\n================================")
        print("OCR TEXT")
        print("================================")

        print(ocr_text)

        print("================================")
        print("END OCR TEXT")
        print("================================")


        # ==================================
        # RESPONSE
        # ==================================

        return jsonify({

            "success": True,

            "message": "Facture analysée avec succès.",

            "ocr_text": ocr_text

        })


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
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)