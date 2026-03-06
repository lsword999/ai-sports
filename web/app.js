const STORAGE_KEY = "ai_sports_web_v1";

const state = loadState();

const playerForm = document.getElementById("player-form");
const sessionForm = document.getElementById("session-form");
const gpsForm = document.getElementById("gps-form");

const playersDiv = document.getElementById("players");
const sessionsDiv = document.getElementById("sessions");
const gpsTable = document.getElementById("gps-table");
const gpsPlayerSelect = document.getElementById("gps-player");
const gpsSessionSelect = document.getElementById("gps-session");

playerForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(playerForm);
  const player = {
    player_id: uid("p"),
    name: String(fd.get("name") || "").trim(),
    position: String(fd.get("position") || "").trim(),
    physical_metrics: {
      height_cm: Number(fd.get("height_cm")),
      weight_kg: Number(fd.get("weight_kg")),
      body_fat_pct: optionalNumber(fd.get("body_fat_pct")),
      resting_heart_rate_bpm: optionalNumber(fd.get("resting_hr")),
    },
  };

  if (!player.name || !player.position) return;
  state.players.push(player);
  persist();
  playerForm.reset();
  render();
});

sessionForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(sessionForm);
  const session = {
    session_id: uid("s"),
    title: String(fd.get("title") || "").trim(),
    session_type: String(fd.get("session_type") || "training"),
    session_date: String(fd.get("session_date") || ""),
    location: String(fd.get("location") || "").trim(),
    opponent: String(fd.get("opponent") || "").trim(),
  };

  if (!session.title || !session.session_date) return;
  state.sessions.push(session);
  persist();
  sessionForm.reset();
  render();
});

gpsForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData(gpsForm);
  const playerId = String(fd.get("player_id") || "");
  const sessionId = String(fd.get("session_id") || "");
  const session = state.sessions.find((s) => s.session_id === sessionId);
  if (!playerId || !session) return;

  state.gps_records.push({
    record_id: uid("g"),
    player_id: playerId,
    session_id: sessionId,
    session_type: session.session_type,
    session_date: session.session_date,
    distance_m: Number(fd.get("distance_m")),
    max_speed_mps: Number(fd.get("max_speed_mps")),
    duration_min: Number(fd.get("duration_min")),
    sprint_count: optionalNumber(fd.get("sprint_count")) || 0,
  });

  persist();
  gpsForm.reset();
  render();
});

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }
  return { players: [], sessions: [], gps_records: [] };
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function uid(prefix) {
  return `${prefix}_${Math.random().toString(36).slice(2, 10)}`;
}

function optionalNumber(v) {
  const t = String(v || "").trim();
  return t ? Number(t) : null;
}

function render() {
  renderPlayers();
  renderSessions();
  renderSelectors();
  renderGpsTable();
}

function renderPlayers() {
  playersDiv.innerHTML = "";
  if (!state.players.length) {
    playersDiv.innerHTML = '<div class="item">暂无球员</div>';
    return;
  }
  state.players.forEach((p) => {
    const el = document.createElement("div");
    el.className = "item";
    el.innerHTML = `<strong>${p.name}</strong> (${p.position})<br/>${p.physical_metrics.height_cm}cm / ${p.physical_metrics.weight_kg}kg`;
    playersDiv.appendChild(el);
  });
}

function renderSessions() {
  sessionsDiv.innerHTML = "";
  if (!state.sessions.length) {
    sessionsDiv.innerHTML = '<div class="item">暂无会话</div>';
    return;
  }
  state.sessions.forEach((s) => {
    const el = document.createElement("div");
    el.className = "item";
    el.innerHTML = `<strong>${s.title}</strong> [${s.session_type}]<br/>${s.session_date}${s.location ? ` @ ${s.location}` : ""}`;
    sessionsDiv.appendChild(el);
  });
}

function renderSelectors() {
  gpsPlayerSelect.innerHTML = "";
  gpsSessionSelect.innerHTML = "";

  state.players.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.player_id;
    opt.textContent = `${p.name} (${p.position})`;
    gpsPlayerSelect.appendChild(opt);
  });

  state.sessions.forEach((s) => {
    const opt = document.createElement("option");
    opt.value = s.session_id;
    opt.textContent = `${s.title} - ${s.session_date}`;
    gpsSessionSelect.appendChild(opt);
  });
}

function renderGpsTable() {
  gpsTable.innerHTML = "";
  if (!state.gps_records.length) {
    gpsTable.innerHTML = '<tr><td colspan="7">暂无 GPS 记录</td></tr>';
    return;
  }

  state.gps_records.forEach((r) => {
    const p = state.players.find((x) => x.player_id === r.player_id);
    const s = state.sessions.find((x) => x.session_id === r.session_id);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p ? p.name : r.player_id}</td>
      <td>${s ? s.title : r.session_id}</td>
      <td>${r.session_type}</td>
      <td>${r.session_date}</td>
      <td>${r.distance_m}</td>
      <td>${r.max_speed_mps}</td>
      <td>${r.duration_min}</td>
    `;
    gpsTable.appendChild(tr);
  });
}

render();
