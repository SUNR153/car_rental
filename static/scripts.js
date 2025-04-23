function togglePasswordVisibility(icon) {
    console.log('Глазик был кликнут');
    const input = icon.previousElementSibling;
    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = '🙈';
        console.log('Пароль теперь виден');
    } else {
        input.type = 'password';
        icon.textContent = '👁️';
        console.log('Пароль скрыт');
    }
}

(function () {
    const toggleButton = document.getElementById('theme-toggle');
    if (!toggleButton) return;

    const icon = toggleButton.querySelector('.theme-toggle i');
    const emojiSpan = toggleButton.querySelector('.nav-link');
    
    // Начальная тема с data-theme
    let isDark = toggleButton.dataset.theme === 'dark';
    applyTheme(isDark);

    toggleButton.addEventListener('click', () => {
        isDark = !isDark;
        applyTheme(isDark);
        localStorage.setItem('darkMode', isDark);
    });

    function applyTheme(dark) {
        document.body.classList.toggle('dark-mode', dark);
        if (icon) {
            icon.className = dark ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        }
        if (emojiSpan) {
            emojiSpan.innerHTML = `<i class="${icon.className}"></i> ${dark ? '☀️' : '🌙'}`;
        }
    }

    // Если localStorage есть — переопределим тему
    const saved = localStorage.getItem('darkMode');
    if (saved !== null) {
        isDark = saved === 'true';
        applyTheme(isDark);
    }
})();



