from flask import Flask, render_template, request, jsonify
import os
import pytesseract
from PIL import Image


app = Flask(__name__)

# =========================
# Configuration
# =========================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# Tesseract configuration
# =========================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================
# Home page
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# Invoice upload + OCR
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    print("UPLOAD ROUTE CALLED")

    # Check if a file was sent
    if "invoice" not in request.files:
        return jsonify({
            "success": False,
            "message": "Aucun fichier reçu."
        }), 400

    file = request.files["invoice"]

    # Check if a file was selected
    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Aucun fichier sélectionné."
        }), 400

    # =========================
    # Save the invoice
    # =========================

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    print(f"Fichier sauvegardé : {file_path}")


    # =========================
    # OCR
    # =========================

    try:

        image = Image.open(file_path)

        print("Image ouverte avec succès.")

        # French + English OCR
        text = pytesseract.image_to_string(
            image,
            lang="fra+eng"
        )

        # =========================
        # Display OCR text
        # =========================

        print("\n========== TEXTE OCR ==========")
        print(text)
        print("========== FIN OCR ==========\n")


        # =========================
        # Send result to JavaScript
        # =========================

        return jsonify({
            "success": True,
            "message": "Facture analysée avec succès.",
            "ocr_text": text
        })


    except Exception as e:

        print("OCR ERROR:", e)

        return jsonify({
            "success": False,
            "message": f"Erreur lors de l'analyse : {str(e)}"
        }), 500


# =========================
# Run Flask
# =========================

if __name__ == "__main__":
    app.run(debug=True)