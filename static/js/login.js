// Student Login
document.getElementById("student-login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const res = await fetch("/api/student/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
            username: document.getElementById("student-user").value,
            password: document.getElementById("student-pass").value
        })
    });
    const data = await res.json();
    if (data.ok) {
        window.location.href = "/student"; // Go to student dashboard
    } else {
        alert(data.error);
    }
});

// Admin Login
document.getElementById("admin-login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
            username: document.getElementById("admin-user").value,
            password: document.getElementById("admin-pass").value
        })
    });
    const data = await res.json();
    if (data.ok) {
        window.location.href = "/admin"; // Go to admin dashboard
    } else {
        alert(data.error);
    }
});
