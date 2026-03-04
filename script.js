function updateTimers() {
    document.querySelectorAll('.countdown').forEach(t => {
        const dist = new Date(t.dataset.end) - new Date();
        if (dist > 0) {
            const d = Math.floor(dist / 86400000);
            const h = Math.floor((dist % 86400000) / 3600000);
            const m = Math.floor((dist % 3600000) / 60000);
            const s = Math.floor((dist % 60000) / 1000);
            t.innerText = `${d}d ${h}h ${m}m ${s}s`;
        } else {
            t.innerText = "COMPLETED";
        }
    });
}

function copyRef() {
    const link = document.getElementById('refLink').innerText;
    navigator.clipboard.writeText(link.trim());
    alert("Link copied!");
}

setInterval(updateTimers, 1000);