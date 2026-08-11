document.addEventListener("DOMContentLoaded", () => {

    console.log("APP.JS IS WORKING");


    // =========================
    // GET HTML ELEMENTS
    // =========================

    const form =
        document.getElementById("invoiceForm");

    const fileInput =
        document.getElementById("invoice");

    const analyzeButton =
        document.getElementById("analyzeButton");

    const ocrResult =
        document.getElementById("ocrResult");

    const statusMessage =
        document.getElementById("statusMessage");


    // =========================
    // CHECK ELEMENTS
    // =========================

    if (!form) {

        console.error(
            "invoiceForm not found"
        );

        return;
    }


    if (!fileInput) {

        console.error(
            "invoice input not found"
        );

        return;
    }


    console.log(
        "Invoice form is ready."
    );


    // =========================
    // FORM SUBMIT
    // =========================

    form.addEventListener(
        "submit",
        async (event) => {

            // Stop normal HTML form submission
            event.preventDefault();


            console.log(
                "FORM SUBMITTED"
            );


            // =========================
            // CHECK FILE
            // =========================

            if (!fileInput.files.length) {

                alert(
                    "Veuillez sélectionner une facture."
                );

                return;
            }


            const file =
                fileInput.files[0];


            console.log(
                "File selected:",
                file.name
            );


            // =========================
            // LOADING
            // =========================

            analyzeButton.disabled = true;

            analyzeButton.textContent =
                "Analyse en cours...";


            statusMessage.textContent =
                "Envoi de la facture au serveur...";


            // =========================
            // FORM DATA
            // =========================

            const formData =
                new FormData();

            formData.append(
                "invoice",
                file
            );


            console.log(
                "Sending request to Flask..."
            );


            try {

                // =========================
                // SEND TO FLASK
                // =========================

                const response =
                    await fetch(
                        "/upload",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                console.log(
                    "Flask response:",
                    response.status
                );


                // =========================
                // READ RESPONSE
                // =========================

                const data =
                    await response.json();


                console.log(
                    "Data received:",
                    data
                );


                // =========================
                // CHECK SUCCESS
                // =========================

                if (
                    !response.ok ||
                    !data.success
                ) {

                    throw new Error(
                        data.message ||
                        "Erreur pendant l'analyse."
                    );
                }


                // =========================
                // DISPLAY OCR
                // =========================

                ocrResult.textContent =
                    data.text ||
                    "Aucun texte détecté.";


                statusMessage.textContent =
                    "✓ Facture analysée avec succès.";


                console.log(
                    "OCR SUCCESS"
                );


            } catch (error) {

                console.error(
                    "ERROR:",
                    error
                );


                statusMessage.textContent =
                    "✕ Erreur pendant l'analyse.";


                alert(
                    "Une erreur est survenue :\n\n" +
                    error.message
                );


            } finally {

                // =========================
                // RESTORE BUTTON
                // =========================

                analyzeButton.disabled =
                    false;

                analyzeButton.textContent =
                    "Analyser";
            }

        }
    );

});