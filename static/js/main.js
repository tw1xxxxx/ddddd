// main.js
// Автоматическое скрытие алертов через 3 секунды
window.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 3000);
    });

    // Инициализация темы
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeIcon(theme);
    updateNavbarStyles(theme);

    // Обработчик переключения темы
    const themeSwitch = document.querySelector('.theme-switch');
    if (themeSwitch) {
        themeSwitch.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            updateNavbarStyles(newTheme);
        });
    }
});

// Обновление иконки темы
function updateThemeIcon(theme) {
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.className = theme === 'light' ? 
            'bi bi-moon-fill theme-icon' : 
            'bi bi-sun-fill theme-icon';
    }
}

// Обновление стилей навигации при переключении темы
function updateNavbarStyles(theme) {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        // Принудительно обновляем стили навигации
        navbar.style.backgroundColor = '';
        // Заставляем браузер пересчитать стили
        navbar.offsetHeight;
    }
} 

