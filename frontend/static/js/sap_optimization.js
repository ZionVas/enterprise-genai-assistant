const optimizeButton =
    document.getElementById(
        "optimize-button"
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

const optimizedCode =
    document.getElementById(
        "optimized-code"
    );

const validationStatus =
    document.getElementById(
        "validation-status"
    );

const validationErrors =
    document.getElementById(
        "validation-errors"
    );

const iterations =
    document.getElementById(
        "iterations"
    );

const sourcesContainer =
    document.getElementById(
        "sources"
    );


optimizeButton.addEventListener(
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

        optimizeButton.disabled =
            true;

        try {

            const response =
                await fetch(
                    "/api/sap-optimization",
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
                    "Optimization failed."
                );
            }


            optimizedCode.textContent =
                data.optimized_code;


            if (data.validation_passed) {

                validationStatus.textContent =
                    "✓ Validation PASSED";

            } else {

                validationStatus.textContent =
                    "⚠ Validation did not pass completely";

            }


            validationErrors.innerHTML =
                "";

            if (
                data.validation_errors &&
                data.validation_errors.length > 0
            ) {

                data.validation_errors.forEach(
                    (error) => {

                        const element =
                            document.createElement(
                                "p"
                            );

                        element.textContent =
                            error;

                        validationErrors.appendChild(
                            element
                        );
                    }
                );

            }


            iterations.textContent =
                data.iterations;


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

            optimizeButton.disabled =
                false;

        }

    }
);