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