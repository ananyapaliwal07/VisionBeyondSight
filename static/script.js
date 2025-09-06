// ===== Camera Setup =====
const video = document.getElementById("camera");
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error(err));

// ===== Map Setup =====
const map = L.map('map').setView([28.6139, 77.2090], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © OpenStreetMap'
}).addTo(map);

let marker = L.marker([28.6139, 77.2090]).addTo(map);

// ===== Messages & Audio =====
const messagesDiv = document.getElementById("messages");
let lastIndex = 0;
let seenObstacles = new Set();

function showMessage(text) {
    const div = document.createElement("div");
    div.className = "card";
    div.textContent = text;
    messagesDiv.appendChild(div);
}

function speak(text) {
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1;
    window.speechSynthesis.speak(utter);
}

// ===== Poll Backend Messages =====
async function pollMessages() {
    try {
        const res = await fetch("/get_latest_messages");
        if (!res.ok) return;
        const data = await res.json();

        for (let i = lastIndex; i < data.length; i++) {
            const msg = data[i];
            if (!msg.toLowerCase().startsWith("obstacle detected")) {
                showMessage(msg);
                speak(msg);
            }
        }
        lastIndex = data.length;
    } catch (e) { console.error(e); }
}

// ===== Update Map Location =====
async function updateLocation() {
    try {
        const res = await fetch("/get_location");
        if (!res.ok) return;
        const data = await res.json();
        marker.setLatLng([data.lat, data.lng]);
        map.panTo([data.lat, data.lng]);
    } catch (e) { console.error(e); }
}
setInterval(updateLocation, 3000);

// ===== Start Navigation Button (Text Input) =====
document.getElementById("startBtn").addEventListener("click", async () => {
    const destination = prompt("Enter your destination (Karkardooma / Connaught Place / Ashok Vihar):");
    if (!destination) return;

    await fetch("/start_navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ destination })
    });

    alert("Navigation started!");
    setInterval(pollMessages, 2000);
});

// ===== Real-time Object Detection =====
async function pollDetection() {
    try {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL("image/jpeg");

        const res = await fetch("/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: dataUrl })
        });
        if (!res.ok) return;
        const data = await res.json();

        if (data.object) {
            const obstacles = data.object.split(", ");
            obstacles.forEach(obj => {
                if (!seenObstacles.has(obj)) {
                    seenObstacles.add(obj);
                    const msg = `Obstacle detected: ${obj}`;
                    speak(msg);
                    showMessage(msg);
                }
            });
        }
    } catch (e) { console.error(e); }
}
setInterval(pollDetection, 1000);
