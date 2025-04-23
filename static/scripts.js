// Показывать/скрывать пароль
function togglePasswordVisibility(icon) {
    const input = icon.closest('.password-wrapper').querySelector('input');
    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = '🙈';
    } else {
        input.type = 'password';
        icon.textContent = '👁️';
    }
}

// Установка/сброс фонового изображения
function applyBackground(url) {
    document.body.style.backgroundImage = `url(${url})`;
    document.body.classList.add('has-background');
}
function clearBackground() {
    document.body.style.backgroundImage = '';
    document.body.classList.remove('has-background');
}

// Глобальная функция для inline onclick и для слушателя
function toggleTheme() {
    // Определяем текущую тему
    const isDark = document.body.classList.contains('theme-dark');
    const newTheme = isDark ? 'theme-light' : 'theme-dark';
    applyTheme(newTheme);
}

// Применить тему и сменить логотип
function applyTheme(theme) {
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add(theme);
    localStorage.setItem('theme', theme);
    changeLogo(theme);
}

// Меняем логотип по data-атрибутам
function changeLogo(theme) {
    const logo = document.getElementById('logo');
    if (!logo) return;
    const lightSrc = logo.getAttribute('data-light-src');
    const darkSrc  = logo.getAttribute('data-dark-src');
    logo.src = (theme === 'theme-dark' ? darkSrc : lightSrc) || logo.src;
}

// Обработка загрузки нового фона
function handleBackgroundUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
        return alert('Пожалуйста, выберите изображение!');
    }
    if (file.size > 5 * 1024 * 1024) {
        return alert('Файл слишком большой. Максимум 5MB.');
    }
    const reader = new FileReader();
    reader.onload = e => {
        applyBackground(e.target.result);
        localStorage.setItem('userBackground', e.target.result);
    };
    reader.readAsDataURL(file);
}

// Вешаем обработчики после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // 1) фон
    const savedBg = localStorage.getItem('userBackground');
    if (savedBg) applyBackground(savedBg);

    // 2) тема
    const savedTheme = localStorage.getItem('theme') || 'theme-light';
    applyTheme(savedTheme);

    // 3) глазики
    document.querySelectorAll('.toggle-password')
            .forEach(icon => icon.addEventListener('click', () => togglePasswordVisibility(icon)));

    // 4) кнопка переключения темы
    const btn = document.getElementById('toggle-theme');
    if (btn) btn.addEventListener('click', toggleTheme);

    // 5) загрузка и сброс фона
    const inp = document.getElementById('background-input');
    if (inp) inp.addEventListener('change', handleBackgroundUpload);
    const reset = document.getElementById('reset-background');
    if (reset) reset.addEventListener('click', () => {
        localStorage.removeItem('userBackground');
        clearBackground();
        alert('Фон сброшен!');
    });
});
