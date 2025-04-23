// Переключение видимости пароля
function togglePasswordVisibility(icon) {
    const input = icon.previousElementSibling;  // Находим поле пароля
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈";  // Изменяем иконку на закрытую
    } else {
        input.type = "password";
        icon.textContent = "👁️";  // Изменяем иконку на открытую
    }
}