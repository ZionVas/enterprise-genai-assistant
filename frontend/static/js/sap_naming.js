const correctButton =
    document.getElementById(
        "correct-button"
    );

const originalCodeInput =
    document.getElementById(
        "original-code"
    );

const loading =
    document.getElementById(
        "loading"
    );

const resultSection =
    document.getElementById(
        "result-section"
    );

const correctedCode =
    document.getElementById(
        "corrected-code"
    );

const sourcesContainer =
    document.getElementById(
        "sources"
    );


correctButton.addEventListener(
    "click",
    async () => {

        const originalCode =
            originalCodeInput.value.trim();

        if (!originalCode) {

            alert(
                "Please enter SAP ABAP code."
            );

            return;
        }

        loading.style.display =
            "block";

        resultSection.style.display =
            "none";

        correctButton.disabled =
            true;

        try {

            const response =
                await fetch(
                    "/api/sap-naming",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify(
                            {
                                original_code:
                                    originalCode,
                            }
                        ),
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Naming correction failed."
                );
            }

            correctedCode.textContent =
                data.corrected_code;

            sourcesContainer.innerHTML =
                "";

            data.sources.forEach(
                (source) => {

                    const sourceElement =
                        document.createElement(
                            "div"
                        );

                    sourceElement.className =
                        "source-card";

                    sourceElement.innerHTML =
                        `
                        <strong>
                            ${source.document_name}
                        </strong>

                        <p>
                            Category:
                            ${source.category}
                        </p>
                        `;

                    sourcesContainer.appendChild(
                        sourceElement
                    );

                }
            );

            resultSection.style.display =
                "block";

        } catch (error) {

            alert(
                error.message
            );

        } finally {

            loading.style.display =
                "none";

            correctButton.disabled =
                false;

        }

    }
);