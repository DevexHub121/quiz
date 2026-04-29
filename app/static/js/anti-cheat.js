// Anti-Cheat System (Proctored Mode)
console.log("Proctored mode initialized");

// 1. Tab Switching & Window Blur Detection
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        logViolation('tab_switch', 'User switched tab or minimized window');
    }
});

window.onblur = function() {
    logViolation('window_blur', 'User clicked outside the browser window');
};

// 2. Prevent Accidental Close / Reload
let isSubmitting = false;

window.onbeforeunload = function() {
    if (!isSubmitting) {
        return "Are you sure you want to exit the exam? Your progress may be lost.";
    }
};

// Disable the popup when the quiz form is submitted
document.addEventListener('submit', function() {
    isSubmitting = true;
});

// 3. Disable Copy/Paste/Right-Click
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('copy', e => e.preventDefault());
document.addEventListener('paste', e => e.preventDefault());

// 4. Fullscreen Enforcement
function enterFullscreen() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
    }
}

// Track fullscreen exit
document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement) {
        logViolation('fullscreen_exit', 'User exited fullscreen mode');
    }
});

// 5. Log Violation to Server (Silent)
function logViolation(type, details) {
    console.warn(`Violation detected: ${type} - ${details}`);
    
    fetch('/log_violation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type, details })
    })
    .catch(err => console.error('Error logging violation:', err));
}

// Auto-trigger fullscreen on start
if (window.location.pathname === '/start') {
    document.addEventListener('click', function initFullscreen() {
        enterFullscreen();
        document.removeEventListener('click', initFullscreen);
    }, { once: true });
}
