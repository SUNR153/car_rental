const App = (function() {
    const config = {
        maxFileSize: 5 * 1024 * 1024,
        defaultTheme: 'theme-light'
    };

    function init() {
        initPasswordToggle();
        initTheme();
        initBackground();
    }

    function initPasswordToggle() {
        document.querySelectorAll('.toggle-password').forEach(button => {
            const input = button.closest('.password-wrapper')?.querySelector('input');
            const icon = button.querySelector('i');
            
            if (!input || !icon) return;

            button.setAttribute('aria-pressed', 'false');
            button.setAttribute('role', 'button');
            button.setAttribute('tabindex', '0');

            button.addEventListener('click', () => togglePassword(input, icon, button));

            button.addEventListener('keydown', (e) => {
                if (['Enter', ' '].includes(e.key)) {
                    e.preventDefault();
                    togglePassword(input, icon, button);
                }
            });
        });
    }

    function togglePassword(input, icon, button) {
        const isVisible = input.type === 'text';
        input.type = isVisible ? 'password' : 'text';

        icon.classList.toggle('fa-eye-slash', !isVisible);
        icon.classList.toggle('fa-eye', isVisible);

        button.setAttribute('aria-pressed', String(!isVisible));
        button.setAttribute('aria-label', 
            isVisible ? 'Показать пароль' : 'Скрыть пароль');
        
        input.focus();
    }

    function initTheme() {
        applyTheme(localStorage.getItem('theme') || config.defaultTheme);
        
        document.getElementById('toggle-theme')?.addEventListener('click', toggleTheme);
    }

    function toggleTheme() {
        const isDark = document.body.classList.contains('theme-dark');
        applyTheme(isDark ? 'theme-light' : 'theme-dark');
    }

    function applyTheme(theme) {
        document.body.classList.remove('theme-light', 'theme-dark');
        document.body.classList.add(theme);
        localStorage.setItem('theme', theme);
        updateLogo(theme);
    }

    function updateLogo(theme) {
        const logo = document.getElementById('logo');
        if (!logo) return;
        
        const newSrc = theme === 'theme-dark' 
            ? logo.dataset.darkSrc 
            : logo.dataset.lightSrc;
        
        if (newSrc) logo.src = newSrc;
    }

    function initBackground() {
        const savedBg = localStorage.getItem('userBackground');
        if (savedBg) applyBackground(savedBg);
        
        document.getElementById('background-input')?.addEventListener('change', handleBackgroundUpload);
        document.getElementById('reset-background')?.addEventListener('click', resetBackground);
    }

    function handleBackgroundUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        if (!file.type.startsWith('image/')) {
            alert('Пожалуйста, выберите изображение!');
            return;
        }
        
        if (file.size > config.maxFileSize) {
            alert(`Файл слишком большой. Максимум ${config.maxFileSize / (1024 * 1024)}MB.`);
            return;
        }
        
        const reader = new FileReader();
        reader.onload = e => {
            applyBackground(e.target.result);
            localStorage.setItem('userBackground', e.target.result);
        };
        reader.readAsDataURL(file);
    }

    function applyBackground(url) {
        document.body.style.backgroundImage = `url(${url})`;
        document.body.classList.add('has-background');
    }

    function resetBackground() {
        document.body.style.backgroundImage = '';
        document.body.classList.remove('has-background');
        localStorage.removeItem('userBackground');
        alert('Фон сброшен!');
    }

    return {
        init,
        togglePasswordVisibility: togglePassword,
        toggleTheme,
        applyTheme,
        applyBackground,
        resetBackground
    };
})();

document.addEventListener('DOMContentLoaded', () => App.init());
setTimeout(() => {
    document.querySelectorAll('.alert-box').forEach(alert => {
        alert.style.transition = "opacity 0.5s";
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 4000);

