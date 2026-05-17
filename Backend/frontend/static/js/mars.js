const API_BASE = "http://localhost:8000";

async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${API_BASE}/auth/token`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    throw new Error("Login failed");
  }

  const data = await res.json();
  localStorage.setItem("mars_token", data.access_token);
  localStorage.setItem("mars_user", username);
}

async function fetchClassrooms() {
  const token = localStorage.getItem("mars_token");
  const res = await fetch(`${API_BASE}/classrooms/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.json();
}

// Placeholder Earth news (later: plug real API)
async function fetchEarthNews() {
  return [
    { title: "Earth: Stable link to Mars confirmed", source: "Mission Control" },
    { title: "Global education summit opens new Mars classrooms", source: "Earth University" }
  ];
}

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const errorDiv = document.getElementById("login-error");

      try {
        await login(username, password);
        window.location.href = "dashboard.html";
      } catch (err) {
        errorDiv.textContent = "Access denied. Check crew ID / access code.";
      }
    });
  }

  const userLabel = document.getElementById("user-label");
  if (userLabel) {
    const user = localStorage.getItem("mars_user") || "Crew Member";
    userLabel.textContent = `Logged in as: ${user}`;
  }

  const classroomList = document.getElementById("classroom-list");
  if (classroomList) {
    fetchClassrooms().then(classrooms => {
      classroomList.innerHTML = "";
      classrooms.forEach(c => {
        const li = document.createElement("li");
        li.textContent = `${c.name} • Linked to: ${c.earth_system}`;
        classroomList.appendChild(li);
      });
    }).catch(() => {
      classroomList.innerHTML = "<li>Unable to load classrooms.</li>";
    });
  }

  const earthNewsList = document.getElementById("earth-news-list");
  if (earthNewsList) {
    fetchEarthNews().then(items => {
      earthNewsList.innerHTML = "";
      items.forEach(n => {
        const li = document.createElement("li");
        li.textContent = `${n.title} (${n.source})`;
        earthNewsList.appendChild(li);
      });
    }).catch(() => {
      earthNewsList.innerHTML = "<li>Unable to reach Earth news link.</li>";
    });
  }
});
