const button = document.getElementById("generate");
const textarea = document.getElementById("prompt");
const palette = document.getElementById("palette");
const history = document.getElementById("history");
const toast = document.getElementById("toast");
const copyAll = document.getElementById("copy-all");
const download = document.getElementById("download");
const guideBtn = document.getElementById("guide-btn");
const guideModal = document.getElementById("guide-modal");
const modalClose = document.querySelector(".modal-close");

button.onclick = generate;
if (copyAll) copyAll.onclick = copyAllHex;
if (download) download.onclick = downloadPNG;
if (guideBtn) guideBtn.onclick = () => guideModal.classList.add("active");
if (modalClose) modalClose.onclick = () => guideModal.classList.remove("active");
guideModal.onclick = (e) => { if (e.target === guideModal) guideModal.classList.remove("active"); };

textarea.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        generate();
    }
});

loadHistory();
restoreFromUrl();

async function generate() {
    const text = textarea.value.trim();
    if (!text) return;

    const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, scheme: "default" })
    });

    const data = await response.json();

    renderPalette(data.palette);
    saveHistory(text, data.palette);
}

function renderPalette(colors) {
    palette.innerHTML = "";
    window.currentColors = colors;

    colors.forEach((color, index) => {
        const div = document.createElement("div");
        div.className = "color";
        div.style.animationDelay = `${index * 0.08}s`;

        div.innerHTML = `
            <div class="box" title="${color.name}" style="background:${color.hex}">
                <span class="color-tooltip">${color.name}</span>
            </div>
            <div class="hex">${color.hex}</div>
        `;

        div.querySelector(".box").onclick = () => {
            navigator.clipboard.writeText(color.hex);
            showToast("Copied " + color.hex);
        };

        palette.appendChild(div);
    });
}

function saveHistory(query, paletteData) {
    let items = JSON.parse(localStorage.getItem("moodpalette.history") || "[]");

    items = items.filter(x => x.query !== query);

    items.unshift({
        query: query,
        palette: paletteData
    });

    items = items.slice(0, 20);

    localStorage.setItem("moodpalette.history", JSON.stringify(items));
    loadHistory();
}

function loadHistory() {
    history.innerHTML = "";

    const items = JSON.parse(localStorage.getItem("moodpalette.history") || "[]");

    items.forEach(item => {
        const div = document.createElement("div");
        div.className = "historyItem";
        div.innerText = item.query;

        // Mini palette preview
        if (item.palette && item.palette.length > 0) {
            const preview = document.createElement("div");
            preview.className = "mini-preview";
            item.palette.forEach(c => {
                const span = document.createElement("span");
                span.style.background = c.hex;
                preview.appendChild(span);
            });
            div.appendChild(preview);
        }

        div.onclick = () => {
            textarea.value = item.query;
            renderPalette(item.palette);
        };

        history.appendChild(div);
    });
}

function copyAllHex() {
    if (!window.currentColors) return;

    const text = window.currentColors.map(x => x.hex).join(", ");
    navigator.clipboard.writeText(text);
    showToast("All HEX copied");
}

function downloadPNG() {
    if (!window.currentColors) return;

    const colors = window.currentColors.map(x => x.hex).join(",");
    window.open("/export?colors=" + encodeURIComponent(colors));
}

function restoreFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const query = params.get("q");

    if (!query) return;

    textarea.value = query;
    generate();
}

function showToast(message) {
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 1200);
}