// Tab Switching
const tabButtons = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    tabContents.forEach((c) => c.classList.remove("active"));

    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");

    if (btn.dataset.tab === "history") {
      loadMeetingHistory();
    }
  });
});

// New Meeting: Upload + Process
document.getElementById("processBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("audioFile");
  if (!fileInput.files.length) {
    alert("Please choose an audio file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("results").classList.add("hidden");

  try {
    const response = await fetch("/api/process", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    showResults(data);
  } catch (err) {
    alert("Something went wrong. Check the server logs.");
    console.error(err);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
});

function showResults(data) {
  document.getElementById("summaryText").textContent = data.notes.summary;
  document.getElementById("transcriptText").textContent = data.transcript;

  const decisionsList = document.getElementById("decisionsList");
  decisionsList.innerHTML = "";
  data.notes.decisions.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    decisionsList.appendChild(li);
  });

  const actionItemsList = document.getElementById("actionItemsList");
  actionItemsList.innerHTML = "";
  data.notes.action_items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    actionItemsList.appendChild(li);
  });

  document.getElementById("results").classList.remove("hidden");
}

// History Tab
async function loadMeetingHistory() {
  const response = await fetch("/api/meetings");
  const meetings = await response.json();

  const listEl = document.getElementById("meetingList");
  listEl.innerHTML = "";

  if (meetings.length === 0) {
    listEl.innerHTML = "<p>No meetings yet. Process one in the New Meeting tab.</p>";
    return;
  }

  meetings.forEach((meeting) => {
    const card = document.createElement("div");
    card.className = "meeting-card";
    card.innerHTML = `
      <strong>${meeting.filename}</strong>
      <p>${meeting.summary}</p>
      <div class="meta">${new Date(meeting.created_at).toLocaleString()}</div>
    `;
    card.addEventListener("click", () => showMeetingDetail(meeting.id));
    listEl.appendChild(card);
  });
}

async function showMeetingDetail(id) {
  const response = await fetch(`/api/meetings/${id}`);
  const meeting = await response.json();

  const detailEl = document.getElementById("meetingDetail");
  detailEl.classList.remove("hidden");
  detailEl.innerHTML = `
    <h2>${meeting.filename}</h2>
    <p><strong>Summary:</strong> ${meeting.summary}</p>
    <p><strong>Decisions:</strong> ${meeting.decisions.join(", ") || "None"}</p>
    <p><strong>Action Items:</strong> ${meeting.action_items.join(", ") || "None"}</p>
    <details>
      <summary>Full Transcript</summary>
      <p>${meeting.transcript}</p>
    </details>
  `;
}
