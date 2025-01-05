// Handle URL form submission
urlForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    urlContainer.innerHTML = "";
    showLoading();

    const urlData = { url: document.getElementById('url').value };

    try {
        const response = await fetch("http://127.0.0.1:5000/scrape", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(urlData),
        });

        if (!response.ok) throw new Error("Failed to scrape URL.");
        const data = await response.json();
        displayUrlData(data);
    } catch (error) {
        urlContainer.innerHTML = `<p class="error-message">${error.message}</p>`;
    } finally {
        hideLoading();
    }
});



// Display URL data
function displayUrlData(data) {
    const urlBox = document.createElement("div");
    urlBox.classList.add("summary-box");
    const title = document.createElement("h2");
    title.textContent = "Scraped Content";
    urlBox.appendChild(title);
    const content = document.createElement("div");
    content.innerHTML = data.content || "<p>No content found.</p>";
    urlBox.appendChild(content);
    urlContainer.appendChild(urlBox);
}
