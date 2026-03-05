const btn = document.getElementById("analyze-btn");
const textarea = document.getElementById("conversation");
const resultsEl = document.getElementById("results");
const errorEl = document.getElementById("error-msg");

const SAMPLE_CONVERSATION = `Doctor: Hi there, sorry for the wait. What can I do for you?
Patient: Hi, no worries. So I've got this really sore throat, it's been going on since like Sunday, maybe Saturday night actually. And it's not getting better.
Doctor: Okay. Any fever?
Patient: Yeah, I've been feeling hot and cold. I took my temperature last night and it was 38.4 I think.
Doctor: Right. Let me have a look. Can you open wide for me? Say ahh.
Patient: Ahhh.
Doctor: Okay… yeah, there's definitely inflammation, and I can see some white patches on your tonsils there. Almost certainly bacterial — strep most likely.
Patient: Is that bad?
Doctor: It's very common, very treatable. I'm going to prescribe you a course of amoxicillin. Are you allergic to penicillin at all?
Patient: No, I don't think so. No.
Doctor: Good. So take one tablet twice a day — morning and evening, ideally with food.
Patient: How long for?
Doctor: Ten days. Now the important thing is you finish the whole course, even once you start feeling better — which should be in a couple of days.
Patient: Right, yeah. It's just — I'm bad at remembering pills once I feel normal again, you know? Like is it a big deal if I stop a bit early?
Doctor: You really should finish them.
Patient: Okay. What about painkillers, can I take anything in the meantime?
Doctor: Yeah, paracetamol or ibuprofen, whatever works for you. Keep your fluids up as well.
Patient: I've got a work thing on Thursday, will I be okay for that?
Doctor: You should be feeling much better by Thursday, yeah.
Patient: And if I'm not?
Doctor: Just call the surgery if things aren't improving.
Patient: Okay great, thank you so much.`;

textarea.value = SAMPLE_CONVERSATION;

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
