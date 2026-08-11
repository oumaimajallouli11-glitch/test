document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("invoiceForm");
    const fileInput = document.getElementById("invoice");
    const fileName = document.getElementById("fileName");

    const analyzeButton = document.getElementById("analyzeButton");

    const loading = document.getElementById("loading");
    const statusMessage = document.getElementById("statusMessage");

    const ocrText = document.getElementById("ocrText");

    const clientName = document.getElementById("clientName");
    const supplierName = document.getElementById("supplierName");

    const clientICE = document.getElementById("clientICE");
    const supplierICE = document.getElementById("supplierICE");

    const invoiceDate = document.getElementById("invoiceDate");

    const amountHT = document.getElementById("amountHT");
    const tva = document.getElementById("tva");
    const amountTTC = document.getElementById("amountTTC");


    // =====================================
    // SELECT FILE
    // =====================================

    fileInput.addEventListener("change", function () {

        if (fileInput.files.length > 0) {

            fileName.textContent =
                fileInput.files[0].name;

        } else {

            fileName.textContent =
                "Aucun fichier sélectionné";
        }

    });


    // =====================================
    // FORM SUBMISSION
    // =====================================

    form.addEventListener("submit", async function (event) {

        event.preventDefault();


        // Check file

        if (fileInput.files.length === 0) {

            statusMessage.textContent =
                "Veuillez sélectionner une facture.";

            return;
        }


        // Show loading

        loading.classList.remove("hidden");

        analyzeButton.disabled = true;

        statusMessage.textContent =
            "Analyse de la facture en cours...";


        // Create FormData

        const formData = new FormData();

        formData.append(
            "invoice",
            fileInput.files[0]
        );


        try {

            // Send invoice to Flask

            const response = await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


            // Convert response to JSON

            const data = await response.json();


            console.log("Flask response:", data);


            // =====================================
            // SUCCESS
            // =====================================

            if (data.success) {

                statusMessage.textContent =
                    "✓ Facture analysée avec succès.";

                statusMessage.className =
                    "status success";


                // Display OCR text

                if (data.ocr_text) {

                    ocrText.textContent =
                        data.ocr_text;

                } else {

                    ocrText.textContent =
                        "Aucun texte n'a été détecté.";
                }


                // =====================================
                // DISPLAY EXTRACTED INFORMATION
                // =====================================

                if (data.client_name !== undefined) {

                    clientName.textContent =
                        data.client_name || "-";
                }


                if (data.supplier_name !== undefined) {

                    supplierName.textContent =
                        data.supplier_name || "-";
                }


                if (data.client_ice !== undefined) {

                    clientICE.textContent =
                        data.client_ice || "-";
                }


                if (data.supplier_ice !== undefined) {

                    supplierICE.textContent =
                        data.supplier_ice || "-";
                }


                if (data.invoice_date !== undefined) {

                    invoiceDate.textContent =
                        data.invoice_date || "-";
                }


                if (data.amount_ht !== undefined) {

                    amountHT.textContent =
                        data.amount_ht || "-";
                }


                if (data.tva !== undefined) {

                    tva.textContent =
                        data.tva || "-";
                }


                if (data.amount_ttc !== undefined) {

                    amountTTC.textContent =
                        data.amount_ttc || "-";
                }


            } else {

                statusMessage.textContent =
                    "Erreur : " +
                    (data.message || "Une erreur est survenue.");

                statusMessage.className =
                    "status error";
            }


        } catch (error) {

            console.error(
                "JavaScript error:",
                error
            );

            statusMessage.textContent =
                "Une erreur est survenue : " +
                error.message;

            statusMessage.className =
                "status error";

        }


        // Hide loading

        loading.classList.add("hidden");

        analyzeButton.disabled = false;

    });

});