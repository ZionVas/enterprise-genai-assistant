const generateButton =
    document.getElementById("generate-button");

const requestInput =
    document.getElementById("user-request");

const languageSelect =
    document.getElementById("language");

const loading =
    document.getElementById("loading");

const resultSection =
    document.getElementById("result-section");

const generatedCode =
    document.getElementById("generated-code");

const sourcesContainer =
    document.getElementById("sources");


generateButton.addEventListener(
    "click",
    async () => {

        const userRequest =
            requestInput.value.trim();

        const language =
            languageSelect.value;

        if (!userRequest) {

            alert(
                "Please enter a code generation request."
            );

            return;
        }

        loading.style.display = "block";

        resultSection.style.display = "none";

        generateButton.disabled = true;

        try {

            const response =
                await fetch(
                    "/api/generate-code",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify(
                            {
                                user_request:
                                    userRequest,

                                language:
                                    language,
                            }
                        ),
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Code generation failed."
                );
            }

            generatedCode.textContent =
                data.generated_code;

            sourcesContainer.innerHTML = "";

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

            alert(error.message);

        } finally {

            loading.style.display = "none";

            generateButton.disabled = false;
        }
    }
);