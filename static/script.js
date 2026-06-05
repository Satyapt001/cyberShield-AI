async function scanThreat() {

    const message =
        document.getElementById("message").value;

    const resultContainer =
        document.getElementById("result");

    if (!message.trim()) {

        alert("Please enter a message.");

        return;
    }

    resultContainer.innerHTML = `
        <div class="result-card">
            <h2>Analyzing Threat...</h2>
        </div>
    `;

    try {

        const response = await fetch("/scan", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message
            })
        });

        const data = await response.json();

        let threatClass = "threat-low";

        if (data.threat_level === "HIGH") {

            threatClass = "threat-high";

        } else if (
            data.threat_level === "MEDIUM"
        ) {

            threatClass = "threat-medium";
        }

        let urlSection = "";

        if (
            data.url_analysis &&
            data.url_analysis.length > 0
        ) {

            urlSection = data.url_analysis
                .map(url => `

                    <div class="url-card">

                        <p>
                            <strong>URL:</strong>
                            ${url.url}
                        </p>

                        <p>
                            <strong>Risk:</strong>
                            ${url.risk}
                        </p>

                        <p>
                            <strong>Reasons:</strong>
                            ${
                                url.reasons.length
                                ? url.reasons.join(", ")
                                : "No suspicious indicators found"
                            }
                        </p>

                    </div>

                `)
                .join("");

        } else {

            urlSection = `
                <p>No URLs detected.</p>
            `;
        }

        resultContainer.innerHTML = `

            <div class="result-card">

                <h2>Scan Result</h2>

                <hr>

                <p>
                    <strong>Spam Detection:</strong>
                    ${data.spam_prediction}
                    (${data.spam_confidence}%)
                </p>

                <p>
                    <strong>Phishing Detection:</strong>
                    ${data.phishing_prediction}
                    (${data.phishing_confidence}%)
                </p>

                <p>
                    <strong>Risk Score:</strong>
                    ${data.risk_score}/100
                </p>

                <p class="${threatClass}">
                    <strong>
                        Threat Level:
                        ${data.threat_level}
                    </strong>
                </p>

                <hr>

                <p>
                    <strong>Suspicious Keywords:</strong>
                </p>

                <p>
                    ${
                        data.keywords.length
                        ? data.keywords.join(", ")
                        : "None Detected"
                    }
                </p>

                <hr>

                <h3>URL Analysis</h3>

                ${urlSection}

            </div>

        `;

    } catch (error) {

        resultContainer.innerHTML = `

            <div class="result-card">

                <h2>Error</h2>

                <p>
                    Failed to connect to the server.
                </p>

                <p>
                    ${error.message}
                </p>

            </div>

        `;

        console.error(error);
    }
}