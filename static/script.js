// ==========================================================================
// Premium Celestial Theme System Icons
// ==========================================================================

const SUN_ICON = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="4"></circle>
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>
</svg>`;

const MOON_ICON = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" fill="currentColor"></path>
</svg>`;

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) themeBtn.innerHTML = savedTheme === 'dark' ? SUN_ICON : MOON_ICON;
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) themeBtn.innerHTML = newTheme === 'dark' ? SUN_ICON : MOON_ICON;
    if (typeof threatChart !== 'undefined' && threatChart) {
        threatChart.options.plugins.legend.labels.color = newTheme === 'dark' ? '#9ca3af' : '#64748b';
        threatChart.update();
    }
}

initTheme();

// Global Chart Pointer
let threatChart;

// ==========================================================================
// Threat Scanner Engine (Split Screen Real-Time Mapping)
// ==========================================================================

async function scanThreat() {
    const message = document.getElementById("message").value;
    const resultContainer = document.getElementById("result");

    if (!message.trim()) {
        alert("Please enter a text message payload to inspect.");
        return;
    }

    resultContainer.innerHTML = `
        <div class="result-card" style="animation: pulse-dot 1.5s infinite ease-in-out; text-align: center; padding: 80px 20px;">
            <h2 style="font-size: 0.85rem; color: var(--muted); letter-spacing:1px;">ANALYZING THREAT PAYLOAD...</h2>
        </div>
    `;

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        let threatClass = "threat-low";
        if (data.threat_level === "HIGH") threatClass = "threat-high";
        else if (data.threat_level === "MEDIUM") threatClass = "threat-medium";

        let urlSection = "";
        if (data.url_analysis && data.url_analysis.length > 0) {
            urlSection = data.url_analysis.map(url => {
                const riskLower = url.risk.toLowerCase();
                const indicatorItems = url.reasons.length
                    ? url.reasons.map(reason => `<span class="indicator-tag">${reason}</span>`).join(", ")
                    : "Clear verification parameters.";

                return `
                    <div class="url-bento-card">
                        <div class="url-header-line">
                            <span class="url-link-pill" title="${url.url}">${url.url}</span>
                            <span class="risk-badge-pill risk-badge-${riskLower}">${url.risk}</span>
                        </div>
                        <div class="url-indicator-box">
                            <span>Threat Rationale</span>
                            <div class="indicator-tags-wrapper">${indicatorItems}</div>
                        </div>
                    </div>
                `;
            }).join("");
        } else {
            urlSection = `<p style="color: var(--muted); font-style: italic; font-size: 0.85rem; padding: 12px 4px;">No explicit URLs extracted from message text.</p>`;
        }

        resultContainer.innerHTML = `
            <div class="result-card">
                <h2>SECURITY INFRASTRUCTURE REPORT</h2>
                <div class="metric-row">
                    <div class="metric-box">
                        <label>Spam Prediction</label>
                        <div>${data.spam_prediction} (${data.spam_confidence}%)</div>
                    </div>
                    <div class="metric-box">
                        <label>Phishing Match</label>
                        <div>${data.phishing_prediction} (${data.phishing_confidence}%)</div>
                    </div>
                </div>

                <div class="index-banner">
                    <div>
                        <span style="font-size:0.75rem; color:var(--muted); font-weight:600; text-transform:uppercase;">Composite Risk Index</span>
                        <div style="font-size:1.4rem; font-weight:800; font-family:var(--font-mono); margin-top:2px;">${data.risk_score} <span style="font-size:0.9rem; font-weight:500; color:var(--muted);">/ 100</span></div>
                    </div>
                    <div class="${threatClass}" style="font-size: 1rem; font-weight:800; letter-spacing:0.5px;">${data.threat_level} VECTOR</div>
                </div>
                
                <p style="margin-bottom: 8px; font-weight: 600; font-size: 0.8rem; color:var(--muted); text-transform:uppercase;">Flagged Structural Tokens:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 24px;">
                    ${data.keywords.length ? data.keywords.map(k => `<span class="keyword">${k}</span>`).join('') : '<span style="color:var(--muted); font-size:0.85rem; font-style:italic;">None detected</span>'}
                </div>
                
                <h3 style="font-size: 0.85rem; margin-bottom: 4px; font-weight:600; color:var(--muted); text-transform:uppercase; font-family:var(--font-mono); letter-spacing:0.5px;">Embedded URL Safety Breakdown</h3>
                ${urlSection}
            </div>
        `;
    } catch (error) {
        resultContainer.innerHTML = `
            <div class="result-card" style="border-color: var(--danger);">
                <h2 style="color: var(--danger);">CONNECTION FAULT</h2>
                <p style="margin-top:8px;">Failed to cleanly communicate with threat intelligence analysis server pipelines.</p>
                <p style="color: var(--muted); font-size: 0.85rem; margin-top:4px;">${error.message}</p>
            </div>
        `;
    }
}

// ==========================================================================
// Dashboard Sync Controller
// ==========================================================================

async function loadDashboard() {
    try {
        const response = await fetch("/dashboard-data");
        const data = await response.json();
        const stats = data.stats;

        document.getElementById("totalScans").innerText = stats.total_scans;
        document.getElementById("spamCount").innerText = stats.spam_detected;
        document.getElementById("phishingCount").innerText = stats.phishing_detected;
        document.getElementById("highThreats").innerText = stats.high_threats;

        updateChart(stats);
        loadRecentScans(stats);
    } catch (error) {
        console.error("Dashboard link sync anomaly:", error);
    }
}

// ==========================================================================
// Meaningful & Interactive Custom Donut Engine
// ==========================================================================

function updateChart(stats) {
    const safeCount = (stats.total_scans || 0) - (stats.spam_detected || 0) - (stats.phishing_detected || 0);
    const chartData = [stats.spam_detected || 0, stats.phishing_detected || 0, safeCount < 0 ? 0 : safeCount];

    if (threatChart) {
        threatChart.data.datasets[0].data = chartData;
        threatChart.update();
        return;
    }

    const ctx = document.getElementById("threatChart");
    if (!ctx) return;

    const activeTheme = document.documentElement.getAttribute('data-theme');
    const labelColor = activeTheme === 'dark' ? '#9ca3af' : '#64748b';

    threatChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Spam", "Phishing Threats", "Verified Clean"],
            datasets: [{
                data: chartData,
                backgroundColor: ["#ef4444", "#f59e0b", "#10b981"],
                borderWidth: 2,
                borderColor: activeTheme === 'dark' ? '#070b12' : '#ffffff',
                hoverOffset: 12,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            onHover: (event, chartElement) => {
                event.native.target.style.cursor = chartElement.length ? 'pointer' : 'default';
            },
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: labelColor,
                        padding: 16,
                        font: { family: "'Plus Jakarta Sans', sans-serif", weight: 600, size: 11 }
                    }
                },
                tooltip: {
                    backgroundColor: activeTheme === 'dark' ? '#0f172a' : '#ffffff',
                    titleColor: activeTheme === 'dark' ? '#f1f5f9' : '#0f172a',
                    bodyColor: activeTheme === 'dark' ? '#94a3b8' : '#64748b',
                    borderColor: 'rgba(255,255,255,0.08)',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6,
                    cornerRadius: 8
                }
            },
            cutout: "75%"
        }
    });
}

function loadRecentScans(stats) {
    const table = document.getElementById("recentScans");
    if (!table || !stats.recent_scans) return;

    table.innerHTML = "";
    stats.recent_scans.slice().reverse().forEach(scan => {
        let badgeClass = "low-threat";
        if (scan.threat_level === "HIGH") badgeClass = "high-threat";
        else if (scan.threat_level === "MEDIUM") badgeClass = "medium-threat";

        table.innerHTML += `
            <tr>
                <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">${scan.timestamp}</td>
                <td>${scan.spam_prediction}</td>
                <td>${scan.phishing_prediction}</td>
                <td>${scan.risk_score} / 100</td>
                <td><span class="${badgeClass}">${scan.threat_level}</span></td>
            </tr>
        `;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    if (window.location.pathname === "/dashboard") {
        loadDashboard();
        setInterval(loadDashboard, 5000);
    }
});