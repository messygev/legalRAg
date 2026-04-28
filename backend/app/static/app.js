const today = new Date().toISOString().slice(0, 10);
for (const id of ["effectiveDate", "noticeEffectiveDate", "receivedDate"]) {
  const el = document.getElementById(id);
  if (el) el.value = today;
}

const print = (node, obj) => node.textContent = JSON.stringify(obj, null, 2);

async function postJSON(url, payload) {
  const res = await fetch(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload)});
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

document.getElementById("searchForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const out = document.getElementById("searchResult");
  try {
    const data = await postJSON("/v1/search", {
      query: document.getElementById("query").value,
      effective_date: document.getElementById("effectiveDate").value,
      mode: "research"
    });
    print(out, data);
  } catch (err) { out.textContent = `Fehler: ${err.message}`; }
});

document.getElementById("noticeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const out = document.getElementById("noticeResult");
  try {
    const data = await postJSON("/v1/notices/analyze-text", {
      text: document.getElementById("noticeText").value,
      received_date: document.getElementById("receivedDate").value || null,
      effective_date: document.getElementById("noticeEffectiveDate").value,
    });
    print(out, data);
  } catch (err) { out.textContent = `Fehler: ${err.message}`; }
});
