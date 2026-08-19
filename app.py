from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

import os
import json
import base64


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

app = Flask(__name__)


# Maximum upload size: 20 MB
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


# ============================================================
# OPENAI CLIENT
# ============================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY n'est pas configurée dans le fichier .env"
    )

client = OpenAI(api_key=api_key)


# Model can be changed from .env if necessary.
# Example:
# OPENAI_MODEL=gpt-5.6-luna
MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)


# ============================================================
# ALLOWED FILES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}


ALLOWED_MIME_TYPES = {
    "application/pdf",

    "image/png",
    "image/jpeg",
    "image/webp"
}


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# CHECK FILE
# ============================================================

def is_allowed_file(filename, mime_type):

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False

    if mime_type not in ALLOWED_MIME_TYPES:
        return False

    return True


# ============================================================
# INVOICE PROMPT
# ============================================================

INVOICE_PROMPT = """
Tu es un système spécialisé dans l'analyse de factures.

Analyse directement la facture fournie.

Ton objectif est d'extraire UNIQUEMENT les 8 informations
suivantes :

1. nom_client
2. nom_fournisseur
3. ice_client
4. ice_fournisseur
5. date_facture
6. total_ht
7. total_tva
8. total_ttc

IMPORTANT :

- Ne devine jamais une information.
- Si une information n'est pas clairement présente,
  retourne null.
- Utilise uniquement les informations visibles dans
  la facture.
- La date demandée est la date de facture.
- Ne confonds pas la date de facture avec la date
  d'échéance.
- Ne confonds pas ICE avec un numéro de facture,
  numéro client, numéro de commande, RIB, IBAN,
  SIRET, SIREN ou numéro de TVA.
- Pour un ICE marocain, conserve les 15 chiffres.
- Les montants doivent être retournés sans symbole
  monétaire lorsque c'est possible.
- Ne retourne aucune information bancaire.
- Ne retourne aucun mode de paiement.
- Ne retourne aucune ligne de produit.
- Ne retourne aucun commentaire.

Réponds uniquement avec un objet JSON contenant
exactement ces 8 propriétés :

{
    "nom_client": null,
    "nom_fournisseur": null,
    "ice_client": null,
    "ice_fournisseur": null,
    "date_facture": null,
    "total_ht": null,
    "total_tva": null,
    "total_ttc": null
}
"""


# ============================================================
# ANALYZE INVOICE
# ============================================================

def analyze_invoice(file_bytes, filename, mime_type):

    # --------------------------------------------------------
    # Convert file to Base64
    # --------------------------------------------------------

    encoded_file = base64.b64encode(
        file_bytes
    ).decode("utf-8")


    # --------------------------------------------------------
    # Create data URL
    # --------------------------------------------------------

    data_url = (
        f"data:{mime_type};base64,{encoded_file}"
    )


    # --------------------------------------------------------
    # Build input
    #
    # PDF  -> input_file
    # Image -> input_image
    # --------------------------------------------------------

    if mime_type == "application/pdf":

        document_input = {
            "type": "input_file",
            "filename": filename,
            "file_data": data_url
        }

    else:

        document_input = {
            "type": "input_image",
            "image_url": data_url,
            "detail": "high"
        }


    # --------------------------------------------------------
    # Call OpenAI Responses API
    # --------------------------------------------------------

    response = client.responses.create(

        model=MODEL,

        input=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "input_text",
                        "text": INVOICE_PROMPT
                    },

                    document_input

                ]
            }
        ]

    )


    # --------------------------------------------------------
    # Read response
    # --------------------------------------------------------

    result = response.output_text.strip()


    print()
    print("=" * 60)
    print("OPENAI RESPONSE")
    print("=" * 60)
    print(result)
    print("=" * 60)


    # --------------------------------------------------------
    # Convert response to JSON
    # --------------------------------------------------------

    try:

        data = json.loads(result)

    except json.JSONDecodeError:

        # Sometimes an AI response can contain
        # extra text around the JSON.
        # We try to recover the JSON object.

        start = result.find("{")
        end = result.rfind("}")

        if start == -1 or end == -1:

            raise ValueError(
                "La réponse de l'IA ne contient pas "
                "un objet JSON valide."
            )

        json_text = result[
            start:end + 1
        ]

        try:

            data = json.loads(
                json_text
            )

        except json.JSONDecodeError:

            raise ValueError(
                "Impossible de convertir la réponse "
                "de l'IA en JSON."
            )


    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    fields = [

        "nom_client",
        "nom_fournisseur",
        "ice_client",
        "ice_fournisseur",
        "date_facture",
        "total_ht",
        "total_tva",
        "total_ttc"

    ]


    # Make sure every field exists
    for field in fields:

        if field not in data:
            data[field] = None


    # --------------------------------------------------------
    # Clean values
    # --------------------------------------------------------

    for field in fields:

        value = data.get(field)

        if value is None:
            continue

        value = str(value).strip()

        if value == "":
            data[field] = None

        else:
            data[field] = value


    # --------------------------------------------------------
    # Validate ICE
    # --------------------------------------------------------

    for field in [
        "ice_client",
        "ice_fournisseur"
    ]:

        value = data.get(field)

        if value is None:
            continue

        # Remove spaces
        cleaned = str(value).replace(
            " ",
            ""
        )

        # Remove common separators
        cleaned = cleaned.replace(
            "-",
            ""
        )

        # An ICE should contain 15 digits.
        if (
            len(cleaned) == 15
            and cleaned.isdigit()
        ):

            data[field] = cleaned

        else:

            data[field] = None


    return data


# ============================================================
# UPLOAD / ANALYZE ROUTE
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    try:

        # ----------------------------------------------------
        # Check file exists
        # ----------------------------------------------------

        if "invoice" not in request.files:

            return jsonify({

                "success": False,

                "message":
                    "Aucune facture n'a été envoyée."

            }), 400


        file = request.files["invoice"]


        # ----------------------------------------------------
        # Check filename
        # ----------------------------------------------------

        if not file.filename:

            return jsonify({

                "success": False,

                "message":
                    "Aucun fichier sélectionné."

            }), 400


        filename = file.filename


        # ----------------------------------------------------
        # Detect MIME type
        # ----------------------------------------------------

        mime_type = (
            file.mimetype or ""
        ).lower()


        # ----------------------------------------------------
        # Validate file
        # ----------------------------------------------------

        if not is_allowed_file(
            filename,
            mime_type
        ):

            return jsonify({

                "success": False,

                "message":
                    "Format non supporté. "
                    "Utilisez PDF, PNG, JPG, JPEG "
                    "ou WEBP."

            }), 400


        # ----------------------------------------------------
        # Read file
        # ----------------------------------------------------

        file_bytes = file.read()


        if not file_bytes:

            return jsonify({

                "success": False,

                "message":
                    "Le fichier est vide."

            }), 400


        # ----------------------------------------------------
        # Analyze invoice
        # ----------------------------------------------------

        data = analyze_invoice(

            file_bytes,

            filename,

            mime_type

        )


        # ----------------------------------------------------
        # Send JSON response to JavaScript
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Facture analysée avec succès.",

            "client_name":
                data.get("nom_client"),

            "supplier_name":
                data.get("nom_fournisseur"),

            "client_ice":
                data.get("ice_client"),

            "supplier_ice":
                data.get("ice_fournisseur"),

            "invoice_date":
                data.get("date_facture"),

            "amount_ht":
                data.get("total_ht"),

            "tva":
                data.get("total_tva"),

            "amount_ttc":
                data.get("total_ttc")

        })


    except Exception as e:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(str(e))
        print("=" * 60)


        return jsonify({

            "success": False,

            "message":
                "Erreur pendant l'analyse : "
                + str(e)

        }), 500


# ============================================================
# FILE TOO LARGE
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "message":
            "Le fichier est trop volumineux. "
            "La taille maximale est de 20 MB."

    }), 413


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )