
const pdfForm = document.getElementById("pdfForm");
const urlForm = document.getElementById("urlForm");
const summaryContainer = document.getElementById("summary-container");
const urlContainer = document.getElementById("url-container");

// Show loading spinner
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

// Hide loading spinner
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Handle PDF form submission
pdfForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    summaryContainer.innerHTML = "";
    showLoading();

    const formData = new FormData(pdfForm);

    try {
        const response = await fetch("http://127.0.0.1:5000/summarizePdf", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Failed to fetch summary.");
        const data = await response.json();
        displaySummary(data);
    } catch (error) {
        summaryContainer.innerHTML = `<p class="error-message">${error.message}</p>`;
    } finally {
        hideLoading();
    }
});

// Display PDF summary
function displaySummary(data) {
    if (!data || !data.summary) {
        summaryContainer.innerHTML = '<p class="error-message">No summary data available.</p>';
        return;
    }

    const summaryBox = document.createElement("div");
    summaryBox.classList.add("summary-box");
    const title = document.createElement("h2");
    title.textContent = "Summary";
    summaryBox.appendChild(title);
    const content = document.createElement("div");
    content.innerHTML = formatSummaryText(data.summary);
    summaryBox.appendChild(content);
    summaryContainer.appendChild(summaryBox);
}


// Format summary text for HTML
function formatSummaryText(text) {
    return text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                .replace(/\n/g, "<br>")
                .replace(/- (.*?)/g, "<li>$1</li>")
                .replace(/(<li>.*?<\/li>)/g, "<ul>$1</ul>");
}
