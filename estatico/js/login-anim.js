document.addEventListener("DOMContentLoaded", () => {

    const passwordInput  = document.getElementById('password');
    const signupPassword = document.getElementById('signup-password');
    const usernameInput  = document.getElementById('username');
    const pupils         = document.querySelectorAll('.owl-pupil');
    const owlContainer   = document.querySelector('.owl-container');
    const browLeft       = document.querySelector('.owl-brow-left');
    const browRight      = document.querySelector('.owl-brow-right');
    const authCard       = document.getElementById('authSplitCard');

    // ── Idle / dormir ──────────────────────────────────────────
    let idleTimer = null;

    const wakeUp = () => owlContainer && owlContainer.classList.remove('is-sleeping');

    const resetIdleTimer = () => {
        clearTimeout(idleTimer);
        if (owlContainer && !owlContainer.classList.contains('password-active')) wakeUp();
        idleTimer = setTimeout(() => {
            if (owlContainer && !owlContainer.classList.contains('password-active')) {
                owlContainer.classList.add('is-sleeping');
                pupils.forEach(p => p.style.transform = 'translate(0px, 0px)');
            }
        }, 6000);
    };

    ['mousemove', 'keydown', 'click', 'touchstart'].forEach(e =>
        document.addEventListener(e, resetIdleTimer)
    );
    resetIdleTimer();

    // ── Ojos siguen el cursor ──────────────────────────────────
    document.addEventListener('mousemove', (e) => {
        if (!owlContainer) return;
        if (owlContainer.classList.contains('password-active') || owlContainer.classList.contains('is-sleeping')) return;

        const rect = owlContainer.getBoundingClientRect();
        const cx = rect.left + rect.width  / 2;
        const cy = rect.top  + rect.height / 2;
        const angle = Math.atan2(e.clientY - cy, e.clientX - cx);
        const maxDist = 6;
        const dx = Math.min(Math.abs(e.clientX - cx) / 70, maxDist);
        const dy = Math.min(Math.abs(e.clientY - cy) / 70, maxDist);
        const mx = Math.cos(angle) * dx;
        const my = Math.sin(angle) * dy;

        pupils.forEach(p => p.style.transform = `translate(${mx}px, ${my}px)`);
        if (browLeft)  browLeft.style.transform  = `translateY(${my * 0.3}px)`;
        if (browRight) browRight.style.transform = `translateY(${my * 0.3}px)`;
    });

    // ── Username focus ─────────────────────────────────────────
    if (usernameInput && owlContainer) {
        usernameInput.addEventListener('focus', () => owlContainer.classList.add('username-active'));
        usernameInput.addEventListener('blur',  () => owlContainer.classList.remove('username-active'));
    }

    // ── Contraseña: tapar ojos (login Y signup) ────────────────
    [passwordInput, signupPassword].forEach(input => {
        if (!input) return;
        input.addEventListener('focus', () => owlContainer && owlContainer.classList.add('password-active'));
        input.addEventListener('blur',  () => owlContainer && owlContainer.classList.remove('password-active'));
    });

    // ── Panel switching: Login ↔ Sign Up ───────────────────────
    document.querySelectorAll('.go-signup').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            authCard && authCard.classList.add('signup');
            owlContainer && owlContainer.classList.remove('password-active', 'username-active');
        });
    });

    document.querySelectorAll('.go-login').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            authCard && authCard.classList.remove('signup');
            owlContainer && owlContainer.classList.remove('password-active', 'username-active');
        });
    });

    // ── Animación de entrada ───────────────────────────────────
    const card = document.querySelector('.auth-split-card');
    if (card) {
        card.style.opacity   = '0';
        card.style.transform = 'translateY(28px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.7s cubic-bezier(0.16,1,0.3,1), transform 0.7s cubic-bezier(0.16,1,0.3,1)';
            card.style.opacity    = '1';
            card.style.transform  = 'translateY(0)';
        }, 150);
    }

    if (owlContainer) {
        owlContainer.style.opacity   = '0';
        owlContainer.style.transform = 'translateX(-50%) scale(0.8) translateY(20px)';
        setTimeout(() => {
            owlContainer.style.transition = 'opacity 0.6s cubic-bezier(0.34,1.56,0.64,1), transform 0.6s cubic-bezier(0.34,1.56,0.64,1)';
            owlContainer.style.opacity    = '1';
            owlContainer.style.transform  = 'translateX(-50%) scale(1) translateY(0)';
        }, 380);
    }

});
