async function generateText() {

    const prompt = document.getElementById("prompt").value.trim();
    const tone = document.getElementById("tone").value;

    const resultBox = document.getElementById("result");
    const loading = document.getElementById("loading");
    const generateButton = document.getElementById("generate-btn");

    if (!prompt) {
        resultBox.textContent = "Please enter a prompt.";
        return;
    }

    const finalPrompt = `
Generate a response to the following request.

Tone: ${tone}

Request:
${prompt}
`;

    loading.classList.remove("hidden");
    generateButton.disabled = true;
    resultBox.textContent = "";

    try {

        const response = await fetch("/api/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                prompt: finalPrompt
            })
        });

        const data = await response.json();

        if (!data.success) {
            resultBox.textContent = `Error: ${data.error}`;
            return;
        }

        resultBox.textContent = data.response;

    } catch (error) {

        resultBox.textContent =
            `Request failed: ${error.message}`;

    } finally {

        loading.classList.add("hidden");
        generateButton.disabled = false;
    }
}

async function generateEmail() {

    const recipient =
        document.getElementById("recipient").value.trim();

    const purpose =
        document.getElementById("purpose").value.trim();

    const keyPoints =
        document.getElementById("key-points").value.trim();

    const tone =
        document.getElementById("email-tone").value;

    const length =
        document.getElementById("email-length").value;

    const resultBox =
        document.getElementById("email-result");

    const loading =
        document.getElementById("email-loading");

    const generateButton =
        document.getElementById("email-generate-btn");


    if (!purpose) {

        resultBox.textContent =
            "Please enter the purpose of the email.";

        return;
    }


    loading.classList.remove("hidden");

    generateButton.disabled = true;

    resultBox.textContent = "";


    try {

        const response = await fetch(
            "/api/generate-email",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    recipient: recipient,
                    purpose: purpose,
                    key_points: keyPoints,
                    tone: tone,
                    length: length
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            resultBox.textContent =
                `Error: ${data.error}`;

            return;
        }


        resultBox.textContent = data.response;


    } catch (error) {

        resultBox.textContent =
            `Request failed: ${error.message}`;

    } finally {

        loading.classList.add("hidden");

        generateButton.disabled = false;
    }
}