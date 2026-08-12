document.addEventListener("DOMContentLoaded", function () {

    // =====================================
    // GET HTML ELEMENTS
    // =====================================

    const form = document.getElementById("invoiceForm");

    const fileInput = document.getElementById("invoice");

    const fileName = document.getElementById("fileName");

    const analyzeButton =
        document.getElementById("analyzeButton");

    const loading =
        document.getElementById("loading");

    const statusMessage =
        document.getElementById("statusMessage");

    const ocrText =
        document.getElementById("ocrText");


    // Invoice information elements

    const clientName =
        document.getElementById("clientName");

    const supplierName =
        document.getElementById("supplierName");

    const clientICE =
        document.getElementById("clientICE");

    const supplierICE =
        document.getElementById("supplierICE");

    const invoiceDate =
        document.getElementById("invoiceDate");

    const amountHT =
        document.getElementById("amountHT");

    const tva =
        document.getElementById("tva");

    const amountTTC =
        document.getElementById("amountTTC");


    // =====================================
    // CHECK THAT IMPORTANT ELEMENTS EXIST
    // =====================================

    console.log("JavaScript loaded.");

    console.log("Form:", form);
    console.log("File input:", fileInput);
    console.log("Analyze button:", analyzeButton);


    // =====================================
    // SELECT FILE
    // =====================================

    if (fileInput) {

        fileInput.addEventListener(
            "change",
            function () {

                if (fileInput.files.length > 0) {

                    fileName.textContent =
                        fileInput.files[0].name;

                    console.log(
                        "File selected:",
                        fileInput.files[0].name
                    );

                } else {

                    fileName.textContent =
                        "Aucun fichier sélectionné";
                }

            }
        );

    }


    // =====================================
    // FORM SUBMISSION
    // =====================================

    if (form) {

        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                console.log(
                    "Analyze button clicked."
                );


                // =================================
                // CHECK FILE
                // =================================

                if (
                    !fileInput ||
                    fileInput.files.length === 0
                ) {

                    if (statusMessage) {

                        statusMessage.textContent =
                            "Veuillez sélectionner une facture.";

                        statusMessage.className =
                            "status error";
                    }

                    return;
                }


                // =================================
                // SHOW LOADING
                // =================================

                if (loading) {

                    loading.classList.remove("hidden");
                }


                if (analyzeButton) {

                    analyzeButton.disabled = true;
                }


                if (statusMessage) {

                    statusMessage.textContent =
                        "Analyse de la facture en cours...";

                    statusMessage.className =
                        "status";
                }


                // =================================
                // CREATE FORM DATA
                // =================================

                const formData = new FormData();

                formData.append(
                    "invoice",
                    fileInput.files[0]
                );


                // =================================
                // SEND TO FLASK
                // =================================

                try {

                    console.log(
                        "Sending invoice to Flask..."
                    );


                    const response =
                        await fetch(
                            "/upload",
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    console.log(
                        "Response status:",
                        response.status
                    );


                    // =================================
                    // CHECK RESPONSE
                    // =================================

                    if (!response.ok) {

                        throw new Error(
                            "Erreur serveur : " +
                            response.status
                        );
                    }


                    // =================================
                    // CONVERT RESPONSE TO JSON
                    // =================================

                    const data =
                        await response.json();


                    console.log(
                        "Flask response:",
                        data
                    );


                    // =================================
                    // SUCCESS
                    // =================================

                    if (data.success) {


                        // -----------------------------
                        // SUCCESS MESSAGE
                        // -----------------------------

                        if (statusMessage) {

                            statusMessage.textContent =
                                "✓ Facture analysée avec succès.";

                            statusMessage.className =
                                "status success";
                        }


                        // -----------------------------
                        // DISPLAY OCR TEXT
                        // -----------------------------

                        if (ocrText) {

                            if (data.ocr_text) {

                                ocrText.textContent =
                                    data.ocr_text;

                            } else {

                                ocrText.textContent =
                                    "Aucun texte n'a été détecté.";
                            }

                        }


                        // =================================
                        // DISPLAY EXTRACTED DATA
                        // =================================

                        if (data.data) {


                            const invoice =
                                data.data;


                            console.log(
                                "Extracted invoice data:",
                                invoice
                            );


                            // -----------------------------
                            // DATE
                            // -----------------------------

                            if (invoiceDate) {

                                invoiceDate.textContent =
                                    invoice.date || "-";
                            }


                            // -----------------------------
                            // ICE CLIENT
                            // -----------------------------

                            if (clientICE) {

                                clientICE.textContent =
                                    invoice.ice_client || "-";
                            }


                            // -----------------------------
                            // ICE FOURNISSEUR
                            // -----------------------------

                            if (supplierICE) {

                                supplierICE.textContent =
                                    invoice.ice_fournisseur || "-";
                            }


                            // -----------------------------
                            // MONTANT HT
                            // -----------------------------

                            if (amountHT) {

                                amountHT.textContent =
                                    invoice.montant_ht || "-";
                            }


                            // -----------------------------
                            // TVA
                            // -----------------------------

                            if (tva) {

                                tva.textContent =
                                    invoice.tva || "-";
                            }


                            // -----------------------------
                            // MONTANT TTC
                            // -----------------------------

                            if (amountTTC) {

                                amountTTC.textContent =
                                    invoice.montant_ttc || "-";
                            }


                            // -----------------------------
// CLIENT NAME
// -----------------------------

if (clientName) {

    clientName.textContent =
        invoice.client_name || "-";
}


// -----------------------------
// SUPPLIER NAME
// -----------------------------

if (supplierName) {

    supplierName.textContent =
        invoice.supplier_name || "-";
}

                        } else {

                            console.warn(
                                "No extracted invoice data received."
                            );

                        }


                    } else {


                        // =================================
                        // SERVER ERROR
                        // =================================

                        if (statusMessage) {

                            statusMessage.textContent =
                                "Erreur : " +
                                (
                                    data.message ||
                                    "Une erreur est survenue."
                                );

                            statusMessage.className =
                                "status error";
                        }

                    }


                } catch (error) {


                    // =================================
                    // JAVASCRIPT / NETWORK ERROR
                    // =================================

                    console.error(
                        "JavaScript error:",
                        error
                    );


                    if (statusMessage) {

                        statusMessage.textContent =
                            "Une erreur est survenue : " +
                            error.message;

                        statusMessage.className =
                            "status error";
                    }

                }


                // =================================
                // HIDE LOADING
                // =================================

                if (loading) {

                    loading.classList.add("hidden");
                }


                // =================================
                // ENABLE BUTTON AGAIN
                // =================================

                if (analyzeButton) {

                    analyzeButton.disabled = false;
                }

            }
        );

    } else {

        console.error(
            "ERROR: invoiceForm was not found."
        );

    }

});