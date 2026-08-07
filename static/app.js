document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".upload form");
    const submitBtn = form.querySelector("button[type='submit']");
    const fileInput = document.getElementById("invoice");
    const resultRows = document.querySelectorAll(".result .row span:last-child");

    // Ordre attendu des champs, dans le même ordre que les lignes du HTML
    const FIELDS = [
        "client_name",
        "supplier_name",
        "client_ice",
        "supplier_ice",
        "date",
        "amount_ht",
        "tva",
        "amount_ttc"
    ];

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!fileInput.files.length) {
            alert("Veuillez sélectionner un fichier avant d'analyser.");
            return;
        }

        setLoading(true);
        resetResults();

        try {
            const formData = new FormData(form);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Erreur serveur (${response.status})`);
            }

            const data = await response.json();
            fillResults(data);

        } catch (err) {
            console.error("Erreur lors de l'analyse :", err);
            alert("Une erreur est survenue lors de l'analyse de la facture. Veuillez réessayer.");
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.textContent = isLoading ? "Analyse en cours..." : "Analyser";
    }

    function resetResults() {
        resultRows.forEach((span) => {
            span.textContent = "-";
        });
    }

    function fillResults(data) {
        resultRows.forEach((span, index) => {
            const key = FIELDS[index];
            const value = data[key];
            span.textContent = (value !== undefined && value !== null && value !== "")
                ? value
                : "-";
        });
    }

});