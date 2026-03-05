const btn = document.getElementById("analyze-btn");
const textarea = document.getElementById("conversation");
const resultsEl = document.getElementById("results");
const errorEl = document.getElementById("error-msg");

const SEVERITY_COLORS = {
  low: "bg-yellow-50 border-yellow-300 text-yellow-800",
  medium: "bg-orange-50 border-orange-300 text-orange-800",
  high: "bg-red-50 border-red-300 text-red-800",
};

btn.addEventListener("click", async () => {
  const conversation = textarea.value.trim();
  if (!conversation) return;

  btn.disabled = true;
  btn.textContent = "Analyzing…";
  errorEl.classList.add("hidden");
  resultsEl.classList.add("hidden");

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation }),
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Server error ${res.status}: ${err}`);
    }

    const report = await res.json();
    render(report);
    resultsEl.classList.remove("hidden");
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Analyze";
  }
});

function render(report) {
  document.getElementById("summary-text").textContent = report.summary;
  renderRisks(report.risks);
  renderQuality(report.quality);
}

function renderRisks(risks) {
  const el = document.getElementById("risk-list");

  if (!risks.length) {
    el.innerHTML = '<p class="text-sm text-gray-500">No risks detected.</p>';
    return;
  }

  el.innerHTML = risks
    .map((risk) => {
      const colors = SEVERITY_COLORS[risk.severity] ?? SEVERITY_COLORS.medium;
      const tags = risk.risk_types
        .map(
          (t) =>
            `<span class="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">${t}</span>`
        )
        .join(" ");

      return `
        <div class="rounded-lg border p-4 ${colors}">
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-semibold uppercase tracking-wide">${risk.severity} severity</span>
            <span class="text-xs">Message #${risk.message_reference}</span>
          </div>
          <p class="text-sm mb-2">${risk.explanation}</p>
          <div class="flex flex-wrap gap-1 mb-3">${tags}</div>
          <div class="bg-white bg-opacity-60 rounded p-3">
            <p class="text-xs font-medium mb-1">Safer rewrite</p>
            <p class="text-sm italic">${risk.safer_rewrite}</p>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderQuality(quality) {
  const scoresEl = document.getElementById("quality-scores");
  const dimensions = ["clarity", "empathy", "safety", "actionability"];

  scoresEl.innerHTML = dimensions
    .map((dim) => {
      const score = quality[dim];
      const color =
        score >= 75 ? "bg-green-500" : score >= 50 ? "bg-yellow-400" : "bg-red-400";

      return `
        <div class="bg-gray-50 rounded-lg p-3 border border-gray-200">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-medium capitalize">${dim}</span>
            <span class="text-sm font-bold">${score}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5">
            <div class="${color} h-1.5 rounded-full" style="width: ${score}%"></div>
          </div>
        </div>
      `;
    })
    .join("");

  document.getElementById("quality-feedback").textContent = quality.feedback;
}
