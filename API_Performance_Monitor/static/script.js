const urlInput = document.getElementById("urlInput");
const errorMessage = document.getElementById("errorMessage");
const resultsTable = document.getElementById("resultsTable");

async function checkAPI() {
    const url = urlInput.value.trim();

    errorMessage.textContent = "";

    if (!url) {
        errorMessage.textContent = "Please enter an API URL.";
        return;
    }

    try {
        const response = await fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            errorMessage.textContent = data.error;
            return;
        }

        urlInput.value = "";

        await loadResults();

    } catch (error) {
        errorMessage.textContent = "Unable to connect to the monitoring server.";
    }
}

async function loadResults() {
    try {
        const response = await fetch("/api/results");
        const results = await response.json();

        resultsTable.innerHTML = "";

        let successful = 0;
        let failed = 0;
        let totalResponseTime = 0;

        results.forEach(result => {

            if (result.status === "Success") {
                successful++;
            } else {
                failed++;
            }

            totalResponseTime += Number(result.response_time || 0);

            const row = document.createElement("tr");

            const statusClass =
                result.status === "Success"
                    ? "status-success"
                    : "status-failed";

            row.innerHTML = `
                <td>${escapeHTML(result.url)}</td>
                <td class="${statusClass}">
                    ${escapeHTML(result.status)}
                </td>
                <td>${result.status_code}</td>
                <td>${result.response_time} ms</td>
                <td>${formatBytes(result.response_size)}</td>
                <td>${formatDate(result.checked_at)}</td>
            `;

            resultsTable.appendChild(row);
        });

        document.getElementById("totalTests").textContent = results.length;
        document.getElementById("successfulTests").textContent = successful;
        document.getElementById("failedTests").textContent = failed;

        const average =
            results.length > 0
                ? (totalResponseTime / results.length).toFixed(2)
                : 0;

        document.getElementById("averageResponse").textContent =
            `${average} ms`;

    } catch (error) {
        errorMessage.textContent = "Unable to load monitoring history.";
    }
}

function formatBytes(bytes) {
    if (!bytes) {
        return "0 B";
    }

    if (bytes < 1024) {
        return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(2)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function formatDate(dateString) {
    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString + " UTC");

    return date.toLocaleString();
}

function escapeHTML(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}

loadResults();

setInterval(loadResults, 30000);