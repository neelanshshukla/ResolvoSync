async function loadStudentComplaints() {
    // The Date.now() trick forces the browser to get fresh data, not cached data
    const res = await fetch("/api/complaints?t=" + Date.now(), { 
        credentials: "same-origin",
        headers: { "Cache-Control": "no-cache" }
    });
    
    const data = await res.json();
    
    if (!data.ok) {
        window.location.href = "/"; 
        return;
    }

    // UPDATE THE NAME AT THE TOP
    if (data.student_name) {
        const welcomeText = document.getElementById("student-welcome");
        if (welcomeText) {
            welcomeText.innerText = "Hi, " + data.student_name;
        }
    }

    const trackerList = document.getElementById("student-tracker-list");
    if (data.complaints.length === 0) {
        trackerList.innerHTML = "<p>No complaints submitted yet.</p>";
        return;
    }

    trackerList.innerHTML = "";
    data.complaints.forEach(c => {
        const card = document.createElement("div");
        card.style.border = "1px solid #ccc";
        card.style.padding = "10px";
        card.style.marginBottom = "10px";
        card.style.borderRadius = "5px";

        const statusColor = c.status === "fixed" ? "green" : "orange";
        const statusText = c.status === "fixed" ? "✅ Fixed" : "⏳ Pending";

        card.innerHTML = `
            <strong>Room: ${c.room_number}</strong> 
            <span style="float: right; color: ${statusColor}; font-weight: bold;">${statusText}</span><br>
            <p style="margin: 5px 0;">${c.description}</p>
        `;
        trackerList.appendChild(card);
    });
}

document.getElementById("new-complaint-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const room = document.getElementById("comp-room").value;
    const desc = document.getElementById("comp-desc").value;
    
    const res = await fetch("/api/complaints", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ room_number: room, description: desc })
    });
    const data = await res.json();

    if (data.ok) {
        alert("Complaint submitted successfully!");
        document.getElementById("new-complaint-form").reset();
        loadStudentComplaints(); 
    } else {
        alert(data.error);
    }
});

document.querySelector(".logout-btn").addEventListener("click", async () => {
    await fetch("/api/student/logout", { method: "POST", credentials: "same-origin" });
    window.location.href = "/";
});

loadStudentComplaints();