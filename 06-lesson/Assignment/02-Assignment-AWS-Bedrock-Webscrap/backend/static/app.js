const crawlForm = document.getElementById("crawlForm");
const urlInput = document.getElementById("urlInput");
const crawlButton = document.getElementById("crawlButton");
const buttonText = document.getElementById("buttonText");
const statusBox = document.getElementById("statusBox");
const statusText = document.getElementById("statusText");
const resultBox = document.getElementById("resultBox");
const copyButton = document.getElementById("copyButton");

let sessionId = localStorage.getItem("crawler_session_id");

if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem("crawler_session_id", sessionId);
}

function showStatus(message, type) {
    statusBox.classList.remove("hidden", "loading", "success", "error");
    statusBox.classList.add(type);
    statusText.textContent = message;
}

function hideStatus() {
    statusBox.classList.add("hidden");
}

function setLoading(isLoading) {
    crawlButton.disabled = isLoading;
    buttonText.textContent = isLoading ? "Crawling..." : "Crawl Website";
}

function displayResult(text) {
    resultBox.textContent = text;
    copyButton.classList.remove("hidden");
}

crawlForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const url = urlInput.value.trim();

    if (!url) {
        showStatus("Please enter a website URL.", "error");
        return;
    }

    setLoading(true);
    showStatus("The Bedrock Agent is crawling and cleaning the webpage...", "loading");

    resultBox.textContent = "Waiting for the Bedrock Agent response...";
    copyButton.classList.add("hidden");

    try {
        const response = await fetch("/api/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url,
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to crawl this website.");
        }

        displayResult(data.answer || "The agent returned an empty response.");
        showStatus("Crawling completed successfully.", "success");

    } catch (error) {
        displayResult(`Error:\n${error.message}`);
        showStatus(error.message, "error");
    } finally {
        setLoading(false);
    }
});

copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(resultBox.textContent);
        copyButton.textContent = "Copied";

        setTimeout(() => {
            copyButton.textContent = "Copy Result";
        }, 1500);

    } catch {
        showStatus("Could not copy the result. Please copy it manually.", "error");
    }
});

document.querySelectorAll(".example-button").forEach((button) => {
    button.addEventListener("click", () => {
        urlInput.value = button.dataset.url;
        urlInput.focus();
    });
});

hideStatus();