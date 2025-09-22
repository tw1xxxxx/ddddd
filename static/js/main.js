// Функция для переключения темы
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

// Функция обновления иконки темы
function updateThemeIcon(theme) {
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill theme-icon' : 'bi bi-moon-fill theme-icon';
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Получаем сохраненную тему или используем светлую по умолчанию
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Устанавливаем тему
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Добавляем обработчик для кнопки переключения темы
    const themeSwitch = document.querySelector('.theme-switch');
    if (themeSwitch) {
        themeSwitch.addEventListener('click', toggleTheme);
    }
}); 