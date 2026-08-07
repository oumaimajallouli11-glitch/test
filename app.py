from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "invoice" not in request.files:
        return "Aucun fichier reçu."

    file = request.files["invoice"]

    if file.filename == "":
        return "Aucun fichier sélectionné."

    file.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )
    )

    return f"Facture '{file.filename}' téléchargée avec succès !"



if __name__ == "__main__":
    app.run(debug=True)