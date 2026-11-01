async function loadAdminComplaints() {
    const res = await fetch("/api/complaints", { credentials: "same-origin" });
    const data = await res.json();
    
    if (!data.ok) {
        window.location.href = "/"; // Kick them out if not logged in
        return;
    }

    // --- UPDATE THE ADMIN NAME AT THE TOP ---
    if (data.admin_name) {
        const adminHeader = document.querySelector(".user-info h2");
        if (adminHeader) {
            adminHeader.innerText = "Hi, " + data.admin_name;
        }
    }
    // ----------------------------------------

    const tbody = document.getElementById("admin-table-body");
    tbody.innerHTML = "";
    
    data.complaints.forEach(c => {
        const tr = document.createElement("tr");
        const dateObj = new Date(c.created_at);
        const timeStr = dateObj.toLocaleString(); 

        // If fixed, strike it through and remove the button
        if (c.status === "fixed") {
            tr.style.textDecoration = "line-through";
            tr.style.color = "gray";
            tr.innerHTML = `
                <td>${c.room_number}</td>
                <td>${c.student_name}</td>
                <td>${c.description}</td>
                <td>${timeStr}</td>
                <td>Fixed</td>
            `;
        } else {
            tr.innerHTML = `
                <td>${c.room_number}</td>
                <td>${c.student_name}</td>
                <td>${c.description}</td>
                <td>${timeStr}</td>
                <td><button onclick="markFixed(${c.id})" class="btn primary-btn" style="padding: 5px 10px; font-size: 12px;">Mark Fixed</button></td>
            `;
        }
        tbody.appendChild(tr);
    });
}

// Mark as fixed function (Must be global for the button onclick to find it)
window.markFixed = async function(id) {
    await fetch(`/api/complaints/${id}/fix`, { 
        method: "PATCH", 
        credentials: "same-origin" 
    });
    loadAdminComplaints(); // Refresh table
}

// Logout button
document.querySelector(".logout-btn").addEventListener("click", async () => {
    await fetch("/api/admin/logout", { method: "POST", credentials: "same-origin" });
    window.location.href = "/";
});

// Load complaints when page opens
loadAdminComplaints();