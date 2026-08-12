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


    // =====================================
    // INVOICE INFORMATION ELEMENTS
    // =====================================

    const invoiceNumber =
        document.getElementById("invoiceNumber");

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
    // PAYMENT INFORMATION ELEMENTS
    // =====================================

    const paymentMethod =
        document.getElementById("paymentMethod");

    const rib =
        document.getElementById("rib");

    const bank =
        document.getElementById("bank");

    const swift =
        document.getElementById("swift");


    // =====================================
    // DEBUG
    // =====================================

    console.log("=================================");
    console.log("JavaScript loaded successfully.");
    console.log("Form:", form);
    console.log("File input:", fileInput);
    console.log("Analyze button:", analyzeButton);
    console.log("=================================");


    // =====================================
    // SELECT FILE
    // =====================================

    if (fileInput) {

        fileInput.addEventListener(
            "change",
            function () {

                if (fileInput.files.length > 0) {

                    if (fileName) {

                        fileName.textContent =
                            fileInput.files[0].name;
                    }

                    console.log(
                        "File selected:",
                        fileInput.files[0].name
                    );

                } else {

                    if (fileName) {

                        fileName.textContent =
                            "Aucun fichier sélectionné";
                    }

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
                        "================================="
                    );

                    console.log(
                        "Flask response:",
                        data
                    );

                    console.log(
                        "================================="
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
                        // DISPLAY INVOICE DATA
                        // =================================

                        console.log(
                            "Displaying extracted invoice data..."
                        );


                        // -----------------------------
                        // INVOICE NUMBER
                        // -----------------------------

                        if (invoiceNumber) {

                            invoiceNumber.textContent =
                                data.invoice_number || "-";
                        }


                        // -----------------------------
                        // CLIENT NAME
                        // -----------------------------

                        if (clientName) {

                            clientName.textContent =
                                data.client_name || "-";
                        }


                        // -----------------------------
                        // SUPPLIER NAME
                        // -----------------------------

                        if (supplierName) {

                            supplierName.textContent =
                                data.supplier_name || "-";
                        }


                        // -----------------------------
                        // CLIENT ICE
                        // -----------------------------

                        if (clientICE) {

                            clientICE.textContent =
                                data.client_ice || "-";
                        }


                        // -----------------------------
                        // SUPPLIER ICE
                        // -----------------------------

                        if (supplierICE) {

                            supplierICE.textContent =
                                data.supplier_ice || "-";
                        }


                        // -----------------------------
                        // INVOICE DATE
                        // -----------------------------

                        if (invoiceDate) {

                            invoiceDate.textContent =
                                data.invoice_date || "-";
                        }


                        // -----------------------------
                        // AMOUNT HT
                        // -----------------------------

                        if (amountHT) {

                            amountHT.textContent =
                                data.amount_ht || "-";
                        }


                        // -----------------------------
                        // TVA
                        // -----------------------------

                        if (tva) {

                            tva.textContent =
                                data.tva || "-";
                        }


                        // -----------------------------
                        // AMOUNT TTC
                        // -----------------------------

                        if (amountTTC) {

                            amountTTC.textContent =
                                data.amount_ttc || "-";
                        }


                        // =================================
                        // PAYMENT INFORMATION
                        // =================================

                        console.log(
                            "Displaying payment information..."
                        );


                        // -----------------------------
                        // PAYMENT METHOD
                        // -----------------------------

                        if (paymentMethod) {

                            paymentMethod.textContent =
                                data.payment_method || "-";
                        }


                        // -----------------------------
                        // RIB
                        // -----------------------------

                        if (rib) {

                            rib.textContent =
                                data.rib || "-";
                        }


                        // -----------------------------
                        // BANK
                        // -----------------------------

                        if (bank) {

                            bank.textContent =
                                data.bank || "-";
                        }


                        // -----------------------------
                        // SWIFT
                        // -----------------------------

                        if (swift) {

                            swift.textContent =
                                data.swift || "-";
                        }


                        // =================================
                        // DEBUG EXTRACTED DATA
                        // =================================

                        console.log(
                            "Client:",
                            data.client_name
                        );

                        console.log(
                            "Supplier:",
                            data.supplier_name
                        );

                        console.log(
                            "Client ICE:",
                            data.client_ice
                        );

                        console.log(
                            "Supplier ICE:",
                            data.supplier_ice
                        );

                        console.log(
                            "Date:",
                            data.invoice_date
                        );

                        console.log(
                            "HT:",
                            data.amount_ht
                        );

                        console.log(
                            "TVA:",
                            data.tva
                        );

                        console.log(
                            "TTC:",
                            data.amount_ttc
                        );

                        console.log(
                            "Payment:",
                            data.payment_method
                        );

                        console.log(
                            "RIB:",
                            data.rib
                        );

                        console.log(
                            "Bank:",
                            data.bank
                        );

                        console.log(
                            "SWIFT:",
                            data.swift
                        );


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