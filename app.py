from flask import Flask, render_template, request, jsonify
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Tesseract installation
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    print("\n========== UPLOAD ROUTE CALLED ==========")

    # Check that a file was received
    if "invoice" not in request.files:

        print("ERROR: No invoice field received")

        return jsonify({
            "success": False,
            "message": "Aucun fichier reçu."
        }), 400

    file = request.files["invoice"]

    print("File received:", file.filename)

    # Check filename
    if file.filename == "":

        print("ERROR: Empty filename")

        return jsonify({
            "success": False,
            "message": "Aucun fichier sélectionné."
        }), 400

    try:

        # Save invoice
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(file_path)

        print("File saved:", file_path)

        # Open image
        image = Image.open(file_path)

        print("Image opened successfully")

        # OCR in French
        text = pytesseract.image_to_string(
            image,
            lang="fra"
        )

        print("OCR completed")

        print("\n========== OCR TEXT ==========")
        print(text)
        print("==============================\n")

        # Send result to JavaScript
        return jsonify({
            "success": True,
            "message": "Facture analysée avec succès.",
            "text": text
        })

    except Exception as e:

        print("OCR ERROR:", str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)