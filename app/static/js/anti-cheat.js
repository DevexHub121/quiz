// Anti-Cheat Logic
document.addEventListener('DOMContentLoaded', function() {
    const isQuizPage = document.querySelector('.quiz-container') !== null;
    if (!isQuizPage) return;

    let violations = 0;
    const maxViolations = 3;

    function handleViolation(type) {
        violations++;
        console.warn(`Violation detected: ${type}. Count: ${violations}`);
        
        // Show overlay
        const overlay = document.createElement('div');
        overlay.className = 'violation-overlay';
        overlay.innerHTML = `
            <h2>⚠️ Security Warning</h2>
            <p>Tab switching or window blurring is not allowed during the exam.</p>
            <p>Violation ${violations}/${maxViolations}</p>
            <button class="btn" style="width: auto; padding: 10px 30px;" onclick="this.parentElement.remove()">I Understand</button>
        `;
        document.body.appendChild(overlay);

        // Optionally notify server
        fetch('/log_violation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: type, details: `Violation ${violations}` })
        });

        if (violations >= maxViolations) {
            alert("Maximum violations reached. Your exam may be disqualified.");
        }
    }

    // Visibility Change
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            handleViolation('tab_switch');
        }
    });

    // Window Blur
    window.addEventListener('blur', function() {
        handleViolation('window_blur');
    });

    // Prevent Context Menu (Right Click)
    document.addEventListener('contextmenu', e => e.preventDefault());

    // Prevent Keyboard Shortcuts (F12, Ctrl+Shift+I, etc.)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) e.preventDefault();
        if (e.key === 'F12') e.preventDefault();
        if (e.ctrlKey && e.key === 'u') e.preventDefault();
    });
});
