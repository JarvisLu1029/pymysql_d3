const form = document.querySelector("#answer-form");
if (form) form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button"), feedback = document.querySelector("#feedback"), data = new FormData(form);
  button.disabled = true; feedback.className = "feedback"; feedback.textContent = "正在核對門禁、物證與口供……";
  try {
    const response = await fetch("/api/check", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({level:Number(data.get("level")), answer:data.get("answer")})});
    const result = await response.json(); feedback.textContent = result.message; feedback.classList.add(result.ok ? "good" : "bad");
    if (result.ok) window.setTimeout(() => window.location.assign(result.next_url), 750);
  } catch (_) { feedback.textContent = "鑑識系統暫時無法回應，請確認伺服器仍在執行。"; feedback.classList.add("bad"); }
  finally { button.disabled = false; }
});
