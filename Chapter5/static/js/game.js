const panelContainer = document.querySelector("#case-panel-container");
const progressPanel = document.querySelector(".progress-panel");
const totalChapters = document.querySelectorAll(".case-tab").length;

async function showPanel(panelNumber) {
  if (!panelContainer || panelContainer.dataset.loading === "true") return;
  panelContainer.dataset.loading = "true";
  panelContainer.setAttribute("aria-busy", "true");

  try {
    const response = await fetch(`/api/panel/${panelNumber}`, {cache: "no-store"});
    if (!response.ok) throw new Error(await response.text());
    panelContainer.innerHTML = await response.text();
    setViewingTab(panelNumber);
    bindPanelActions();
  } catch (_) {
    panelContainer.innerHTML = '<div class="query-state error"><span class="state-icon">!</span><div><strong>無法切換卷宗</strong><p>請確認伺服器仍在執行後再試一次。</p></div></div>';
  } finally {
    panelContainer.dataset.loading = "false";
    panelContainer.removeAttribute("aria-busy");
  }
}

function setViewingTab(panelNumber) {
  document.querySelectorAll(".case-dots li").forEach((item) => {
    const selected = Number(item.dataset.chapter) === panelNumber;
    item.classList.toggle("viewing", selected);
    item.querySelector(".case-tab")?.setAttribute("aria-selected", String(selected));
  });
}

function updateProgress(unlocked) {
  const progressText = progressPanel?.querySelector(".progress-copy strong");
  const progressBar = progressPanel?.querySelector(".progress-track i");
  if (progressText) progressText.textContent = `${unlocked} / ${totalChapters}`;
  if (progressBar) progressBar.style.width = `${Math.round(unlocked / totalChapters * 100)}%`;

  document.querySelectorAll(".case-dots li").forEach((item) => {
    const chapter = Number(item.dataset.chapter);
    const tab = item.querySelector(".case-tab");
    item.classList.toggle("done", chapter <= unlocked);
    item.classList.toggle("active", unlocked < totalChapters && chapter === unlocked + 1);
    if (tab) tab.disabled = chapter > Math.min(unlocked + 1, totalChapters);
  });
}

function bindAnswerForm() {
  const form = panelContainer?.querySelector("#answer-form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector("button");
    const feedback = form.querySelector("#feedback");
    const data = new FormData(form);
    button.disabled = true;
    feedback.className = "feedback";
    feedback.textContent = "正在核對門禁、物證與口供……";

    try {
      const response = await fetch("/api/check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({level: Number(data.get("level")), answer: data.get("answer")}),
      });
      const result = await response.json();
      feedback.textContent = result.message;
      feedback.classList.add(result.ok ? "good" : "bad");

      if (result.ok) {
        updateProgress(result.unlocked);
        window.setTimeout(() => showPanel(result.next_panel), 500);
      }
    } catch (_) {
      feedback.textContent = "鑑識系統暫時無法回應，請確認伺服器仍在執行。";
      feedback.classList.add("bad");
    } finally {
      button.disabled = false;
    }
  });
}

function bindPanelActions() {
  bindAnswerForm();
  panelContainer?.querySelector(".review-return")?.addEventListener("click", (event) => {
    showPanel(Number(event.currentTarget.dataset.panel));
  });
}

document.querySelectorAll(".case-tab").forEach((tab) => {
  tab.addEventListener("click", () => showPanel(Number(tab.dataset.chapter)));
});

document.addEventListener("submit", (event) => {
  if (event.target.matches("[data-reset-form]") && !window.confirm("確定要清除所有關卡進度，重新從第一關開始嗎？")) {
    event.preventDefault();
  }
});

bindPanelActions();
